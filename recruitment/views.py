from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Candidate, JobRole
import PyPDF2
import csv
from django.db.models.functions import TruncMonth
import json
from django.db.models import Count, Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings

# ================  Login ==================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid Credentials"})

    return render(request, "login.html")

# ================= LOGOUT =================
@login_required
def custom_logout(request):
    logout(request)
    return redirect("login")


# ================= DASHBOARD =================



@login_required
def dashboard(request):

    query = request.GET.get("q")
    status_filter = request.GET.get("status")

    candidates = Candidate.objects.all()

    # 🔍 Search Filter
    if query:
        candidates = candidates.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(status__icontains=query)
        )

    # 🔥 Status Filter
    if status_filter:
        candidates = candidates.filter(status=status_filter)

    total = candidates.count()
    shortlisted = candidates.filter(status="Shortlisted").count()
    rejected = candidates.filter(status="Rejected").count()
    selected = candidates.filter(status="Selected").count()

    avg = 0
    if total > 0:
        avg = round(sum([c.score for c in candidates]) / total, 2)

    selection_rate = 0
    if total > 0:
        selection_rate = round((selected / total) * 100, 2)

    # ===== Monthly Hiring Data =====
    monthly_data = (
        Candidate.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = []
    counts = []

    for item in monthly_data:
        if item['month']:
            months.append(item['month'].strftime("%b %Y"))
            counts.append(item['count'])

    return render(request, "dashboard.html", {
        "candidates": candidates,
        "total": total,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "selected": selected,
        "average_score": avg,
        "selection_rate": selection_rate,
        "months": json.dumps(months),
        "monthly_counts": json.dumps(counts),
    })


# ================= APPLY =================
@login_required
def apply(request):
    job = JobRole.objects.first()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        resume = request.FILES.get("resume")

        if name and email and resume:
            Candidate.objects.create(
                name=name,
                email=email,
                resume=resume,
                job_role=job
            )

        return redirect("dashboard")

    return render(request, "apply.html")


# ================= SCREEN =================
@login_required
def screen_candidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)

    resume_text = ""

    with candidate.resume.open('rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    resume_text = resume_text.lower()
    job_description = candidate.job_role.skills.lower()

    # ===== AI Matching =====
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    ai_score = round(similarity[0][0] * 100)

    candidate.score = ai_score

    # ===== Status Decision + Email =====
    if ai_score >= 85:
        candidate.status = "Shortlisted"
        candidate.interview_stage = "Round 2"

        send_mail(
            "Interview Invitation - Round 2",
            f"Hi {candidate.name},\n\nCongratulations! You are shortlisted for Round 2.",
            settings.EMAIL_HOST_USER,
            [candidate.email],
            fail_silently=False,
        )

    elif ai_score >= 60:
        candidate.status = "Shortlisted"
        candidate.interview_stage = "Round 1"

        send_mail(
            "Interview Invitation - Round 1",
            f"Hi {candidate.name},\n\nYou are shortlisted for Round 1 interview.",
            settings.EMAIL_HOST_USER,
            [candidate.email],
            fail_silently=False,
        )

    elif ai_score >= 40:
        candidate.status = "Shortlisted"
        candidate.interview_stage = "Round 1"

        # 🔥 Email add karo yahan bhi (warna mail nahi jayega)
        send_mail(
            "Application Under Review",
            f"Hi {candidate.name},\n\nYour profile is under review. We will update you soon.",
            settings.EMAIL_HOST_USER,
            [candidate.email],
            fail_silently=False,
        )

    else:
        candidate.status = "Rejected"
        candidate.interview_stage = "Rejected"

        send_mail(
            "Application Update",
            f"Hi {candidate.name},\n\nThank you for applying. Unfortunately, you were not shortlisted.",
            settings.EMAIL_HOST_USER,
            [candidate.email],
            fail_silently=False,
        )

    candidate.save()
    return redirect("dashboard")
# ================= MOVE STAGE =================
@login_required
def move_stage(request, id):
    candidate = get_object_or_404(Candidate, id=id)

    if candidate.interview_stage == "Round 1":
        candidate.interview_stage = "Round 2"

    elif candidate.interview_stage == "Round 2":
        candidate.interview_stage = "HR"

    elif candidate.interview_stage == "HR":
        candidate.interview_stage = "Selected"
        candidate.status = "Selected"

    candidate.save()

    return redirect("dashboard")


# ================= EXPORT =================
@login_required
def export_excel(request):
    candidates = Candidate.objects.all()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="candidates.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Score", "Status"])

    for c in candidates:
        writer.writerow([c.name, c.email, c.score, c.status])

    return response


# ================= DETAIL PAGE =================
@login_required
def candidate_detail(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    return render(request, "candidate_detail.html", {"candidate": candidate})


#================= ANALYTICS  ===================

@login_required
def analytics(request):
    candidates = Candidate.objects.all()

    total = candidates.count()
    shortlisted = candidates.filter(status="Shortlisted").count()
    rejected = candidates.filter(status="Rejected").count()
    selected = candidates.filter(status="Selected").count()

    return render(request, "analytics.html", {
        "total": total,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "selected": selected
    })

@login_required
@require_POST
def update_feedback(request, id):
    candidate = get_object_or_404(Candidate, id=id)

    candidate.recruiter_notes = request.POST.get("recruiter_notes")

    rating_value = request.POST.get("rating")
    if rating_value:
        candidate.rating = int(rating_value)

    candidate.feedback = request.POST.get("feedback")

    candidate.save()

    return redirect("candidate_detail", id=id)
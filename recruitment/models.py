from django.db import models


class JobRole(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField()

    def __str__(self):
        return self.title


class Candidate(models.Model):

    STAGE_CHOICES = [
        ('Applied', 'Applied'),
        ('Round 1', 'Round 1'),
        ('Round 2', 'Round 2'),
        ('HR', 'HR'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    interview_stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default="Applied"
    )

    recruiter_notes = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
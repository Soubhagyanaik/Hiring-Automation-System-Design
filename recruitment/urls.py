from django.urls import path
from . import views

urlpatterns = [

    # 🔥 LOGIN (IMPORTANT – ye missing tha)
    path('', views.login_view, name='login'),

    # 🔥 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 🔥 Analytics
    path('analytics/', views.analytics, name='analytics'),

    # 🔥 Apply Candidate
    path('apply/', views.apply, name='apply'),

    # 🔥 Screening
    path('screen/<int:id>/', views.screen_candidate, name='screen_candidate'),

    # 🔥 Move Stage
    path('move/<int:id>/', views.move_stage, name='move_stage'),

    # 🔥 Export CSV
    path('export/', views.export_excel, name='download_excel'),

    # 🔥 Candidate Detail
    path('candidate/<int:id>/', views.candidate_detail, name='candidate_detail'),

    # 🔥 Feedback Update
    path('candidate/<int:id>/feedback/', views.update_feedback, name='update_feedback'),

    # 🔥 Logout
    path('logout/', views.custom_logout, name='logout'),
]
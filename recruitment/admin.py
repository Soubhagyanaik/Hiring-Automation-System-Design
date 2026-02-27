from django.contrib import admin
from .models import Candidate, JobRole

admin.site.register(Candidate)
admin.site.register(JobRole)
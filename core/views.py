import os
import platform

from django import get_version as django_version
from django.shortcuts import render
from django.utils import timezone


def home(request):
    """Render the landing screen with loader and environment details."""
    host_name = request.get_host().lower()
    agent_brand = "AppWizzy" if host_name == "appwizzy.com" else "Flatlogic"
    now = timezone.now()

    context = {
        "project_name": "New Style",
        "agent_brand": agent_brand,
        "django_version": django_version(),
        "python_version": platform.python_version(),
        "current_time": now,
        "host_name": host_name,
        "project_description": os.getenv("PROJECT_DESCRIPTION", ""),
        "project_image_url": os.getenv("PROJECT_IMAGE_URL", ""),
    }
    return render(request, "core/index.html", context)

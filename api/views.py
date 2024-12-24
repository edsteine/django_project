"""
File: views.py
Date updated: 2024-12-23
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Contains views for the project, including the home view.
Used Libraries: django
"""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def custom_404(request: HttpRequest, exception: Http404) -> HttpResponse:
    return render(request, "404.html", status=404)

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from core.forms import CompanyForm
from core.models import Company
from django.conf import settings

import logging

import json

# Create your views here.
lgr = logging.getLogger(__name__)


def dashboard(request):
    return render(request, 'core/dashboard.html', {})



def record_create(request):
    if request.method == "POST":
        lgr.info(request.POST)
        form = CompanyForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.freelancer = request.user
            search.save()

            return redirect('/')
        else:
            lgr.error('search form error')
            lgr.error(form.errors)

    else:
        form = CompanyForm()

    return render(request, "core/company/create.html", {
        'form': form,
    })


def company_create(request):
    if request.method == "POST":
        lgr.info(request.POST)
        form = CompanyForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.freelancer = request.user
            search.save()

            return redirect('/')
        else:
            lgr.error('search form error')
            lgr.error(form.errors)

    else:
        form = CompanyForm()

    return render(request, "core/company/create.html", {
        'form': form,
    })

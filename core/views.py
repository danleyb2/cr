from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from core.forms import CompanyForm
from core.models import Company
from django.conf import settings
from authentication.models import User

import logging

import json

# Create your views here.
lgr = logging.getLogger(__name__)


def dashboard(request):

    if request.user.is_superuser:
        companies_count = Company.objects.all().count()
    else:
        companies_count = Company.objects.filter(freelancer=request.user).count()

    freelancers = User.objects.exclude(is_superuser=True)
    freelancers_count = freelancers.count()
    active_freelancers_count = freelancers.filter(is_active=True).count()
    pending_freelancers_count = freelancers.filter(is_active=False).count()


    return render(request, 'core/dashboard.html', {
        'companies_count':companies_count,
        'freelancers_count':freelancers_count,
        'active_freelancers_count':active_freelancers_count,
        'pending_freelancers_count':pending_freelancers_count
    })




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def record_list(request):
    if request.user.is_superuser:
        contacts_qs = Company.objects.all().order_by('created_at')
    else:
        contacts_qs = Company.objects.filter(freelancer=request.user).order_by('created_at')

    page = request.GET.get('page', 1)

    paginator = Paginator(contacts_qs, 50)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'companies':contacts
    }

    return  render(request, 'core/company/list.html',context)


def freelancer_list(request):
    contacts_qs = User.objects.exclude(is_superuser=True).order_by('pk')

    page = request.GET.get('page', 1)

    paginator = Paginator(contacts_qs, 50)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'companies':contacts
    }

    return  render(request, 'core/freelancer/list.html',context)


def company_create(request):
    if request.method == "POST":
        lgr.info(request.POST)
        form = CompanyForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.freelancer = request.user
            search.save()

            return redirect(reverse('core:records:list'))
        else:
            lgr.error('search form error')
            lgr.error(form.errors)

    else:
        form = CompanyForm()

    return render(request, "core/company/create.html", {
        'form': form,
    })

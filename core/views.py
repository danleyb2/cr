from django.http import JsonResponse, HttpResponse
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



def freelancer_records(request,freelancer_pk):
    contacts_qs = Company.objects.filter(freelancer__pk=freelancer_pk).order_by('created_at')

    total = contacts_qs.count()
    paid_count = contacts_qs.filter(paid=True).count()
    not_paid_count = contacts_qs.filter(paid=False).count()

    page = request.GET.get('page', 1)

    paginator = Paginator(contacts_qs, 50)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'freelancer_pk':freelancer_pk,
        'companies':contacts,
        'total':total,
        'paid_count':paid_count,
        'not_paid_count':not_paid_count
    }

    return  render(request, 'core/freelancer/records.html',context)



def freelancer_records_paid(request,freelancer_pk):
    contacts_qs = Company.objects.filter(freelancer__pk=freelancer_pk).update(paid=True)

    return  redirect(reverse('core:freelancers:freelancer:records',args={freelancer_pk}))



import csv
import datetime

def export(request):

    now = datetime.datetime.now()

    filename = now.strftime("records_%B_%d_%Y__%H_%M")

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

    contacts_qs = Company.objects.all().order_by('created_at')

    writer = csv.writer(response)
    writer.writerow([
        'id',
        'name',
        'website',
        'email',
        'phone_number',
        'product_page',
    ])

    pk = None
    try:
        for li in contacts_qs:
            pk = li.id
            writer.writerow([
                li.pk,
                li.name,
                li.website,
                li.phone_number,
                li.product_page
            ])
    except Exception as e:
        lgr.info(pk)
        raise

    return response



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

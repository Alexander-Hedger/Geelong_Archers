from django.shortcuts import render, redirect
from functions.functions import sidebar
from .models import CommitteeMinutes, AgmMinutes
# Create your views here.


def minutes_admin(request):

    committee_minutes = CommitteeMinutes.objects.order_by('-date_published')

    agm_minutes = AgmMinutes.objects.order_by('-date_published')

    context = sidebar()

    context['committee_minutes'] = committee_minutes
    context['agm_minutes'] = agm_minutes

    return render(request, 'minutes/minutes-admin.html', context)


def minutes_upload(request):
    if request.method == 'POST' and request.FILES['minutes_upload']:
        title = request.POST['minutes_title']
        date = request.POST['minutes_date']
        minutes = request.FILES['minutes_upload']

        if request.POST['minutes_type'] == 'committee':
            minutes_upload = CommitteeMinutes(
                title=title, date=date, minutes=minutes)

        if request.POST['minutes_type'] == 'agm':
            minutes_upload = AgmMinutes(
                title=title, date=date, minutes=minutes)

        minutes_upload.save()

    return redirect('minutes-admin')


def minutes_delete(request, minutes_type, pk):
    if request.method == 'POST':

        if minutes_type == 'committee':
            minutes = CommitteeMinutes.objects.get(pk=pk)

        if minutes_type == 'agm':
            minutes = AgmMinutes.objects.get(pk=pk)

        minutes.delete()

        return redirect('minutes-admin')


def minutes_main(request):
    committee_minutes = CommitteeMinutes.objects.order_by(
        '-date_published')

    agm_minutes = AgmMinutes.objects.order_by('-date_published')

    context = sidebar()

    context['committee_minutes'] = committee_minutes
    context['agm_minutes'] = agm_minutes

    return render(request, 'minutes/minutes-main.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import views
from django.contrib import messages
from .models import EventIntro, EventComp, EventMotD
from functions.functions import sidebar
from accounts.models import Committee
import datetime


@login_required(login_url='home')
def events_admin(request):

    events_motd = EventMotD.objects.order_by(
        'date_start').filter(is_published=True)
    events_comp = EventComp.objects.order_by(
        'date_start').filter(is_published=True)
    events_intro = EventIntro.objects.order_by(
        'date_start').filter(is_published=True)

    context = sidebar(request)

    context['events_motd'] = events_motd
    context['events_comp'] = events_comp
    context['events_intro'] = events_intro

    return render(request, 'events/events-admin.html', context)


def events_main(request):

    events_motd = EventMotD.objects.order_by(
        'date_start').filter(is_published=True, date_end__gte=datetime.date.today())[:6]
    events_comp = EventComp.objects.order_by(
        'date_start').filter(is_published=True, date_end__gte=datetime.date.today())[:6]
    events_intro = EventIntro.objects.order_by(
        'date_start').filter(is_published=True, date_end__gte=datetime.date.today())[:6]

    context = sidebar(request)

    context['events_motd'] = events_motd
    context['events_comp'] = events_comp
    context['events_intro'] = events_intro

    return render(request, 'events/events-main.html', context)


def intro_listing(request, event_id):

    contact_event = get_object_or_404(EventIntro, pk=event_id)

    context = sidebar(request)
    context['listing_event'] = contact_event
    return render(request, 'events/intro-listing.html', context)


def comp_listing(request, event_id):

    contact_event = get_object_or_404(EventComp, pk=event_id)

    context = sidebar(request)
    context['listing_event'] = contact_event
    return render(request, 'events/comp-listing.html', context)


@login_required(login_url='home')
def events_create(request, event_type):

    if request.method == 'POST':
        if event_type == 'motd':
            event_short_title = request.POST['event_short_title']
            event_short_description = request.POST['event_short_description']
            event_date_start = request.POST['event_date_start']
            event_date_end = request.POST['event_date_end']

            event = EventMotD(short_title=event_short_title, short_description=event_short_description,
                              date_start=event_date_start, date_end=event_date_end)

            event.save()
            messages.success(request, 'Your event has been published!')
            return redirect('events-admin')

        elif event_type == 'comp':
            event_title = request.POST['event_title']
            event_short_title = request.POST['event_short_title']
            event_description = request.POST['event_description']
            event_short_description = request.POST['event_short_description']
            event_max_participants = request.POST['event_max_participants']
            event_date_start = request.POST['event_date_start']
            event_date_end = request.POST['event_date_end']
            event_url = request.POST['event_url']

            event = EventComp(title=event_title, short_title=event_short_title, description=event_description, short_description=event_short_description,
                              max_participants=event_max_participants, date_start=event_date_start, date_end=event_date_end, event_url=event_url)

            event.save()
            messages.success(request, 'Your event has been published!')
            return redirect('events-admin')

        elif event_type == 'intro':
            event_title = request.POST['event_title']
            event_short_title = request.POST['event_short_title']
            event_description = request.POST['event_description']
            event_short_description = request.POST['event_short_description']
            event_max_participants = request.POST['event_max_participants']
            event_min_age = request.POST['event_min_age']
            event_date_start = request.POST['event_date_start']
            event_date_end = request.POST['event_date_end']

            event = EventIntro(title=event_title, short_title=event_short_title, description=event_description, short_description=event_short_description,
                               max_participants=event_max_participants, min_age=event_min_age, date_start=event_date_start, date_end=event_date_end)

            event.save()

            messages.success(request, 'Your event has been published!')
            return redirect('events-admin')

    context = sidebar(request)
    context['event_type'] = event_type
    return render(request, 'events/events-create.html', context)


@login_required(login_url='home')
def events_edit(request, event_type, event_id):
    context = sidebar(request)

    if event_type == 'motd':
        event = get_object_or_404(EventMotD, pk=event_id)
        context['event'] = event
    if event_type == 'comp':
        event = get_object_or_404(EventComp, pk=event_id)
        context['event'] = event
    if event_type == 'intro':
        event = get_object_or_404(EventIntro, pk=event_id)
        context['event'] = event

    if request.method == 'POST':

        if event_type == 'motd':

            event.short_title = request.POST['event_short_title']
            event.short_description = request.POST['event_short_description']
            event.date_start = request.POST['event_date_start']
            event.date_end = request.POST['event_date_end']

            event.save()

            messages.success(request, 'Your event has been saved!')
            return redirect('events-admin')

        elif event_type == 'comp':

            event.title = request.POST['event_title']
            event.short_title = request.POST['event_short_title']
            event.description = request.POST['event_description']
            event.short_description = request.POST['event_short_description']
            event.max_participants = request.POST['event_max_participants']
            event.date_start = request.POST['event_date_start']
            event.date_end = request.POST['event_date_end']
            event.event_url = request.POST['event_url']

            event.save()

            messages.success(request, 'Your event has been saved!')
            return redirect('events-admin')

        elif event_type == 'intro':

            event.title = request.POST['event_title']
            event.short_title = request.POST['event_short_title']
            event.description = request.POST['event_description']
            event.short_description = request.POST['event_short_description']
            event.max_participants = request.POST['event_max_participants']
            event.max_lh = request.POST['event_max_lh']
            event.min_age = request.POST['event_min_age']
            event.date_start = request.POST['event_date_start']
            event.date_end = request.POST['event_date_end']

            event.save()

            messages.success(request, 'Your event has been saved!')
            return redirect('events-admin')

    context['event_type'] = event_type
    return render(request, 'events/events-edit.html', context)


@login_required(login_url='home')
def events_delete(request, event_type, event_id):

    if event_type == 'motd':
        event = get_object_or_404(EventMotD, id=event_id)
    elif event_type == 'comp':
        event = get_object_or_404(EventComp, id=event_id)
    elif event_type == 'intro':
        event = get_object_or_404(EventIntro, id=event_id)

    if request.method == 'POST':
        event.is_published = False
        event.save()
        messages.success(request, 'Your Event has been deleted!')
        return redirect('events-admin')

    return

from django.shortcuts import render, redirect, get_object_or_404
from . import views
from django.contrib import messages
from .models import EventIntro, EventComp, EventMotD
from functions.functions import sidebar, validate
from accounts.models import Committee


def events_admin(request):

    events_motd = EventMotD.objects.order_by(
        'date_start')
    events_comp = EventComp.objects.order_by(
        'date_start')
    events_intro = EventIntro.objects.order_by(
        'date_start')

    context = sidebar()

    context2 = validate()

    context['events_motd'] = events_motd
    context['events_comp'] = events_comp
    context['events_intro'] = events_intro

    for item in context2:
        context[item] = context2[item]

    return render(request, 'events/events-admin.html', context)


def events_main(request):

    events_motd = EventMotD.objects.order_by(
        'date_start').filter(is_published=True)[:6]
    events_comp = EventComp.objects.order_by(
        'date_start').filter(is_published=True)[:6]
    events_intro = EventIntro.objects.order_by(
        'date_start').filter(is_published=True)[:6]

    context = sidebar()

    context['events_motd'] = events_motd
    context['events_comp'] = events_comp
    context['events_intro'] = events_intro

    return render(request, 'events/events-main.html', context)


def events_listing(request, event_type, event_id):

    if event_type == 'motd':
        contact_event = get_object_or_404(EventMotD, pk=event_id)
    if event_type == 'comp':
        contact_event = get_object_or_404(EventComp, pk=event_id)
    if event_type == 'intro':
        contact_event = get_object_or_404(EventIntro, pk=event_id)

    context = sidebar()
    context['listing_event'] = contact_event
    context['event_type'] = event_type
    return render(request, 'events/events-listing.html', context)


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

            event = EventComp(title=event_title, short_title=event_short_title, description=event_description, short_description=event_short_description,
                              max_participants=event_max_participants, date_start=event_date_start, date_end=event_date_end)

            event.save()
            messages.success(request, 'Your event has been published!')
            return redirect('events-admin')

        elif event_type == 'intro':
            event_title = request.POST['event_title']
            event_short_title = request.POST['event_short_title']
            event_description = request.POST['event_description']
            event_short_description = request.POST['event_short_description']
            event_max_participants = request.POST['event_max_participants']
            event_max_lh = request.POST['event_max_lh']
            event_min_age = request.POST['event_min_age']
            event_date_start = request.POST['event_date_start']
            event_date_end = request.POST['event_date_end']

            event = EventIntro(title=event_title, short_title=event_short_title, description=event_description, short_description=event_short_description,
                               max_participants=event_max_participants, max_lh=event_max_lh, min_age=event_min_age, date_start=event_date_start, date_end=event_date_end)

            event.save()

            messages.success(request, 'Your event has been published!')
            return redirect('events-admin')

    context = sidebar()
    context['event_type'] = event_type
    return render(request, 'events/events-create.html', context)

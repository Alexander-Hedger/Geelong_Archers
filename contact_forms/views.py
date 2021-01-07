from django.shortcuts import render, redirect, get_object_or_404
from functions.functions import sidebar
from django.contrib import messages
from events.models import EventIntro, EventComp, EventMotD
from .models import ContactIntro
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

# Create your views here.


def contact_admin(request):
    context = sidebar(request)
    return render(request, 'contact_forms/contact-admin.html', context)


def contact_awards(request):
    context = sidebar(request)
    return render(request, 'contact_forms/contact-awards.html', context)


def contact_events(request, contact_type, event_id):

    contact_event = get_object_or_404(EventIntro, pk=event_id)

    if request.method == 'POST':
        if contact_type == 'intro':
            contact_event_id = contact_event
            contact_fname = request.POST['contact_fname']
            contact_lname = request.POST['contact_lname']
            contact_email = request.POST['contact_email']
            contact_phone = request.POST['contact_phone']
            contact_age = request.POST['contact_age']
            contact_dominant = request.POST['contact_dominant']
            contact_experience = request.POST['contact_experience']
            contact_reason = request.POST['contact_reason']

            contact = ContactIntro(event_id=contact_event_id, first_name=contact_fname,
                                   last_name=contact_lname, email=contact_email, phone=contact_phone, age=contact_age, left_right=contact_dominant, shot_before=contact_experience, reason=contact_reason)

            contact.save()

            contact_event.current_participants = int(
                contact_event.current_participants) + 1

            if contact_dominant == 'left':
                contact_event.current_lh = int(contact_event.current_lh) + 1

            contact_event.save()

            #### Send user confirmation email ####
            plaintext = get_template(
                settings.BASE_DIR + '/templates/emails/contact-intro-course.txt')
            htmly = get_template(settings.BASE_DIR +
                                 '/templates/emails/contact-intro-course.html')

            context = {'contact': contact, 'event': contact_event}
            subject = "Geelong Archers: Introduction Course Sign Up Confirmation"
            from_email = 'donotreply@geelongarchers.com.au'
            to_email = contact_email
            text_content = plaintext.render(context)
            html_content = htmly.render(context)

            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            ##################################################

            messages.success(
                request, 'You have successfully signed up to the event!')
            return redirect('events-main')

    context = sidebar(request)
    context['contact_type'] = contact_type
    context['contact_event'] = contact_event
    return render(request, 'contact_forms/contact-events.html', context)

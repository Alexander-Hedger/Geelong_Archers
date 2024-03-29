from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import views
from django.contrib import messages
from .models import Announcement
from functions.functions import sidebar

# Create your views here.


def announcements_main(request):

    admin_announcements = Announcement.objects.order_by(
        '-date_published')

    context = sidebar(request)

    context['admin_announcements'] = admin_announcements

    return render(request, 'announcements/announcements-main.html', context)


@login_required(login_url='home')
def announcements_create(request):
    if request.method == 'POST':
        announcement_title = request.POST['announcement_title']
        announcement_short_title = request.POST['announcement_short_title']
        announcement_description = request.POST['announcement_description']
        announcement_short_description = request.POST['announcement_short_description']

        if request.POST.get('announcement_published'):
            announcement_is_published = True
        else:
            announcement_is_published = False

        announcement = Announcement(title=announcement_title, short_title=announcement_short_title,
                                    announcement=announcement_description, short_announcement=announcement_short_description, is_published=announcement_is_published,)

        announcement.save()

        messages.success(request, 'Your announcement has been published!')
        return redirect('announcements-admin')

    else:
        context = sidebar(request)
        return render(request, 'announcements/announcements-create.html', context)


@login_required(login_url='home')
def announcements_admin(request):
    admin_announcements = Announcement.objects.order_by(
        '-date_published')

    context = sidebar(request)

    context['admin_announcements'] = admin_announcements
    return render(request, 'announcements/announcements-admin.html', context)


@login_required(login_url='home')
def announcements_edit(request, announcement_id):

    announcement = Announcement.objects.get(id=announcement_id)

    if request.method == 'POST':

        if request.POST.get('announcement_published'):
            announcement.is_published = True
        else:
            announcement.is_published = False

        announcement.title = request.POST['announcement_title']
        announcement.short_title = request.POST['announcement_short_title']
        announcement.announcement = request.POST['announcement_description']
        announcement.short_announcement = request.POST['announcement_short_description']

        announcement.save()

        messages.success(request, 'Your announcement has been edited!')
        return redirect('announcements-admin')

    context = sidebar(request)
    context['announcement'] = announcement
    return render(request, 'announcements/announcements-edit.html', context)


@login_required(login_url='home')
def announcements_delete(request, announcement_id):

    announcement = get_object_or_404(Announcement, pk=announcement_id)

    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Your announcement has been deleted!')
        return redirect('announcements-admin')

    return

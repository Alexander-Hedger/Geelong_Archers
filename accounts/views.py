from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from functions.functions import sidebar, scrape
from django.views.decorators.clickjacking import xframe_options_exempt
from awards.models import MemberEvents, MemberAwards, MemberAvailableAwards, Awards, MemberClassificationAnnual, MemberClassification
from .models import Account
import os


@xframe_options_exempt
def dashboard(request):
    context = sidebar()
    # Scrape Archers Diary
    if request.method == 'POST':
        scrape(request)

    # Your Classifications
    disciplines = ['Outdoor', 'Field', 'Indoor', 'Clout']
    division = request.user.division
    archer_class = request.user.archer_class

    try:
        if request.GET['request_type'] == 'classification':
            division = request.GET['division']
            archer_class = request.GET['archer_class']
    except:
        pass

    for discipline in disciplines:
        score_count = 0
        score_count_var = f'{discipline}_score'

        query = MemberClassificationAnnual.objects.order_by('-rank').filter(
            member=request.user, discipline=discipline, division=division, archer_class=archer_class, score_count__gte=3)[:1]

        if query:
            rank = (query[0].rank) + 1

            query2 = MemberClassificationAnnual.objects.filter(
                member=request.user, discipline=discipline, division=division, archer_class=archer_class, rank=rank)

            if query2:
                score_count = query2[0].score_count
                score_count = 3 - score_count
            else:
                score_count = 3

        else:
            query = MemberClassification.objects.order_by('-rank').filter(
                member=request.user, discipline=discipline, division=division, archer_class=archer_class, score_count__gte=3)[:1]

            if query:
                # If they are gold check in the annual table
                if query[0].rank == 4:
                    rank = (query[0].rank) + 1

                    query2 = MemberClassificationAnnual.objects.filter(
                        member=request.user, discipline=discipline, division=division, archer_class=archer_class, rank=rank)
                else:
                    rank = (query[0].rank) + 1

                    query2 = MemberClassification.objects.filter(
                        member=request.user, discipline=discipline, division=division, archer_class=archer_class, rank=rank)

                if query2:
                    score_count = query2[0].score_count
                    score_count = 3 - score_count
                else:
                    score_count = 3

        context[discipline] = query
        context[score_count_var] = score_count

    #  Your Events
    event_history = MemberEvents.objects.order_by(
        '-date').filter(member=request.user)

    # Your Awards
    member_awards = MemberAwards.objects.order_by(
        'award').filter(member=request.user)

    # Your Unclaimed Awards
    unclaimed_awards = MemberAvailableAwards.objects.order_by(
        'award').filter(member=request.user)

    divisions = ['Recurve', 'Compound', 'Longbow',
                 'Barebow Recurve', 'Barebow Compound', 'Crossbow']
    archer_classes = ['Cub', 'Intermediate', 'Cadet',
                      '20 & Under', 'Open', 'Master', 'Veteran', 'Veteran+', 'Para Archer', 'Vision Impaired']

    context['event_history'] = event_history
    context['member_awards'] = member_awards
    context['unclaimed_awards'] = unclaimed_awards

    context['values'] = request.GET
    context['divisions'] = divisions
    context['archer_classes'] = archer_classes

    return render(request, 'accounts/dashboard.html', context)


def login(request):
    if request.method == 'POST':
        # Login User
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        context = sidebar()
        return render(request, 'accounts/login.html', context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')


def account_update(request):
    if request.method == 'POST':
        division = request.POST['user_division']
        archer_class = request.POST['user_class']
        email = request.POST['user_email']

        user = Account.objects.get(id=request.user.id)

        user.division = division
        user.archer_class = archer_class
        user.email = email

    try:
        if request.FILES['user_photo']:
            if user.photo != 'photos/users/display_photo.jpg':
                if os.path.isfile(user.photo.path):
                    os.remove(user.photo.path)

            photo = request.FILES['user_photo']
            user.photo = photo

    except:
        pass

    user.save()

    return redirect('dashboard')

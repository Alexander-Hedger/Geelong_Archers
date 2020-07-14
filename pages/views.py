from django.shortcuts import render
from . import views
from announcements.models import Announcement
from functions.functions import sidebar
from pages.models import PageContent
from accounts.models import Committee


def about_archery(request):
    context = sidebar()

    page = PageContent.objects.get(name='about_archery')

    context['page'] = page

    return render(request, 'pages/about_archery.html', context)


def archers_diary(request):
    context = sidebar()

    page = PageContent.objects.get(name='archers_diary')
    context['page'] = page

    return render(request, 'pages/archers_diary.html', context)


def arrow_cutter(request):
    context = sidebar()

    page = PageContent.objects.get(name='arrow_cutter')
    context['page'] = page

    return render(request, 'pages/arrow_cutter.html', context)


def bowpress(request):
    context = sidebar()

    page = PageContent.objects.get(name='bowpress')
    context['page'] = page

    return render(request, 'pages/bowpress.html', context)


def by_laws(request):
    context = sidebar()

    page = PageContent.objects.get(name='by_laws')
    context['page'] = page

    return render(request, 'pages/by_laws.html', context)


def committee(request):
    context = sidebar()

    committee = Committee.objects.order_by(
        'order')
    context['committee'] = committee

    page = PageContent.objects.get(name='committee')
    context['page'] = page

    return render(request, 'pages/committee.html', context)


def contact(request):
    context = sidebar()

    page = PageContent.objects.get(name='contact')
    context['page'] = page

    return render(request, 'pages/contact.html', context)


def equipment(request):
    context = sidebar()

    page = PageContent.objects.get(name='equipment')
    context['page'] = page

    return render(request, 'pages/equipment.html', context)


def facilities(request):
    context = sidebar()

    page = PageContent.objects.get(name='facilities')
    context['page'] = page

    return render(request, 'pages/facilities.html', context)


def faq(request):
    context = sidebar()

    page = PageContent.objects.get(name='faq')
    context['page'] = page

    return render(request, 'pages/faq.html', context)


def feedback(request):
    context = sidebar()

    page = PageContent.objects.get(name='feedback')
    context['page'] = page

    return render(request, 'pages/feedback.html', context)


def fletching(request):
    context = sidebar()

    page = PageContent.objects.get(name='fletching')
    context['page'] = page

    return render(request, 'pages/fletching.html', context)


def history(request):
    context = sidebar()

    page = PageContent.objects.get(name='history')
    context['page'] = page

    return render(request, 'pages/history.html', context)


def home(request):
    context = sidebar()

    page = PageContent.objects.get(name='home')
    context['page'] = page

    return render(request, 'pages/home.html', context)


def intro_course_info(request):
    context = sidebar()

    page = PageContent.objects.get(name='intro_course_info')
    context['page'] = page

    return render(request, 'pages/intro_course_info.html', context)


def life_member(request):
    context = sidebar()

    page = PageContent.objects.get(name='life_member')
    context['page'] = page

    return render(request, 'pages/life_member.html', context)


def maintenance(request):
    context = sidebar()

    page = PageContent.objects.get(name='maintenance')
    context['page'] = page

    return render(request, 'pages/maintenance.html', context)


def nocking(request):
    context = sidebar()

    page = PageContent.objects.get(name='nocking')
    context['page'] = page

    return render(request, 'pages/nocking.html', context)


def sponsors(request):
    context = sidebar()

    page = PageContent.objects.get(name='sponsors')
    context['page'] = page

    return render(request, 'pages/sponsors.html', context)


def string_making(request):
    context = sidebar()

    page = PageContent.objects.get(name='string_making')
    context['page'] = page

    return render(request, 'pages/string_making.html', context)


def wiki_compound(request):
    context = sidebar()

    page = PageContent.objects.get(name='wiki_compound')
    context['page'] = page

    return render(request, 'pages/wiki-compound.html', context)


def wiki_longbow(request):
    context = sidebar()

    page = PageContent.objects.get(name='wiki_longbow')
    context['page'] = page

    return render(request, 'pages/wiki-longbow.html', context)


def wiki_main(request):
    context = sidebar()

    page = PageContent.objects.get(name='wiki_main')
    context['page'] = page

    return render(request, 'pages/wiki-main.html', context)


def wiki_recurve(request):
    context = sidebar()

    page = PageContent.objects.get(name='wiki_recurve')
    context['page'] = page

    return render(request, 'pages/wiki-recurve.html', context)

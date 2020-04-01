from django.shortcuts import render
# Create your views here.


def archers_diary(request):
    return render(request, 'pages/archers_diary.html')


def arrow_cutter(request):
    return render(request, 'pages/arrow_cutter.html')


def bowpress(request):
    return render(request, 'pages/bowpress.html')


def by_laws(request):
    return render(request, 'pages/by_laws.html')


def committee(request):
    return render(request, 'pages/committee.html')


def conduct(request):
    return render(request, 'pages/conduct.html')


def contact(request):
    return render(request, 'pages/contact.html')


def equipment(request):
    return render(request, 'pages/equipment.html')


def facilities(request):
    return render(request, 'pages/facilities.html')


def fletching(request):
    return render(request, 'pages/fletching.html')


def history(request):
    return render(request, 'pages/history.html')


def home(request):
    return render(request, 'pages/home.html')


def intro_course_info(request):
    return render(request, 'pages/intro_course_info.html')


def life_member(request):
    return render(request, 'pages/life_member.html')


def maintenance(request):
    return render(request, 'pages/maintenance.html')


def nocking(request):
    return render(request, 'pages/nocking.html')


def regulations(request):
    return render(request, 'pages/regulations.html')


def string_making(request):
    return render(request, 'pages/string_making.html')


def wiki_compound(request):
    return render(request, 'pages/wiki-compound.html')


def wiki_longbow(request):
    return render(request, 'pages/wiki-longbow.html')


def wiki_main(request):
    return render(request, 'pages/wiki-main.html')


def wiki_recurve(request):
    return render(request, 'pages/wiki-recurve.html')

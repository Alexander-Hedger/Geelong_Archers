from django.shortcuts import render
# Create your views here.


def awards_main(request):
    return render(request, 'awards/awards-main.html')


def awards_sub(request):
    return render(request, 'awards/awards-sub.html')

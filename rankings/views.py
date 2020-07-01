from django.shortcuts import render
# Create your views here.


def rankings_main(request):
    return render(request, 'rankings/rankings-main.html')

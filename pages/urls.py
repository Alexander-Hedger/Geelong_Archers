from django.urls import path

from . import views

urlpatterns = [

    path('about_archery', views.about_archery, name='about_archery'),
    path('archers_diary', views.archers_diary, name='archers_diary'),
    path('arrow_cutter', views.arrow_cutter, name='arrow_cutter'),
    path('bowpress', views.bowpress, name='bowpress'),
    path('by_laws', views.by_laws, name='by_laws'),
    path('committee', views.committee, name='committee'),
    path('contact', views.contact, name='contact'),
    path('equipment', views.equipment, name='equipment'),
    path('facilities', views.facilities, name='facilities'),
    path('faq', views.faq, name='faq'),
    path('feedback', views.feedback, name='feedback'),
    path('fletching', views.fletching, name='fletching'),
    path('history', views.history, name='history'),
    path('', views.home, name='home'),
    path('intro_course_info', views.intro_course_info, name='intro_course_info'),
    path('life_member', views.life_member, name='life_member'),
    path('maintenance', views.maintenance, name='maintenance'),
    path('nocking', views.nocking, name='nocking'),
    path('sponsors', views.sponsors, name='sponsors'),
    path('string_making', views.string_making, name='string_making'),
    path('wiki_compound', views.wiki_compound, name='wiki-compound'),
    path('wiki_longbow', views.wiki_longbow, name='wiki-longbow'),
    path('wiki_main', views.wiki_main, name='wiki-main'),
    path('wiki_recurve', views.wiki_recurve, name='wiki-recurve'),
]

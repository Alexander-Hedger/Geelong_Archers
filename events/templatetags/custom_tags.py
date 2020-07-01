from django import template
from accounts.models import Committee

register = template.Library()


@register.simple_tag
def validate(request):
    webmaster_id = Committee.objects.all().filter(
        position='Webmaster').values_list('member')

    return print('SUCCESS')

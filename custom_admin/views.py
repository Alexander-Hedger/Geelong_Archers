import os
import csv
import datetime
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from functions.functions import sidebar, scrape, bulk_scrape
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from awards.models import Awards
from events.models import EventIntro, EventComp, EventMotD
from accounts.models import Account, Committee
from contact_forms.models import ContactIntro
from pages.models import PageContent
from pages.forms import ContentForm
from PIL import UnidentifiedImageError, Image as PILImage
from django.core.files.storage import default_storage
from django.http import JsonResponse

regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


@login_required(login_url='home')
def admin_dashboard(request):
    context = sidebar(request)

    events_intro = EventIntro.objects.order_by(
        'date_start').filter(is_published=True)

    if events_intro.exists():
        try:
            intro_course_id = request.GET['intro_filter']
            event = EventIntro.objects.get(id=intro_course_id)
            contacts_intro = ContactIntro.objects.order_by(
                'contact_date').filter(event_id=event)

            context['value'] = int(intro_course_id)

        except:
            event = events_intro.first()
            contacts_intro = ContactIntro.objects.order_by(
                'contact_date').filter(event_id=event)

        context['contacts_intro'] = contacts_intro

    context['events_intro'] = events_intro

    return render(request, 'custom_admin/admin_dashboard.html', context)


@login_required(login_url='home')
def delete_contact(request):
    context = sidebar(request)

    if request.method == 'POST':

        contact_id = request.POST['contact_id']
        contact = ContactIntro.objects.get(id=contact_id)
        event = EventIntro.objects.get(id=contact.event_id.id)

        messages.success(
            request, f'{contact} has been removed from {contact.event_id}!')

        event.current_participants -= 1
        event.save()

        contact.delete()

    return redirect('admin_dashboard')


@login_required(login_url='home')
def bulk_upload_main(request):
    context = sidebar(request)
    return render(request, 'custom_admin/bulk_upload_main.html', context)


@login_required(login_url='home')
def bulk_event_update(request):
    context = sidebar(request)

    if request.method == 'POST':
        bulk_scrape(request)

    return render(request, 'custom_admin/bulk_event_update.html', context)


@login_required(login_url='home')
def committee_admin(request):
    context = sidebar(request)

    committee = Committee.objects.order_by(
        'order')
    context['committee'] = committee

    page = PageContent.objects.get(name='committee')
    context['page'] = page

    if request.method == 'POST':
        position = request.POST['position']
        member_name = request.POST['position_member']

        committee_position = Committee.objects.get(position=position)

        committee_position.member = member_name

        try:
            if request.FILES['position_photo']:
                print("new photo request")
                if committee_position.photo != 'photos/users/user_placeholder.jpg':
                    if os.path.isfile(committee_position.photo.path):
                        os.remove(committee_position.photo.path)

                photo = request.FILES['position_photo']
                committee_position.photo = photo

        except:
            pass

        try:
            if request.POST['delete_image']:
                if committee_position.photo != 'photos/users/user_placeholder.jpg':
                    if os.path.isfile(committee_position.photo.path):
                        os.remove(committee_position.photo.path)

                photo = 'photos/users/user_placeholder.jpg'
                committee_position.photo = photo
        except:
            pass

        committee_position.save()

    return render(request, 'custom_admin/committee_admin.html', context)


@login_required(login_url='home')
def page_editor(request, page):
    context = sidebar(request)

    page = PageContent.objects.get(name=page)

    if request.method == 'POST':
        page.content = request.POST['content']
        page.save()
        messages.success(request, 'Your Page has been edited!')

    page_content = PageContent.objects.order_by(
        'title')

    context['page_content'] = page_content
    context['page'] = page

    return render(request, 'custom_admin/page_editor.html', context)


@login_required(login_url='home')
def tinymce_image_handler(request):

    image = request.FILES
    print(image)

    try:
        is_image = PILImage.open(image)
        is_image.verify()
        file_path = default_storage.save(image.name, image)

        responseData = {
            "location": file_path,
        }

        print(JsonResponse(responseData))

        return JsonResponse(responseData)
    except UnidentifiedImageError:
        return


@login_required(login_url='home')
def bulk_upload_map(request):
    context = sidebar(request)

    if request.method == 'POST':
        csv_upload = request.FILES['csv_upload']

        if not csv_upload.name.endswith('.csv'):
            messages.error(request, 'Uploaded file MUST be a CSV file')
            return redirect('bulk_upload_main')

        fs = FileSystemStorage()
        filename = fs.save(csv_upload.name, csv_upload)
        uploaded_file_url = fs.path(filename)

        context['uploaded_file_url'] = uploaded_file_url

        with open(uploaded_file_url) as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            print(headers)

        if request.POST['data_type'] == 'awards':
            context['form_type'] = 'awards'

        if request.POST['data_type'] == 'members':
            context['form_type'] = 'members'

        if request.POST['data_type'] == 'intro':
            context['form_type'] = 'intro'

        if request.POST['data_type'] == 'comp':
            context['form_type'] = 'comp'

        if request.POST['data_type'] == 'motd':
            context['form_type'] = 'motd'

        context['headers'] = headers

    return render(request, 'custom_admin/bulk_upload_map.html', context)


@login_required(login_url='home')
def bulk_upload_tool(request, data_type):

    if request.method == 'POST':
        uploaded_file_url = request.POST['uploaded_file_url']

        total = 0
        uploaded = 0
        failed = 0
        exists = 0
        updated = 0

        with open(uploaded_file_url) as csv_file:
            reader = csv.DictReader(csv_file)

            if data_type == 'motd':
                for row in reader:
                    total += 1

                    title = row[request.POST['title']]
                    description = row[request.POST['description']]
                    start_date = row[request.POST['start_date']]
                    end_date = row[request.POST['end_date']]

                    upload, created = EventMotD.objects.get_or_create(
                        short_title=title,
                        short_description=description,
                        date_start=start_date,
                        date_end=end_date,
                    )

                    if created:
                        uploaded += 1
                    else:
                        upload.short_title = title
                        upload.short_description = description
                        upload.date_start = start_date
                        upload.date_end = end_date
                        updated += 1

                    upload.save()

            if data_type == 'award':
                for row in reader:
                    total += 1

                    award_name = row[request.POST['award_name']]
                    award_image = row[request.POST['award_image']]

                    upload, created = Awards.objects.get_or_create(
                        name=award_name,
                    )

                    upload.image = award_image

                    if created:
                        uploaded += 1
                        upload.save()
                    else:
                        try:
                            exist_check = Awards.objects.get(
                                name=award_name,
                                image=award_image
                            )
                            exists += 1

                        except Awards.DoesNotExist:
                            award_record = Awards.objects.get(name=award_name)
                            award_record.image = award_image
                            award_record.save()

                            updated += 1

            if data_type == 'member':
                for row in reader:
                    total += 1

                    email = row[request.POST['email']]
                    first_name = row[request.POST['first_name']]
                    last_name = row[request.POST['last_name']]
                    archery_australia_id = row[request.POST['archery_australia_id']]
                    birth_date = row[request.POST['birth_date']]
                    member_expiry = row[request.POST['member_expiry']]
                    password = row[request.POST['password']]

                    if(re.search(regex, email)) == None:
                        failed += 1
                        continue

                    if Account.objects.filter(email=email).exists():
                        exists += 1
                        continue

                    try:
                        birth_date_clean = datetime.datetime.strptime(
                            birth_date, '%d/%m/%Y').strftime('%Y-%m-%d')
                        member_expiry_clean = datetime.datetime.strptime(
                            member_expiry, '%d/%m/%Y').strftime('%Y-%m-%d')
                    except:
                        failed += 1
                        print('BIRTHDATE/MEMBER FAIL')
                        continue

                    upload, created = Account.objects.get_or_create(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        archery_australia_id=archery_australia_id,
                        birth_date=birth_date_clean,
                        member_expiry=member_expiry_clean,
                    )

                    if created:
                        uploaded += 1
                        upload.set_password(password)
                        upload.save()
                    else:
                        exists += 1

    if uploaded > 0:
        messages.success(
            request, f'{uploaded} of {total} records have been uploaded')
    if updated > 0:
        messages.success(
            request, f'{updated} of {total} records have been updated')
    if exists > 0:
        messages.info(request, f'{exists} of {total} records already exist')
    if failed > 0:
        messages.error(request, f'{failed} of {total} records have failed')

    os.remove(uploaded_file_url)

    return redirect('bulk_upload_main')

from django.shortcuts import render, redirect
from django.contrib import messages
from functions.functions import sidebar
from .models import Image, Album
from PIL import UnidentifiedImageError, Image as PILImage


def gallery_admin(request):
    context = sidebar()

    albums = Album.objects.order_by('title')

    context['albums'] = albums

    return render(request, 'gallery/gallery-admin.html', context)


def gallery_create(request):
    context = sidebar()

    if request.method == 'POST':
        title = request.POST['album_title']
        uploaded_images = request.FILES.getlist('images')
        position = 0

        new_album = Album(title=title, quantity=0)
        new_album.save()

        album = Album.objects.get(pk=new_album.pk)

        for uploaded_image in uploaded_images:

            try:
                is_image = PILImage.open(uploaded_image)
                is_image.verify()
                position += 1
                image_upload = Image(
                    album=album, image=uploaded_image, position=position)
                image_upload.save()

                image = Image.objects.get(pk=image_upload.pk)

                album.quantity += 1
                album.images.add(image)

            except UnidentifiedImageError:
                continue

        album.save()
        messages.success(request, 'Your album have been uploaded!')
        return redirect('gallery-admin')

    return render(request, 'gallery/gallery-create.html', context)


def gallery_main(request):
    context = sidebar()

    albums = Album.objects.order_by('title').filter(hidden=False)

    context['albums'] = albums

    return render(request, 'gallery/gallery-main.html', context)


def gallery_edit(request, album_id):
    context = sidebar()
    album = Album.objects.get(id=album_id)

    if request.method == 'POST':
        if request.POST['action_type'] == 'feature':

            images = request.POST.getlist('images')

            if len(images) > 1:
                messages.error(
                    request, 'Only one image can be the feature image')
                return redirect('gallery-edit', album_id)
            else:
                album.feature_image = Image.objects.get(pk=images[0])
                album.save()
                messages.success(
                    request, 'Featured Image has been updated')
                return redirect('gallery-edit', album_id)

        elif request.POST['action_type'] == 'delete':

            images = request.POST.getlist('images')
            count = 0

            for image in images:
                # image = Image.objects.get(pk=images[images.index(image)])
                image = Image.objects.get(pk=image)
                if album.feature_image == image:
                    album.feature_image = None

                # if album.feature_image == image:
                #     album.feature_image = None
                count += 1

                image.delete()
                album.quantity -= 1

            album.save()
            messages.success(request, f'{count} images deleted from album')
            return redirect('gallery-edit', album_id)

        elif request.FILES.getlist('upload_images'):

            uploaded_images = request.FILES.getlist('upload_images')
            exists = 0
            count = 0
            for uploaded_image in uploaded_images:
                try:
                    test = Image.objects.get(
                        image=f'photos/albums/{uploaded_image}')
                    print(test)
                    exists += 1
                    continue
                except:
                    image_upload = Image(
                        album=album, image=uploaded_image, position=0)
                    image_upload.save()

                    image = Image.objects.get(pk=image_upload.pk)

                    count += 1
                    album.quantity += 1
                    album.images.add(image)

            album.save()
            if count > 0:
                messages.success(request, f'{count} images uploaded!')
            if exists > 0:
                messages.info(
                    request, f'{exists} images already existed and were not uploaded')
            return redirect('gallery-edit', album_id)

        else:
            album.title = request.POST['album_title']

            if request.POST.get('album_hidden'):
                album.hidden = True
            else:
                album.hidden = False

            album.save()
            return redirect('gallery-admin')

    context['album'] = album
    return render(request, 'gallery/gallery-edit.html', context)


def gallery_delete(request, album_id):
    album = Album.objects.get(id=album_id)
    album.delete()

    messages.success(request, 'Your album have been deleted!')

    return redirect('gallery-admin')


def gallery_album(request, album_id):
    context = sidebar()
    album = Album.objects.get(id=album_id)

    context['album'] = album
    return render(request, 'gallery/gallery-album.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from functions.functions import sidebar
from django.shortcuts import redirect
from .models import Item, OrderItem, Order
from django.utils import timezone
# Create your views here.


def store_admin(request):
    context = sidebar()
    return render(request, 'store/store-admin.html', context)


def store_create(request):
    context = sidebar()
    return render(request, 'store/store-create.html', context)


def store_item(request, slug):
    context = sidebar()
    item = get_object_or_404(Item, slug=slug)
    context['item'] = item
    return render(request, 'store/store-item.html', context)


def store_checkout(request):
    context = sidebar()
    return render(request, 'store/store-item.html', context)


def store_main(request):
    context = sidebar()

    context['items'] = Item.objects.all()

    return render(request, 'store/store-main.html', context)


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_query = Order.objects.filter(user=request.user, ordered=False)

    # Checks if there is an order already
    if order_query.exists():
        order = order_query[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This item quantity was updated")
        else:
            messages.success(request, "This item was added to your cart")
            order.items.add(order_item)

    # If no order, create an order and add the order item to it
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item was added to your cart")

    return redirect('store-item', slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_query = Order.objects.filter(user=request.user, ordered=False)

    if order_query.exists():
        order = order_query[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect('store-item', slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('store-item', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('store-item', slug=slug)

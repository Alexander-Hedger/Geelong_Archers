from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functions.functions import sidebar
from django.shortcuts import redirect
from .models import Item, OrderItem, Order, Payment
from django.utils import timezone
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def store_admin(request):
    context = sidebar()
    return render(request, 'store/store-admin.html', context)


def store_create(request):
    context = sidebar()
    return render(request, 'store/store-create.html', context)


@login_required
def store_checkout(request):
    context = sidebar()

    if request.method == 'POST':
        order = Order.objects.get(user=request.user, ordered=False)
        # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
        token = request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)  # amount is in cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="aud",
                source=token,
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge.id
            payment.user = request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(request, "Your order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network Error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(
                request, "Something went wrong. You were not charged. Please try again")
            return redirect("/")

        except Exception as e:
            # Send email to webmaster as error is server side
            messages.error(
                request, "A serious error occurred. We have been notified")
            return redirect("/")

    return render(request, 'store/store-checkout.html', context)


def store_item(request, slug):
    context = sidebar()
    item = get_object_or_404(Item, slug=slug)
    context['item'] = item
    return render(request, 'store/store-item.html', context)


def store_main(request):
    context = sidebar()

    context['items'] = Item.objects.all()

    return render(request, 'store/store-main.html', context)


@login_required
def store_order_summary(request):
    context = sidebar()

    try:
        context['order'] = Order.objects.get(user=request.user, ordered=False)

        return render(request, 'store/store-order-summary.html', context)

    except ObjectDoesNotExist:
        messages.error(request, "You do not have an active order")
        return redirect("/")


@login_required
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


@login_required
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
            return redirect('store-order-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('store-item', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('store-item', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_query = Order.objects.filter(user=request.user, ordered=False)

    if order_query.exists():
        order = order_query[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect('store-order-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('store-item', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('store-item', slug=slug)


@login_required
def add_single_item_to_cart(request, slug):
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

    return redirect('store-order-summary')

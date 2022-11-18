from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

import stripe

from payments.models import Item

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

def index(request):
    return HttpResponse("Hello, this is a simple API with 2 methods ('/buy/1' and '/sitem/1').")

def success(request):
    return HttpResponse("Success")

def cancel(request):
    return HttpResponse("Cancel")

def buy_item(request, item_id):
    
    try:
      item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
      item = None

    if item:
      session = stripe.checkout.Session.create(
          line_items=[{
          'price_data': {
              'currency': 'usd',
              'product_data': {
              'name': item.name,
              },
              'unit_amount': item.price * 100,
          },
          'quantity': 1,
          }],
          mode='payment',
          success_url=request.build_absolute_uri(reverse('success')),
          cancel_url=request.build_absolute_uri(reverse('cancel')),
      )
      return JsonResponse({'session_id': session.stripe_id})
    else:
      return JsonResponse({'session_id': None}, status=404)


def get_item(request, item_id):
    try:
      item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
      item = None
    if item:
      context = {'item': item}
      return render(request, 'payments/get_item.html', context=context)
    else:
      return JsonResponse({'status': 'not found'}, status=404)
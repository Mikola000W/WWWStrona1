from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import JsonResponse

from items.models import Item


def item_list(request):
    items = Item.objects.all()
    context = {
        'customers': items,
    }
    return render(request, 'items/item_list.html', context=context)


def item_table(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'items/item_table.html', context=context)


def item_create(request):
    data = {}
    if request.method == 'POST':
        data['name'] = request.POST.get('name')
        data['description'] = request.POST.get('description')
        data['price'] = request.POST.get('price', '')
        data['code'] = request.POST.get('code', '')
        data['is_available'] = bool(request.POST.get('is_available', ''))
        item = Item(**data)

        if request.method == 'POST':

            name = request.POST['name']
            if Item.objects.filter(name=name).exists():
                return render(request, 'items/item_create.html', {'errors': 'You already used this name'})

        if data['name'] and data['description'] and data['price'] and data['is_available']:
            try:
                item.save()
                item_list_url = reverse_lazy('home')
                return HttpResponseRedirect(item_list_url)
            except Exception as e:
                print(e)
        else:
            data['errors'] = 'Fill all brackets'

    return render(request, 'items/item_create.html', context=data)

def add_to_cart(request, item_id):
    # print('item id', item_id)
    cart_in_session = request.session['cart'] if 'cart' in request.session else []
    cart_in_session.append(item_id)
    # request.session.flush('cart')
    request.session.update({'cart': cart_in_session})
    # print('session', request.session['cart'])
    return JsonResponse({'message': 'Added item to cart.'})


def delete_from_cart(request):
    cart_in_session = request.session['cart'] if 'cart' in request.session else []
    cart_in_session.clear()
    request.session.update({'cart': cart_in_session})
    return render(request, 'items/cart.html')

def cart(request):
    cart_in_session = request.session['cart'] if 'cart' in request.session else []

    context = {'cart': []}
    amount = 0
    items = Item.objects.filter(id__in=cart_in_session)

    for item in items:
        counter = cart_in_session.count(item.id)
        context['cart'].append({'item_object': item, 'count': counter})
        amount += counter * item.price

    context.update({'amount': amount})

    return render(request, 'items/cart.html', context=context)
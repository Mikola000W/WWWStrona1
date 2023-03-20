from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy

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
    print("Hello")
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

        if data['name'] and data['description'] and data['price']:
            try:
                item.save()
                item_list_url = reverse_lazy('home')
                return HttpResponseRedirect(item_list_url)
            except Exception as e:
                print(e)
        else:
            data['errors'] = 'Fill all brackets'

    return render(request, 'items/item_create.html', context=data)

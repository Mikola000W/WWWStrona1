from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from customers.models import User
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

def customer_list(request):
    customers = User.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'customers/customer_list.html', context=context)


def customer_table(request):
    customers = User.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'customers/customer_table.html', context=context)


def home(request):
    return render(request, 'home.html')


def customer_create(request):
    data = {}
    if request.method == 'POST':
        data['first_name'] = request.POST.get('first_name')
        data['last_name'] = request.POST.get('last_name')
        data['street'] = request.POST.get('street', '')
        data['city'] = request.POST.get('city', '')
        data['state'] = request.POST.get('state', '')
        data['zip_code'] = request.POST.get('zip_code', '')
        data['country'] = request.POST.get('country', '')
        data['username'] = request.POST.get('username', '')
        password = request.POST.get('password', '')
        customer = User(**data)

        if request.method == 'POST':

            username = request.POST['username']
            if User.objects.filter(username=username).exists():
                return render(request, 'customers/customer_create.html', {'errors': 'You already used this name'})


        if data['first_name'] and data['last_name'] and data['username']:
            try:
                customer.set_password(password)
                customer.save()
                customer_list_url = reverse_lazy('home')
                return HttpResponseRedirect(customer_list_url)
            except Exception as e:
                print(e)
        else:
            data['errors'] = 'First Name and Last Name fields are required'

    return render(request, 'customers/customer_create.html', context=data)


def customer_detail(request, pk):
    try:
        customer = User.objects.get(pk=pk)
    except User.DoesNotExist as e:
        print(e)
        customer = User.objects.none()

    context = {
        'customer': customer,
    }
    return render(request, 'customers/customer_detail.html', context=context)


def customer_update(request, pk):
    customer = User.objects.get(pk=pk)
    data = {'customer': customer}
    if request.method == 'POST':
        customer.first_name = request.POST.get(
            'first_name', customer.first_name)
        customer.last_name = request.POST.get('last_name', customer.last_name)
        customer.street = request.POST.get('street', customer.street)
        customer.city = request.POST.get('city', customer.city)
        customer.state = request.POST.get('state', customer.state)
        customer.zip_code = request.POST.get('zip_code', customer.zip_code)
        customer.country = request.POST.get('country', customer.country)

        if customer.first_name and customer.last_name:
            try:
                customer.save()
                customer_detail_url = reverse_lazy(
                    'customer_detail', kwargs={'pk': pk})
                return HttpResponseRedirect(customer_detail_url)
            except Exception as e:
                print(e)
                data['errors'] = str(e)
        else:
            data['errors'] = 'First Name and Last Name fields are required'

    return render(request, 'customers/customer_update.html', context=data)


class CustomUserCreationForm(UserCreationForm):
    password_confirm = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("Enter the same password as above, for verification."),
        required=True,
    )

def clean_password(self):
    password = self.cleaned_data.get('password')
    if not re.search("[a-z]", password):
        raise forms.ValidationError(_("The password must contain at least one lowercase letter."))
    if not re.search("[A-Z]", password):
        raise forms.ValidationError(_("The password must contain at least one uppercase letter."))
    if not re.search("[0-9]", password):
        raise forms.ValidationError(_("The password must contain at least one digit."))
    if not re.search("[@#$%^&+=]", password):
        raise forms.ValidationError(_("The password must contain at least one special character (@#$%^&+=)."))
    if len(password) < 8:
        raise forms.ValidationError(_("The password must be at least 8 characters long."))
    return password

def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    password_confirm = cleaned_data.get('password_confirm')
    if password and password_confirm and password != password_confirm:
        raise forms.ValidationError(_("The two password fields must match."))
    return cleaned_data

class Meta:
    model = User
    fields = UserCreationForm.Meta.fields + ('password_confirm',)
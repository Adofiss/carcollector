from secrets import token_bytes
from django.shortcuts import render, redirect
from .models import Car, Mod
from .forms import MaintenanceForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse


# Define the home view


def home(request):
    return HttpResponse(request, 'home.html')


def about(request):
    return render(request, 'about.html')


class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['name', 'hp', 'description', 'year', 'msrp', 'img']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/cars/'


class CarUpdate(UpdateView):
    model = Car
    fields = ['hp', 'description', 'year', 'msrp', 'img']
    success_url = '/cars/'


class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'

@login_required
def cars_index(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, 'cars/index.html', {'cars': cars})


def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    id_list = car.mods.all().values_list('id')
    mods_car_doesnt_have = Mod.objects.exclude(id__in=id_list)
    maintenance_form = MaintenanceForm
    return render(request, 'cars/detail.html', {
        'car': car, 'maintenance_form': maintenance_form,
        'mods': mods_car_doesnt_have
    })


def add_maintenance(request, car_id):
    form = MaintenanceForm(request.POST)
    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.car_id = car_id
        new_maintenance.save()
        return redirect('detail', car_id=car_id)


class ModList (ListView):
    model = Mod


class ModDetail(DetailView):
    model = Mod


class ModCreate(CreateView):
    model = Mod
    fields = '__all__'
    success_url = '/mods/'


class ModUpdate(UpdateView):
    model = Mod
    fields = ['name', 'price']
    success_url = '/mods/'


class ModDelete(DeleteView):
    model = Mod
    success_url = '/mods/'


def assoc_mod(request, car_id, mod_id):
    car = Car.objects.get(id=car_id)
    car.mods.add(mod_id)
    return redirect('detail', car_id=car_id)


def unassoc_mod(request, car_id, mod_id):
    car = Car.objects.get(id=car_id)
    car.mods.remove(mod_id)
    return redirect('detail', car_id=car_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up credentials - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

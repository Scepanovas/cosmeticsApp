from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, filters
from restApp.serializers import *
from modelsViews.models import *
from .forms import ClientLoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

class Top15(TemplateView):
    template_name = 'top15.html'
class Ingredients(TemplateView):
    template_name = 'ingredients.html'
class Products(TemplateView):
    template_name = 'products.html'
class ViewProduct(TemplateView):
    template_name = 'viewProduct.html'
class Brands(TemplateView):
    template_name = 'brands.html'
class Profile(TemplateView):
    template_name = 'profile.html'
class SkinTest(TemplateView):
    template_name = 'skinTest.html'
class Register(TemplateView):
    template_name = 'register.html'
class CreateProduct(TemplateView):
    template_name = 'createProduct.html'

def ClientAccView(request):
    if request.user.is_authenticated:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ClientFormView(View):
    form_class = ClientLoginForm

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def LogoffView(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

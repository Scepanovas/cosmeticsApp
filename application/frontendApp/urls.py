from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import *

# Redirect any request that goes into here to static/index.html
urlpatterns = [
    url(r'^$', Top15.as_view(), name='top15'),
    url(r'^produktai/', Products.as_view(), name='products'),
    url(r'^naujas_produktas/', CreateProduct.as_view(), name='createProduct'),
    url(r'^produktas/', ViewProduct.as_view(), name='viewProduct'),
    url(r'^prekeszenklai/', Brands.as_view(), name='brands'),
    url(r'^ingredientai/', Ingredients.as_view(), name='ingredients'),

    url(r'^odos-testas/', SkinTest.as_view(), name='skintest'),
    url(r'^profilis/', Profile.as_view(), name='profile'),
    url(r'^registracija/', Register.as_view(), name='register'),

    url(r'^', include('django.contrib.auth.urls')),
    url(r'^logoff/$', LogoffView, name='logoff'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

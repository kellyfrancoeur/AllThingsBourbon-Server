"""AllThingsBourbon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from AllThingsBourbonAPI.views import register_user, login_user
from django.conf.urls import include
from rest_framework import routers
from AllThingsBourbonAPI.views import BourbonView, CocktailView, DistilleryView, CocktailTypeView, BourbonTypeView, BourbonUserView, BourbonStaffView, BourbonsTriedView, CocktailsTriedView, DistilleriesVisitedView, DescriptorView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bourbons', BourbonView, 'bourbon')
router.register(r'descriptors', DescriptorView, 'descriptor')
router.register(r'cocktails', CocktailView, 'cocktail')
router.register(r'distilleries', DistilleryView, 'distillery')
router.register(r'bourbontypes', BourbonTypeView, 'bourbontype')
router.register(r'cocktailtypes', CocktailTypeView, 'cocktailtype')
router.register(r'bourbonstaffs', BourbonStaffView, 'bourbonstaff')
router.register(r'bourbonusers', BourbonUserView, 'bourbonuser')
router.register(r'bourbonstried', BourbonsTriedView, 'bourbontried')
router.register(r'cocktailstried', CocktailsTriedView, 'cocktailtried')
router.register(r'distilleriesvisited',
                DistilleriesVisitedView, 'distilleryvisited')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

"""nexiaEnhance URL Configuration

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
from django.urls import path, include
from nexiaEnhance import views

from riskreg import views_dashboard as riskregviews

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path('home/', riskregviews.RiskRegHomeView.as_view(), name='index'),
    # path('home/', views.HomePage.as_view(), name='index'),

    # Error page:
    path('error/',views.ErrorView.as_view(),name='error'),

    # login
    path("", auth_views.LoginView.as_view(template_name="accounts/08_b_login_video.html"), name='login'),

    # Risk Database:
    path('risk-database/', include('riskdatabase.urls', namespace='risk-database')),

    # Risk Register:
    path('risk-register/',include('riskregister.urls', namespace='risk-register')),

    # Risk Register 2:
    path('risk-register-2/',include('riskreg.urls', namespace='risk-register-2')),

    # Administration:
    path('annual-declaration/', include('annualdeclaration.urls', namespace="annual_declaration")),

    # Administration:
    path('accounts/',include('accounts.urls', namespace="accounts")),

    # path(r"^test/$", views.TestPage.as_view(), name="test"),
    path("thanks/", views.ThanksPage.as_view(), name="thanks"),


]

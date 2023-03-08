"""isqm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from annualdeclaration import views

# TEMPLATE TAGGING
app_name = 'annual_declaration'

urlpatterns = [
    # 0.0. Success and error urls:
    # path('success/', views.SuccessView.as_view(), name='success'),
    # path('error/', views.ErrorView.as_view(), name='error'),

    # Annual declaration:
    # 1. Make declaration:
    # path('make-declaration/', views.MakeDeclarationView.as_view(), name='make-declaration'),
    # 2. View declaration:
    # path('view-declaration/', views.ViewDeclarationView.as_view(), name='view-declaration'),
    path('view-declaration/', views.ViewDeclarations.as_view(), name='view-declaration'),
    path('view-declaration/<int:pk>/', views.ViewDeclarationsDetail.as_view(), name='view-declaration'),

    # 3. Test Date:
    path('date-test/', views.MakeDeclarationView.as_view(), name='date-test'),

    # 4. Edit
    path('edit-declaration/<int:pk>', views.EditDeclaration.as_view(), name='edit-declaration'),

    # 5. Delete
    path('delete-declaration/<int:pk>', views.DeleteDeclaration.as_view(), name='delete-declaration'),

]

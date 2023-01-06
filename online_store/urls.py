"""online_store URL Configuration

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
from django.urls import path
from products.views import main_view, CategoriesCBV, ProductsCBV, ProductsDetailCBV, PostCreateCBV
from django.conf.urls.static import static
from online_store import settings
from users.views import LoginViewCBV, LogoutCBV, RegisterCBV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main_view),
    path('products/', ProductsCBV.as_view()),
    path('products/<int:pk>/',ProductsDetailCBV.as_view()),
    path('product/create', PostCreateCBV.as_view()),
    path('categories/', CategoriesCBV.as_view()),
    path('users/login/', LoginViewCBV.as_view()),
    path('users/logout', LogoutCBV.as_view()),
    path('users/register/', RegisterCBV.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
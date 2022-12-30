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
from products.views import main_view, products_view, products_detail_view, categories_view, post_create_view
from django.conf.urls.static import static
from online_store import settings
from users.views import login_view, logout_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main_view),
    path('products/', products_view),
    path('products/<int:id>/', products_detail_view),
    path('product/create', post_create_view),
    path('categories/', categories_view),
    path('users/login/', login_view),
    path('users/logout', logout_view),
    path('users/register/', register_view)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
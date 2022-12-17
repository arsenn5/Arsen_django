from django.shortcuts import HttpResponse, render
from products.models import Products

# Create your views here.

def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Products.objects.all()
        print(products)
        return render(request, 'products/products.html', context={'products': products})

def products_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)
        print(product)
        data = {
            'product': product,
            'review': product.review.all()
        }
        return render(request, 'products/detail.html', context=data)

from django.shortcuts import HttpResponse, render
from products.models import Products, Category


# Create your views here.

def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Products.objects.all()
        category_id = request.GET.get('category_id', None)
        if category_id:
            products = products.filter(category__in=[category_id])
        return render(request, 'products/products.html', context={'products': products})


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)
        print(product)
        data = {
            'product': product,
            'review': product.review.all(),
            'category': product.category.all()
        }
        return render(request, 'products/detail.html', context=data)


def categories_view(request):
    if request.method == 'GET':
        category = Category.objects.all()

        context = {
            'category': category
        }
        return render(request, 'category/index.html', context=context)

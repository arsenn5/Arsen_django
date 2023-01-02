from django.shortcuts import render, redirect
from users.utils import get_user_from_request

from products.forms import ReviewCreateForm
from products.models import Products, Category, Review

PAGINATION_LIMIT = 6


# Create your views here.

def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html', context={'user': get_user_from_request(request)})


def products_view(request):
    if request.method == 'GET':
        products = Products.objects.all()
        category_id = request.GET.get('category_id', None)
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = products.filter(category__in=[category_id])
        if search:
            products = products.filter(title__icontains=search)


        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]



        return render(request, 'products/products.html', context={
            'products': products,
            'user': get_user_from_request(request),
            'maх_page': range(1, max_page + 1)
        })


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)

        data = {
            'product': product,
            'review': product.review.all(),
            'category': product.category.all(),
            'review_form': ReviewCreateForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'products/detail.html', context=data)
    if request.method == 'POST':
        product = Products.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author=request.user,
                product_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')
        else:
            return render(request, 'products/detail.html', context={
                'product': product,
                'review': product.review.all(),
                'category': product.category.all(),
                'review_form': form,
                'user': get_user_from_request(request)
            })


def categories_view(request):
    if request.method == 'GET':
        category = Category.objects.all()

        context = {
            'category': category,
            'user': get_user_from_request(request)
        }
        return render(request, 'category/index.html', context=context)


def post_create_view(request, **kwargs):
    if request.method == 'GET':
        return render(request, 'products/create.html', context={"user": get_user_from_request(request)})

    if request.method == 'POST':
        errors = {}

        if len(request.POST.get('title')) < 8:
            errors['title_error'] = 'min length 8'

        if len(request.POST.get('description')) < 1:
            errors['description_errors'] = 'this field required'

        Products.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            rate=request.POST.get('rate', 0)
        )
        return redirect("/products/")

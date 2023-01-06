from django.shortcuts import render, redirect
from users.utils import get_user_from_request

from products.forms import ReviewCreateForm, ProductCreateForm
from products.models import Products, Category, Review
from django.views.generic import ListView, DetailView, CreateView

PAGINATION_LIMIT = 6


# Create your views here.

def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html', context={'user': get_user_from_request(request)})


class ProductsCBV(ListView):
    queryset = Products.objects.all()
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'products': self.get_queryset()
        }

    def get(self, request, **kwargs):
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

        print(max_page)
        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        return render(request, 'products/products.html', context={
            'products': products,
            'user': get_user_from_request(request),
            'maх_page': range(1, round(max_page) + 1)
        })


# def products_view(request):
#     if request.method == 'GET':
#         products = Products.objects.all()
#         category_id = request.GET.get('category_id', None)
#         search = request.GET.get('search')
#         page = int(request.GET.get('page', 1))
#
#         if category_id:
#             products = products.filter(category__in=[category_id])
#
#         if search:
#             products = products.filter(title__icontains=search)
#
#         max_page = products.__len__() / PAGINATION_LIMIT
#
#         if round(max_page) < max_page:
#             max_page = round(max_page) + 1
#
#         print(max_page)
#         products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]
#
#         return render(request, 'products/products.html', context={
#             'products': products,
#             'user': get_user_from_request(request),
#             'maх_page': range(1, round(max_page) + 1)
#         })


class ProductsDetailCBV(DetailView, CreateView):
    template_name = 'products/detail.html'

    def get(self, request, pk=None, **kwargs):
        product = Products.objects.get(pk=pk)
        data = {
            'product': product,
            'review': product.review.all(),
            'categories': product.category.all(),
            'form': ReviewCreateForm,
            'user': None if request.user.is_anonymous else request.user
        }
        return render(request, 'products/detail.html', context=data)

    def post(self, request, pk=None):
        product = Products.objects.get(pk=pk)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author_id=request.user.id,
                product_id=pk,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{pk}/')
        else:
            return render(request, 'products/detail.html', context={
                'product': product,
                'category': product.category,
                'form': form,
                'review': product.review.all()
            })


# def products_detail_view(request, id):
#     if request.method == 'GET':
#         product = Products.objects.get(id=id)
#
#         data = {
#             'product': product,
#             'review': product.review.all(),
#             'category': product.category.all(),
#             'review_form': ReviewCreateForm,
#             'user': get_user_from_request(request)
#         }
#         return render(request, 'products/detail.html', context=data)
#     if request.method == 'POST':
#         product = Products.objects.get(id=id)
#         form = ReviewCreateForm(data=request.POST)
#
#         if form.is_valid():
#             Review.objects.create(
#                 author=request.user,
#                 product_id=id,
#                 text=form.cleaned_data.get('text')
#             )
#             return redirect(f'/products/{id}/')
#         else:
#             return render(request, 'products/detail.html', context={
#                 'product': product,
#                 'review': product.review.all(),
#                 'category': product.category.all(),
#                 'review_form': form,
#                 'user': get_user_from_request(request)
#             })

class CategoriesCBV(ListView):
    template_name = 'category/index.html'
    queryset = Category.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'category': self.get_queryset()
        }


class PostCreateCBV(CreateView):
    form_class = ProductCreateForm
    template_name = 'products/create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            Products.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                rate=request.POST.get('rate', 0)
            )
        return redirect('/products')

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class
        }

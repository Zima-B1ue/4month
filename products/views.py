import products

from django.shortcuts import render, redirect

import products
from onlinestore.form import ProductCreateForm, CommentsCreateForm
from products.models import Products, Comment
from products.constans import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView, DeleteView


# Create your views here.
class MainPageCBV(ListView):
    model = Products


class ProductCBV(ListView):
    model = Products
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get(self, request, **kwargs):
        search = request.GET.get('search')
        products = self.get_queryset().order_by('-created_date', '-rate')
        page = int(request.GET.get('page', 1))

        if search:
            products = \
                products.filter(title__icontains=search) | products.filter(description__icontains=search)
        max_page = products.__len__() / PAGINATION_LIMIT
        # max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)

        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'products': products,
            "user": request.user,
            'pages': range(1, max_page + 1)
        }
        return render(request, self.template_name, context=context)


class ProductDetailCBV(DetailView, CreateView):
    model = Products
    template_name = 'products/detail.html'
    form_class = CommentsCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'product': self.get_object(),
            'Reviews': Comment.objects.filter(product=self.get_object()),
            'form': kwargs.get('form', self.form_class)
        }

    def post(self, request, **kwargs):
        form = CommentsCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                rate=form.cleaned_data.get('rate'),
                product_id=self.get_object().id,
            )
            return redirect(f'/products/{self.get_object().id}/')

        return render(request, self.template_name, context=self.get_context_data(
            form=form
        ))


class CreateProductCBV(CreateView, ListView):
    model = Products
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title'),
                quantity=form.cleaned_data.get('quantity'),
                image=form.cleaned_data.get('image'),
                description=form.cleaned_data.get('description')
            )
            return redirect('/products/')
        return render(request, self.template_name, context={self.get_context_data(form=form)})

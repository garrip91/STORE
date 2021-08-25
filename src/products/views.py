from django.shortcuts import render, HttpResponseRedirect

from .models import ProductCategory, Product, Basket

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.views.generic import ListView
from django.db.models import Q


# Create your views here.
def index(request):

    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)
    
    
def products(request, category_id=None, page=1):

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
    }
    if category_id:
        # context.update({
            # 'products': Product.objects.filter(category_id=category_id)
        # })
        products = Product.objects.filter(category_id=category_id)
    else:
        # context.update({
            # 'products': Product.objects.all()
        # })
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page)
    context.update({
        'products': products_paginator
    })
    return render(request, 'products/products.html', context)
    
    
class SearchResultsView(ListView):

    model = Product
    context_object_name = 'object_list'
    template_name = 'products/search_results.html'
    
    def get_queryset(self):
        search_query = self.request.GET.get('q')
        print(F'{search_query}')
        object_list = Product.objects.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(short_description__icontains=search_query)
        )
        if Product.objects.filter(name__icontains=search_query).exists():
            print(F'{object_list}')
        else:
            print("Товара(-ов) с таким ***[ НАЗВАНИЕМ ]*** нет!")
        return object_list
    

@login_required
def basket_add(request, product_id):

    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)
        

@login_required
def basket_delete(request, id):

    current_page = request.META.get('HTTP_REFERER')
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(current_page)
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'main/product/list.html', context={
        'category': category,
        'categories': categories,
        'products': products,
    })
    
    
def product_details(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,
                                              available=True).exclude(id=product.id)[:4]
    return render(request, 'main/product/detail.html', context={'product': product,
                                                                'related_products': related_products})
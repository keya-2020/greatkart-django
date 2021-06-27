
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
from .models import Products
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

def store(request, category_slug=None):# filter la page en fonction de la category
    categories = None
    products = None
    
    if category_slug != None: 
        categories = get_object_or_404(Category, slug=category_slug)  # Element pour faire le filtre
        products = Products.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')# recuperation de la page dans request
        paged_products = paginator.get_page(page) # charger les données correspondantes dans la page
        products_count = products.count()
    else:# implémenter une pagination
        products = Products.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')# recuperation de la page dans request
        paged_products = paginator.get_page(page) # charger les données correspondantes dans la page
        products_count = products.count()
    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() # verification si le produit est dans le panier
    except Exception as e:
        raise e
    context = {
        'in_cart': in_cart,
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)

def search(request): # fonction de recherche
    
    if 'keyword' in request.GET: #vérifier que le mot keyword se trouve dans la request
        keyword = request.GET['keyword'] #Recuperer la valeur de keyword
        if keyword:
            products = Products.objects.order_by('-create_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            productS_count = products.count()
    context = {
        'products': products,
        'products_count': productS_count,
    }
    return render(request, 'store/store.html', context)
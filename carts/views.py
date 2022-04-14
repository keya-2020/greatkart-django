from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import (get_object_or_404, redirect, render)
from store.models import Products, Variation
from .models import (Cart, CartItem)
from django.contrib.auth.decorators import login_required


# Create your views here.

# Recuper l'identification de la session
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# L'ajouter un produit dans le panier
def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    # Ajout au paniel si l'utilisateur est connecté
    current_user = request.user
    if current_user.is_authenticated:

        product_variation = []  # liste vide pour accueillir les éléments de variation
        if request.method == 'POST':
            for item in request.POST:  # recuperer la clé et valeur de la requete POST
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)  # ajout des éléments dans la liste
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # on va chaque cart_item et récuperer les variations
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()  # retourne un queryset
                ex_var_list.append(list(existing_variation))  # convertir en list
                id.append(item.id)  # recuperation dans id des carts dans une list

                if product_variation in ex_var_list:
                    # increase the cart item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]  # on recuperer l'id en fonction de l'index
                    cart_item = CartItem.objects.get(product=product, id=item_id)
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:  # vérifier que le tableau n'est pas vide
                        cart_item.variation.clear()
                        cart_item.variation.add(*product_variation)
                    cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1,
            )
            if len(product_variation) > 0:  # vérifier que le tableau n'est pas vide
                cart_item.variation.clear()
                # et parcourir le tableau
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # si l'utilisateur n'est pas authentifié
    else:
        product = Products.objects.get(id=product_id)
        product_variation = []  # liste vide pour accueillir les éléments de variation
        if request.method == 'POST':
            for item in request.POST:  # recuperer la clé et valeur de la requete POST
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)  # ajout des éléments dans la liste
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # on va chaque cart_item et récuperer les variations
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()  # retourne un queryset
                ex_var_list.append(list(existing_variation))  # convertir en list
                id.append(item.id)  # recuperation dans id des carts dans une list

                if product_variation in ex_var_list:
                    # increase the cart item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]  # on recuperer l'id en fonction de l'index
                    cart_item = CartItem.objects.get(product=product, id=item_id)
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                    if len(product_variation) > 0:  # vérifier que le tableau n'est pas vide
                        cart_item.variation.clear()
                        cart_item.variation.add(*product_variation)
                    cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,
            )
            if len(product_variation) > 0:  # vérifier que le tableau n'est pas vide
                cart_item.variation.clear()
                # et parcourir le tableau
                cart_item.variation.add(*product_variation)
            cart_item.save()
    return redirect('cart')


# Supprimer un produit du panier
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Products,
                                id=product_id)  # on utilise get_object_or_404 car product_id provient de l'url
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart_id=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


# Supprimer l'élément produit du panier
def remove_item_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            # on utilise get_object_or_404 car product_id provient de l'url
            cart_item = CartItem.objects.get(product=product, cart_id=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')


# creation du panier
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        grand_total = 0
        tax = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # faire un filtre sur la clé étrangère cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    grand_total, tax = 0, 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # faire un filtre sur la clé étrangère cart
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

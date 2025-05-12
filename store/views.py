from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Order, OrderItem, Banner

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.all()[:6]
    banners = Banner.objects.filter(active=True)  # только активные баннеры
    return render(request, 'store/index.html', {
        'categories': categories,
        'featured_products': featured_products,
        'banners': banners,
    })

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html',
                  {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    items, total = [], 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        items.append({'product': product, 'quantity': qty})
        total += product.price * qty
    return render(request, 'store/cart.html', {'items': items, 'total': total})

def checkout(request):
    if request.method == 'POST':
        phone   = request.POST.get('phone')
        address = request.POST.get('address', '')
        cart    = request.session.get('cart', {})
        if not cart:
            return redirect('home')
        order = Order.objects.create(phone=phone, address=address)
        total = 0
        for pid, qty in cart.items():
            product = get_object_or_404(Product, pk=int(pid))
            OrderItem.objects.create(order=order, product=product,
                                     quantity=qty, price=product.price)
            total += product.price * qty
        order.total_price = total
        order.save()
        request.session['cart'] = {}
        # здесь будет логика оплаты Kaspi
        return render(request, 'store/checkout.html', {'order': order})
    return render(request, 'store/checkout.html')
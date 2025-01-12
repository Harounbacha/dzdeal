from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Category, Order, OrderItem, Cart, CartItem, Favorite
from .forms import ProductForm
from django.db.models import Q
from django.http import JsonResponse

def home(request):
    featured_products = Product.objects.filter(featured=True)[:8]
    latest_products = Product.objects.order_by('-created_at')[:8]
    categories = Category.objects.all()  # Get all categories
    print("Categories in home view:", [(c.name, c.slug) for c in categories])  # Debug print
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,  # Pass categories to template
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Check if product is in user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'is_favorite': is_favorite
    }
    return render(request, 'core/product_detail.html', context)

def category_products(request, category):
    category_obj = get_object_or_404(Category, slug=category)
    products = Product.objects.filter(category=category_obj)
    return render(request, 'core/product_list.html', {
        'products': products,
        'category': category_obj
    })

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ) if query else Product.objects.none()
    return render(request, 'core/product_list.html', {
        'products': products,
        'search_query': query
    })

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = []
    total = 0
    
    if cart:
        cart_items = cart.items.all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/orders.html', {'orders': orders})

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    favorite_products = [favorite.product for favorite in favorites]
    return render(request, 'core/favorites.html', {'products': favorite_products})

@login_required
def seller_center(request):
    user_products = Product.objects.filter(seller=request.user)
    return render(request, 'core/seller_center.html', {'products': user_products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'تم إضافة المنتج بنجاح')
            return redirect('core:seller_center')
    else:
        form = ProductForm()
    
    return render(request, 'core/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المنتج بنجاح')
            return redirect('core:seller_center')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'core/edit_product.html', {
        'form': form,
        'product': product
    })

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'تم حذف المنتج بنجاح')
        return redirect('core:seller_center')
    return render(request, 'core/delete_product.html', {'product': product})

@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        # Check if we have enough stock
        if cart_item.quantity > product.stock:
            return JsonResponse({
                'status': 'error',
                'message': 'عذراً، الكمية المطلوبة غير متوفرة في المخزون'
            })
            
        cart_item.save()
        
        cart_count = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'status': 'success',
            'message': 'تمت إضافة المنتج إلى السلة',
            'cart_count': cart_count
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'المنتج غير موجود'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'حدث خطأ أثناء إضافة المنتج إلى السلة'
        })

@login_required
@require_POST
def update_cart(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 0))
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            message = 'تم حذف المنتج من السلة'
        else:
            if quantity > cart_item.product.stock:
                return JsonResponse({
                    'status': 'error',
                    'message': 'عذراً، الكمية المطلوبة غير متوفرة في المخزون'
                })
            
            cart_item.quantity = quantity
            cart_item.save()
            message = 'تم تحديث الكمية'
        
        cart = cart_item.cart
        cart_total = sum(item.product.price * item.quantity for item in cart.items.all())
        cart_count = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'status': 'success',
            'message': message,
            'cart_total': cart_total,
            'cart_count': cart_count
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'المنتج غير موجود في السلة'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'حدث خطأ أثناء تحديث السلة'
        })

@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        
        cart = Cart.objects.get(user=request.user)
        cart_total = sum(item.product.price * item.quantity for item in cart.items.all())
        cart_count = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'status': 'success',
            'message': 'تم حذف المنتج من السلة',
            'cart_total': cart_total,
            'cart_count': cart_count
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'المنتج غير موجود في السلة'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'حدث خطأ أثناء حذف المنتج من السلة'
        })

@login_required
@require_POST
def toggle_favorite(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
        message = 'تم إزالة المنتج من المفضلة'
    else:
        is_favorite = True
        message = 'تم إضافة المنتج إلى المفضلة'
    
    return JsonResponse({
        'status': 'success',
        'is_favorite': is_favorite,
        'message': message
    })

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def policies(request):
    return render(request, 'core/policies.html')

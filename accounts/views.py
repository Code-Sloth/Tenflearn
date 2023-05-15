from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAutentication, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from courses.models import Review
from courses.models import Course
from decimal import Decimal
from accounts.models import ShoppingCart



def login(request):
    if request.method == 'POST':
        form = CustomAutentication(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('courses:index')
    else:
        form = CustomAutentication()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('courses:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('courses:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('courses:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('courses:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('courses:index')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('courses:index')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def mypage(request):
    q = request.GET.get('q')
    
    context = {
        'q': q,
    }
    return render(request, 'accounts/mypage.html', context)


@login_required
def add_cart(request, course_id):
    course = Course.objects.get(id=course_id)
    quantity = 1
    
    # Add the course to the cart for the authenticated user
    request.user.cart_courses.add(course)
    
    return redirect('accounts:mypage')


@login_required
def remove_cart(request, course_id):
    course = Course.objects.get(id=course_id)
    
    # Remove the course from the cart for the authenticated user
    request.user.cart_courses.remove(course)
    
    return redirect('accounts:mypage')


@login_required
def view_cart(request):
    cart_items = request.user.cart_courses.all()
    cart_total = sum(course.price for course in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': '{:,.0f}'.format(cart_total),
    }
    return render(request, 'accounts/mypage.html', context)


# @login_required
# def add_cart(request, course_id):
#     course = Course.objects.get(id=course_id)
#     quantity = int(request.GET.get('quantity', 1))
#     cart = request.session.get('cart', {})
    
#     if course_id in cart:
#         cart[course_id]['quantity'] += quantity
#     else:
#         cart[course_id] = {'quantity': quantity, 'price': str(course.price)}
        
#     # 장바구니 데이터 저장
#     if request.user.is_authenticated:
#         ShoppingCart.objects.update_or_create(
#             user=request.user,
#             course=course,
#             defaults={
#                 'quantity': cart[course_id]['quantity'],
#                 'price': course.price,
#             }
#         )
        
#     request.session['cart'] = cart
#     return redirect('accounts:mypage')


# @login_required
# def remove_cart(request, course_id):
#     cart = request.session.get('cart', {})
#     course_id = str(course_id)

#     if course_id in cart:
#         del cart[course_id]
#         request.session['cart'] = cart

#      # Delete the cart item from the database if the user is authenticated
#     if request.user.is_authenticated:
#         ShoppingCart.objects.filter(user=request.user, course_id=course_id).delete()

#     return redirect('accounts:mypage')


# @login_required
# def view_cart(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     cart_total = 0

#     for course_id, course_info in cart.items():
#         course = Course.objects.get(id=course_id)
#         total_price = Decimal(course_info.get('quantity', 0)) * course.price
#         cart_total += total_price
#         cart_items.append({
#             'course': course,
#             'quantity': course_info.get('quantity', 0),
#             'total_price': '{:.2f}'.format(total_price),
#         })

#     context = {
#         'cart_items': cart_items,
#         'cart_total': '{:,.0f}'.format(cart_total),
#     }
#     return render(request, 'accounts/mypage.html', context)

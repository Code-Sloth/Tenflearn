from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAutentication, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from courses.models import Review
from courses.models import Course
from decimal import Decimal


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
        form = CustomUserChangeForm(request.POST, instance=request.user)
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
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('courses:index')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)


def mypage(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    reviews = Review.objects.filter(user_id=person.id)
    courses = Course.objects.filter(enrolment_users=person.id)
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for course_id, course_info in cart.items():
        course = Course.objects.get(id=course_id)
        total_price = Decimal(course_info['quantity']) * course.price
        cart_total += total_price
        cart_items.append({
            'course': course,
            'quantity': course_info['quantity'],
            'total_price': total_price,
        })

    context = {
        'person': person,
        'reviews': reviews,
        'courses': courses,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'accounts/mypage.html', context)


def add_cart(request, course_id):
    course = Course.objects.get(id=course_id)
    quantity = int(request.GET.get('quantity', 1))
    cart = request.session.get('cart', {})

    if course_id in cart:
        cart[course_id]['quantity'] += quantity
    else:
        cart[course_id] = {'quantity': quantity, 'price': str(course.price)}

    request.session['cart'] = cart

    return redirect('accounts:mypage', username=request.user.username)


def remove_cart(request, course_id):
    cart = request.session.get('cart', {})
    course_id = str(course_id)

    if course_id in cart:
        del cart[course_id]
        request.session['cart'] = cart

    return redirect('accounts:mypage', username=request.user.username)


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for course_id, course_info in cart.items():
        course = Course.objects.get(id=course_id)
        total_price = Decimal(course_info['quantity']) * course.price
        cart_total += total_price
        cart_items.append({
            'course': course,
            'quantity': course_info['quantity'],
            'total_price': total_price,
        })

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'accounts/mypage.html', context)
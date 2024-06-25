from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Item, FavoriteItem, PriceHistory, CustomUser, Computer, Phone, PrivateLesson, Vehicle  # Import CustomUser model
from .forms import ItemForm, SignUpForm, UserLoginForm, UserUpdateForm, ComputerForm, PrivateLessonForm, VehicleForm, PhoneForm  # Import forms from the same directory
from .helpers import generate_verification_code
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.auth import login
from .forms import VerificationForm
from django.contrib.auth import get_user_model
from decimal import Decimal
from bson import Decimal128
from django.contrib.auth.decorators import user_passes_test


# Decorator to check if user is admin
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required
def all_users(request):
    users = CustomUser.objects.all()  # Assuming CustomUser is your user model
    return render(request, 'all_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # Delete associated items
    user_items = Item.objects.filter(owner_id=user.id)
    user_items.delete()
    user.delete()
    return redirect('all_users')

@admin_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return redirect('index')

@login_required
def add_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            category = item_form.cleaned_data['category']
            category_form = None
            if category == 'computers':
                category_form = ComputerForm(request.POST)
            elif category == 'phones':
                category_form = PhoneForm(request.POST)
            elif category == 'vehicles':
                category_form = VehicleForm(request.POST)
            elif category == 'private_lessons':
                category_form = PrivateLessonForm(request.POST)
            #print(category_form)

            if category_form:
                if category_form.is_valid():
                    item = item_form.save(commit=False)
                    item.owner_id = request.user.id
                    item.save()
                    category_instance = category_form.save(commit=False)
                    #category_instance.item_id = item.id
                    #setattr(category_instance, 'item', item)  # Assign the item to the category instance
                    category_instance.save()
                    return redirect('index')
    else:
        item_form = ItemForm()
    return render(request, 'marketplace/add_item.html', {'form': item_form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.is_active = False  # Mark user as inactive until verification is complete
            verification_code = generate_verification_code()
            user.verification_code = verification_code  # Save verification code to user model
            user.save()
            
            # Send verification email
            subject = 'Please verify your email address'
            html_message = render_to_string('verification_email.html', {'verification_code': verification_code})
            plain_message = strip_tags(html_message)
            from_email = 'e2380533@ceng.metu.edu.tr'  # Update with your email address
            to_email = user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            
            if user is not None:
                login(request, user)
                request.session['verification_code'] = verification_code
                request.session['user_id'] = user.id
                # Redirect user to a page where they can enter the verification code
                return redirect('verify_email')  # You need to create this view
            else:
                print("Authentication failed.")

    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            verification_code_input = form.cleaned_data['verification_code']
            verification_code = request.session.get('verification_code')
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)  # Get the current user
            if verification_code == verification_code_input:
                user.is_active = True
                #user.verification_code = ''  # Clear verification code
                user.save()
                login(request, user)  # Automatically log in the user
                messages.success(request, 'Your email has been verified. Welcome!')
                return redirect('login')  # Redirect to the homepage
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
    else:
        form = VerificationForm()
    return render(request, 'registration/verify_email.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def index(request):
    # Retrieve all items and then filter out the inactive ones in Python
    all_items = Item.objects.all()
    active_items = [item for item in all_items if item.active]
    active_items_sorted = sorted(active_items, key=lambda item: item.id, reverse=True)
    category = request.GET.get('category')  # Get the category from the URL query parameters    
    if category:
        active_items_sorted = [
            item for item in all_items
            if item.active and item.category == category
        ]
        active_items_sorted = sorted(active_items_sorted, key=lambda item: item.id, reverse=True)

    if request.user.is_authenticated:
        context = {'latest_items': active_items_sorted}
        return render(request, 'marketplace/index.html', context)
    else:
        context = {'latest_items': active_items_sorted}
        return render(request, 'marketplace/index_unauthenticated.html', context)

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.owner == request.user:
        if request.method == 'POST':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = ItemForm(instance=item)
        return render(request, 'marketplace/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.owner_id == request.user.id or request.user.is_superuser==True:
        if request.method == 'POST':
            item.delete()
            messages.success(request, 'Item deleted successfully')
            return redirect('index')
    else:
        messages.error(request, "You are not authorized to delete this item.")
    return redirect('index')

@login_required
def toggle_activation(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.owner == request.user:
        item.active = not item.active
        item.save()
    return redirect('index')

@login_required
def add_to_favorite(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    favorite_item, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)
    return render(request, 'marketplace/item_details.html', {'item': item})

@login_required
def remove_from_favorite(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    FavoriteItem.objects.filter(user=request.user, item=item).delete()
    return render(request, 'marketplace/item_details.html', {'item': item})

def item_details(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    is_favorite = False
    try:
        owner = CustomUser.objects.get(pk=item.owner_id)
        owner_username = owner.username
        owner_phone = owner.phone_number  # Assuming CustomUser model has a phone_number field
    except User.DoesNotExist:
        # Handle the case where the owner does not exist (optional)
        owner_username = None
        owner_phone = None
    if request.user.is_authenticated:
        user_favorites = request.user.favoriteitem_set.all()
        for favorite in user_favorites:
            if favorite.item_id == item_id:
                is_favorite = True
                break
        #is_favorite = FavoriteItem.objects.filter(user=request.user, item=item).exists()
    return render(request, 'marketplace/item_details.html', {'item': item, 'is_favorite': is_favorite, 'owner_username': owner_username, 'owner_phone': owner_phone})

def my_favorite_list(request):
    if request.user.is_authenticated:
        favorite_items = FavoriteItem.objects.filter(user=request.user)
        context = {'favorite_items': favorite_items}
        return render(request, 'marketplace/my_favorite_list.html', context)
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'marketplace/unauthenticated.html')

@login_required
def deactivate_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.active = False
    item.save()
    return redirect('item_details', item_id=item_id)

@login_required
def reactivate_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.active = True
    item.save()
    return redirect('item_details', item_id=item_id)

def send_price_decrease_email(item,old_price, new_price):
    # Query all users who have added the item to their favorites
    favorite_users = FavoriteItem.objects.filter(item=item).values_list('user__email', flat=True).distinct()
    print(favorite_users)
    if favorite_users:
        # Compose email content
        subject = f'Price Decrease Alert for {item.title}'
        context = {
        'item_title': item.title,
        'old_price': old_price,
        'new_price': new_price,
        'item_url' : "http://127.0.0.1:8000/item/"+str(item.id)+"/"
        }
        html_message = render_to_string('price_decrease_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'e2380533@ceng.metu.edu.tr'  # Update with your email address
        recipient_list = list(favorite_users)
        print("deneme5")
        # Send email to all users who have added the item to their favorites
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
           

@login_required
def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.owner_id == request.user.id:
        if request.method == 'POST':
            old_price = item.price
            if isinstance(old_price, Decimal128):
                old_price = item.price.to_decimal()
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                # Store the old price before saving the form
                form.save()
                new_price = item.price
                if isinstance(new_price, Decimal128):
                    new_price = item.price.to_decimal()
                #print(old_price , new_price)
                # Check if the price has decreased
                if new_price < old_price:
                    # If the price decreased, send email notifications
                    print("deneme2")
                    send_price_decrease_email(item, old_price, new_price)

                return redirect('item_details', item_id=item_id)
        else:
            form = ItemForm(instance=item)
        return render(request, 'marketplace/update_item.html', {'form': form, 'item': item})
    else:
        messages.error(request, "You are not authorized to update this item.")
        return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'marketplace/profile.html', {'form': form})


@staff_member_required
def delete_item_admin(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return redirect('index')

from django.contrib import admin
from django.urls import path
from marketplace.views import profile
from django.contrib.auth import views as auth_views  # Import Django's built-in login view
from marketplace import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # URL pattern for the homepage
    path('index_unauthenticated/', views.index, name='index_unauthenticated'),  # Add this line
    path('item/<int:item_id>/', views.item_details, name='item_details'),  # URL pattern for item details
    path('add/', views.add_item, name='add_item'),  # URL pattern for adding a new item
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),  # URL pattern for editing an existing item
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('toggle-activation/<int:item_id>/', views.toggle_activation, name='toggle_activation'),  # URL pattern for toggling item activation
    path('add-to-favorite/<int:item_id>/', views.add_to_favorite, name='add_to_favorite'),  # URL pattern for adding an item to favorites
    path('remove_favorite/<int:item_id>/', views.remove_from_favorite, name='remove_from_favorite'),
    path('sign-up/', views.sign_up, name='sign_up'),  # URL pattern for user registration (sign up)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('item/<int:item_id>/deactivate/', views.deactivate_item, name='deactivate_item'),
    path('item/<int:item_id>/reactivate/', views.reactivate_item, name='reactivate_item'),
    path('item/<int:item_id>/update/', views.update_item, name='update_item'),
    path('profile/', profile, name='profile'),
    path('my-favorite-list/', login_required(views.my_favorite_list), name='my_favorite_list'),
    path('verify-email/', views.verify_email, name='verify_email'),  # URL pattern for verifying email address
    path('all-users/', views.all_users, name='all_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

]

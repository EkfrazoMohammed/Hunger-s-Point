from django.urls import path,include,re_path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from HungerPointApp.views import *

app_name = 'HungerPointApp'


urlpatterns = [

    path('register', RegistrationApiVew.as_view()),
    path('login', LoginApiView.as_view()),

    path('custom-user', CustomUserView.as_view()),
    path('custom-user/<int:pk>', CustomUserView.as_view()),
    path('address-post', UserAddressView.as_view()),

    path('role', UserRoleView.as_view()),
    path('role/<int:pk>', UserRoleView.as_view()),

    path('social-media', SocialMediaView.as_view()),
    path('social-media/<int:pk>', SocialMediaView.as_view()),

    path('country', CountryView.as_view()),
    path('country/<int:pk>', CountryView.as_view()),

    path('address', AddressView.as_view()),
    path('address/<int:pk>', AddressView.as_view()),

    path('restaurent', RestaurentView.as_view()),
    path('restaurent/<int:pk>', RestaurentView.as_view()),

    path('menu-tags', MenuTagView.as_view()),
    path('menu-tags-item', MenuTagItemView.as_view()),

    path('web-menu-tags-item', WebMenuTagItemView.as_view()),

    path('restaurent-by-id/<int:id>/', RestaurentDetailAPIView.as_view(), name='restaurent-detail'),

    path('menu', MenuView.as_view()),
    path('menu/<int:pk>', MenuView.as_view()),

    path('tag', TagApiView.as_view()),
    path('tag/<int:pk>', TagApiView.as_view()),

    # later
    path('food-categories', FoodCategoriesView.as_view()),
    path('food-categories/<int:pk>', FoodCategoriesView.as_view()),
    # later

    # path('food-items', FoodItemsView.as_view()),
    # path('food-items/<int:pk>', FoodItemsView.as_view()),

    path('menu-items', MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemsView.as_view()),

    path('user-offers', OffersView.as_view()),
    path('user-offers/<int:pk>', OffersView.as_view()),

    path('offers-duration', OffersDurationView.as_view()),
    path('check-offers', CheckOffersView.as_view()),
    path('target-user', TargetUserView.as_view()),

    path('toppings', ToppingsView.as_view()),
    path('toppings/<int:pk>', ToppingsView.as_view()),

    path('toppings-items', ToppingsItemsView.as_view()),
    path('toppings-items/<int:pk>', ToppingsItemsView.as_view()),

    path('cart-items', CartItemsView.as_view()),
    path('cart-items/<int:pk>', CartItemsView.as_view()),
    path('delete-cart-items', DeleteCartItemsView.as_view()),

    path('delivery-driver', DeliveryDriverView.as_view()),
    path('delivery-driver/<int:pk>', DeliveryDriverView.as_view()),

    path('delivery-partner', DeliveryPartnersView.as_view()),
    path('delivery-partner/<int:pk>', DeliveryPartnersView.as_view()),

    path('orders', OrdersView.as_view()),
    path('orders/<int:pk>', OrdersView.as_view()),

    path('user-place-orders', UserPlaceOrdersView.as_view()),


    path('order-items', OrdersItemsView.as_view()),
    path('order-items/<int:pk>', OrdersItemsView.as_view()),

    path('likes', LikesView.as_view()),
    path('likes/<int:pk>', LikesView.as_view()),

    path('promo-code', PromoCodeView.as_view()),
    path('promo-code/<int:pk>', PromoCodeView.as_view()),

    path('user-action-tracking', UserActionTrackingView.as_view()),
    path('user-action-tracking/<int:pk>', UserActionTrackingView.as_view()),

    path('user-payment', UserPaymentView.as_view()),
    path('user-payment/<int:pk>', UserPaymentView.as_view()),

    path('order-tracking', OrderTrackingView.as_view()),
    path('order-tracking/<int:pk>', OrderTrackingView.as_view()),

    path('default-tax', DefaultTaxRateApiView.as_view()),
    path('default-tax/<int:pk>', DefaultTaxRateApiView.as_view()),

    path('admin-profile', AdminProfile.as_view()),
    path('admin-profile/<int:pk>', AdminProfile.as_view()),

    path('user-items-reaction', UserItemReact.as_view()),

    path('submit-form', SubmitForm.as_view()),
]
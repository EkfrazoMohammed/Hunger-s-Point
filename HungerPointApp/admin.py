from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
model_list = [
            
            
            Menu,
            Toppings,
            ToppingsItems,
            CartItems,
            DeliveryDriver,
            DeliveryPartners,
            
            OrdersItems,
            Likes,
            PromoCode,
            UserActionTracking,
            UserPayment,
            OrderTracking,
           

]   
admin.site.register(model_list)   
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id",
                "super_user_id",
"address_id",
"user_name",
"email_id",
"password",
"phone_number",
"facebook_id",)

@admin.register(Restaurent)
class RestaurentAdmin(admin.ModelAdmin):
    list_display = ("id","address_id",
"restaurent_name",
"dp_list",
"leave_list",
"every_day_time_list",
"mobile_number",
"branch",
"description",
"logo_path",
                )

@admin.register(FoodItems)
class FoodItemsAdmin(admin.ModelAdmin):
    list_display = ("id","menu_id",
"name",
"tag_list",
"description",
"price",
"image_path",
"default_tax_rate",
"display_photo_path",
"poppable",
"available_for_online_order",
"taxable",
                )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id","country_id",
                        "f_name",
                        "l_name",
                        "address_tag",
                        "mobile_number",
                        "flat",
                        "area",
                        "postal_code",
                        "city",
                        "google_map_link",
                        "pickup_enabled",
                        "delivery_enabled",
                        "publishing_name",
                        "email_id",
                        "location_name",
                        "google_place_id",)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id",
                "country_name")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id",
                "name",
"abbreivation",
"add_img_path",)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id",
                "customer_user_id",
"delivery_partner_id",
"restaurent_id",
"delivery_driver_id",
"order_dt",
"total_amount",
"order_status",
"payment_method",
"transaction_id",
"devlivery_method",
"delivery_fee",
"requested_delivery_time",
"driver_rating",
"restaurent_rating",)


            
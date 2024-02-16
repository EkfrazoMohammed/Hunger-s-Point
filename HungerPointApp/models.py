from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from .models import *




class Country(models.Model):
    country_name = models.CharField(max_length=250, blank=True, null=True)
    c_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    c_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    f_name= models.CharField(max_length=250, blank=True, null=True)
    l_name= models.CharField(max_length=250, blank=True, null=True)
    address_tag= models.CharField(max_length=250, blank=True, null=True)
    mobile_number= models.CharField(max_length=250, blank=True, null=True)
    flat= models.CharField(max_length=250, blank=True, null=True)
    area= models.CharField(max_length=250, blank=True, null=True)
    postal_code= models.CharField(max_length=250, blank=True, null=True)
    city= models.CharField(max_length=250, blank=True, null=True)
    google_map_link= models.CharField(max_length=250, blank=True, null=True)
    a_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    a_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)
    pickup_enabled = models.BooleanField(default=False)
    delivery_enabled= models.BooleanField(default=False)
    publishing_name= models.CharField(max_length=250, blank=True, null=True)
    email_id= models.CharField(max_length=250, blank=True, null=True)
    location_name= models.CharField(max_length=250, blank=True, null=True)
    google_place_id= models.CharField(max_length=250, blank=True, null=True)

class UserRole(models.Model):
    role_name = models.CharField(max_length=250, blank=True, null=True)
    c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class CustomUser(models.Model):
    super_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, blank=True, null=True)
    user_name= models.CharField(max_length=250, blank=True, null=True)
    f_name= models.CharField(max_length=250, blank=True, null=True)
    l_name= models.CharField(max_length=250, blank=True, null=True)
    email_id= models.CharField(max_length=250, blank=True, null=True)
    password= models.CharField(max_length=250, blank=True, null=True)
    phone_number= models.CharField(max_length=250, blank=True, null=True)
    facebook_id= models.CharField(max_length=250, blank=True, null=True)
    permission_list = models.JSONField(blank=True, null=True)
    customer_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    customer_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)



class Restaurent(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    restaurent_name = models.CharField(max_length=250, blank=True, null=True)
    dp_list= models.CharField(max_length=250, blank=True, null=True)
    leave_list= models.CharField(max_length=250, blank=True, null=True)
    every_day_time_list= models.CharField(max_length=5000, blank=True, null=True)
    mobile_number= models.CharField(max_length=250, blank=True, null=True)
    branch= models.CharField(max_length=250, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    logo_path = models.CharField(max_length=250, blank=True, null=True)
    r_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    r_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

class SocialMedia(models.Model):
    restaurent = models.ForeignKey(Restaurent, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    url= models.CharField(max_length=250, blank=True, null=True)

class FoodCategories(models.Model):
    restaurent = models.ForeignKey(Restaurent, on_delete=models.CASCADE, blank=True, null=True)
    category_name= models.CharField(max_length=250, blank=True, null=True)
    mobile_number= models.CharField(max_length=250, blank=True, null=True)
    menu_list  = models.JSONField(blank=True, null=True)
    fc_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    fc_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

class Menu(models.Model):
    menu_title= models.CharField(max_length=250, blank=True, null=True)
    menu_display_title= models.CharField(max_length=250, blank=True, null=True)
    disclaimer= models.CharField(max_length=250, blank=True, null=True)
    image_path = models.CharField(max_length=250, blank=True, null=True)


   


class FoodItems(models.Model):
    food_category = models.ForeignKey(FoodCategories, on_delete=models.CASCADE, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)
    name= models.CharField(max_length=250, blank=True, null=True)
    tag_list= models.CharField(max_length=250, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    price= models.CharField(max_length=250, blank=True, null=True)
    image_path = models.CharField(max_length=250, blank=True, null=True)
    default_tax_rate= models.CharField(max_length=250, blank=True, null=True)
    display_photo_path = models.BooleanField(default=False)
    poppable= models.BooleanField(default=False)
    available_for_online_order= models.BooleanField(default=False)
    taxable= models.BooleanField(default=False)
    f_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    f_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

class Toppings(models.Model):
    name= models.CharField(max_length=250, blank=True, null=True)
    price= models.CharField(max_length=250, blank=True,null=True)
    t_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    t_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

class ToppingsItems(models.Model):
    food_items = models.ForeignKey(FoodItems, on_delete=models.CASCADE, blank=True, null=True)
    toppings_id_list= models.JSONField(blank=True, null=True)
    ti_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    ti_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class CartItems(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    food_items = models.ForeignKey(FoodItems, on_delete=models.CASCADE, blank=True, null=True)
    quantity=models.CharField(max_length=250, blank=True,null=True)
    c_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    c_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class DeliveryDriver(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=250, blank=True, null=True)
    dd_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    dd_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class DeliveryPartners(models.Model):
    dp_name = models.CharField(max_length=250, blank=True, null=True)
    dp_img_path= models.CharField(max_length=250, blank=True, null=True)
    dp_ph_number= models.CharField(max_length=250, blank=True, null=True)
    dp_charges= models.CharField(max_length=250, blank=True, null=True)
    dp_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    dp_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class Orders(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    delivery_partner = models.ForeignKey(DeliveryPartners, on_delete=models.CASCADE, blank=True, null=True)
    restaurent = models.ForeignKey(Restaurent, on_delete=models.CASCADE, blank=True, null=True)
    delivery_driver = models.ForeignKey(DeliveryDriver, on_delete=models.CASCADE, blank=True, null=True)
    order_dt= models.CharField(max_length=250, blank=True, null=True)
    # order_time= models.CharField(max_length=250, blank=True, null=True)
    total_amount= models.CharField(max_length=250, blank=True, null=True)
    order_status= models.CharField(max_length=250, blank=True, null=True)
    payment_method= models.CharField(max_length=250, blank=True, null=True)
    transaction_id= models.CharField(max_length=250, blank=True, null=True)
    devlivery_method= models.CharField(max_length=250, blank=True, null=True)
    delivery_fee= models.CharField(max_length=250, blank=True, null=True)
    requested_delivery_time= models.CharField(max_length=250, blank=True, null=True)
    driver_rating= models.CharField(max_length=250, blank=True, null=True)
    restaurent_rating= models.CharField(max_length=250, blank=True, null=True)
    o_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    o_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class OrdersItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, blank=True, null=True)
    food_items = models.ForeignKey(FoodItems, on_delete=models.CASCADE, blank=True, null=True)
    toppings_id_list =models.JSONField(blank=True, null=True)
    complete_order_item = models.JSONField(blank=True, null=True)
    quantity = models.CharField(max_length=250, blank=True, null=True)
    ot_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    ot_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class Likes(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    food_items = models.ForeignKey(FoodItems, on_delete=models.CASCADE, blank=True, null=True)
    l_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    l_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

class PromoCode(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    code= models.CharField(max_length=250, blank=True, null=True)
    discount_amount= models.CharField(max_length=250, blank=True, null=True)
    valid_from= models.CharField(max_length=250, blank=True, null=True)
    valid_to= models.CharField(max_length=250, blank=True, null=True)
    pc_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    pc_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

    
class UserActionTracking(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    action_type= models.CharField(max_length=250, blank=True, null=True)
    action_time_stamp= models.CharField(max_length=250, blank=True, null=True)
    uat_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    uat_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)



class UserPayment(models.Model):
    customer_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, blank=True, null=True)
    amount= models.CharField(max_length=250, blank=True, null=True)
    payment_date= models.CharField(max_length=250, blank=True, null=True)
    payment_status= models.CharField(max_length=250, blank=True, null=True)
    transaction_id= models.CharField(max_length=250, blank=True, null=True)
    payment_gateway_response= models.CharField(max_length=250, blank=True, null=True)
    up_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    up_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)


class OrderTracking(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, blank=True, null=True)
    status= models.CharField(max_length=250, blank=True, null=True)
    time_stamp= models.CharField(max_length=250, blank=True, null=True)
    ot_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    ot_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)

class Tag(models.Model):
    name= models.CharField(max_length=250, blank=True, null=True)
    abbreivation= models.CharField(max_length=250, blank=True, null=True)
    add_img_path= models.CharField(max_length=250, blank=True, null=True)
    tag_c_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    tag_u_timestamp  = models.DateTimeField(auto_now=True,verbose_name="Update_TimeStamp",blank=True,null=True)



    

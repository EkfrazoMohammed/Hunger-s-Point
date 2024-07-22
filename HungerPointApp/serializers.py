from rest_framework import serializers
from HungerPointApp.models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    # address = AddressSerializer()  # Include AddressSerializer here

    class Meta:
        model = Restaurent
        fields = '__all__'






# class MenuSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Menu
#         fields = '__all__'

class FoodCategorySerializer(serializers.ModelSerializer):
    restaurent = RestaurantSerializer(read_only=True)  # Include MenuSerializer here

    class Meta:
        model = FoodCategories
        fields = '__all__'
    

class FoodItemsSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True)  # Include MenuSerializer here
    # food_category = FoodCategorySerializer(read_only=True)
    class Meta:
        model = FoodItems
        fields = '__all__'
    
# class RestaurentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Restaurent
#         fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['profile_img',
'user_name',
'f_name',
'l_name',
'email_id',
'password',
'phone_number',]  # Add other fields as needed

    def get_profile_img(self, obj):
        # Prepend the URL to profile_img field value
        if obj.profile_img:
            return 'https://hunger.thestorywallcafe.com' + obj.profile_img.url
        else:
            return None





class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class MenuItemsSerializer(serializers.ModelSerializer):
    select_item_tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItems
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    menuitems_set = MenuItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'

class RestaurentSerializer(serializers.ModelSerializer):
    menu_set = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurent
        fields = '__all__'



class CartItemsSerializer(serializers.ModelSerializer):
    customer_user = CustomUserSerializer()
    menu_items = MenuItemsSerializer()
    
    class Meta:
        model = CartItems
        fields = '__all__'
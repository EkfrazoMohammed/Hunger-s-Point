from django.conf import settings
from django.db.models import base
from django.db.utils import IntegrityError
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
# from requests import api
from rest_framework.response import Response
from requests.api import head, request
import http
from django.utils.decorators import method_decorator

import requests
import random

import inspect
from django.core.mail import message, send_mail, EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponsePermanentRedirect

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from .models import *
import jwt
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework import generics, viewsets, status
from django.contrib import auth
# from .serializers import *
from rest_framework import viewsets, status

from rest_framework.authtoken.views import ObtainAuthToken
import time
import datetime
from django.db.models import Sum
import re


from django.views.decorators.csrf import csrf_exempt

# import urllib.request as urllib2
from urllib.request import urlopen

import urllib.request
import urllib.error
import json


# from accounts.backends import *
from HungerPointApp.backends import *
import urllib.parse
import http.client





class CountryView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Country.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Country.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)

        data = request.data
        country_name=data.get('country_name')
       
        try:
            country = Country.objects.create(
                country_name=country_name)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data

        country_name=data.get('country_name')

        try:
            country= Country.objects.filter(id=pk).update(country_name=country_name)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = Country.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class AddressView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Address.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Address.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)

        data = request.data
        country=data.get('country_id')
        f_name=data.get('f_name')
        l_name=data.get('l_name')
        address_tag=data.get('address_tag')
        mobile_number=data.get('mobile_number')
        flat=data.get('flat')
        area=data.get('area')
        postal_code=data.get('postal_code')
        google_map_link=data.get('google_map_link')
        city=data.get('city')
       
        try:
            country = Address.objects.create(
                    country_id  = country,
                    f_name = f_name,
                    l_name = l_name,
                    address_tag = address_tag,
                    mobile_number = mobile_number,
                    flat = flat,
                    area = area,
                    postal_code = postal_code,
                    google_map_link = google_map_link,
                    city = city
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        country=data.get('country_id')
        f_name=data.get('f_name')
        l_name=data.get('l_name')
        address_tag=data.get('address_tag')
        mobile_number=data.get('mobile_number')
        flat=data.get('flat')
        area=data.get('area')
        postal_code=data.get('postal_code')
        google_map_link=data.get('google_map_link')
        city=data.get('city')

        try:
            country= Address.objects.filter(id=pk).update(country_id  = country,
                    f_name = f_name,
                    l_name = l_name,
                    address_tag = address_tag,
                    mobile_number = mobile_number,
                    flat = flat,
                    area = area,
                    postal_code = postal_code,
                    google_map_link = google_map_link,
                    city = city)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = Address.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class RestaurentView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Restaurent.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Restaurent.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        address=data.get('address_id')
        restaurent_name=data.get('restaurent_name')
        dp_list=data.get('dp_list')
        leave_list=data.get('leave_list')
        every_day_time_list=data.get('every_day_time_list')
        mobile_number=data.get('mobile_number')
        branch=data.get('branch')
        description=data.get('description')
        logo_path=data.get('logo_path')
       
       
        try:
            country = Restaurent.objects.create(
                    address_id = address,
                    restaurent_name = restaurent_name,
                    dp_list = dp_list,
                    leave_list = leave_list,
                    every_day_time_list = every_day_time_list,
                    mobile_number = mobile_number,
                    branch = branch,
                    description = description,
                    logo_path = logo_path,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        address=data.get('address_id')
        restaurent_name=data.get('restaurent_name')
        dp_list=data.get('dp_list')
        leave_list=data.get('leave_list')
        every_day_time_list=data.get('every_day_time_list')
        mobile_number=data.get('mobile_number')
        branch=data.get('branch')
        description=data.get('description')
        logo_path=data.get('logo_path')
        try:
            country= Restaurent.objects.filter(id=pk).update(address_id = address,
                    restaurent_name = restaurent_name,
                    dp_list = dp_list,
                    leave_list = leave_list,
                    every_day_time_list = every_day_time_list,
                    mobile_number = mobile_number,
                    branch = branch,
                    description = description,
                    logo_path = logo_path,)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = Restaurent.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})




class FoodCategoriesView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = FoodCategories.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = FoodCategories.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        restaurent=data.get('restaurent_id')
        category_name=data.get('category_name')
        mobile_number=data.get('mobile_number')
       
       
       
        try:
            country = FoodCategories.objects.create(
                   restaurent_id=restaurent,
                    category_name=category_name,
                    mobile_number=mobile_number,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        restaurent=data.get('restaurent_id')
        category_name=data.get('category_name')
        mobile_number=data.get('mobile_number')
        try:
            country= FoodCategories.objects.filter(id=pk).update(restaurent_id=restaurent,
                    category_name=category_name,
                    mobile_number=mobile_number,)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = FoodCategories.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class FoodItemsView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = FoodItems.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = FoodItems.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        food_category=data.get('food_category_id')
        name=data.get('name')
        tag_list=data.get('tag_list')
        description=data.get('description')
        price=data.get('price')
        image_path=data.get('image_path')
       
       
       
        try:
            country = FoodItems.objects.create(
                    food_category_id=food_category,
                    name=name,
                    tag_list=tag_list,
                    description=description,
                    price=price,
                    image_path=image_path,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        food_category=data.get('food_category_id')
        name=data.get('name')
        tag_list=data.get('tag_list')
        description=data.get('description')
        price=data.get('price')
        image_path=data.get('image_path')
        try:
            country= FoodItems.objects.filter(id=pk).update(food_category_id=food_category,
                    name=name,
                    tag_list=tag_list,
                    description=description,
                    price=price,
                    image_path=image_path,
                    logo_path = logo_path,)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = FoodItems.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class ToppingsView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Toppings.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Toppings.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        name=data.get('name')
        price=data.get('price')
       
       
        try:
            country = Toppings.objects.create(
                    price=price,
                    name=name,
                   
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        name=data.get('name')
        price=data.get('price')

        try:
            country= Toppings.objects.filter(id=pk).update(price=price,
                    name=name,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = Toppings.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})


class ToppingsItemsView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = ToppingsItems.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = ToppingsItems.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        name=data.get('name')
        price=data.get('price')
       
        try:
            country = ToppingsItems.objects.create(
                    price=price,
                    name=name,     
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        name=data.get('name')
        price=data.get('price')

        try:
            country= ToppingsItems.objects.filter(id=pk).update(price=price,
                    name=name,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = ToppingsItems.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})





class CartItemsView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = CartItems.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = CartItems.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user=data.get('customer_user_id')
        food_items=data.get('food_items_id')
        quantity=data.get('quantity')

        try:
            country = CartItems.objects.create(
                    customer_user_id=customer_user,
                    food_items_id=food_items,
                    quantity   =quantity,  
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data.get('customer_user_id')
        food_items=data.get('food_items_id')
        quantity=data.get('quantity')

        try:
            country= CartItems.objects.filter(id=pk).update(customer_user_id=customer_user,
                    food_items_id=food_items,
                    quantity   =quantity,  
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = CartItems.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})





class DeliveryDriverView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = DeliveryDriver.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = DeliveryDriver.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        name=data.get('name')
        phone_number=data.get('phone_number')
        

        try:
            country = CarDeliveryDrivertItems.objects.create(
                    name=name,
                    phone_number=phone_number,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        name=data.get('name')
        phone_number=data.get('phone_number')

        try:
            country= DeliveryDriver.objects.filter(id=pk).update(name=name,
                    phone_number=phone_number,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = DeliveryDriver.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})




class DeliveryPartnersView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = DeliveryPartners.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = DeliveryDriver.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        dp_name=data.get('dp_name')
        dp_img_path=data.get('dp_img_path')
        dp_ph_number=data.get('dp_ph_number')
        dp_charges=data.get('dp_charges')

    

        try:
            country = DeliveryPartners.objects.create(
                  dp_name=dp_name,
                dp_img_path=dp_img_path,
                dp_ph_number=dp_ph_number,
                dp_charges=dp_charges,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        dp_name=data.get('dp_name')
        dp_img_path=data.get('dp_img_path')
        dp_ph_number=data.get('dp_ph_number')
        dp_charges=data.get('dp_charges')

        try:
            country= DeliveryPartners.objects.filter(id=pk).update(dp_name=dp_name,
                dp_img_path=dp_img_path,
                dp_ph_number=dp_ph_number,
                dp_charges=dp_charges,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = DeliveryPartners.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})




class OrdersView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Orders.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Orders.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user=data.get('customer_user_id')
        delivery_partner=data.get('delivery_partner_id')
        restaurent=data.get('restaurent_id')
        delivery_driver=data.get('delivery_driver_id')
        order_date=data.get('order_date')
        order_time=data.get('order_time')
        total_amount=data.get('total_amount')
        order_status=data.get('order_status')
        payment_method=data.get('payment_method')
        transaction_id=data.get('transaction_id')
        devlivery_method=data.get('devlivery_method')
        delivery_fee=data.get('delivery_fee')
        requested_delivery_time=data.get('requested_delivery_time')
        driver_rating=data.get('driver_rating')
        restaurent_rating=data.get('restaurent_rating')


        try:
            country = Orders.objects.create(
                customer_user_id=customer_user,
                delivery_partner_id=delivery_partner,
                restaurent_id=restaurent,
                delivery_driver_id=delivery_driver,
                order_date=order_date,
                order_time=order_time,
                total_amount=total_amount,
                order_status=order_status,
                payment_method=payment_method,
                transaction_id=transaction_id,
                devlivery_method=devlivery_method,
                delivery_fee=delivery_fee,
                requested_delivery_time=requested_delivery_time,
                driver_rating=driver_rating,
                restaurent_rating=restaurent_rating,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data.get('customer_user_id')
        delivery_partner=data.get('delivery_partner_id')
        restaurent=data.get('restaurent_id')
        delivery_driver=data.get('delivery_driver_id')
        order_date=data.get('order_date')
        order_time=data.get('order_time')
        total_amount=data.get('total_amount')
        order_status=data.get('order_status')
        payment_method=data.get('payment_method')
        transaction_id=data.get('transaction_id')
        devlivery_method=data.get('devlivery_method')
        delivery_fee=data.get('delivery_fee')
        requested_delivery_time=data.get('requested_delivery_time')
        driver_rating=data.get('driver_rating')
        restaurent_rating=data.get('restaurent_rating')
        try:
            country= Orders.objects.filter(id=pk).update(customer_user_id=customer_user,
                delivery_partner_id=delivery_partner,
                restaurent_id=restaurent,
                delivery_driver_id=delivery_driver,
                order_date=order_date,
                order_time=order_time,
                total_amount=total_amount,
                order_status=order_status,
                payment_method=payment_method,
                transaction_id=transaction_id,
                devlivery_method=devlivery_method,
                delivery_fee=delivery_fee,
                requested_delivery_time=requested_delivery_time,
                driver_rating=driver_rating,
                restaurent_rating=restaurent_rating,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = Orders.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})




class OrdersItemsView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = OrdersItems.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = OrdersItems.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        order=data.get('order_id')
        food_items=data.get('food_items_id')
        toppings_id_list=data.get('toppings_id_list')
        complete_order_item=data.get('complete_order_item')
        quantity=data.get('quantity')



        try:
            country = OrdersItems.objects.create(
                order_id=order,
                food_items_id=food_items,
                toppings_id_list=toppings_id_list,
                complete_order_item=complete_order_item,
                quantity=quantity,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        order=data.get('order_id')
        food_items=data.get('food_items_id')
        toppings_id_list=data.get('toppings_id_list')
        complete_order_item=data.get('complete_order_item')
        quantity=data.get('quantity')
        try:
            country= OrdersItems.objects.filter(id=pk).update(order_id=order,
                food_items_id=food_items,
                toppings_id_list=toppings_id_list,
                complete_order_item=complete_order_item,
                quantity=quantity,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = OrdersItems.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})




class LikesView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Likes.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = OrdersItems.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user=data.get('customer_user_id')
        food_items=data.get('food_items_id')
        


        try:
            country = Likes.objects.create(
                customer_user_id=customer_user,
                food_items_id=food_items,
                
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data.get('customer_user_id')
        food_items=data.get('food_items_id')
        try:
            country= Likes.objects.filter(id=pk).update(ocustomer_user_id=customer_user,
                food_items_id=food_items,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = Likes.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class PromoCodeView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = PromoCode.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = PromoCode.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user=data.get('customer_user_id')
        code=data.get('code')
        discount_amount=data.get('discount_amount')
        valid_from=data.get('valid_from')
        valid_to=data.get('valid_to')



        try:
            country = PromoCode.objects.create(
                customer_user_id=customer_user,
                code=code,
                discount_amount=discount_amount,
                valid_from=valid_from,
                valid_to=valid_to,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data.get('customer_user_id')
        code=data.get('code')
        discount_amount=data.get('discount_amount')
        valid_from=data.get('valid_from')
        valid_to=data.get('valid_to')
        try:
            country= PromoCode.objects.filter(id=pk).update(customer_user_id=customer_user,
                code=code,
                discount_amount=discount_amount,
                valid_from=valid_from,
                valid_to=valid_to,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = PromoCode.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class UserActionTrackingView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = UserActionTracking.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = UserActionTracking.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user=data.get('customer_user_id')
        action_type=data.get('action_type')
        action_time_stamp=data.get('action_time_stamp')
        



        try:
            country = UserActionTracking.objects.create(
                customer_user_id=customer_user,
                action_type=action_type,
                action_time_stamp=action_time_stamp,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data.get('customer_user_id')
        action_type=data.get('action_type')
        action_time_stamp=data.get('action_time_stamp')
        try:
            country= UserActionTracking.objects.filter(id=pk).update(customer_user_id=customer_user,
                action_type=action_type,
                action_time_stamp=action_time_stamp,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = UserActionTracking.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class UserPaymentView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = UserPayment.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Orders.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user=data.get('customer_user_id')
        order=data.get('order_id')
        amount=data.get('restaurent_id')
        payment_date=data.get('payment_date')
        payment_status=data.get('payment_status')
        transaction_id=data.get('transaction_id')
        payment_gateway_response=data.get('payment_gateway_response')
       

        try:
            country = UserPayment.objects.create(
                customer_user_id=customer_user,
                order_id=order,
                restaurent_id=restaurent,
                payment_date=payment_date,
                payment_status=payment_status,
                transaction_id=transaction_id,
                payment_gateway_response=payment_gateway_response,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data.get('customer_user_id')
        order=data.get('order_id')
        amount=data.get('restaurent_id')
        payment_date=data.get('payment_date')
        payment_status=data.get('payment_status')
        transaction_id=data.get('transaction_id')
        payment_gateway_response=data.get('payment_gateway_response')
        try:
            country= UserPayment.objects.filter(id=pk).update(customer_user_id=customer_user,
                order_id=order,
                restaurent_id=restaurent,
                payment_date=payment_date,
                payment_status=payment_status,
                transaction_id=transaction_id,
                payment_gateway_response=payment_gateway_response,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = UserPayment.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})



class OrderTrackingView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = OrderTracking.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Orders.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        order=data.get('order_id')
        status=data.get('status')
        time_stamp=data.get('time_stamp')
        
       

        try:
            country = OrderTracking.objects.create(
                
                order_id=order,
              
                status=status,
                time_stamp=time_stamp,
                    )
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        order=data.get('order_id')
        status=data.get('status')
        time_stamp=data.get('time_stamp')
        try:
            country= OrderTracking.objects.filter(id=pk).update(order_id=order,
              
                status=status,
                time_stamp=time_stamp,
                   )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request,pk):
        test = (0,{})
        all_values = OrderTracking.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})






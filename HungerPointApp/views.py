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

from django.db.models import Sum
import re


from django.views.decorators.csrf import csrf_exempt

# import urllib.request as urllib2
from urllib.request import urlopen

import urllib.request
import urllib.error
import json
import time
import datetime


# from accounts.backends import *
from HungerPointApp.backends import *
import urllib.parse
import http.client


class RegistrationApiVew(APIView):
    def post(self,request):
        data = request.data
        response = {}
        email   = data['email']
        if 'password' in data:
            # Admin register
            password = data['password']
            f_name = data['f_name']
            l_name = data['l_name']
            role_name = data['role_name']
            permission_list = data['permission_list']

            if User.objects.filter(Q(email=email)).exists():
                return Response({'error':'User Already Exists'})
            else:
                role_data = UserRole.objects.get(role_name=role_name)
                create_super_user = User.objects.create_user(username=email,email=email,password=password)
                user_create = CustomUser.objects.create(email_id=email,password=password,f_name=f_name,l_name=l_name,role_id=role_data.id)
            
                auth_token = jwt.encode(
                            {'email': create_super_user.email,'role_name':role_name,'user_id':user_create.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'result': {'data': str(role_name) + ' Register successful',
                    'email_id':email,
                    'role_name':role_name,
                    'user_id':user_create.id,
                    'token':authorization,
                    }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK

                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)
        else:
            # User register
            role_data = UserRole.objects.get(role_name='USER')
            create_super_user = User.objects.create_user(username=email,email=email)
            user_create = CustomUser.objects.create(email_id=email,f_name=email,l_name=email,role_id=role_data.id)
        
            auth_token = jwt.encode(
                        {'email': create_super_user.email,'role_name':role_data.role_name,'user_id':user_create.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
            authorization = 'Bearer'+' '+auth_token
            response_result = {}
            response_result['result'] = {
                'result': {'data': 'USER Register successful',
                'email_id':email,
                'role_name':role_data.role_name,
                'user_id':user_create.id,
                'token':authorization,
                }}
            response['Authorization'] = authorization
            response['status'] = status.HTTP_200_OK

            return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)

        
class LoginApiView(APIView):
    
    def post(self, request):
        response = {}
        data = request.data
        email   = data['email']
        if 'password' in data:
            # Admin register
            password = data['password']
            user_check = User.objects.filter(email= email)
            if user_check:
                user = auth.authenticate(username=email, password=password)
                if user:
                    custom_user = CustomUser.objects.get(email_id=email)
                    role_data = UserRole.objects.get(id=custom_user.role_id)
                    auth_token = jwt.encode(
                        {'email_id': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                    
                    # serializer = CustomUserTableSerializers(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    response_result['result'] = {
                        'detail': str(role_data.role_name) + ' Login successfull',
                        'email_id':email,
                        'role_name':role_data.role_name,
                        'user_id':custom_user.id,
                        'token':authorization,
                        }
                    response['Authorization'] = authorization
                    response['status'] = status.HTTP_200_OK
                else:
                    header_response = {}
                    response['error'] = {'error': {
                        'detail': 'invalid emailid/password', 'status': status.HTTP_401_UNAUTHORIZED}}
                    return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)
                return Response(response_result, headers=response,status= status.HTTP_200_OK)
            else:
                response['error'] = {'error': {
                        'detail': 'User not exists', 'status': status.HTTP_401_UNAUTHORIZED}}
                return Response(response['error'], status= status.HTTP_401_UNAUTHORIZED)

        else:
            user_check = User.objects.filter(email= email)
            if user_check:
                custom_user = CustomUser.objects.get(email_id=email)
                role_data = UserRole.objects.get(id=custom_user.role_id)
                auth_token = jwt.encode(
                    {'email_id': custom_user.f_name, 'email': custom_user.email_id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                
                # serializer = CustomUserTableSerializers(user)
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'detail': str(role_data.role_name) + ' Login successfull',
                    'email_id':email,
                    'role_name':role_data.role_name,
                    'user_id':custom_user.id,
                    'token':authorization,
                    }
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK
            
                return Response(response_result, headers=response,status= status.HTTP_200_OK)
            else:
                response['error'] = {'error': {
                        'detail': 'User not exists', 'status': status.HTTP_401_UNAUTHORIZED}}
                return Response(response['error'], status= status.HTTP_401_UNAUTHORIZED)

            

class CustomUserView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = CustomUser.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = CustomUser.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)

        data = request.data
        address=data['address_id']
        role=data['role_id']
        user_name=data['user_name']
        email_id=data['email_id']
        password=data['password']
        phone_number=data['phone_number']
       
        try:
            
            c_user = CustomUser.objects.create(
                address_id=address,
                role_id=role,
                user_name=user_name,
                email_id=email_id,
                password=password,
                phone_number=phone_number,)
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        address=data['address_id']
        role=data['role_id']
        user_name=data['user_name']
        email_id=data['email_id']
        password=data['password']
        phone_number=data['phone_number']

        try:
            c_user= CustomUser.objects.filter(id=pk).update(address_id=address,
                role_id=role,
                user_name=user_name,
                email_id=email_id,
                password=password,
                phone_number=phone_number,)

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
        all_values = CustomUser.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})


class UserRoleView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = UserRole.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = UserRole.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)

        data = request.data
        role_name=data['role_name']
       
        try:
            
            role_name = UserRole.objects.create(
                role_name=role_name)
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data

        role_name=data['role_name']

        try:
            role_name= UserRole.objects.filter(id=pk).update(role_name=role_name)

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
        all_values = UserRole.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})


class SocialMediaView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = SocialMedia.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = SocialMedia.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)

        data = request.data
        restaurent=data['restaurent_id']
        name=data['name']
        url=data['url']
       
        try:
            
            social = SocialMedia.objects.create(
                restaurent_id=restaurent,
                    name=name,
                    url=url,)
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        restaurent=data['restaurent_id']
        name=data['name']
        url=data['url']

        try:
            social= SocialMedia.objects.filter(id=pk).update(restaurent_id=restaurent,
                    name=name,
                    url=url,)

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
        all_values = SocialMedia.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})




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
        country_name=data['country_name']
       
        try:
            if Country.objects.filter(country_name=country_name).exists():
                return Response({'result':{'status':'Country Name already exists'}})
            else:
                country = Country.objects.create(
                    country_name=country_name)
                return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data

        country_name=data['country_name']

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
        country=data['country_id']
        f_name=data['f_name']
        l_name=data['l_name']
        address_tag=data['address_tag']
        mobile_number=data['mobile_number']
        flat=data['flat']
        area=data['area']
        postal_code=data['postal_code']
        google_map_link=data['google_map_link']
        city=data['city']

        pickup_enabled =data['pickup_enabled']
        delivery_enabled=data['delivery_enabled']
        publishing_name=data['publishing_name']
        email_id=data['email_id']
        location_name=data['location_name']
        google_place_id=data['google_place_id']
       
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
                    city = city,
                    pickup_enabled=pickup_enabled,
                    delivery_enabled=delivery_enabled,
                    publishing_name=publishing_name,
                    email_id=email_id,
                    location_name=location_name,
                    google_place_id=google_place_id,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        country=data['country_id']
        f_name=data['f_name']
        l_name=data['l_name']
        address_tag=data['address_tag']
        mobile_number=data['mobile_number']
        flat=data['flat']
        area=data['area']
        postal_code=data['postal_code']
        google_map_link=data['google_map_link']
        city=data['city']

        pickup_enabled =data['pickup_enabled']
        delivery_enabled=data['delivery_enabled']
        publishing_name=data['publishing_name']
        email_id=data['email_id']
        location_name=data['location_name']
        google_place_id=data['google_place_id']

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
                    city = city,
                    pickup_enabled=pickup_enabled,
                    delivery_enabled=delivery_enabled,
                    publishing_name=publishing_name,
                    email_id=email_id,
                    location_name=location_name,
                    google_place_id=google_place_id,
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
        address=data['address_id']
        restaurent_name=data['restaurent_name']
        dp_list=data['dp_list']
        leave_list=data['leave_list']
        every_day_time_list=data['every_day_time_list']
        mobile_number=data['mobile_number']
        branch=data['branch']
        description=data['description']
        logo_path=data['logo_path']
       
       
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
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        address=data['address_id']
        restaurent_name=data['restaurent_name']
        dp_list=data['dp_list']
        leave_list=data['leave_list']
        every_day_time_list=data['every_day_time_list']
        mobile_number=data['mobile_number']
        branch=data['branch']
        description=data['description']
        logo_path=data['logo_path']
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
        restaurent=data['restaurent_id']
        category_name=data['category_name']
        mobile_number=data['mobile_number']
        menu_list = data['menu_list']
       
       
       
        try:
            country = FoodCategories.objects.create(
                   restaurent_id=restaurent,
                    category_name=category_name,
                    mobile_number=mobile_number,
                    menu_list =menu_list,
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
        restaurent=data['restaurent_id']
        category_name=data['category_name']
        mobile_number=data['mobile_number']
        menu_list = data['menu_list']
       
        try:
            country= FoodCategories.objects.filter(id=pk).update(restaurent_id=restaurent,
                    category_name=category_name,
                    mobile_number=mobile_number,
                    menu_list=menu_list,
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
        all_values = FoodCategories.objects.filter(id=pk).delete()
        if test == all_values:
            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})


class MenuView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Menu.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Menu.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        menu_title = data['menu_title']
        menu_display_title = data['menu_display_title']
        disclaimer=data['disclaimer']
        image_path=data['image_path']
    
       
        try:
            country = Menu.objects.create(
                    menu_title=menu_title,
                    menu_display_title=menu_display_title,
                    disclaimer=disclaimer,
                    image_path=image_path,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        menu_title=data['menu_title']
        menu_display_title = data['menu_display_title']
        disclaimer=data['disclaimer']
        image_path=data['image_path']
    


        try:
            country= Menu.objects.filter(id=pk).update(menu_title=menu_title,
                    menu_display_title=menu_display_title,
                    disclaimer=disclaimer,
                    image_path=image_path,)

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
        all_values = Menu.objects.filter(id=pk).delete()
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
        food_category=data['food_category_id']
        menu = data['menu_id']
        name=data['name']
        tag_list=data['tag_list']
        description=data['description']
        price=data['price']
        image_path=data['image_path']

        default_tax_rate =data['default_tax_rate']
        display_photo_path=data['display_photo_path']
        poppable=data['poppable']
        available_for_online_order=data['available_for_online_order']
        taxable=data['taxable']
       
       
       
        try:
            country = FoodItems.objects.create(
                    food_category_id=food_category,
                    menu_id = menu,
                    name=name,
                    tag_list=tag_list,
                    description=description,
                    price=price,
                    image_path=image_path,
                    default_tax_rate=default_tax_rate,
                    display_photo_path=display_photo_path,
                    poppable=poppable,
                    available_for_online_order=available_for_online_order,
                    taxable=taxable,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        food_category=data['food_category_id']
        menu = data['menu_id']
        name=data['name']
        tag_list=data['tag_list']
        description=data['description']
        price=data['price']
        image_path=data['image_path']
        default_tax_rate =data['default_tax_rate']
        display_photo_path=data['display_photo_path']
        poppable=data['poppable']
        available_for_online_order=data['available_for_online_order']
        taxable=data['taxable']
        try:
            country= FoodItems.objects.filter(id=pk).update(food_category_id=food_category,
                    menu_id = menu,
                    name=name,
                    tag_list=tag_list,
                    description=description,
                    price=price,
                    image_path=image_path,
                    default_tax_rate=default_tax_rate,
                    display_photo_path=display_photo_path,
                    poppable=poppable,
                    available_for_online_order=available_for_online_order,
                    taxable=taxable,
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
        name=data['name']
        price=data['price']
       
       
        try:
            country = Toppings.objects.create(
                    price=price,
                    name=name,
                   
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        name=data['name']
        price=data['price']

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
        food_items=data['food_items_id']
        toppings_id_list=data['toppings_id_list']
       
        try:
            country = ToppingsItems.objects.create(
                    food_items_id=food_items,
                    toppings_id_list =toppings_id_list,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        food_items=data['food_items_id']
        toppings_id_list=data['toppings_id_list']

        try:
            country= ToppingsItems.objects.filter(id=pk).update(food_items_id=food_items,
                    toppings_id_list =toppings_id_list,
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
        customer_user=data['customer_user_id']
        food_items=data['food_items_id']
        quantity=data['quantity']

        try:
            country = CartItems.objects.create(
                    customer_user_id=customer_user,
                    food_items_id=food_items,
                    quantity   =quantity,  
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data['customer_user_id']
        food_items=data['food_items_id']
        quantity=data['quantity']

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
        name=data['name']
        phone_number=data['phone_number']
        

        try:
            country = DeliveryDriver.objects.create(
                    name=name,
                    phone_number=phone_number,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        name=data['name']
        phone_number=data['phone_number']

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
            all_data = DeliveryPartners.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        dp_name=data['dp_name']
        dp_img_path=data['dp_img_path']
        dp_ph_number=data['dp_ph_number']
        dp_charges=data['dp_charges']

    

        try:
            country = DeliveryPartners.objects.create(
                  dp_name=dp_name,
                dp_img_path=dp_img_path,
                dp_ph_number=dp_ph_number,
                dp_charges=dp_charges,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        dp_name=data['dp_name']
        dp_img_path=data['dp_img_path']
        dp_ph_number=data['dp_ph_number']
        dp_charges=data['dp_charges']

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
        customer_user=data['customer_user_id']
        delivery_partner=data['delivery_partner_id']
        restaurent=data['restaurent_id']
        delivery_driver=data['delivery_driver_id']
        # order_date=['order_date']
        # order_time=['order_time']
        total_amount=data['total_amount']
        order_status=data['order_status']
        payment_method=data['payment_method']
        transaction_id=data['transaction_id']
        devlivery_method=data['devlivery_method']
        delivery_fee=data['delivery_fee']
        # requested_delivery_time=['requested_delivery_time']
        driver_rating=data['driver_rating']
        restaurent_rating=data['restaurent_rating']

        odt= data['order_dt']
        order_dateandtime_timestamp = time.mktime(datetime.strptime(odt, "%d/%m/%Y").timetuple())

        rdt= data.get('requested_delivery_time')
        requested_order_date_timestamp = time.mktime(datetime.strptime(rdt, "%d/%m/%Y").timetuple())

        
        try:
            country = Orders.objects.create(
                customer_user_id=customer_user,
                delivery_partner_id=delivery_partner,
                restaurent_id=restaurent,
                delivery_driver_id=delivery_driver,
                order_dt=order_dateandtime_timestamp,
                total_amount=total_amount,
                order_status=order_status,
                payment_method=payment_method,
                transaction_id=transaction_id,
                devlivery_method=devlivery_method,
                delivery_fee=delivery_fee,

                requested_delivery_time=requested_order_date_timestamp,
                driver_rating=driver_rating,
                restaurent_rating=restaurent_rating,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data['customer_user_id']
        delivery_partner=data['delivery_partner_id']
        restaurent=data['restaurent_id']
        delivery_driver=data['delivery_driver_id']
        # order_date=['order_date']
        # order_time=['order_time']
        total_amount=data['total_amount']
        order_status=data['order_status']
        payment_method=data['payment_method']
        transaction_id=data['transaction_id']
        devlivery_method=data['devlivery_method']
        delivery_fee=data['delivery_fee']
        # requested_delivery_time=['requested_delivery_time']
        driver_rating=data['driver_rating']
        restaurent_rating=data['restaurent_rating']

        odt= data['order_dt']
        order_dateandtime_timestamp = time.mktime(datetime.strptime(odt, "%d/%m/%Y").timetuple())

        rdt= data.get('requested_delivery_time')
        requested_order_date_timestamp = time.mktime(datetime.strptime(rdt, "%d/%m/%Y").timetuple())

        try:
            country= Orders.objects.filter(id=pk).update(
                customer_user_id=customer_user,
                delivery_partner_id=delivery_partner,
                restaurent_id=restaurent,
                delivery_driver_id=delivery_driver,
                order_dt=order_dateandtime_timestamp,
                total_amount=total_amount,
                order_status=order_status,
                payment_method=payment_method,
                transaction_id=transaction_id,
                devlivery_method=devlivery_method,
                delivery_fee=delivery_fee,

                requested_delivery_time=requested_order_date_timestamp,
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
        order=data['order_id']
        food_items=data['food_items_id']
        toppings_id_list=data['toppings_id_list']
        complete_order_item=data['complete_order_item']
        quantity=data['quantity']



        try:
            country = OrdersItems.objects.create(
                order_id=order,
                food_items_id=food_items,
                toppings_id_list=toppings_id_list,
                complete_order_item=complete_order_item,
                quantity=quantity,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        order=data['order_id']
        food_items=data['food_items_id']
        toppings_id_list=data['toppings_id_list']
        complete_order_item=data['complete_order_item']
        quantity=data['quantity']
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
        customer_user=data['customer_user_id']
        food_items=data['food_items_id']
        


        try:
            country = Likes.objects.create(
                customer_user_id=customer_user,
                food_items_id=food_items,
                
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data['customer_user_id']
        food_items=data['food_items_id']

        try:
            country= Likes.objects.filter(id=pk).update(customer_user_id=customer_user,
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
        customer_user=data['customer_user_id']
        code=data['code']
        discount_amount=data['discount_amount']
        # valid_from=data['valid_from']
        # valid_to=data['valid_to']

        vf= data['valid_from']
        valid_from__timestamp = time.mktime(datetime.strptime(vf, "%d/%m/%Y").timetuple())

        vt= data['valid_to']
        valid_to_date_timestamp = time.mktime(datetime.strptime(vt, "%d/%m/%Y").timetuple())

        try:
            country = PromoCode.objects.create(
                customer_user_id=customer_user,
                code=code,
                discount_amount=discount_amount,
                valid_from=valid_from__timestamp,
                valid_to=valid_to_date_timestamp,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data['customer_user_id']
        code=data['code']
        discount_amount=data['discount_amount']
        # valid_from=data['valid_from']
        # valid_to=data['valid_to']

        vf= data['valid_from']
        valid_from__timestamp = time.mktime(datetime.strptime(vf, "%d/%m/%Y").timetuple())

        vt= data['valid_to']
        valid_to_date_timestamp = time.mktime(datetime.strptime(vt, "%d/%m/%Y").timetuple())

        try:
            country= PromoCode.objects.filter(id=pk).update(customer_user_id=customer_user,
                code=code,
                discount_amount=discount_amount,
                valid_from=valid_from__timestamp,
                valid_to=valid_to_date_timestamp,
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
        customer_user=data['customer_user_id']
        action_type=data['action_type']
        # action_time_stamp=data['action_time_stamp']
        
        act= data['action_time_stamp']
        order_dateandtime_timestamp = time.mktime(datetime.strptime(act, "%d/%m/%Y %H:%M").timetuple())


        try:
            country = UserActionTracking.objects.create(
                customer_user_id=customer_user,
                action_type=action_type,
                action_time_stamp=order_dateandtime_timestamp,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data['customer_user_id']
        action_type=data['action_type']
        # action_time_stamp=data['action_time_stamp']

        act= data['action_time_stamp']
        order_dateandtime_timestamp = time.mktime(datetime.strptime(act, "%d/%m/%Y %H:%M").timetuple())
        try:
            country= UserActionTracking.objects.filter(id=pk).update(customer_user_id=customer_user,
                action_type=action_type,
                action_time_stamp=act,
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
        customer_user=data['customer_user_id']
        order=data['order_id']
        amount=data['amount']
        # payment_date=data['payment_date']
        payment_status=data['payment_status']
        transaction_id=data['transaction_id']
        payment_gateway_response=data['payment_gateway_response']


        pd= data['payment_date']
        payment_date_time = time.mktime(datetime.strptime(pd, "%d/%m/%Y").timetuple())
       

        try:
            country = UserPayment.objects.create(
                customer_user_id=customer_user,
                order_id=order,
                amount=amount,
                payment_date=payment_date_time,
                payment_status=payment_status,
                transaction_id=transaction_id,
                payment_gateway_response=payment_gateway_response,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user=data['customer_user_id']
        order=data['order_id']
        amount=data['amount']
        # payment_date=data['payment_date']
        payment_status=data['payment_status']
        transaction_id=data['transaction_id']
        payment_gateway_response=data['payment_gateway_response']

        pd= data['payment_date']
        order_dateandtime_timestamp = time.mktime(datetime.strptime(pd, "%d/%m/%Y").timetuple())

        try:
            country= UserPayment.objects.filter(id=pk).update(customer_user_id=customer_user,
                order_id=order,
                amount=amount,
                payment_date=payment_date_time,
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
        order=data['order_id']
        status=data['status']
        time_stamp=data['time_stamp']
        
        pd= data['time_stamp']
        order_tracking = time.mktime(datetime.strptime(pd, "%d/%m/%Y %H:%M").timetuple())

        try:
            country = OrderTracking.objects.create(
                
                order_id=order,
              
                status=status,
                time_stamp=order_tracking,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        order=data['order_id']
        status=data['status']
        time_stamp=data['time_stamp']

        ts= data['time_stamp']
        order_tracking = time.mktime(datetime.strptime(ts, "%d/%m/%Y %H:%M").timetuple())

        try:
            country= OrderTracking.objects.filter(id=pk).update(order_id=order,
              
                status=status,
                time_stamp=order_tracking,
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



class TagApiView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            all_data = Tag.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Tag.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})
            pagination_result = HungerPointAppPagination(all_data,request)

            return pagination_result

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        name=data['name']
        abbreivation=data['abbreivation']
        add_img_path=data['add_img_path']
        
       

        try:
            tag = Tag.objects.create(
                
                name=name,
                abbreivation=abbreivation,
                add_img_path=add_img_path,
                    )
            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        name=data['name']
        abbreivation=data['abbreivation']
        add_img_path=data['add_img_path']
        try:
            tag= Tag.objects.filter(id=pk).update( name=name,
                abbreivation=abbreivation,
                add_img_path=add_img_path,
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






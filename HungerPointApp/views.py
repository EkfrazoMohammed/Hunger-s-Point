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
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponsePermanentRedirect

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from .models import *
import jwt
from django.db.models import Q,Count
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework import generics, viewsets, status
from django.contrib import auth
from .serializers import *
from rest_framework import viewsets, status

from rest_framework.authtoken.views import ObtainAuthToken

from django.db.models import Sum
import re
from django.core.exceptions import ObjectDoesNotExist


from django.views.decorators.csrf import csrf_exempt

# import urllib.request as urllib2
from urllib.request import urlopen

import urllib.request
import urllib.error
import json
import time
from datetime import datetime



# from accounts.backends import *
from HungerPointApp.backends import *
import urllib.parse
import http.client
from HungerPointApp.serializers import *
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def OrderUpdate():
    all_order_obj = Orders.objects.all()
    # Get the current datetime
    current_datetime = timezone.now()
    for order in all_order_obj:
        # Extract the order timestamp and convert it to a datetime object
        order_timestamp = order.o_c_timestamp
        if isinstance(order_timestamp, str):
            order_timestamp = datetime.strptime(order_timestamp, '%Y-%m-%d %H:%M:%S.%f%z')
        
        # Calculate the difference between the current datetime and order timestamp
        time_difference = current_datetime - order_timestamp
        
        # If the difference exceeds 20 minutes, update the order status to "PICKED UP"
        if time_difference > timedelta(minutes=2):
            order.order_status = "PICKED UP"
            order.save()

    print('ALL====>notificationcenter')
    return "ALL NOTIFICATION DELETED"

import ssl
import smtplib

def SendSavedEmail():
    # Get today's date
    today_date = timezone.now().date()

    # Fetch all Reaction objects
    all_reaction_obj = Reaction.objects.all()

    # Iterate through each Reaction object
    for reaction in all_reaction_obj:
        # Check if saveit is True and saveit_date is not None
        if reaction.saveit and reaction.saveit_date:
            # Ensure the saveit_date dictionary contains the 'startDate' and 'endDate' keys
            if 'startDate' in reaction.saveit_date and 'endDate' in reaction.saveit_date:
                start_date_str = reaction.saveit_date['startDate']
                end_date_str = reaction.saveit_date['endDate']

                # Check if startDate and endDate are not None
                if start_date_str and end_date_str:
                    try:
                        # Parse the startDate and endDate
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()

                        print(start_date, today_date, end_date, 'start_date, today_date, end_date')

                        # Check if today's date falls within the range defined by startDate and endDate
                        if 'email_sent' not in reaction.saveit_date or not reaction.saveit_date['email_sent']:
                            if start_date <= today_date <= end_date:
                                # Compose your email message
                                subject = 'Hungers Point reminder'
                                print(subject, 'subject==>11111111', today_date, 'menu_items_id', reaction.menu_items_id)

                                cuser = CustomUser.objects.get(id=reaction.cuser_id)
                                print(cuser.email_id, 'cuser.email_id')

                                menu_item_data = MenuItems.objects.get(id=reaction.menu_items_id)

                                # HTML email template path
                                html_tpl_path = 'new-email.html'
                                
                                # Context data to render the template
                                context_data = {
                                    'name': cuser.user_name if cuser.user_name else "There",
                                    'menu_image_url': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item_data.item_image),
                                    'menu_name': menu_item_data.name,
                                }

                                # Render the HTML template with context data
                                email_html_content = render_to_string(html_tpl_path, context_data)
                                email_text_content = strip_tags(email_html_content)  # Fallback to plain text

                                # Create the email with both plain text and HTML content
                                email = EmailMultiAlternatives(
                                    subject,
                                    email_text_content,  # Plain text content
                                    from_email='your_email@example.com',  # Replace with your from email address
                                    to=[cuser.email_id],
                                )

                                email.attach_alternative(email_html_content, "text/html")
                                
                                # Send the email
                                email.send()
                                # Update the email_sent flag in saveit_date
                                reaction.saveit_date['email_sent'] = True
                                reaction.save()
                        else:
                            print('email sent previously message==>')
                            

                    except ValueError as e:
                        print("Error parsing date: ", e)
                else:
                    print("Error: startDate or endDate is None in the saveit_date dictionary.")
            else:
                print("Error: 'startDate' or 'endDate' key is missing in the saveit_date dictionary.")
        else:
            print("saveit is False or saveit_date is None for this reaction.")

    return "Saved date notification sent"


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
                    'email_id':create_super_user.email,
                    'role_name':role_name,
                    'user_id':user_create.id,
                    'phone_number':user_create.phone_number,
                    'spr_user_id':create_super_user.id,
                    'token':authorization,
                    }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK

                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)
        else:
            if 'spr_user_id' in data:
                spr_user_id   = data['spr_user_id']
                
                if User.objects.filter(Q(id=spr_user_id)).exists():
                    role_data = UserRole.objects.get(role_name='USER')
                    create_super_user = User.objects.get(id=spr_user_id)
                    user_create = CustomUser.objects.get(email_id=create_super_user.email,role_id=role_data.id)
                    auth_token = jwt.encode(
                                {'email': create_super_user.email,'role_name':role_data.role_name,'user_id':user_create.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {}
                    response_result['result'] = {
                        'result': {'data': 'User Already Exists',
                        'email_id':create_super_user.email,
                        'role_name':role_data.role_name,
                        'user_id':user_create.id,
                        'phone_number':user_create.phone_number,
                        'token':authorization,
                        'spr_user_id':create_super_user.id,
                        'code':1
                        }}
                    response['Authorization'] = authorization
                    response['status'] = status.HTTP_200_OK

                    return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)

            if 'user_name' in data:
                user_name = data['user_name']
                role_data = UserRole.objects.get(role_name='USER')
                if User.objects.filter(username=email,email=email).exists():
                    create_super_user = User.objects.get(username=email,email=email)
                    user_create = CustomUser.objects.get((Q(user_name=user_name) | Q(email_id=email)) & Q(role_id=role_data.id))
                else:
                    create_super_user = User.objects.create_user(username=email,email=email)
                    user_create = CustomUser.objects.create(user_name=user_name,email_id=email,role_id=role_data.id)
            
                auth_token = jwt.encode(
                            {'email': create_super_user.email,'role_name':role_data.role_name,'user_id':user_create.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'result': {'data': 'USER Register successful',
                    'email_id':create_super_user.email,
                    'role_name':role_data.role_name,
                    'user_id':user_create.id,
                    'token':authorization,
                    'phone_number':user_create.phone_number,
                    'spr_user_id':create_super_user.id,
                    'code':2
                    }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK

                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)

            if User.objects.filter(Q(email=email)).exists():
                role_data = UserRole.objects.get(role_name='USER')
                create_super_user = User.objects.get(username=email,email=email)
                user_create = CustomUser.objects.get(email_id=email,role_id=role_data.id)
                auth_token = jwt.encode(
                            {'email': create_super_user.email,'role_name':role_data.role_name,'user_id':user_create.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'result': {'data': 'User Already Exists',
                    'email_id':create_super_user.email,
                    'role_name':role_data.role_name,
                    'user_id':user_create.id,
                    'token':authorization,
                    'phone_number':user_create.phone_number,
                    'spr_user_id':create_super_user.id,
                    'code':1
                    }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK

                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)
   
            else:
                # User register
                firstName   = data['firstName']
                lastName   = data['lastName']
                phoneNumber   = data['phoneNumber']
                role_data = UserRole.objects.get(role_name='USER')
                create_super_user = User.objects.create_user(username=email,email=email)
                user_create = CustomUser.objects.create(user_name=firstName,email_id=email,role_id=role_data.id,f_name=firstName,l_name=lastName,phone_number=phoneNumber)
            
                auth_token = jwt.encode(
                            {'email': create_super_user.email,'role_name':role_data.role_name,'user_id':user_create.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'result': {'data': 'USER Register successful',
                    'email_id':create_super_user.email,
                    'role_name':role_data.role_name,
                    'user_id':user_create.id,
                    'phone_number':user_create.phone_number,
                    'token':authorization,
                    'spr_user_id':create_super_user.id,
                    'code':2
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
            user_check = User.objects.filter(email=email)
            if user_check:
                user = auth.authenticate(username=email, password=password)
                if user:
                    custom_user = CustomUser.objects.get(email_id=email)
                    role_data = UserRole.objects.get(id=custom_user.role_id)
                    auth_token = jwt.encode(
                        {'email_id': user.username, 'email': user.email}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

                    # serializer = CustomUserTableSerializers(user)
                    authorization = 'Bearer'+' '+auth_token
                    response_result = {
                        'detail': str(role_data.role_name) + ' Login successful',
                        'role_name': role_data.role_name,
                        'user_id': custom_user.id,
                        'token': authorization,
                        'username': custom_user.user_name,
                        'email': custom_user.email_id,
                        'firstName': custom_user.f_name,
                        'lastName': custom_user.l_name,
                        'phone': custom_user.phone_number,
                    }
                    if 'profile_img' in data:
                        response_result['profile_img'] = data['profile_img']

                    response['Authorization'] = authorization
                    response['status'] = status.HTTP_200_OK
                else:
                    user = User.objects.get(username=email)
                    # print(user.username,'user.username')
                    # print(user.password,'user.password')
                    header_response = {}
                    response['error'] = {
                        'detail': 'Invalid email/password', 'status': status.HTTP_401_UNAUTHORIZED}
                    return Response(response['error'], headers=header_response, status=status.HTTP_401_UNAUTHORIZED)
                return Response(response_result, headers=response, status=status.HTTP_200_OK)
            else:
                response['error'] = {
                    'detail': 'User does not exist', 'status': status.HTTP_401_UNAUTHORIZED}
                return Response(response['error'], status=status.HTTP_401_UNAUTHORIZED)
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


# Function to update an object in the list based on ID
def update_object_by_id(data_list, id_to_update, update_data):
    for item in data_list:
        if item["id"] == id_to_update:
            item.update(update_data)
            break  # Stop iteration after updating the first matching object
    return data_list

class UserAddressView(APIView):

    def post(self,request):
        # CheckAccess(request)

        data = request.data
        email_id=data['email_id']
        
        # complete_address=data['complete_address']
        # city=data['city']
        phone_number=data['phone_number']
        f_name=data['f_name']
        l_name=data['l_name']
        # state=data['state']
        method=data['method']
        spr_user_id=data['spr_user_id']
        response = {}
        try:
            # if CustomUser.objects.filter(Q(id=user_id)).exists():
                
                
            if method == 'ADD':
                user_id=data['user_id']
                if CustomUser.objects.filter(email_id=email_id).exists():
                    get_use_data = CustomUser.objects.get(email_id=email_id)
                    CartItems.objects.filter(customer_user_id=user_id).update(customer_user_id=get_use_data.id)
                else:
                    user_id=data['user_id']
                    get_use_data = CustomUser.objects.get(id=user_id)
                rand = random.randint(0, 1000)
                fresh_list = []
                address_obj = {
                    "id":rand,
                    # "complete_address":complete_address,
                    # "city":city,
                    "phone_number":phone_number,
                    "f_name":f_name,
                    "l_name":l_name,
                    # "state":state,
                    "email_id":email_id
                }
                print(address_obj,'address_obj====>')
                fresh_list.append(address_obj)
                if get_use_data.address_list:
                    combined_list = fresh_list + get_use_data.address_list
                else:
                    combined_list = fresh_list

                c_user = CustomUser.objects.filter(id=get_use_data.id).update(
                    address_list = combined_list,
                    # complete_address = complete_address,
                    # city = city,
                    phone_number = phone_number,
                    f_name = f_name,
                    l_name = l_name,
                    # state = state,
                    email_id=email_id,
                    user_name = str(f_name) + str(l_name)
                    )
                if User.objects.filter(email=email_id).exists():
                    user_data = User.objects.get(email=email_id)
                    # Update the username and email fields
                    user_data.username = email_id
                    user_data.email = email_id
                    user_data.save()
                else:
                    user_data = User.objects.get(id=spr_user_id)
                    # Update the username and email fields
                    user_data.username = email_id
                    user_data.email = email_id
                    user_data.save()
                    
                
                auth_token = jwt.encode(
                            {'email': get_use_data.email_id,'role_name':'USER','user_id':get_use_data.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'result': {'data': 'USER Token Updated',
                    'email_id':get_use_data.email_id,
                    'role_name':'USER',
                    'user_id':get_use_data.id,
                    'phone_number':get_use_data.phone_number,
                    'spr_user_id':user_data.id,
                    'token':authorization,
                    }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK

                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)


                # return Response({'result':{'status':'Address created successfully '}})
            else:
                user_id=data['user_id']
                id=data['id']
                get_use_data = CustomUser.objects.get(id=user_id)

                address_obj = {
                    # "complete_address":complete_address,
                    # "city":city,
                    "phone_number":phone_number,
                    "f_name":f_name,
                    "l_name":l_name,
                    # "state":state,
                    "email_id":email_id
                }

                print(address_obj,'address_obj====>')
                # Call the function to update an object with ID 839
                updated_object_list  = update_object_by_id(get_use_data.address_list, id, address_obj)
                print(updated_object_list,'updated_object_list====>')

                c_user = CustomUser.objects.filter(id=user_id).update(
                    address_list = updated_object_list,
                    # complete_address = complete_address,
                    # city = city,
                    phone_number = phone_number,
                    f_name = f_name,
                    l_name = l_name,
                    # state = state,
                    user_name = str(f_name) + str(l_name),
                    email_id=email_id
                    )
                # user_data = User.objects.filter(id=spr_user_id).update(
                #     username=email_id,
                #     email=email_id
                # )
                user_data = User.objects.get(id=spr_user_id)
                # Update the username and email fields
                user_data.username = email_id
                user_data.email = email_id
                user_data.save()

                auth_token = jwt.encode(
                            {'email': get_use_data.email_id,'role_name':'USER','user_id':get_use_data.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'result': {'data': 'USER Token Updated',
                    'email_id':get_use_data.email_id,
                    'role_name':'USER',
                    'user_id':get_use_data.id,
                    'phone_number':get_use_data.phone_number,
                    'spr_user_id':user_data.id,
                    'token':authorization,
                    }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK

                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)


                # return Response({'result':{'status':'Address updated successfully '}})
            # else:
            #     return Response({'result':{'status':'User already exists '}},status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)




class CustomUserView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        email_id = request.query_params.get('email_id')
        user_id = request.query_params.get('user_id')
        if id:
            all_data = CustomUser.objects.filter(id=id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        elif email_id:
            all_data = CustomUser.objects.filter(email_id=email_id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        elif user_id:
            all_data = CustomUser.objects.filter(id=user_id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = CustomUser.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})
            # pagination_result = HungerPointAppPagination(all_data,request)

            # return pagination_result

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
                phone_number=phone_number
                )
            if 'profile_img' in data:
                backgroundImage=data['profile_img']
                if profile_img.startswith('data:image'):
                    c_user.profile_img = base64_to_image(profile_img)
                    c_user.save()

            # Find the user by email or any other unique identifier
            user = User.objects.get(email=email_id)
            user.set_password(password)
            user.save()

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

class AdminProfile(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            try:
                all_data = CustomUser.objects.get(id=id)
                serializer = CustomUserSerializer(all_data)

                return Response({'result': {'status': 'GET by Id', 'data': serializer.data}})
            except CustomUser.DoesNotExist:
                return Response({
                    'error': {
                        'message': 'Record not found!',
                        'status_code': status.HTTP_404_NOT_FOUND,
                    }},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            all_data = CustomUser.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})
            # pagination_result = HungerPointAppPagination(all_data,request)

            # return pagination_result

    def post(self,request):
        # CheckAccess(request)

        data = request.data
       
        email=data['email']
        first_name=data['first_name']
        last_name=data['last_name']
        phone_number=data['phone_number']

        old_password = data['old_password']
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        
        try:
            c_user = CustomUser.objects.create(
                f_name = f_name,
                l_name = l_name,
                email_id = email_id,
                phone_number = phone_number,
                )
            if 'profile_img' in data:
                backgroundImage=data['profile_img']
                if profile_img.startswith('data:image'):
                    c_user.profile_img = base64_to_image(profile_img)
                    c_user.save()

            user = User.objects.get(email=email_id)
            if not user.check_password(old_password):
                return Response({
                'error':{'message':'Old password is incorrect',
                'detail':'Old password is incorrect'
                }},status=status.HTTP_400_BAD_REQUEST)
        
            if new_password != confirm_password:
                return Response({
                'error':{'message':'New password and confirm password do not match',
                'detail':'New password and confirm password do not match'
                }},status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            c_user.password = new_password
            c_user.save()

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
        
        c_user_data = CustomUser.objects.get(id=pk)
        required_1_keys = ['email','firstName','lastName','phone',]
        if all(key in data for key in required_1_keys):
            email=data['email']
            first_name=data['firstName']
            last_name=data['lastName']
            phone_number=data['phone']

       
            c_user= CustomUser.objects.filter(id=pk).update(
                f_name = first_name,
                l_name = last_name,
                email_id = email,
                phone_number = phone_number,
                )
            
            if 'profile_img' in data:
                profile_img=data['profile_img']
                if profile_img.startswith('data:image'):
                    c_user_data.profile_img = base64_to_image(profile_img)
                    c_user_data.save()

        required_keys = [ 'new_password', 'confirm_password']
        if all(key in data for key in required_keys):
            old_password = data['old_password']
            new_password = data['new_password']
            confirm_password = data['confirm_password']
    
            
            c_user_data.password = new_password
            c_user_data.save()
        
            user = User.objects.get(email=c_user_data.email_id)
            # if not user.check_password(old_password):
            #     return Response({
            #     'error':{'message':'Old password is incorrect',
            #     'detail':'Old password is incorrect'
            #     }},status=status.HTTP_400_BAD_REQUEST)
        
            if new_password != confirm_password:
                return Response({
                'error':{'message':'New password and confirm password do not match',
                'detail':'New password and confirm password do not match'
                }},status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
        


        
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


class RestaurentDetailAPIView(generics.RetrieveAPIView):
    queryset = Restaurent.objects.all()
    serializer_class = RestaurentSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Restaurent.DoesNotExist:
            return Response({
                'error': {
                    'message': 'Record not found!',
                    'status_code': status.HTTP_404_NOT_FOUND,
                }
            }, status=status.HTTP_404_NOT_FOUND)


class MenuTagItemView(APIView):
    def get(self,request):
        # CheckAccess(request)
        id = request.query_params.get('id')
        menu_id = request.query_params.get('menu_id')
        tag_id = request.query_params.get('tag_id')
        
        if menu_id:
            if menu_id == 'ALL':
                items_linked_menus = []
                # menus = Menu.objects.all()
                menu_item_data = MenuItems.objects.all().values()
                for item in menu_item_data:
                    # print(item['selected_location_list'],'itemssss==============================')
                    for location in item['selected_location_list']:
                        # print(type(location['id']),'location---ids',type(id),'id given')
                        if int(location['id']) == int(id):
                            # print('Inside--location',item['name'])
                            # items_linked_to_location.append(item)
                            if item['selected_menu_list'] and item['selected_menu_list'][0] not in items_linked_menus:
                                items_linked_menus.append(item['selected_menu_list'][0])
                # print(items_linked_menus,'items_linked_menus====>')
                return Response({'result': {'status': 'GET_BY_ID', 'data': items_linked_menus}})
            else:
                menus = Menu.objects.filter(id=menu_id)
                all_menu_data = []

                # Iterate over each menu
                for menu in menus:
                    # Initialize counters and lists for the menu
                    item_counter = Counter()
                    item_info_list = []  # Move this initialization outside the loop

                    # Fetch menu items related to this menu
                    menu_items = MenuItems.objects.filter(menu_id=menu_id)
                    
                    # Iterate over menu items
                    for menu_item in menu_items:
                        # Increment the count for each menu ID
                        for selected_menu in menu_item.selected_menu_list:
                            item_counter[selected_menu['id']] += 1
                            # print(selected_menu,'selected_menu111')
                            # print(selected_menu['id'],'selected_menu===>')
                        # print(item_counter,'item_counter===>')
                        # Fetch additional information about the menu item
                        item_info = {
                            'id':menu_item.id,
                            'name': menu_item.name,
                            'amount': menu_item.amount,
                            'item_count': sum(item_counter.values()),
                            'item_image': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image),
                            # Add more fields as needed
                            
                        }
                        item_info_list.append(item_info)
                    
                    # Store the count and information for the menu
                    menu_item_info = {
                        'menu_id': menu.id,
                        'item_count': sum(item_counter.values()),
                        'item_info_list': item_info_list,  # Use the accumulated item_info_list
                    }

                    # Initialize counters and lists for the menu
                    location_counter = Counter()
                    location_info_list = []
                    
                    # Iterate over menu items related to this menu
                    for menu_item in menu_items:
                        # Increment the count for each location ID
                        for selected_location in menu_item.selected_location_list:
                            location_counter[selected_location['id']] += 1
                        
                        # Fetch additional information about the location
                        for location_id in menu_item.selected_location_list:
                            location_info = {
                                'name': str(Restaurent.objects.get(id=location_id['id']).published_name),
                                'address': str(Restaurent.objects.get(id=location_id['id']).address),
                                # Add more fields as needed
                            }
                            location_info_list.append(location_info)
                    
                    # Use a set to store unique location names
                    unique_location_names = set()
                    # Iterate through the list and add unique names to the set
                    for entry in location_info_list:
                        unique_location_names.add(entry["name"])
                    # Create a comma-separated string from the set
                    unique_location_string = ", ".join(unique_location_names)

                    # Store menu data in a dictionary
                    main_dic = {
                        'id': menu.id,
                        'menu_title': menu.menu_title,
                        'm_u_timestamp': menu.m_u_timestamp,
                        'menu_item_count': sum(item_counter.values()),
                        'menu_item_info_list': [dict(t) for t in {tuple(d.items()) for d in item_info_list}],
                        'menu_location_count': len(location_counter),
                        'menu_location_info_list': [dict(t) for t in {tuple(d.items()) for d in location_info_list}],
                        'unique_location_string': unique_location_string
                    }

                    all_menu_data.append(main_dic)

                return Response({'result': {'status': 'GET_BY_ID', 'data': all_menu_data}})

def getmenuitem(menu, menu_id, id):
    menu = Menu.objects.get(id=menu_id)
    all_menu_data = []
    item_counter = Counter()
    item_info_list = [] 
    menu_items = MenuItems.objects.filter(
        Q(menu_id=menu_id) &
        Q(selected_location_list__contains=[{"id": int(id)}])
    )
    for menu_item in menu_items:
        for selected_menu in menu_item.selected_menu_list:
            item_counter[selected_menu['id']] += 1

        item_info = {
            'id':menu_item.id,
            'name': menu_item.name,
            'amount': menu_item.amount,
            'item_count': sum(item_counter.values()),
            'item_image': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image),
        }
        item_info_list.append(item_info)

    menu_item_info = {
        'menu_id': menu_id,
        'item_count': sum(item_counter.values()),
        'item_info_list': item_info_list,  
    }

    location_counter = Counter()
    location_info_list = []
    
    for menu_item in menu_items:
        for selected_location in menu_item.selected_location_list:
            location_counter[selected_location['id']] += 1
    
        for location_id in menu_item.selected_location_list:
            location_info = {
                'name': str(Restaurent.objects.get(id=location_id['id']).published_name),
                'address': str(Restaurent.objects.get(id=location_id['id']).address),
            }
            location_info_list.append(location_info)
    
    unique_location_names = set()
    for entry in location_info_list:
        unique_location_names.add(entry["name"])
    unique_location_string = ", ".join(unique_location_names)

    main_dic = {
        'id': menu_id,
        'menu_title': menu.menu_title,
        'm_u_timestamp': menu.m_u_timestamp,
        'menu_item_count': sum(item_counter.values()),
        'menu_item_info_list': [dict(t) for t in {tuple(d.items()) for d in item_info_list}],
        'menu_location_count': len(location_counter),
        'menu_location_info_list': [dict(t) for t in {tuple(d.items()) for d in location_info_list}],
        'unique_location_string': unique_location_string
    }
    all_menu_data.append(main_dic)
    return all_menu_data
 

class WebMenuTagItemView(APIView):
    def get(self,request):
        # CheckAccess(request)
        id = request.query_params.get('id')
        menu_id = request.query_params.get('menu_id')
        tag_id = request.query_params.get('tag_id')
        
        if menu_id:
            if menu_id == 'ALL':
                all_menu = Menu.objects.all()
              
            else:
                all_menu = Menu.objects.filter(id=menu_id)
            
            all_menu_data = []

            for menu_loop in all_menu:
                menu = Menu.objects.get(id=menu_loop.id)
                
                item_counter = Counter()
                item_info_list = [] 
                print(tag_id,'tag_id===>11')
                if tag_id and int(tag_id) != 0:
                    print('tag_id====>',tag_id)
                    menu_items = MenuItems.objects.filter(
                        Q(menu_id=menu_loop.id) &
                        Q(selected_location_list__contains=[{"id": int(id)}]) &
                        Q(select_item_tag__contains=[{"id": int(tag_id)}])
                    )
                else:
                    menu_items = MenuItems.objects.filter(
                    Q(menu_id=menu_loop.id) &
                    Q(selected_location_list__contains=[{"id": int(id)}])
                    )
                print(menu_items,'menu_items==all')
                for menu_item in menu_items:
                    for selected_menu in menu_item.selected_menu_list:
                        item_counter[selected_menu['id']] += 1
                    try:
                        user_id = request.query_params.get('user_id')
                        if user_id:
                            # Fetch user-specific reaction data
                            get_reaction_data = Reaction.objects.get(Q(menu_items_id=menu_item.id) & Q(cuser_id=user_id))
                        else:
                            # If user_id is not provided, assign default values
                            get_reaction_data = None

                        reaction_counts = Reaction.objects.filter(menu_items_id=menu_item.id).aggregate(
                            loveit_count=Count('id', filter=Q(loveit=True)),
                            likeit_count=Count('id', filter=Q(likeit=True)),
                            dislikeit_count=Count('id', filter=Q(dislikeit=True)),
                            saveit_count=Count('id', filter=Q(saveit=True))
                        )
                        # Retrieve counts from the aggregated result
                        loveit_count = reaction_counts.get('loveit_count', 0)
                        likeit_count = reaction_counts.get('likeit_count', 0)
                        dislikeit_count = reaction_counts.get('dislikeit_count', 0)
                        saveit_count = reaction_counts.get('saveit_count', 0)

                        # Total count of all reactions
                        total_reaction_count = loveit_count + likeit_count + dislikeit_count + saveit_count

                        if get_reaction_data:
                            loveit = get_reaction_data.loveit
                            likeit = get_reaction_data.likeit
                            dislikeit = get_reaction_data.dislikeit
                            saveit = get_reaction_data.saveit
                            saveit_date = get_reaction_data.saveit_date
                        else:
                            # If user-specific reaction data is not available, assign default values
                            loveit = False
                            likeit = False
                            dislikeit = False
                            saveit = False
                            saveit_date = None


                        
                        loveit_count = loveit_count
                        likeit_count = likeit_count
                        dislikeit_count = dislikeit_count
                        saveit_count = saveit_count
                        total_reaction_count=total_reaction_count
                    except ObjectDoesNotExist:
                        # If Reaction data does not exist, assign default values
                        loveit = False
                        likeit = False
                        dislikeit = False
                        saveit = False
                        saveit_date = None
                        loveit_count = 0
                        likeit_count = 0
                        dislikeit_count = 0
                        saveit_count = 0
                        total_reaction_count =0

                    item_info = {
                        'id':menu_item.id,
                        'data':menu_item.data,
                        'name': menu_item.name,
                        'amount': menu_item.amount,
                        'description': menu_item.description,
                        'item_count': sum(item_counter.values()),
                        'item_image': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image),
                        'loveit':loveit,
                        'likeit':likeit,
                        'dislikeit':dislikeit,
                        'saveit':saveit,
                        'saveit_date':saveit_date,
                        'loveit_count':loveit_count,
                        'likeit_count':likeit_count,
                        'dislikeit_count':dislikeit_count,
                        'saveit_count':saveit_count,
                        'total_reaction_count':total_reaction_count
                    }
                    item_info_list.append(item_info)
                # print(item_info_list,'item_info_list===>')
                menu_item_info = {
                    'menu_id': menu_loop.id,
                    'item_count': sum(item_counter.values()),
                    'item_info_list': item_info_list,  
                }

                location_counter = Counter()
                location_info_list = []
                
                for menu_item in menu_items:
                    for selected_location in menu_item.selected_location_list:
                        location_counter[selected_location['id']] += 1
                
                    for location_id in menu_item.selected_location_list:
                        location_info = {
                            'name': str(Restaurent.objects.get(id=location_id['id']).published_name),
                            'address': str(Restaurent.objects.get(id=location_id['id']).address),
                        }
                        location_info_list.append(location_info)
                
                unique_location_names = set()
                for entry in location_info_list:
                    unique_location_names.add(entry["name"])
                unique_location_string = ", ".join(unique_location_names)
                print(item_info_list,'item_info_list===>11')
                if item_info_list:
                    main_dic = {
                        'id': menu_loop.id,
                        'menu_title': menu.menu_title,
                        'm_u_timestamp': menu.m_u_timestamp,
                        'menu_item_count': sum(item_counter.values()),
                        'menu_item_info_list': [
                            {
                                'id': item['id'],
                                'data': item['data'],
                                'name': item['name'],
                                'amount': item['amount'],
                                'description': item['description'],
                                'item_count': item['item_count'],
                                'item_image': item['item_image'],
                                'loveit': item['loveit'],
                                'likeit': item['likeit'],
                                'dislikeit': item['dislikeit'],
                                'saveit': item['saveit'],
                                'saveit_date': item['saveit_date'],
                                'loveit_count': item['loveit_count'],
                                'likeit_count': item['likeit_count'],
                                'dislikeit_count': item['dislikeit_count'],
                                'saveit_count': item['saveit_count'],
                                'total_reaction_count': item['total_reaction_count']
                            }
                            for item in item_info_list
                        ],
                        'menu_location_count': len(location_counter),
                        'menu_location_info_list': [dict(t) for t in {tuple(d.items()) for d in location_info_list}],
                        'unique_location_string': unique_location_string
                    }
                    all_menu_data.append(main_dic)



            return Response({'result': {'status': 'GET_BY_ID', 'data': all_menu_data}})



from django.db.models import F, Value
from django.db.models.functions import Concat

class MenuTagView(APIView):
    def get(self,request):
        # CheckAccess(request)
        id = request.query_params.get('id')
        menu_id = request.query_params.get('menu_id')
        if menu_id:
            try:
                restaurent = Restaurent.objects.get(id=id)
                menu_item_tags = []
                if menu_id == 'ALL':
                    all_menu = Menu.objects.all()
                else:
                    all_menu = Menu.objects.filter(id=menu_id)

                for i in all_menu:
                    menu_item_data = MenuItems.objects.filter(Q(menu_id=i.id) &
                            Q(selected_location_list__contains=[{"id": int(id)}])).select_related('menu').values('menu__menu_title','select_item_tag','id','name','description','amount')

                    for item in menu_item_data:
                        for menu_tag in item['select_item_tag']:
                            if menu_tag not in menu_item_tags:
                                menu_item_tags.append(menu_tag)

                unique_items = []
                seen_ids = set()

                for item in menu_item_tags:
                    if item['id'] not in seen_ids:
                        unique_items.append(item)
                        seen_ids.add(item['id'])

                menu_item_tags = unique_items
               
                return Response({'result': {'status': 'GET by Id','data':menu_item_tags,'all_data':menu_item_data}})

            except Restaurent.DoesNotExist:
                return Response({
                    'error': {
                        'message': 'Record not found!',
                        'status_code': status.HTTP_404_NOT_FOUND,
                    }
                }, status=status.HTTP_404_NOT_FOUND)
        

class RestaurentView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        menu_id = request.query_params.get('menu_id')
        if menu_id:
            try:
                restaurent = Restaurent.objects.get(id=id)
                menu_related_data = []
                menu_item_tags = []
                menu_item_data = MenuItems.objects.all().values()
                for item in menu_item_data:
                    # print(item['selected_location_list'],'itemssss==============================')
                    for location in item['selected_menu_list']:
                        if int(location['id']) == int(menu_id):
                            menu_related_data.append(item)

                return Response({'result': {'status': 'GET by Id','data':menu_related_data}})

            except Restaurent.DoesNotExist:
                return Response({
                    'error': {
                        'message': 'Record not found!',
                        'status_code': status.HTTP_404_NOT_FOUND,
                    }
                }, status=status.HTTP_404_NOT_FOUND)
        

        if id:
            try:
                
                items_linked_to_location = []
                items_linked_menus = []
                menu_item_data = MenuItems.objects.all().values()
                for item in menu_item_data:
                    for location in item['selected_location_list']:
                        if int(location['id']) == int(id):
                            if item['selected_menu_list'] and item['selected_menu_list'][0] not in items_linked_menus:
                                items_linked_menus.append(item['selected_menu_list'][0])

                unique_menus = []
                encountered_ids = set()
                for menu in items_linked_menus:
                    if menu['id'] not in encountered_ids:
                        unique_menus.append(menu)
                        encountered_ids.add(menu['id'])

                restaurent = Restaurent.objects.filter(id=id).values()
            
                return Response({'result': {'status': 'GET by Id','items_linked_menus':unique_menus, 'data': restaurent}})

            except Restaurent.DoesNotExist:
                return Response({
                    'error': {
                        'message': 'Record not found!',
                        'status_code': status.HTTP_404_NOT_FOUND,
                    }
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            restaurant_instance = Restaurent.objects.all()
            serializer = RestaurantSerializer(restaurant_instance, many=True)
            # # print(serializer.data)
            # pagination_result = HungerPointAppPagination(all_data,request)
            return Response({'result':{'data':serializer.data}})
            # return pagination_result

    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        # address=data['address_id']
        # restaurent_name=data['restaurent_name']
        # dp_list=data['dp_list']
        # leave_list=data['leave_list']
        # every_day_time_list=data['every_day_time_list']
        # mobile_number=data['mobile_number']
        # branch=data['branch']
        # description=data['description']
        # logo_path=data['logo_path']

        location  =data['location']
        published_name =data['publishingName']
        location_phone =data['locationPhone']
        contact_email =data['contactEmail']
        address =data['address']
        city =data['city']
        state =data['state']
        country =data['country']       
        phone =data['phone']
        # google_place_id =data['google_place_id']
        # every_day_time_list =data['every_day_time_list']
        try:
            country = Restaurent.objects.create(
                    location = location,
                    published_name = published_name,
                    location_phone = location_phone,
                    contact_email = contact_email,
                    address_info = address,
                    city = city,
                    state = state,
                    country = country,
                    phone = phone,
                    # google_place_id = google_place_id,
                    # every_day_time_list = every_day_time_list,
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

        required_1_keys = ['google_place_id']
        if all(key in data for key in required_1_keys):
            google_place_id  =data['google_place_id']
            country= Restaurent.objects.filter(id=pk).update(
                google_place_id =google_place_id)
            return Response({'result':{'status':'Google Place ID Updated'}})
        else:    
            location  =data['location']
            published_name =data['publishingName']
            location_phone =data['locationPhone']
            contact_email =data['contactEmail']
            address =data['address']
            city =data['city']
            state =data['state']
            country =data['country']       
            phone =data['phone']
            # google_place_id =data['google_place_id']
            # every_day_time_list =data['every_day_time_list']
            try:
                country= Restaurent.objects.filter(id=pk).update(
                    location =location,
                    published_name =published_name,
                    location_phone =location_phone,
                    contact_email =contact_email,
                    address_info =address,
                    city =city,
                    state =state,
                    country =country,
                    phone =phone,
                    # google_place_id =google_place_id,
                    # every_day_time_list =every_day_time_list,
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
    queryset  = Menu.objects.all()
    serializer = MenuSerializer

    def get(self,request):
    

        menu_id = request.query_params.get('menu_id')
        if menu_id:
            try:
                # Get the menu object by ID
                menu = Menu.objects.get(id=menu_id)

                # Initialize counters and lists for the menu
                item_counter = Counter()
                item_info_list = []
                location_counter = Counter()
                location_info_list = []

                # Fetch menu items related to this menu
                menu_items = MenuItems.objects.filter(selected_menu_list__contains=[{'id': menu_id}])

                # If menu_items is empty, return menu information without item and location details
                if not menu_items:
                    menu_data = {
                        'id': menu_id,
                        'menu_title':menu.menu_title,
                        'menu_display_title':menu.menu_display_title,
                        'disclaimer':menu.disclaimer,
                        # 'menu_image':menu.menu_image,
                        'm_u_timestamp':menu.m_u_timestamp,
                        'menu_location_info': {
                            'menu_id': menu_id,
                            'location_count': 0,
                            'location_info_list': [],
                        },
                        'menu_item_info': {
                            'menu_id': menu_id,
                            'item_count': 0,
                            'item_info_list': [],
                        },
                        'menu_item_count': 0,
                        'menu_location_count': 0,
                        'unique_location_string': "",
                    }
                    # print(menu.menu_image,'menu.menu_image')
                    if menu.menu_image:
                        menu_data['menu_image'] = 'https://hunger.thestorywallcafe.com/media/' + str(menu.menu_image)

                    return Response({'result': {'status': 'Success', 'data': menu_data}})

                # Iterate over menu items
                for menu_item in menu_items:
                    # Increment the count for each menu ID
                    for selected_menu in menu_item.selected_menu_list:
                        item_counter[selected_menu['id']] += 1

                    # Fetch additional information about the menu item
                    item_info = {
                        'id':menu_item.id,
                        'name': menu_item.name,
                        'amount': menu_item.amount,
                        'item_image': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image),
                        # Add more fields as needed
                    }
                    item_info_list.append(item_info)

                    # Increment the count for each location ID
                    for selected_location in menu_item.selected_location_list:
                        location_counter[selected_location['id']] += 1

                        # Fetch additional information about the location
                        location_info = {
                            'name': str(Restaurent.objects.get(id=selected_location['id']).restaurant_name),
                            'address': str(Restaurent.objects.get(id=selected_location['id']).address),
                            # Add more fields as needed
                        }
                        location_info_list.append(location_info)

                # Use a set to store unique location names
                unique_location_names = set()
                # Iterate through the list and add unique names to the set
                for entry in location_info_list:
                    unique_location_names.add(entry["name"])
                # Create a comma-separated string from the set
                unique_location_string = ", ".join(unique_location_names)

                # Construct the menu data dictionary
                menu_data = {
                    'id': menu_id,
                    'menu_title':menu.menu_title,
                    'menu_display_title':menu.menu_display_title,
                    'disclaimer':menu.disclaimer,
                    # 'menu_image':menu.menu_image,
                    'm_u_timestamp':menu.m_u_timestamp,
                    'menu_location_info': {
                        'menu_id': menu_id,
                        'location_count': len(location_counter),
                        'location_info_list': location_info_list,
                    },
                    'menu_item_info': {
                        'menu_id': menu_id,
                        'item_count': sum(item_counter.values()),
                        'item_info_list': item_info_list,
                    },
                    'menu_item_count': sum(item_counter.values()),
                    'menu_location_count': len(location_counter),
                    'unique_location_string': unique_location_string
                }
                if menu.menu_image:
                    menu_data['menu_image'] = 'https://hunger.thestorywallcafe.com/media/' + str(menu.menu_image)

                return Response({'result': {'status': 'Success', 'data': menu_data}})
            
            except Menu.DoesNotExist:
                return Response({'result': {'status': 'Error', 'message': 'Menu with the specified ID does not exist'}})
                    
        else:
           
            menus = Menu.objects.all()
            all_menu_data = []

            # Iterate over each menu
            for menu in menus:
                # Initialize counters and lists for the menu
                item_counter = Counter()
                item_info_list = []  # Move this initialization outside the loop

                # Fetch menu items related to this menu
                menu_items = MenuItems.objects.filter(selected_menu_list__contains=[{'id': menu.id}])
                
                # Iterate over menu items
                for menu_item in menu_items:
                    # Increment the count for each menu ID
                    for selected_menu in menu_item.selected_menu_list:
                        item_counter[selected_menu['id']] += 1
                        # print(selected_menu,'selected_menu111')
                        # print(selected_menu['id'],'selected_menu===>')
                    # print(item_counter,'item_counter===>')
                    # Fetch additional information about the menu item
                    item_info = {
                        'id': menu_item.id,
                        'name': menu_item.name,
                        'amount': menu_item.amount,
                        'item_image': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image),
                        'item_count': sum(item_counter.values()),
                        # Add more fields as needed
                    }
                    item_info_list.append(item_info)
                
                # Store the count and information for the menu
                menu_item_info = {
                    'menu_id': menu.id,
                    'item_count': sum(item_counter.values()),
                    'item_info_list': item_info_list,  # Use the accumulated item_info_list
                }

                # Initialize counters and lists for the menu
                location_counter = Counter()
                location_info_list = []
                
                # Iterate over menu items related to this menu
                for menu_item in menu_items:
                    # Increment the count for each location ID
                    for selected_location in menu_item.selected_location_list:
                        location_counter[selected_location['id']] += 1
                    
                    # Fetch additional information about the location
                    for location_id in menu_item.selected_location_list:
                        location_info = {
                            'name': str(Restaurent.objects.get(id=location_id['id']).published_name),
                            'address': str(Restaurent.objects.get(id=location_id['id']).address),
                            # Add more fields as needed
                        }
                        location_info_list.append(location_info)
                
                # Use a set to store unique location names
                unique_location_names = set()
                # Iterate through the list and add unique names to the set
                for entry in location_info_list:
                    unique_location_names.add(entry["name"])
                # Create a comma-separated string from the set
                unique_location_string = ", ".join(unique_location_names)

                # Store menu data in a dictionary
                main_dic = {
                    'id': menu.id,
                    'menu_title': menu.menu_title,
                    'm_u_timestamp': menu.m_u_timestamp,
                    'menu_location_info': {
                        'menu_id': menu.id,
                        'location_count': len(location_counter),
                        'location_info_list': location_info_list,
                    },
                    'menu_item_info': menu_item_info,
                    'menu_item_count': sum(item_counter.values()),
                    'menu_item_info_list': [dict(t) for t in {tuple(d.items()) for d in item_info_list}],
                    'menu_location_count': len(location_counter),
                    'menu_location_info_list': [dict(t) for t in {tuple(d.items()) for d in location_info_list}],
                    'unique_location_string': unique_location_string
                }

                all_menu_data.append(main_dic)

            return Response({'result': {'status': 'Created', 'data': all_menu_data}})

          

            # food_category = FoodCategories.objects.all()
            # food_category_items = food_category.prefetch_related('fooditems_set').values()
            # all_food_category_data = []

            # for menu in menus_with_food_items:
            #     menu_serializer = MenuSerializer(menu)  # Serialize menu object
            #     serialized_menu = menu_serializer.data  # Get serialized data
            #     food_items_data = []
            #     unique_locations = set()

            #     for food_item in menu.fooditems_set.all():
            #         food_item_serializer = FoodItemsSerializer(food_item)  # Serialize food item object
            #         serialized_food_item = food_item_serializer.data  # Get serialized data for food item
            #         food_items_data.append(serialized_food_item)
            
            #         unique_locations.update(serialized_food_item.get('available_location', []))
                   
            #     # print(unique_locations,'unique_locations===')
            #     # Calculate the count of distinct available locations
            #     serialized_menu['available_location_count'] = len(unique_locations)
            #     # Query Restaurent information for each available location
            #     restaurent_info = []
            #     for location_id in unique_locations:
            #         # print(location_id,'location_id')
            #         restaurent = Restaurent.objects.get(id=location_id)
            #         if restaurent:
            #             # Serialize restaurant data if found
            #             restorent_data={
            #                 'restorent_name':restaurent.restaurent_name,
            #                 'branch_name':restaurent.branch,
            #             }
            #             restaurent_info.append(restorent_data)
            #     # print(restaurent_info,'restaurent_info')

            #     # Extract restaurant names from the list of dictionaries
            #     restorent_names = [restaurent['restorent_name'] for restaurent in restaurent_info]

            #     # Create a comma-separated string of restaurant names
            #     restorent_names_string = ', '.join(restorent_names)

            #     serialized_menu['restorent_names_string'] = restorent_names_string
            #     serialized_menu['restaurent_info'] = restaurent_info
            #     serialized_menu['food_items'] = food_items_data
            #     serialized_menu['food_items_count'] = len(food_items_data) 
            #     menu_image = serialized_menu['menu_image']
            #     if menu_image is not None:
            #         serialized_menu['menu_image'] = 'https://hunger.thestorywallcafe.com' + menu_image
                
            #     # serialized_menu['menu_available_location'] = len(food_items_data.available_location) 
            #     all_menu_data.append(serialized_menu)

            # return Response({'result': {'status': 'Created', 'all_menu_data': all_menu_data}})
    def post(self,request):
        # CheckAccess(request)
        data = request.data
        menu_title = data['menu_title']
        menu_display_title = data['menu_display_title']
        disclaimer=data['disclaimer']
        
    
       
        try:
            menu = Menu.objects.create(
                    menu_title=menu_title,
                    menu_display_title=menu_display_title,
                    disclaimer=disclaimer,
                    # image_path=backgroundImage,
                    )
            if 'backgroundImage' in data:
                backgroundImage=data['backgroundImage']
                if backgroundImage.startswith('data:image'):
                    menu.menu_image = base64_to_image(backgroundImage)
                    menu.save()
            
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
        menu_title = data['menu_title']
        menu_display_title = data['menu_display_title']
        disclaimer=data['disclaimer']
        
    
        file_stored_path = '/media/'
        project_base_url = 'https://hunger.thestorywallcafe.com/'
        
        
        try:
            country= Menu.objects.filter(id=pk).update(menu_title=menu_title,
                    menu_display_title=menu_display_title,
                    disclaimer=disclaimer,
                    )
            if 'backgroundImage' in data:
                backgroundImage=data['backgroundImage']
                if backgroundImage.startswith('data:image'):
                    menu = Menu.objects.get(id=pk)
                    menu.menu_image = base64_to_image(backgroundImage)
                    menu.save()

            

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





class MenuItemsView(APIView):
    menu = FoodItems.objects.all()
    serializer_class = FoodItemsSerializer
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            # Fetch the specific MenuItems object by ID
            menu_item = MenuItems.objects.get(id=id)

            # Fetch related menu details
            selected_menu_list = menu_item.selected_menu_list
            selected_location_list = menu_item.selected_location_list
            # You may need to adjust the following fields according to your model structure
            menu_id = menu_item.id
            selected_menu_list = menu_item.selected_menu_list
            selected_location_list = menu_item.selected_location_list
            name = menu_item.name
            description = menu_item.description
            amount = menu_item.amount
            select_item_tag = menu_item.select_item_tag
            select_default_tax_rate = menu_item.select_default_tax_rate
            display_photo = menu_item.display_photo
            poppable = menu_item.poppable
            online_order_available = menu_item.online_order_available
            taxable = menu_item.taxable
            selected_suggested_menu_list = menu_item.selected_suggested_menu_list
            data = menu_item.data
            # item_image = menu_item.item_image
            # item_image = menu_item.item_image.strip() if menu_item.item_image else None
            
            # Fetch available locations from the selected_location_list
            restorent_list = []
            for location_id in selected_location_list:
                restorent_info = Restaurent.objects.get(id=location_id['id'])
                restorent_list.append(restorent_info.published_name)

            restorent_menu_list = []
            for menu_data in selected_menu_list:
                restorent_menu_list.append(menu_data['menu_title'])
            
            # Convert the list of strings into a single string separated by commas
            available_menu_str = ','.join(restorent_menu_list)
            available_location_str = ','.join(restorent_list)

            # Construct the serialized item
            serialized_item = {
                'id': menu_id,
                "selected_menu_list":selected_menu_list,
                "selected_location_list":selected_location_list,
                "name":name,
                "description":description,
                "amount":amount,
                "select_item_tag":select_item_tag,
                "select_default_tax_rate":select_default_tax_rate,
                "display_photo":display_photo,
                "poppable":poppable,
                "online_order_available":online_order_available,
                "taxable":taxable,
                "selected_suggested_menu_list":selected_suggested_menu_list,
                "data":data,
            }

            if menu_item.item_image:
                item_image = 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image)
                serialized_item['item_image'] = item_image

            # Return the serialized data in the response
            return Response({'result': {'status': 'GET by ID', 'data': serialized_item}})
        else:
            # Fetch all menu items along with related menu information
            all_menu_items = MenuItems.objects.all()

            # Create a list to hold the serialized data
            serialized_data = []

            for menu_item in all_menu_items:
                # Fetch related menu details
                selected_menu_list = menu_item.selected_menu_list
                selected_location_list = menu_item.selected_location_list
                # You may need to adjust the following fields according to your model structure
                menu_id = menu_item.id
                name = menu_item.name
                description = menu_item.description
                amount = menu_item.amount
                select_item_tag = menu_item.select_item_tag
                select_default_tax_rate = menu_item.select_default_tax_rate
                display_photo = menu_item.display_photo
                poppable = menu_item.poppable
                online_order_available = menu_item.online_order_available
                taxable = menu_item.taxable
                selected_suggested_menu_list = menu_item.selected_suggested_menu_list
                data = menu_item.data
                # item_image = str(menu_item.item_image).strip() if menu_item.item_image else None
                # if menu_item.item_image:
                #     menu_item.item_image = 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image)

                

                # Fetch available locations from the selected_location_list
                restorent_list = []
                for location_id in selected_location_list:
                    restorent_info = Restaurent.objects.get(id=location_id['id'])
                    restorent_list.append(restorent_info.published_name)

                restorent_menu_list = []
                for menu_data in selected_menu_list:
                    # print(menu_data,'menu_data===>')
                    # restorent_info = Restaurent.objects.get(id=location_id['id'])
                    restorent_menu_list.append(menu_data['menu_title'])
                
                # Convert the list of strings into a single string separated by commas
                available_menu_str = ','.join(restorent_menu_list)
                available_location_str = ','.join(restorent_list)

                # Construct the serialized item
                serialized_item = {
                    'id':menu_id,
                    'name': name,
                    'description': description,
                    'amount': amount,
                    'selected_menu_list':selected_menu_list,
                    'selected_location_list':selected_location_list,
                    'select_item_tag': select_item_tag,
                    'select_default_tax_rate': select_default_tax_rate,
                    'display_photo': display_photo,
                    'poppable': poppable,
                    'online_order_available': online_order_available,
                    'taxable': taxable,
                    'available_location': available_location_str,
                    'available_menu':available_menu_str,
                    'selected_suggested_menu_list':selected_suggested_menu_list,
                    'data':data,
                    # Add other fields as needed
                }
                if menu_item.item_image:
                    item_image = 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image)
                    serialized_item['item_image'] = item_image

                serialized_data.append(serialized_item)

            # Return the serialized data in the response
            return Response({'result': {'status': 'GET All', 'data': serialized_data}})
    
    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        selected_menu_list = data['selected_menu_list']
        selected_location_list = data['selected_location_list']
        name = data['name']
        description = data['description']
        amount = data['amount']
        select_item_tag = data['select_item_tag']
        select_default_tax_rate = data['select_default_tax_rate']
        


       
        try:
            menu_item_data = {
                    'menu_id' : selected_menu_list[0]['id'],
                    'selected_menu_list': selected_menu_list,
                    'selected_location_list': selected_location_list,
                    'name': name,
                    'description': description,
                    'amount': amount,
                    'select_item_tag': select_item_tag,
                    'select_default_tax_rate': select_default_tax_rate,
                    
                }
            if 'display_photo' in data:
                display_photo = data['display_photo']
                menu_item_data['display_photo'] = display_photo
            if 'poppable' in data:
                poppable = data['poppable']
                menu_item_data['poppable'] = poppable
            if 'online_order_available' in data:
                online_order_available = data['online_order_available']
                menu_item_data['online_order_available'] = online_order_available
            if 'taxable' in data:
                taxable = data['taxable']
                menu_item_data['taxable'] = taxable
            # print(menu_item_data,'menu_item_data')

            if 'backgroundImage' in data:
                backgroundImage=data['backgroundImage']
                if backgroundImage.startswith('data:image'):
                    menu_item_data['item_image'] = base64_to_image(backgroundImage)

            if 'selected_suggested_menu_list' in data:
                selected_suggested_menu_list=data['selected_suggested_menu_list']
                menu_item_data['selected_suggested_menu_list'] = selected_suggested_menu_list

            if 'data' in data:
                data=data['data']
                menu_item_data['data'] = data



            country = MenuItems.objects.create(**menu_item_data)
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
        selected_menu_list = data['selected_menu_list']
        selected_location_list = data['selected_location_list']
        name = data['name']
        description = data['description']
        amount = data['amount']
        select_item_tag = data['select_item_tag']
        select_default_tax_rate = data['select_default_tax_rate']
        display_photo = data['display_photo']
        poppable = data['poppable']
        online_order_available = data['online_order_available']
        taxable = data['taxable']

        selected_suggested_menu_list = data['selected_suggested_menu_list']
        data1 = data['data']
       
        try:
            country = MenuItems.objects.filter(id=pk).update(
                    menu_id = selected_menu_list[0]['id'],
                    selected_menu_list = selected_menu_list,
                    selected_location_list= selected_location_list,
                    name= name,
                    description= description,
                    amount= amount,
                    select_item_tag= select_item_tag,
                    select_default_tax_rate= select_default_tax_rate,
                    display_photo= display_photo,
                    poppable= poppable,
                    online_order_available= online_order_available,
                    taxable= taxable,
                    selected_suggested_menu_list=selected_suggested_menu_list,
                    data=data1
                    )
            menu_data = MenuItems.objects.get(id=pk)
            if 'backgroundImage' in data:
                print('backgroundImage----if')
                backgroundImage=data['backgroundImage']
                if backgroundImage.startswith('data:image'):
                    menu_data.item_image = base64_to_image(backgroundImage)
                    menu_data.save()

            return Response({'result':{'status':'Menu Item Updated successfully'}})

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


class DeleteCartItemsView(APIView):
    def post(self,request):
        data = request.data
        customer_user_id=data['customer_user_id']
        menu_items_id=data['menu_items_id']
        cart_id=data['cart_id']

        test = (0,{})

        print(customer_user_id,menu_items_id,'menu_items_id======>')

        if CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(id=cart_id)).exists():
            cart_data = CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(id=cart_id)).delete()

            basket_count = CartItems.objects.filter(customer_user_id=customer_user_id).count()
            return Response({'result':{'status':'Deleted','basket_count':basket_count}})
        else:
            return Response({'result':{'status':'Item Not Found'}},status=status.HTTP_404_NOT_FOUND)

def merge_lists(*lists):
    merged_set = set()
    for lst in lists:
        for item in lst:
            # Convert the dictionary to a frozenset of its key-value pairs
            item_frozenset = frozenset(item.items())
            # Add the frozenset to the set
            merged_set.add(item_frozenset)
    # Convert each frozenset back to a dictionary
    merged_list = [dict(item_frozenset) for item_frozenset in merged_set]
    return merged_list

class CartItemsView(APIView):
    serializer_class = CartItemsSerializer
    def get(self,request):
        # CheckAccess(request)
    
        # id = request.query_params.get('id')
        customer_user_id = request.query_params.get('customer_user_id')
        menu_items_id = request.query_params.get('menu_items_id')
        restaurent_id = request.query_params.get('restaurent_id')
        cart_id = request.query_params.get('cart_id')
        if customer_user_id:
            if customer_user_id and menu_items_id and restaurent_id:
                if CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(id=cart_id) & Q(restaurent_id=restaurent_id)).exists():

                    cart_data = CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(id=cart_id) & Q(restaurent_id=restaurent_id)).values()

                    return Response({'result':{'status':'User related data','data':cart_data,'basket_count':0,'summary':{}}})


            if CartItems.objects.filter(Q(customer_user_id=customer_user_id)).exists():
                
                all_data = CartItems.objects.filter(Q(customer_user_id=customer_user_id))
                if all_data:
                    serializer = self.serializer_class(all_data, many=True)
                serialized_data = [dict(item) for item in serializer.data]
                # print(serialized_data,'serializer.data===>')
                merged_list = []
                # Create an empty set to store unique item IDs
                unique_ids = set()

                # Create a new list to store unique items
                unique_menu_items = []
                subtotal = 0
                shipping = 0
                tax  = 0
                for item in serialized_data:
                    total_amount = 0
                    
                    # Merge the lists
                    if 'selected_suggested_menu_list' in item['menu_items']:
                        if item['menu_items']['selected_suggested_menu_list']:
                            for suggested_item in item['menu_items']['selected_suggested_menu_list']:
                                if suggested_item["id"] not in unique_ids:
                                    # If not, add the ID to the set and append the item to the new list
                                    unique_ids.add(suggested_item["id"])
                                    unique_menu_items.append(suggested_item)

                                merged_list.append(suggested_item)
                                # print(suggested_item['id'],'suggested_item.id===>')
                                all_menu_item = get_all_menu_data(suggested_item['id'], 0, 1)
                                # print(all_menu_item,'all_menu_item====>',len(all_menu_item))
                                if len(all_menu_item) > 0:
                                    suggested_item['menu_item_info'] = all_menu_item[0]['menu_item_info_list']
                                    for k in suggested_item['menu_item_info']:
                                        menu_item_all_data = MenuItems.objects.get(id=k['id'])
                                        k['menu_add_on'] = menu_item_all_data.data

                    if item['menu_items']['item_image'] is not None:
                        item['menu_items']['item_image'] = 'https://hunger.thestorywallcafe.com'+item['menu_items']['item_image']
                    
                    size_present = False
                    print("==============")
                    if item['menu_items_add_on']:
                        print("IN IFF")
                        for j in item['menu_items_add_on']:
                            # print(j,'jjjjjj')
                            for k in j['value']:
                                
                                if 'selected' in k:
                                    # print(j['key'],'k===>key')
                                    if k['selected'] == True:
                                        if j['key'].lower() != 'size':
                                            total_amount = float(total_amount) + float(k['price']) 
                                        else:
                                            total_amount = float(total_amount) + float(k['price'])
                                            size_present = True
                                            
                        print(total_amount,'Total Amount')
                        print(item['menu_items']['name'],"=> ","Menu Item Amount =",float(item['menu_items']['amount']),'Total Add on amount =', float(total_amount))
                        
                        print('Menu + total_amount = ',float(item['menu_items']['amount']) + float(total_amount))
                        if size_present:
                            total_amount = float(total_amount)
                        else:
                            total_amount = float(item['menu_items']['amount']) + float(total_amount)
                        # print(total_amount,'total_amount=====>finalll')
                        item['total_amount'] = float(round(total_amount, 2) )
                    else:
                        print("IN ELSEE")
                        item['total_amount'] =  float(item['menu_items']['amount'])
                    
                    
                    print("Subtotal=","Subtotal",float(subtotal),"+ Total Amount * Quantity",float(item['total_amount'])* int(item['quantity']),"*",int(item['quantity']))
                    subtotal = float(subtotal) + float(item['total_amount'])* int(item['quantity'])
                    print(item['total_amount'],'Menu Item amount 111',item['menu_items']['name'])
                    
                    try:
                        if item['menu_items']['select_default_tax_rate'][0]['price']:
                         
                            tax = round((float(float(item['menu_items']['select_default_tax_rate'][0]['price']) * int(item['quantity'])) / 100) * subtotal, 2)

                            print(float(float(item['menu_items']['select_default_tax_rate'][0]['price']) * int(item['quantity'])),'111111')
                            print((float(item['menu_items']['select_default_tax_rate'][0]['price'] * int(item['quantity'])) / 100),'22222222')
                            print(subtotal,'3333333= subtotal')
                            print(tax,'444444 = tax')

                    except IndexError:
                        tax = (float(0 * int(item['quantity']) ) / 100) * subtotal
                        print(tax,'IndexError==tax===>222')


                # subtotal = 0
                # shipping = 0
                # tax  = 0
                
                # for i in all_data:
                    # subtotal = float(subtotal) + float(i.total_amount)* int(i.quantity)
                    # print(i.total_amount,'Menu Item amount 111',i.menu_items.name)
                    
                    # try:
                    #     if i.menu_items.select_default_tax_rate[0]['price']:
                    #         tax = (float(i.menu_items.select_default_tax_rate[0]['price']* int(i.quantity) ) / 100) * subtotal
                    # except IndexError:
                    #     tax = (float(0 * int(i.quantity) ) / 100) * subtotal
                
                
                # print('Total = ',≈(subtotal), '+', float(shipping),'+',float(tax))
                final_total = float(subtotal) + float(shipping) + float(tax)
                discount_amount = 0
                promo_code_offer_percent = 0
                final_total_after_dic = 0
                if 'promo_code' in request.query_params:
                    print("Please select")
                    promo_code = request.query_params.get('promo_code')
                    target = ['Registered User','ALL']
                    print(promo_code,target , "====>")
                    
                    offer_data = Offers.objects.get(promo_code=promo_code)
                    promo_code_offer_percent = offer_data.promo_code_offer_percent
                    # Calculate the discount amount
                    discount_amount = (float(subtotal) + float(shipping) + float(tax)) * (float(offer_data.promo_code_offer_percent) / 100)
                    # Calculate the final total after applying the discount
                    final_total_after_dic = (float(subtotal) + float(shipping) + float(tax)) - discount_amount

                if final_total_after_dic == 0:
                    final_total_after_dic = final_total
                
                summary = {
                   'subtotal':round(subtotal, 2),
                   'shipping':shipping,
                   'taxes': round(tax, 2),
                   'total': round(final_total, 2) ,
                   'final_total':round(final_total_after_dic, 2) ,
                   'discount_percentage':promo_code_offer_percent,
                   'discount_amount':round(discount_amount, 2)
                }
                basket_count = CartItems.objects.filter(Q(customer_user_id=customer_user_id)).count()
                return Response({'result':{'status':'GET by Id','data':serialized_data,'basket_count':basket_count,'summary':summary,'reccomandations':unique_menu_items}})
            else:
                return Response({'result':{'status':'Basket is empty','data':[],'basket_count':0,'summary':{}}})
        else:
            all_data = CartItems.objects.all().values()
            for item in all_data:
                print(item['item_image'],'item_image====>')
                # item['item_image'] = get_updated_item_image_url(item['item_id'])  

            basket_count = CartItems.objects.filter(Q(customer_user_id=customer_user_id)).count()
            return Response({'result':{'status':'GET ALL','data':all_data,'basket_count':basket_count}})
            
    def post(self,request):
        # CheckAccess(request)
        data = request.data
        customer_user_id=data['customer_user_id']
        menu_items_id=data['menu_items_id']
        quantity=data['quantity']
        restaurent_id=data['restaurent_id']
        menu_items_add_on=data['menu_items_add_on']
        total_amount=data['total_amount']
        
        try:
            CartItems.objects.filter(Q(customer_user_id=customer_user_id) & ~Q(restaurent_id=restaurent_id) ).delete()
            
            
            if 'cart_id' in data:
                cart_id=data['cart_id']
                cart_data = CartItems.objects.get(Q(id=cart_id))
                country = CartItems.objects.filter(id=cart_data.id).update(
                    customer_user_id=customer_user_id,
                    menu_items_id=menu_items_id,
                    quantity   = quantity,  
                    restaurent_id=restaurent_id,
                    menu_items_add_on=menu_items_add_on,
                    total_amount=total_amount
                    )
                basket_count = CartItems.objects.filter(customer_user_id=customer_user_id).count()
                return Response({'result':{'status':'Updated','basket_count':basket_count,'code':2}})
        
            else:
                country = CartItems.objects.create(
                customer_user_id=customer_user_id,
                menu_items_id=menu_items_id,
                quantity   = quantity,  
                restaurent_id=restaurent_id,
                menu_items_add_on=menu_items_add_on,
                total_amount=total_amount
                )

                
                
                
            # else:
            #     country = CartItems.objects.create(
            #         customer_user_id=customer_user_id,
            #         menu_items_id=menu_items_id,
            #         quantity   = quantity,  
            #         restaurent_id=restaurent_id,
            #         menu_items_add_on=menu_items_add_on,
            #         total_amount=total_amount
            #         )

            basket_count = CartItems.objects.filter(customer_user_id=customer_user_id).count()
            return Response({'result':{'status':'Created','basket_count':basket_count,'code':1}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user_id=data['customer_user_id']
        menu_items_id=data['menu_items_id']
        quantity=data['quantity']

        try:
            country = CartItems.objects.filter(id=pk).update(
                    customer_user_id=customer_user_id,
                    menu_items_id=menu_items_id,
                    quantity   = quantity,  
                    )
    

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request):
        data = request.data
        customer_user_id = request.data.get('customer_user_id')
        menu_items_id = request.data.get('menu_items_id')

        test = (0,{})

        print(customer_user_id,menu_items_id,'menu_items_id======>')

        if CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(menu_items_id=menu_items_id)).exists():
            cart_data = CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(menu_items_id=menu_items_id)).delete()

            basket_count = CartItems.objects.filter(customer_user_id=customer_user_id).count()
            return Response({'result':{'status':'Deleted','basket_count':basket_count}})
        else:
            return Response({'result':{'status':'Item Not Found'}},status=status.HTTP_404_NOT_FOUND)



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





class UserPlaceOrdersView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        customer_user_id = request.query_params.get('customer_user_id')
        if customer_user_id:
            all_data = Orders.objects.filter(customer_user_id=customer_user_id).values()
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
       
    def post(self,request):
        data = request.data
        user_id=data['user_id']
        user_address=data['user_address']
        menu_items=data['menu_items']
        order_summary=data['order_summary']
        promo_code=data['promo_code']
        shipping_method=data['shipping_method']
        location_address=data['location_address']
        print(location_address,'location_address')
        try:
            country = Orders.objects.create(
                order_number = '#'+ str(random.randint(0, 100000)),
                customer_user_id = user_id,
                restaurent_id = location_address['id'],
                location_address = location_address,
                user_address = user_address,
                menu_items = menu_items,
                order_summary = order_summary,
                promo_code = promo_code,
                shipping_method = shipping_method,
                order_status="PREPARING FOOD"
                    )

            CartItems.objects.filter(Q(customer_user_id=user_id)).delete()
            return Response({'result':{'status':'Order created successfully'}})

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





class OrdersView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            orders_with_info = Orders.objects.filter(id=id)
            # if not all_data:
            #     return Response({
            #     'error':{'message':'Record not found!',
            #     'status_code':status.HTTP_404_NOT_FOUND,
            #     }},status=status.HTTP_404_NOT_FOUND)

            # return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            orders_with_info = Orders.objects.select_related('customer_user', 'restaurent').all()
            
        # Serialize the orders with related customer and restaurant information
        serialized_orders = []
        for order in orders_with_info:
            customer_address = order.customer_user.address
            print(customer_address,'customer_address===>')
            if customer_address:
                address_info = ", ".join([
                    customer_address.mobile_number,
                    customer_address.address_tag,
                    customer_address.flat,
                    customer_address.area,
                    customer_address.postal_code,
                    customer_address.city
                ])
            else:
                address_info=""
                order_data = {
                'order_id': order.id if hasattr(order, 'id') else None,
                'order_summary': order.order_summary if hasattr(order, 'order_summary') else None,
                'menu_items':order.menu_items,
                'promo_code': order.promo_code if hasattr(order, 'promo_code') else None,
                'shipping_method': order.shipping_method if hasattr(order, 'shipping_method') else None,
                'order_date': order.order_dt if hasattr(order, 'order_dt') else None,
                'total_amount': order.total_amount if hasattr(order, 'total_amount') else None,
                'order_status': order.order_status if hasattr(order, 'order_status') else None,
                'payment_method': order.payment_method if hasattr(order, 'payment_method') else None,
                'transaction_id': order.transaction_id if hasattr(order, 'transaction_id') else None,
                'delivery_method': order.devlivery_method if hasattr(order, 'devlivery_method') else None,
                'delivery_fee': order.delivery_fee if hasattr(order, 'delivery_fee') else None,
                'due_requested_delivery_time': order.requested_delivery_time if hasattr(order, 'requested_delivery_time') else None,
                'driver_rating': order.driver_rating if hasattr(order, 'driver_rating') else None,
                'restaurant_rating': order.restaurent_rating if hasattr(order, 'restaurent_rating') else None,
                'customer_name': order.customer_user.user_name if hasattr(order.customer_user, 'user_name') else None,
                'address_info': address_info if hasattr(address_info, 'address_info') else None,
                'city': order.customer_user.address.city if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'city') else None,
                'customer': {
                    'id': order.customer_user.id if hasattr(order.customer_user, 'id') else None,
                    'username': order.customer_user.user_name if hasattr(order.customer_user, 'user_name') else None,
                    'first_name': order.customer_user.f_name if hasattr(order.customer_user, 'f_name') else None,
                    'last_name': order.customer_user.l_name if hasattr(order.customer_user, 'l_name') else None,
                    'address': {
                        'id': order.customer_user.address.id if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'id') else None,
                        'first_name': order.customer_user.address.f_name if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'f_name') else None,
                        'last_name': order.customer_user.address.l_name if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'l_name') else None,
                        'address_tag': order.customer_user.address.address_tag if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'address_tag') else None,
                        'mobile_number': order.customer_user.address.mobile_number if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'mobile_number') else None,
                        'flat': order.customer_user.address.flat if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'flat') else None,
                        'area': order.customer_user.address.area if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'area') else None,
                        'postal_code': order.customer_user.address.postal_code if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'postal_code') else None,
                        'city': order.customer_user.address.city if hasattr(order.customer_user, 'address') and hasattr(order.customer_user.address, 'city') else None,
                    }
                },
                'restaurant': {
                    'id': order.restaurent.id if hasattr(order, 'restaurent') and hasattr(order.restaurent, 'id') else None,
                    'name': order.restaurent.published_name if hasattr(order, 'restaurent') and hasattr(order.restaurent, 'published_name') else None,
                    'branch': order.restaurent.branch if hasattr(order, 'restaurent') and hasattr(order.restaurent, 'branch') else None,
                    'mobile_number': order.restaurent.mobile_number if hasattr(order, 'restaurent') and hasattr(order.restaurent, 'mobile_number') else None,
                    'description': order.restaurent.description if hasattr(order, 'restaurent') and hasattr(order.restaurent, 'description') else None,
                    'r_c_timestamp':order.restaurent.r_c_timestamp,
                    'r_u_timestamp':order.restaurent.r_u_timestamp
                    

                }
            }
            serialized_orders.append(order_data)

        
        return Response({'result':{'status':'GET by Id','data':serialized_orders}})

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

from collections import Counter
from django.shortcuts import get_object_or_404

class TagApiView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            # Fetch the specific Tag object by ID
            tag = Tag.objects.get(id=id)

            # print(tag.id,'tag=====>')
            # Initialize a Counter to count tag occurrences
            # tag_counts = Counter()

            # Query MenuItems and get select_item_tag of all rows
            # menu_items = MenuItems.objects.all()

            # # Iterate over menu items
            # for menu_item in menu_items:
            #     # Get select_item_tag for the current menu item
            #     select_item_tag = menu_item.select_item_tag

            #     # If select_item_tag is not None, iterate over the tags and update counts
            #     if select_item_tag:
            #         for tag in select_item_tag:
            #             tag_counts[tag['id']] += 1

            # # Get the count for the specific tag_id
            # tag_count = tag_counts.get(id, 0)

            # Convert tag object to dictionary
            # # print(tag,'tag')
            # Construct the tag data dictionary
            # tag_data = {
            #     'id': tag['id'],
            #     'name': tag['name'],
            #     'photo': tag['photo'],  # Assuming photo is a field in your Tag model
            #     'tag_count': tag_count,
            #     'abbreviation':tag['abbreviation']
            # }
            tag_data = {
                'id': tag.id,
                'name': tag.name,
                # 'photo': tag.photo,  # Assuming photo is a field in your Tag model
                # 'tag_count': tag_count,
                'abbreviation':tag.abbreviation
            }

            # Optionally update the photo URL if present
            photo = tag.photo
            # print(photo,'photo======>')
            if photo:
                tag_data['photo'] = 'https://hunger.thestorywallcafe.com/media/' + str(photo)

            return Response({'result': {'status': 'GET by Id', 'data': tag_data}})

        else:
            # Query all tags
            all_data = Tag.objects.all().values()

            # Query MenuItems and get select_item_tag of all rows
            menu_items = MenuItems.objects.all()

            # Initialize a Counter to count tag occurrences
            tag_counts = Counter()

            # Iterate over menu items
            for menu_item in menu_items:
                # Get select_item_tag for the current menu item
                select_item_tag = menu_item.select_item_tag
                
                # If select_item_tag is not None, iterate over the tags and update counts
                if select_item_tag:
                    for tag in select_item_tag:
                        tag_counts[tag['id']] += 1

            # Update each item in all_data with count information
            for item in all_data:
                tag_id = item['id']
                count = tag_counts.get(tag_id, 0)  # Get the count for this tag_id, default to 0 if not found
                item['tag_count'] = count

                # Optionally update the photo URL if present
                photo = item['photo'] 
                if photo:
                    item['photo'] = 'https://hunger.thestorywallcafe.com/media/' + photo

            return Response({'result': {'status': 'GET by Id', 'data': all_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        name=data['name']
        abbreviation=data['abbreviation']

        try:
            tag = Tag.objects.create(
                name=name,
                abbreviation=abbreviation,
                    )
            if 'photo' in data:
                photo=data['photo']
                if photo.startswith('data:image'):
                    tag.photo = base64_to_image(photo)
                    tag.save()
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
        abbreviation=data['abbreviation']


        file_stored_path = '/media/'
        project_base_url = 'https://hunger.thestorywallcafe.com/'
        
        try:
            tag= Tag.objects.filter(id=pk).update( name=name,
                abbreviation=abbreviation
                   )
            if 'photo' in data:
                photo=data['photo']
                if photo.startswith('data:image'):
                    tag = Tag.objects.get(id=pk)
                    tag.photo = base64_to_image(photo)
                    tag.save()

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


class DefaultTaxRateApiView(APIView):
    def get(self,request):
        # CheckAccess(request)
    
        id = request.query_params.get('id')
        if id:
            # Query a single DefaultTaxRate by ID
            tag_instance = DefaultTaxRate.objects.get(id=id).values()
            return Response({'result': {'status': 'GET by Id', 'data': tag_instance}})

        else:
            # Query all DefaultTaxRate
            all_data = DefaultTaxRate.objects.all().values()
            return Response({'result':{'status':'GET ALL','data':all_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        name = data['name']

        try:
            tax = DefaultTaxRate.objects.create(name=name)
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
        abbreviation=data['abbreviation']


        file_stored_path = '/media/'
        project_base_url = 'https://hunger.thestorywallcafe.com/'
        
        try:
            tag= Tag.objects.filter(id=pk).update( name=name,
                abbreviation=abbreviation
                   )
            if 'photo' in data:
                photo=data['photo']
                if photo.startswith('data:image'):
                    tag = Tag.objects.get(id=pk)
                    tag.photo = base64_to_image(photo)
                    tag.save()

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


def get_today_date_and_day():
    # Get today's date
    today_date = datetime.today().date()
    
    # Get today's day (as a string)
    today_day = datetime.today().strftime('%A')
    
    return today_date, today_day

class CheckOffersView(APIView):
    def get(self,request):
        
        target = request.query_params.get('target')

        if target:
            all_data = Offers.objects.filter(select_target_audiance__contains={"name": target}).values()
            offer_count = Offers.objects.filter(select_target_audiance__contains={"name": target}).values().count()
            for item in all_data:
                item['banner_image'] = 'https://hunger.thestorywallcafe.com/media/' + item['banner_image']
            print(all_data,'all_data===>')
            return Response({'result': {'status': 'GET All target', 'data': all_data,'offer_count':offer_count}})
        else:
            all_data = Offers.objects.all().values()
            for item in all_data:
                item['banner_image'] = 'https://hunger.thestorywallcafe.com/media/' + item['banner_image']
            print(all_data,'all_data===>11111')
            return Response({'result': {'status': 'GET All', 'data': all_data}})
    

    def post(self,request):
        data = request.data
        target = data.get('target')
        offer_dict = {}  # Dictionary to store unique offer data by ID
        final_list = []

        if target:
            for offer_name in target:
                print(offer_name,'offer_name===>')
                offer_data = Offers.objects.filter(select_target_audiance__contains={"name": offer_name}).values()

                # Update offer_dict with new offer data, keeping only the latest data for each ID
                for offer in offer_data:
                    if 'banner_image' in offer and isinstance(offer['banner_image'], str) and offer['banner_image'].strip():
                        offer['banner_image'] = 'https://hunger.thestorywallcafe.com/media/' + offer['banner_image']
                    else:
                        offer['banner_image'] = None  

                    offer_id = offer['id']
                    print(offer['banner_image'],'banner_image=====>')

                    today_date, today_day = get_today_date_and_day()
                
                    if "Every " in offer['select_offer_duration'][0]['name']:
                        if offer['select_offer_duration'][0]['name'].split()[1] == today_day:
                            print('YES Today===>')
                            offer_dict[offer_id] = offer

                    if "Custom date range" in offer['select_offer_duration'][0]['name']:
                        print(offer['select_offer_duration'][0]['name'])
                        if offer['trigger_date']:
                            print(offer['trigger_date']['startDate'],'trigger_date==>startDate')
                            print(offer['trigger_date']['endDate'],'trigger_date==>endDate')
                            # Convert string dates to datetime objects
                            start_date = datetime.strptime(offer['trigger_date']['startDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                            end_date = datetime.strptime(offer['trigger_date']['endDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

                            # Get today's date
                            today = datetime.now().date()
                            print(start_date.date(),'\n',end_date.date(),'\n',today,'today===========>')
                            if start_date.date() <= today <= end_date.date():
                                print("111 Today falls within the range")
                                offer_dict[offer_id] = offer    
                            else:
                                print("222 Today does not fall within the range")
                       
                    
                    if offer['select_offer_duration'][0]['name'] == "Everyday":
                        offer_dict[offer_id] = offer

                    
            # Extract unique offer data from the dictionary
            final_list = list(offer_dict.values())

            return Response({
                'result': {
                    'status': 'GET All target',
                    'data': final_list,
                    'offer_count': len(final_list)
                }
            })
        else:
            all_data = Offers.objects.all().values()
            
            return Response({'result': {'status': 'GET All', 'data': all_data}})
    


class OffersView(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            all_data = Offers.objects.filter(id=id).values()
            for data in all_data:
                if data['banner_image']:
                    data['banner_image_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['banner_image'])
        else:
            all_data = Offers.objects.all().values()
            for data in all_data:
                if data['banner_image']:
                    data['banner_image_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['banner_image'])
        return Response({'result': {'status': 'GET All', 'data': all_data}})
    
    def post(self,request):
        # CheckAccess(request)
        
        data = request.data
        offer_duration = data['offer_duration']
        offer_heading = data['offer_heading']
        promo_code = data['promo_code']
        promo_code_offer_percent = data['promo_code_offer_percent']
        promo_code_offer_price = data['promo_code_offer_price']
        select_offer_duration = data['select_offer_duration']
        select_target_audiance = data['select_target_audiance']
        target_audiance = data['target_audiance']
        trigger_date = data['trigger_date']
        
        
        
    
    
        offer_item_data = {
            'offer_duration':offer_duration,
            'offer_heading':offer_heading,
            'promo_code':promo_code,
            'promo_code_offer_percent':promo_code_offer_percent,
            'promo_code_offer_price':promo_code_offer_price,
            'select_offer_duration':select_offer_duration,
            'select_target_audiance':select_target_audiance,
            'trigger_date':trigger_date,
            }
        
        offer_obj = Offers.objects.create(**offer_item_data)

        if 'banner_image' in data:
            banner_image = data['banner_image']
            if banner_image.startswith('data:image'):
                offer_obj.banner_image = base64_to_image(banner_image)
                offer_obj.save()

        return Response({'result':{'status':'Created'}})


    def put(self,request,pk):
        
        data = request.data
        offer_duration = data['offer_duration']
        offer_heading = data['offer_heading']
        promo_code = data['promo_code']
        promo_code_offer_percent = data['promo_code_offer_percent']
        # promo_code_offer_price = data['promo_code_offer_price']
        select_offer_duration = data['select_offer_duration']
        select_target_audiance = data['select_target_audiance']
        target_audiance = data['target_audiance']
        trigger_date = data['trigger_date']
    
        offer_item_data = {
            'offer_duration':offer_duration,
            'offer_heading':offer_heading,
            'promo_code':promo_code,
            'promo_code_offer_percent':promo_code_offer_percent,
            # 'promo_code_offer_price':promo_code_offer_price,
            'select_offer_duration':select_offer_duration,
            'select_target_audiance':select_target_audiance,
            'trigger_date':trigger_date,
            }
        
        offer_obj = Offers.objects.filter(Q(id=pk)).update(**offer_item_data)

        if 'banner_image' in data:
            banner_image = data['banner_image']
            if banner_image.startswith('data:image'):
                offer_obj1 = Offers.objects.get(Q(id=pk))
                offer_obj1.banner_image = base64_to_image(banner_image)
                offer_obj1.save()

        return Response({'result':{'status':'Created'}})



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




class OffersDurationView(APIView):
    def get(self,request):
        # id = request.query_params.get('id')
        all_data = OffersDuration.objects.all().values()

        return Response({'result': {'status': 'GET All', 'data': all_data}})

class TargetUserView(APIView):
    def get(self,request):
        # id = request.query_params.get('id')
        all_data = TargetUser.objects.all().values()

        return Response({'result': {'status': 'GET All', 'data': all_data}})
    



class UserItemReact(APIView):
    serializer_class = CartItemsSerializer
    def get(self,request):
        # CheckAccess(request)
    
        menu_items_id = request.query_params.get('menu_items_id')
        cuser_id = request.query_params.get('cuser_id')
        if Reaction.objects.filter(cuser_id=cuser_id).exists():
            react_data = Reaction.objects.filter(cuser_id=cuser_id).values()
            return Response({'result':{'status':'GET User Reaction','data':react_data}})
        else:
            return Response({
            'error':{'message':'This user does not put any raction yet',
            'status_code':status.HTTP_404_NOT_FOUND,
            }},status=status.HTTP_404_NOT_FOUND)

        
            
    # def post(self,request):
    #     # CheckAccess(request)
    #     data = request.data
        
    #     menu_items_id=data['menu_items_id']
    #     reaction=data['reaction']
    #     menu_object = MenuItems.objects.get(id=menu_items_id)
    #     if 'cuser_id' in data:
    #         cuser_id = data['cuser_id']
    #         react_dic = {}
    #         react_dic['cuser_id']  = cuser_id
    #         react_dic['menu_items_id']  = menu_items_id
    #         if reaction == 'loveit':
    #             react_dic['loveit']  = True
    #         if reaction == 'likeit':
    #             react_dic['likeit']  = True
    #         if reaction == 'dislikeit':
    #             react_dic['dislikeit']  = True
    #         if reaction == 'saveit':
    #             saveit_date = data['saveit_date']
    #             react_dic['saveit']  = True
    #             react_dic['saveit_date']  = saveit_date

    #         if Reaction.objects.filter(cuser_id=cuser_id).exists():
    #             Reaction.objects.filter(id=menu_items_id).update(**react_dic)
    #             return Response({'result':{'status':'Reaction Added successfully','method':'PUT'}})

    #         else:
    #             Reaction.objects.create(**react_dic)
    #             return Response({'result':{'status':'Reaction Added successfully','method':'POST'}})

    #     return Response({
    #         'error':{'message':'Please Register/login to like the items',
    #         'status_code':status.HTTP_400_BAD_REQUEST,
    #         }},status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        data = request.data
        
        menu_items_id = data['menu_items_id']
        reaction = data['reaction']
        menu_object = get_object_or_404(MenuItems, id=menu_items_id)
        
        if 'cuser_id' in data:
            cuser_id = data['cuser_id']
            react_dic = {
                'cuser_id': cuser_id,
                'menu_items_id': menu_items_id
            }
            
            existing_reaction = Reaction.objects.filter(cuser_id=cuser_id, menu_items_id=menu_items_id).first()
        if 'email_id' in data:
            email_id = data['email_id']
            if CustomUser.objects.filter(email_id=email_id).exists():
                cuser_data = CustomUser.objects.get(email_id=email_id)
            else:
                create_super_user = User.objects.create_user(username=email_id,email=email_id,password=email_id)
                cuser_data = CustomUser.objects.create(email_id=email_id,password=email_id)

            react_dic = {
                'cuser_id': cuser_data.id,
                'menu_items_id': menu_items_id
            }
            
            existing_reaction = Reaction.objects.filter(cuser_id=cuser_data.id, menu_items_id=menu_items_id).first()

        if existing_reaction:
            # If the user has already reacted, toggle the reaction flag
            if reaction == 'loveit':
                existing_reaction.loveit = not existing_reaction.loveit
            elif reaction == 'likeit':
                existing_reaction.likeit = not existing_reaction.likeit
            elif reaction == 'dislikeit':
                existing_reaction.dislikeit = not existing_reaction.dislikeit
            elif reaction == 'saveit':
                print("IN saveIT")
                existing_reaction.saveit = not existing_reaction.saveit
                if 'saveit_date' in data:
                    print(data['saveit_date'],'saveit_date')
                    existing_reaction.saveit_date = data['saveit_date']
                else:
                    existing_reaction.saveit_date = None
            existing_reaction.save()
            return Response({'result': {'status': 'Reaction updated successfully', 'method': 'PUT'}})
        else:
            # If the user has not reacted yet, create a new reaction entry
            if reaction == 'loveit':
                react_dic['loveit'] = True
            elif reaction == 'likeit':
                react_dic['likeit'] = True
            elif reaction == 'dislikeit':
                react_dic['dislikeit'] = True
            elif reaction == 'saveit':
                react_dic['saveit'] = True
                if 'saveit_date' in data:
                    react_dic['saveit_date'] = data['saveit_date']
            Reaction.objects.create(**react_dic)
            return Response({'result': {'status': 'Reaction added successfully', 'method': 'POST'}})

        return Response({
            'error': {
                'message': 'Please Register/login to like the items',
                'status_code': status.HTTP_400_BAD_REQUEST,
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        customer_user_id=data['customer_user_id']
        menu_items_id=data['menu_items_id']
        quantity=data['quantity']

        try:
            country = CartItems.objects.filter(id=pk).update(
                    customer_user_id=customer_user_id,
                    menu_items_id=menu_items_id,
                    quantity   = quantity,  
                    )
    

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})


    def delete(self,request):
        data = request.data
        customer_user_id = request.data.get('customer_user_id')
        menu_items_id = request.data.get('menu_items_id')

        test = (0,{})

        print(customer_user_id,menu_items_id,'menu_items_id======>')

        if CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(menu_items_id=menu_items_id)).exists():
            cart_data = CartItems.objects.filter(Q(customer_user_id=customer_user_id) & Q(menu_items_id=menu_items_id)).delete()

            basket_count = CartItems.objects.filter(customer_user_id=customer_user_id).count()
            return Response({'result':{'status':'Deleted','basket_count':basket_count}})
        else:
            return Response({'result':{'status':'Item Not Found'}},status=status.HTTP_404_NOT_FOUND)



class SubmitForm(APIView):
    # serializer_class = CartItemsSerializer
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            react_data = FormData.objects.filter(id=id).order_by('-id').values()
            for data in react_data:
                if data['resume']:
                    data['resume_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['resume'])
                if data['cover_letter']:
                    data['cover_letter_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['cover_letter'])
                if data['fsc_certificate']:
                    data['fsc_certificate_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['fsc_certificate'])
            return Response({'result': {'status': 'GET Id Submit Form', 'data': react_data}})
        else:
            react_data = FormData.objects.all().order_by('-id').values()
            for data in react_data:
                if data['resume']:
                    data['resume_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['resume'])
                if data['cover_letter']:
                    data['cover_letter_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['cover_letter'])
                if data['fsc_certificate']:
                    data['fsc_certificate_path'] = 'https://hunger.thestorywallcafe.com/media/' + str(data['fsc_certificate'])
            return Response({'result': {'status': 'GET All Submit Form', 'data': react_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
       

        feedboack_opt = data['feedboack_opt']
        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        email_id = data['email_id']
        message = data['message']
        # resume = data['resume']

        try:
            form_data_obj = FormData.objects.create(
                feedboack_opt = feedboack_opt,
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number,
                email_id = email_id,
                message = message,
                    )
            print("OutSide IF cover_letter")
            if 'cover_letter' in data:
                print("Inside IF cover_letter")
                
                cover_letter=data['cover_letter']
                if cover_letter:
                    if cover_letter.startswith('data:application'):
                        form_data_obj.cover_letter = base64_to_image(cover_letter)
                        print(base64_to_image(cover_letter),'form_data_obj==>')
                        form_data_obj.save()
            
            if 'resume' in data:
                print("Inside IF resume")
                resume=data['resume']
                if resume:
                    # if resume.startswith('data:application'):
                    form_data_obj.resume = base64_to_image(resume)
                    print(base64_to_image(resume),'form_data_obj==>')
                    form_data_obj.save()
            
            if 'fsc_certificate' in data:
                print("Inside IF resume")
                fsc_certificate=data['fsc_certificate']
                if fsc_certificate:
                    # if fsc_certificate.startswith('data:application'):
                    form_data_obj.fsc_certificate = base64_to_image(fsc_certificate)
                    print(base64_to_image(fsc_certificate),'form_data_obj==>')
                    form_data_obj.save()

            if 'menu_item' in data:
                menu_item=data['menu_item']
                print(menu_item,'menu_item==>')
                if menu_item != '':
                    form_data_obj.menu_items_id = menu_item
                    form_data_obj.save()
            
            if 'fsc_opt' in data:
                fsc_opt=data['fsc_opt']
                print(menu_item,'menu_item==>')
                if fsc_opt != '':
                    form_data_obj.fsc_opt = fsc_opt
                    form_data_obj.save()

            return Response({'result':{'status':'Created'}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
    
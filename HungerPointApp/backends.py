
import jwt
from rest_framework import authentication, exceptions,status
from datetime import datetime,timedelta
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
import random
import re
from mimetypes import guess_extension
import http.client
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import Counter
from django.db.models import Q

# def StoreBase64ReturnPath(file_base64, file_stored_path, project_base_url):

#     media_url = project_base_url + 'media' + file_stored_path.split('/media')[1]
#     print(media_url,'media_url')
#     # split_base
#     split_base_url_data = file_base64.split(';base64,')[1]
#     imgdata1 = base64.b64decode(split_base_url_data)

#     # guess_extension
#     guess_extension_data = file_base64.split(';')[0].split('/')[1]

#     # file_extention
#     rand = random.randint(0, 1000)

#     print(str(guess_extension_data), '===guess_extension_data===')
#     file_path = str(file_stored_path)+str(rand)+'.'+str(guess_extension_data)
#     file_extention = str(rand)+'.'+str(guess_extension_data)

#     # stored_file_object
#     stored_file_object = open(file_path, 'wb')
#     stored_file_object.write(imgdata1)
#     stored_file_object.close()

#     # return file_path_url
#     file_path_url = str(media_url)+str(file_extention)

#     return file_path_url

import os
import string
from django.core.files.base import ContentFile
from uuid import uuid4
import magic

def base64_to_image(base64_string):
    # Decode the base64 string
    decoded_data = base64.b64decode(base64_string)
    
    # Use the 'magic' library to determine the file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(decoded_data)
    
    # Create a unique name for the file
    filename = f"{uuid4().hex}.{file_type.split('/')[-1]}"
    
    # Create a ContentFile with the decoded data
    return ContentFile(decoded_data, name=filename)

# def base64_to_image(base64_string):
#     format, imgstr = base64_string.split(';base64,')
#     ext = format.split('/')[-1]
#     return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)

    
def store_base64_return_path(file_base64, file_stored_path, project_base_url):
    # Construct the media URL
    media_url = project_base_url + 'media' + file_stored_path.split('/media')[1]
    
    # Split the base64 data and decode it
    split_base_url_data = file_base64.split(';base64,')[1]
    imgdata = base64.b64decode(split_base_url_data)

    # Guess the file extension
    guess_extension_data = file_base64.split(';')[0].split('/')[1]

    # Generate a random filename
    rand = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    file_path = 'https://hunger.thestorywallcafe.com'+os.path.join(file_stored_path, f"{rand}.{guess_extension_data}")

    # Write the decoded data to the file
    with open(file_path, 'wb') as stored_file_object:
        stored_file_object.write(imgdata)

    # Construct the full file path URL
    file_path_url = f"{media_url}/{rand}.{guess_extension_data}"
    
    return file_path_url


def HungerPointAppPagination(data,request):

    # ----------- CheckPaginationParams

    pagination = request.query_params.get('pagination')
    if pagination == 'FALSE':
        return Response({'result':{'status':'GET all without pagination','data':data}})
    
    elif pagination == 'TRUE':
        page_number = request.query_params.get('page_number')
        data_per_page = request.query_params.get('data_per_page')
        all_keys = {'page_number','data_per_page','pagination'}

        if all_keys <= request.query_params.keys():
            missing_list = []
            for i in request.query_params:
                if (request.query_params[i] == None) | (request.query_params[i] == '') :
                    missing_list.append({ i : request.query_params[i]})          
                else:
                    print('===inside_else')                
            
            if len(missing_list) >= 1:
                print('===inside_missing_list')
                return Response({
                    'error':{'message':'Key value missing!',
                    'missing_key_value':missing_list,
                    'status_code':status.HTTP_404_NOT_FOUND,
                    }},status=status.HTTP_404_NOT_FOUND)
            
        else:
            missing_keys = all_keys - request.query_params.keys()
            return Response({
                        'error':{'message':'Key missing!',
                        'missing_key':missing_keys,
                        'status_code':status.HTTP_404_NOT_FOUND,
                        }},status=status.HTTP_404_NOT_FOUND)
        
        
        # -----------


        base_url = request.build_absolute_uri('?page_number')

        paginator = Paginator(data, data_per_page)
        page = paginator.page(page_number)
    
        if page.has_next():
            next_page = int(page_number) + 1
            next_url = str(base_url) + '=' + str(next_page) +'&data_per_page='+str(data_per_page)+'&pagination=TRUE'
        else:
            next_url = None

        if page.has_previous():
            previous_page = int(page_number) - 1
            previous_url = str(base_url) + '=' + str(previous_page) +'&data_per_page='+str(data_per_page)+'&pagination=TRUE'
        else:
            previous_url = None
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        pagination_data = {
            'current_page':page.number,
            'number_of_pages':paginator.num_pages,
            'next_url':next_url,
            'previous_url':previous_url,
            'has_next':page.has_next(),
            'has_previous':page.has_previous(),
            'has_other_pages':page.has_other_pages(),
            'data_count':len(data)
        }
        
        return Response({'result':{
            'status':'GET_ALL_DATA',
            'pagination':pagination_data,
            'data':list(page_obj)
                }})

    else:
        return Response({
                        'error':{'message':'Key value missing!',
                        'missing_key_value':{'pagination':pagination},
                        'status_code':status.HTTP_404_NOT_FOUND,
                        }},status=status.HTTP_404_NOT_FOUND)
        
# Check Pagination Params 

def CheckPaginationParams(request):
    print(request.query_params,'request.query_params==>CheckPaginationParams')

    page_number = request.query_params.get('page_number')
    data_per_page = request.query_params.get('data_per_page')
    if (page_number == None) | (page_number == '') | (data_per_page ==None ) | (data_per_page == '') :
        return Response({
            'error':{'message':'page_number or data_per_page parameter missing!',
            'status_code':status.HTTP_404_NOT_FOUND,
            }},status=status.HTTP_404_NOT_FOUND)



def get_all_menu_data(menu_id, tag_id, id):
    all_menu = Menu.objects.filter(id=menu_id)
    all_menu_data = []

    for menu_loop in all_menu:
        menu = Menu.objects.get(id=menu_loop.id)
        
        item_counter = Counter()
        item_info_list = [] 
        
        if tag_id and int(tag_id) != 0:
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

        for menu_item in menu_items:
            for selected_menu in menu_item.selected_menu_list:
                item_counter[selected_menu['id']] += 1

            item_info = {
                'id': menu_item.id,
                'name': menu_item.name,
                'amount': menu_item.amount,
                'item_count': sum(item_counter.values()),
                'item_image': 'https://hunger.thestorywallcafe.com/media/' + str(menu_item.item_image),
            }
            item_info_list.append(item_info)

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

        if item_info_list:
            main_dic = {
                'id': menu_loop.id,
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
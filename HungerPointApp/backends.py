
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

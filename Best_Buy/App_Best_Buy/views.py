import requests
from django.contrib.auth.models import User
from django.shortcuts import render
import random
import re
import string
# import requests
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from rest_framework.utils import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status, viewsets, mixins, generics, response

# Generate Jwt-Token
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
class Best_Buy(viewsets.ViewSet):#User class
    @action(detail=False,methods=['get'])
    def All_Best_Buy(self, request):
        data=request.GET['cat']



# http://127.0.0.1:8000/bb/bestbuy/All_Best_Buy/
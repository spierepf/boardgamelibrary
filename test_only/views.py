import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    return JsonResponse({})


@csrf_exempt
def reset(request):
    User.objects.all().delete()
    return JsonResponse({})


@csrf_exempt
def create_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User.objects.create_user(username=body['username'], password=body['password'])
    return JsonResponse({'username': user.username})

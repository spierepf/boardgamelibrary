import json

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view

from library.models import Title


def is_admin(user):
    if user.groups.filter(name='ADMIN').exists():
        return True
    raise PermissionDenied


def is_committee(user):
    if user.groups.filter(name='COMMITTEE').exists():
        return True
    raise PermissionDenied


# Create your views here.

def index(request):
    return JsonResponse({})


@api_view(['GET'])
@user_passes_test(is_admin)
def admin_only(request):
    return JsonResponse({})


@api_view(['GET'])
@user_passes_test(is_committee)
def committee_only(request):
    return JsonResponse({})


def reset(request):
    User.objects.all().delete()
    Title.objects.all().delete()
    return JsonResponse({})


@csrf_exempt
def create_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    group_names = body['groups']

    user = User.objects.create_user(username=body['username'], password=body['password'])

    for group_name in group_names:
        group = Group.objects.get_or_create(name=group_name)[0]
        group.user_set.add(user)

    return JsonResponse({'id': user.id, 'username': user.username, 'groups': [g.name for g in user.groups.all()]})

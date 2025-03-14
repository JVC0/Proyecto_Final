from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from .forms import CreateUserForm
# Create your views here.
def auth(request):
    username, password = json.loads(request.body).values()
    print(password)
    if user := authenticate(username=username, password=password):
        return JsonResponse({'token': user.token.key})
    return JsonResponse({'error': 'Invalid credentials'}, status=401)
def user_profile(request):
    pass
def edit_profile(request):
    pass
def delete_profile(request):
    pass
def profile_groups(request):
    pass
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)
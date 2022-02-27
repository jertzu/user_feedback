from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core import serializers
from django.forms import modelform_factory
from django.middleware import csrf
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from .serializers import FeedbackSerializer, UserSerializer
from .forms import FeedbackForm, SignUpForm
from .models import Feedback

import json

def user_list(request):
    authentication_classes = []

    users = User.objects.all()
    return render(request, "user_feedback/user_list.html", {"users": users})

def user_detail(request, username):
    authentication_classes = []

    user = User.objects.get(username=username)

    feedbacks = Feedback.objects.filter(owner=user)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "Please login to leave feedback.")
            return HttpResponseRedirect(".")

        form = FeedbackForm(request.POST)

        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.owner = user
            new_feedback.author = request.user
            new_feedback.save()

            return redirect("user_detail", username=username)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = FeedbackForm()

    return render(request, "user_feedback/user_detail.html", {"user": user, "feedbacks": feedbacks, "form": form})

def signup(request):
    authentication_classes = []

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("user_list")
    else:
        form = SignUpForm()

    return render(request, "user_feedback/signup.html", {"form": form})

class FeedbackViewSet(viewsets.ModelViewSet):
    authentication_classes = []

    queryset = Feedback.objects.all().order_by('owner')
    serializer_class = FeedbackSerializer
    http_method_names = ['get']

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

@api_view(['GET'])
def get_user_feedbacks(request, pk):
    user = User.objects.get(pk=pk)
    queryset = Feedback.objects.filter(owner=user)
    serialize = FeedbackSerializer(queryset, many=True)

    return Response(serialize.data)

@api_view(['POST'])
def new_feedback(request):
    if request.user.is_authenticated:
        feedback = Feedback()
        feedback.body = request.data["body"]
        feedback.author = User.objects.get(pk=request.user.id)
        feedback.owner = User.objects.get(pk=request.data["owner"])

        if feedback.clean:
            feedback.save()
            return Response("Feedback added succesfully.")

    return Response("Feedback could not be added.")

@api_view(['POST'])
def user_login(request):
    authentication_classes = []

    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(f"Succesfully logged in user {user.username}.")
    else:
        return Response("Could not log in.")

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response("Logged out succesfully.")

@api_view(['POST'])
def user_signup(request):
    authentication_classes = []

    form = SignUpForm(request.data)

    if form.is_valid():
        user = form.save()

        login(request, user)

        return Response(f"User {user.username} created succesfully. You have been logged in.")

    return Response("User could not be created.")

@api_view(['POST'])
def delete_user(request):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=request.data["id"])

            user.delete()
            return Response("User deleted succesfully.")
        except User.DoesNotExist:
            return Response("User does not exist.")

        return Response("User could not be destroyed.")
    return Response("You need to be an admin to delete users.")

from django.shortcuts import render
from rest_framework import decorators, response

from api.models import User
from api.serializers import *

import jwt
import bcrypt


@decorators.api_view(["GET"])
def allUsers(request):
    authHeader = request.META.get("HTTP_AUTHORIZATION")
    token = authHeader.split(" ")[1]

    if token != "admin-secret-token":
        return response.Response({"error": "Authorization failed"}, status=401)

    users = User.objects.all()
    serializedUsers = UserSerializer(users, many=True)
    return response.Response(serializedUsers.data, status=200)


@decorators.api_view(["POST"])
def register(request):
    serializedUser = UserSerializer(data=request.data)
    if serializedUser.is_valid():
        serializedUser.save()
        token = jwt.encode(
            {"email": request.data["email"]}, "secret", algorithm="HS256"
        )
        return response.Response({"token": token}, status=201)

    return response.Response(serializedUser.errors, status=400)


@decorators.api_view(["POST"])
def login(request):
    email = request.data["email"]
    password = request.data["password"]

    if email == "" or password == "":
        return response.Response(
            {"error": "Email and password are required"}, status=400
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return response.Response({"error": "User not found"}, status=404)

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        return response.Response({"error": "Email or password incorrect"}, status=400)

    token = jwt.encode({"email": email}, "secret", algorithm="HS256")

    return response.Response({"token": token}, status=200)


@decorators.api_view(["GET"])
def getUser(request):
    authHeader = request.META.get("HTTP_AUTHORIZATION")
    token = authHeader.split(" ")[1]

    decoded = jwt.decode(token, "secret", algorithms=["HS256"])
    email = decoded["email"]

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return response.Response({"error": "User not found"}, status=404)

    if user is None:
        return response.Response({"error": "User not found"}, status=404)

    serializedUser = PublicUserSerializer(user)
    return response.Response(serializedUser.data, status=200)


@decorators.api_view(["PUT"])
def updateUser(request):
    authHeader = request.META.get("HTTP_AUTHORIZATION")
    token = authHeader.split(" ")[1]

    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.DecodeError:
        return response.Response({"error": "Invalid token"}, status=400)

    email = decoded["email"].lower()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return response.Response({"error": "User not found"}, status=404)

    serializedUser = UpdateUserSerializer(user, data=request.data)
    if serializedUser.is_valid():
        print(serializedUser.validated_data)
        User.objects.filter(email=email).update(**serializedUser.validated_data)
        return response.Response(status=200)

    return response.Response(serializedUser.errors, status=400)


@decorators.api_view(["DELETE"])
def deleteUser(request):
    authHeader = request.META.get("HTTP_AUTHORIZATION")
    token = authHeader.split(" ")[1]

    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.DecodeError:
        return response.Response({"error": "Invalid token"}, status=400)

    email = decoded["email"].lower()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return response.Response({"error": "User not found"}, status=404)

    user.delete()
    return response.Response(status=204)

import random

from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import UserSerializer, VerifyCodeTokenObtainPairSerializer


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin' or request.user.is_superuser


class UserSignupView(APIView):
    def post(self, request):
        exception_data = {}
        if "email" not in request.data:
            exception_data['email'] = ['Не указан']
        if "username" not in request.data:
            exception_data['username'] = ['Не указано']
        if exception_data:
            return Response(
                exception_data,
                status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            verify_code = ''.join(
                [str(random.randint(0, 10)) for _ in range(30)]
            )
            data = {
                'email': request.data['email'],
                'username': request.data['username']
            }
            user: User = User.objects.get_or_create(
                **data
            )[0]
            user.email_user(
                subject="Verification code",
                message=verify_code
            )
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(password=verify_code)
            return Response(request.data)


class VerifyCodeTokenObtainPairView(TokenObtainPairView):
    serializer_class = VerifyCodeTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        exception_data = {}
        if 'username' not in request.data:
            exception_data['username'] = ['Не указано']
        if 'confirmation_code' not in request.data:
            exception_data['confirmation_code'] = ['Не указан']
        elif not request.data['confirmation_code'].isdigit():
            exception_data['confirmation_code'] = [
                'Должен состоять только из цифр']
        if exception_data:
            return Response(
                exception_data,
                status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=request.data['username'])
        if request.data['confirmation_code'] != user.password:
            return Response(
                {'confirmation_code': ['Не верный']},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = VerifyCodeTokenObtainPairSerializer.get_token(user)

        return Response(
            data={'refresh': str(refresh), 'access': str(refresh.access_token)}
        )


class UsersView(APIView, PageNumberPagination):
    permission_classes = (IsAdmin,)

    def post(self, request):
        exception_data = {}
        if "email" not in request.data:
            exception_data['email'] = ['Не указан']
        if "username" not in request.data:
            exception_data['username'] = ['Не указано']
        if exception_data:
            return Response(
                exception_data,
                status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        users = User.objects.get_queryset().order_by('username')
        result = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class UsernameView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SelfUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        data = request.data.dict()
        if 'role' in data:
            print(data)
            if user.role == 'moderator' and data['role'] == 'admin':
                data['role'] = 'moderator'
            elif user.role == 'user':
                data['role'] = 'user'
        print(data)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from . import serializers
from .email import send_otp_via_mail
from . import models
# Create your views here.
class UserRegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = serializers.UserRegisterserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_otp_via_mail(serializer.data['email'])
            return Response({
                    'status': 200,
                    'message': 'registration successfully check mail',
                    'data': serializer.data,
                })
        return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors,
            })        

# class UserRegisterView(generics.CreateAPIView):
#     serializer_class = serializers.UserRegister
class OtpVerificationView(APIView):
    def post(self, request):
        data = request.data
        serializer = serializers.OtpVerificationSerializer(data=data) 

        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = models.User.objects.filter(email=email)
            if not user.exists():
                return Response({
                        "status": 400,
                        "message": "something went wrong",
                        "data": "wrong email"
                        })
            if user[0].otp != otp:
                return Response({
                    "status": 400,
                    "message": "something went wrong",
                    "data": "wrong otp"
                })   
            user = user.first()
            user.is_verified = True
            user.save()

            return Response({
                'status': 200,
                'message': 'account verified',
                'data': {},
            })

        return Response({
            'status': 400,
            'message': 'something went wrong',
            'data': serializer.errors,
        })    

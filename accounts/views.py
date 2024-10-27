from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class SignUpView(generics.GenericAPIView):
    serializer_class=SignUpSerializer
    permission_classes=[]
    
    @swagger_auto_schema(
        operation_summary="Sign up a user",
        operation_description="Signs up a user"
    )
    
    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                "message":"User Created Successfully",
                "data":serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes=[]
    
    @swagger_auto_schema(
        operation_summary="generate jwt pair & Login a user",
        operation_description="Logs in a user"
    )
    
    def post(self, request:Request):
        email=request.data.get("email")
        password=request.data.get("password")
        
        user=authenticate(email=email, password=password)
        if user is not None:
            
            tokens=create_jwt_pair_for_user(user)
            response={
                "message":"Login Successful",
                "tokens":tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"Invalid email or password"})
        
    @swagger_auto_schema(
        operation_summary="get request info",
        operation_description="Refreshes jwt pair"
    )
    
    def get(self, request:Request):
        content={
            "user":str(request.user),
            "auth":str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)
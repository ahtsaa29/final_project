from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from user_rl.renderers import UserRenderer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from userdetails.serializers import CompanySerializer, PayrollSerializer,IssueSerializer, IssueTypeSerializer, DesignationSerializer, ApplicationSerializer
# Create your views here.

# class CompanyViewSet(viewsets.ModelViewSet):
class CompanyView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        serializer = CompanySerializer(data =request.company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PayrollView (APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = PayrollSerializer(data =request.payroll)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = ApplicationSerializer(data =request.application)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IssueView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = IssueSerializer(data =request.issue)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IssueTypeView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        serializer = IssueTypeSerializer(data =request.issuetype)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DesignationView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        serializer = DesignationSerializer(data =request.designation)
        return Response(serializer.data, status=status.HTTP_200_OK)
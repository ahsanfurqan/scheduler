from django.shortcuts import render

# Create your views here.
from rest_framework import generics,status
from .models import CustomUser, Patient, Counsellor
from .serializers import PatientSerializer, CounsellorSerializer,CustomUserSerializer,PatientUpdateSerializer,CounsellorUpdateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class PatientListCreateView(generics.ListAPIView):
    queryset = Patient.objects.filter(user__is_active=True)
    serializer_class = PatientSerializer

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientUpdateSerializer

    def get_queryset(self):
        return Patient.objects.filter(user__is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.user.save()


class CounsellorListCreateView(generics.ListAPIView):
    queryset = Counsellor.objects.filter(user__is_active=True)
    serializer_class = CounsellorSerializer


class CounsellorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CounsellorUpdateSerializer

    def get_queryset(self):
        return Counsellor.objects.filter(user__is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.user.save()

class ActivePatientListView(generics.ListAPIView):
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerializer

class ActiveCounsellorListView(generics.ListAPIView):
    queryset = Counsellor.objects.filter(is_active=True)
    serializer_class = CounsellorSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
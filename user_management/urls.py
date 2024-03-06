from django.urls import path
from .views import PatientListCreateView,PatientDetailView,CounsellorListCreateView,CounsellorDetailView,UserRegistrationView

app_name = 'user_management'

urlpatterns = [
    path('v1/patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('v1/patients/<int:pk>/', PatientDetailView.as_view(), name='patient-retrieve-update-delete'),
    path('v1/counsellors/', CounsellorListCreateView.as_view(), name='counsellor-list-create'),
    path('v1/counsellors/<int:pk>/', CounsellorDetailView.as_view(), name='counsellor-retrieve-update-delete'),
    path('v1/register/', UserRegistrationView.as_view(), name='user-registration'),
]

from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_management.urls', namespace='user_management')),
    path('api/', include('appointments.urls', namespace='appointments')),

]

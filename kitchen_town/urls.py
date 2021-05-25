from django.urls import path, include

urlpatterns = [
    path('', include('kitchen_app.urls')),
]
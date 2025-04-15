from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('courses/', include('courses.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('appointments/', include('appointments.urls')),
    path('contacts/', include('contacts.urls')),
    path('blog/', include('blog.urls')),
]

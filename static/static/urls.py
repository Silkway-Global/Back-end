from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="LabbayHizmatda Swagger Documentation",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),    
    
    # apps  
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('appointments/', include('appointments.urls')),
    path('contacts/', include('contacts.urls')),
    path('blog/', include('blog.urls')),

    # swagger
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]



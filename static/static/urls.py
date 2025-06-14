from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Silkway Global",
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
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('courses.urls')),
    path('api/v1/', include('testimonials.urls')),
    path('api/v1/', include('appointments.urls')),
    path('api/v1/', include('contacts.urls')),
    path('api/v1/', include('blog.urls')),
    path('api/v1/', include('stats.urls')),
    # swagger
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]



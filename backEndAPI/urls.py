from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
        
    path('api/v3/auth/', include('userAuth.urls')),
    path('api/v3/dropdowns/', include('dropdowns.urls')),
    path('api/v3/sql/', include('users.urls')),
    path('api/v3/registro/', include('users.urls')),
    path('api/v3/logros/', include('logros.urls')),
    path('api/v3/correo/',include('correos.urls'))
] 

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve ,{
        'document_root' : settings.MEDIA_ROOT
    })
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from finance_manager.views import error_400, error_403, error_404, error_405, error_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finance_manager.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler405 = error_405
handler500 = error_500

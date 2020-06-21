

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from customer.views import CustomerViewSet, DocumentsViewSet, DataSheetViewSet, ProfessionViewSet
from rest_framework.authtoken.views import obtain_auth_token
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Customers', CustomerViewSet, basename='customer')
router.register(r'Documents', DocumentsViewSet)
router.register(r'DataSheet', DataSheetViewSet)
router.register(r'Profession', ProfessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

    path(r'^api-token-auth/', obtain_auth_token),
    path(r'^api-auth/', include('rest_framework.urls')),
]

# path('', include('rest_framework.urls')),
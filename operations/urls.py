from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DailyDisbursementViewSet, 
    DailySettlementViewSet, 
    active_radar_api, 
    api_login, 
    api_my_dashboard, 
    api_submit_application
)

# Your existing router for the admin dashboards
router = DefaultRouter()
router.register(r'disbursements', DailyDisbursementViewSet)
router.register(r'settlements', DailySettlementViewSet)

urlpatterns = [
    # The standard ViewSets
    path('api/', include(router.urls)),
    
    # Your Custom Application APIs
    path('api/radar/', active_radar_api, name='active-radar'),
    path('api/login/', api_login, name='api-login'),
    path('api/my-dashboard/', api_my_dashboard, name='api-my-dashboard'),
    
    # THE MISSING LINK: The Application Form Route
    path('api/apply/', api_submit_application, name='api-apply'),
]
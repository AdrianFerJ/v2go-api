from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from main import views as main_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'main'

router = DefaultRouter()
router.register('stations', main_views.ChargingStationViewSet, base_name='stations')
router.register('vehicles', main_views.ElectricVehicleViewSet, base_name='vehicles')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('sign-up', main_views.SignUpView.as_view(), name='sign_up'),
    path('login', main_views.LogInView.as_view(), name='log_in'),
    path('logout', main_views.LogOutView.as_view(), name='log_out'),
    path('my-account/<user_id>', main_views.DriverProfileView.as_view(), name='my_account'),
]

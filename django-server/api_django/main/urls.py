from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationViewSet, EVViewSet, \
                       SignUpView, LogInView, LogOutView
from rest_framework.routers import DefaultRouter


app_name = 'main'

router = DefaultRouter()
router.register('stations', ChargingStationViewSet, base_name='stations')
router.register('vehicles', EVViewSet, base_name='vehicles')


urlpatterns = [
    path('', include(router.urls)),
    path('sign-up', SignUpView.as_view(), name='sign_up'),
    path('login', LogInView.as_view(), name='log_in'),
    path('logout', LogOutView.as_view(), name='log_out'),
]

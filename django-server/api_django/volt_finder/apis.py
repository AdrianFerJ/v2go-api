from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm 

from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, ChargingStationSerializer
from .models import ChargingStation


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(views.APIView):
    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user=form.get_user())
            return Response(UserSerializer(user).data)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, *args, **kwargs):
        logout(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChargingStationListView(viewsets.ReadOnlyModelViewSet):
    """ Basic CharginStation view, returns a list of CS near user
    #TODO: This view should return an array of CS near the user's POI
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


class ChargingStationDetailView(viewsets.ReadOnlyModelViewSet):  
    lookup_field = 'nk'
    lookup_url_kwarg = 'cStation_nk'
    permission_classes = (permissions.IsAuthenticated,)
    # TODO:  FIX QUERY ... READ THIS https://docs.djangoproject.com/en/2.1/topics/db/queries/
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


#   if len(results) > 5:
#         top_marks = results[:5]
#     else:
#         top_marks = results
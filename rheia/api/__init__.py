from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets

from rheia.models import time
from rheia.models import categories

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class TimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = time.LoggedTime
        fields = (
            'url',
            'duration',
            'owner',
            'client',
            'product',
            'activity',
            'first_created',
            'start_date',
            'start_time',
        )


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = categories.Client
        fields = (
            'name', 'first_created'
        )


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = categories.Product
        fields = (
            'name', 'first_created'
        )


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = categories.Activity
        fields = (
            'name', 'first_created'
        )


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ViewSets define the view behavior.
class TimeViewSet(viewsets.ModelViewSet):
    queryset = time.LoggedTime.objects.all()
    serializer_class = TimeSerializer


class ClientViewset(viewsets.ModelViewSet):
    queryset = categories.Client.objects.all()
    serializer_class = ClientSerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = categories.Product.objects.all()
    serializer_class = ProductSerializer


class ActivityViewset(viewsets.ModelViewSet):
    queryset = categories.Activity.objects.all()
    serializer_class = ActivitySerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'time', TimeViewSet)
router.register(r'clients', ClientViewset)
router.register(r'products', ProductViewset)
router.register(r'activities', ActivityViewset)

__all__ = ("router",)


from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from account.views import LoginView, UserViewSet,register

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),

]

urlpatterns += router.urls
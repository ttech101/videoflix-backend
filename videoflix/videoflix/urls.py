
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from account.views import LoginView, UserProfileView, UserViewSet, activate, change_email_and_username, change_password, change_password_acc, check_token, delete_current_user,register, reset_password
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', register, name='register'),
    path('check_token/', check_token, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('reset_password/', reset_password, name='register'),
    path('change_password/', change_password, name='change_password'),
    path('delete_current_user/', delete_current_user, name='delete_user'),
    path('account_change_mail/', change_email_and_username, name='change_mail'),
    path('change_password_acc/', change_password_acc, name='change_password_acc'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += router.urls

from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework import routers
from account.views import LoginView, Watchlist, UserProfileView, UserViewSet, activate, change_email_and_username, change_password, change_password_acc, check_token, delete_current_user,register, reset_password
from django.conf.urls.static import static
from storage.views import CheckWatchlist, DeleteMovie, MovieView, PreviewSerializer, CreateMovie, ShowMedia, UploadMovie
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'preview', PreviewSerializer)
router.register(r'movies', MovieView)
router.register(r'checkwachlist', CheckWatchlist)


def redirect_to_login(request):
    return redirect(reverse_lazy('login'))

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
    path('create_movie/', CreateMovie.as_view(), name='create_movie'),
    path('upload_movie/', UploadMovie.as_view(), name='upload_movie'),
    path('watchlist/', Watchlist.as_view(), name='update-watchlist'),
    path('delete_movie/', DeleteMovie.as_view(), name='delete_movie'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('django-rq/', include('django_rq.urls')),
    #path('media/<path:path>', ShowMedia),
    path('media/<path:path>', login_required(serve), {'document_root': settings.MEDIA_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls


from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework import routers
from account.views import LoginView, Watchlist, UserProfileView, UserViewSet, activate, change_email_and_username, change_password, change_password_acc, check_token, delete_current_user, get_sessionid, my_view,register, reset_password, serve_protected_media
from django.conf.urls.static import static
from storage.views import CheckWatchlist, DeleteMovie, MovieView, PreviewSerializer, CreateMovie, UploadMovie
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.urls import re_path



router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'preview', PreviewSerializer)
router.register(r'movies', MovieView)
router.register(r'checkwachlist', CheckWatchlist)


def redirect_to_login(request):
    return redirect(reverse_lazy('https://videoflix.tech-mail.eu/login'))

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('loginnew/', my_view, name='loginnew'),
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
    path('get_sessionid/', get_sessionid, name='get_sessionid'),
    path('media/<path:path>', login_required(serve, login_url=reverse_lazy('redirect_to_login')), {'document_root': settings.MEDIA_ROOT}),
    #re_path(r'^media/(?P<path>.*)$', serve_protected_media),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls



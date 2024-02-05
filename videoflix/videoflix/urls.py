
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from account.views import LoginView, Watchlist, UserProfileView, UserViewSet, activate, change_email_and_username, change_password, change_password_acc, check_token, delete_current_user,register, reset_password
from django.conf.urls.static import static
from storage.views import CheckWatchlist, DeleteMovie, MovieView, PreviewSerializer, CreateMovie, UploadMovie
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

<<<<<<< HEAD
=======
def redirect_to_frontend(request):
    return redirect('https://videoflix.tech-mail.eu/')
def is_authenticated_user(user):
    return user.is_authenticated

>>>>>>> 4b2e27574c54bcdc00b3edc3e9573875dba86b1c
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'preview', PreviewSerializer)
router.register(r'movies', MovieView)
router.register(r'checkwachlist', CheckWatchlist)

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
<<<<<<< HEAD
    path('media/<path:path>', login_required(serve, login_url='https://videoflix.tech-mail.eu/'), {'document_root': settings.MEDIA_ROOT}),
] + staticfiles_urlpatterns()

# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
=======
    path('media/<path:path>', user_passes_test(is_authenticated_user)(serve),{'document_root': settings.MEDIA_ROOT},name='protected_media'),
   # path('media/<path:path>', login_required(serve, login_url='https://videoflix.tech-mail.eu/'), {'document_root': settings.MEDIA_ROOT}),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
>>>>>>> 4b2e27574c54bcdc00b3edc3e9573875dba86b1c

urlpatterns += router.urls

from django.shortcuts import redirect

class MediaAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, 'user', None) and not request.user.is_authenticated and request.path.startswith('/media/'):
            # Benutzer ist nicht authentifiziert und versucht auf MEDIA_ROOT zuzugreifen
            return redirect('login')  # Du kannst dies an deine Login-Seite anpassen

        response = self.get_response(request)
        return response
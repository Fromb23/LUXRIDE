from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class PreventBackMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add headers to prevent browser caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Frame-Options'] = 'DENY'
        # response['Content-Security-Policy'] = (
        #     "default-src 'self'; "
        #     "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        #     "font-src https://fonts.gstatic.com; "
        #     "img-src 'self' data: https://via.placeholder.com; "
        #     "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com;"
        # )

        return response

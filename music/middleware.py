
from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from datetime import datetime, time, timedelta


class MyCustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:

            #  later on it is done with celery
            if 'Auser_limit' in request.session:
                now = datetime.now().time()
                print(now)
                midnight = time(0, 0)
                print(midnight)
                if now <= midnight:
                    del request.session['Auser_limit']
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            user_limit_data = request.session.get('Auser_limit', 0)
            if view_func.__name__ == 'listen_music':
                if user_limit_data > 10:
                    messages.warning(
                        request, 'you have reached limit for today, please login')
                    return redirect('users:login')
                else:
                    if view_func.__name__ == 'listen_music':
                        user_limit_data += 1
                        request.session['Auser_limit'] = user_limit_data

    # def process_exception(self, request, exception):
    #     print("an error raised", exception)
    #     return render(request, 'music/error.html')

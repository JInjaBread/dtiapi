from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        if user.is_authenticated:
            if user.is_superuser == True:
                if modulename == "dtiApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("dashboard")
            else:
                return redirect("home")
        else:
                if request.path == reverse("home") or request.path == reverse("doLogin"):
                    pass
                else:
                    return redirect("home")

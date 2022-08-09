import json
import os
from datetime import datetime
from uuid import uuid4

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import login, views as auth_views, logout
from django.template.defaulttags import register
from keitaro.keitaro_api import Keitaro


@register.filter
def get_item(dictionary, index):
    return list(dictionary)[index]


@csrf_exempt
@require_POST
def create_user(request) -> HttpResponse:
    if not request.body:
        return HttpResponse("Where your json body?", status=400)
    body = json.loads(request.body)
    if set(body.keys()) != {"login", "key"}:
        return HttpResponse("Your json request must contain a key and a login", status=400)
    if body["key"] == "":
        return HttpResponse("I'm waiting your key...", status=400)
    if body["key"] != os.getenv("API_KEY"):
        return HttpResponse("Invalid key", status=403)
    user_body = {
        "username": body["login"],
        "password": uuid4().hex
    }
    model = User.objects.create_user(**user_body)
    return JsonResponse({"error": False, "user": user_body}) \
        if model else JsonResponse({"error": True})


class LoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


@require_GET
def home(request) -> render:
    report = Keitaro().report(
        from_=datetime.strptime(request.GET.get('from'), '%Y-%m-%d'),
        to=datetime.strptime(request.GET.get('to'), '%Y-%m-%d'),

        grouping=["sub_id_6"],
        metrics=["clicks", "conversions"],
    ) if request.user.is_authenticated else None
    return render(request, "app/home.html", {"report": report})


def handler404(request, exception=None) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse("login"))

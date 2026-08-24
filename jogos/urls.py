from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("quiz/", views.quiz, name="quiz"),
    path("ranking/", views.ranking, name="ranking"),
    path("qrcode/", views.qrcode_view, name="qrcode"),
    path("sair/", views.sair, name="sair"),
    path(
    "quem-e-esse-bebe/",
    views.bebe,
    name="bebe"
),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("quiz/", views.quiz, name="quiz"),
    path("ranking/", views.ranking, name="ranking"),
    path("qrcode/", views.qrcode_view, name="qrcode"),
    path("sair/", views.sair, name="sair"),
    path("quebra-cabeca/",views.quebra_cabeca,name="quebra_cabeca"),
path("quebra-cabeca/finalizar/",views.finalizar_quebra_cabeca, name="finalizar_quebra_cabeca"),
]

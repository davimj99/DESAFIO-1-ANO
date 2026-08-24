from django.contrib import admin
from .models import Convidado, Pergunta, Resposta


@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "pontos", "criado_em")
    search_fields = ("nome",)
    ordering = ("-pontos", "criado_em")


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ("ordem", "texto", "correta", "pontos", "ativa")
    list_filter = ("ativa", "correta")
    search_fields = ("texto",)
    ordering = ("ordem", "id")


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ("convidado", "pergunta", "alternativa", "correta", "respondida_em")
    list_filter = ("correta",)
    search_fields = ("convidado__nome", "pergunta__texto")

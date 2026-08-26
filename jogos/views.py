from io import BytesIO

import qrcode
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Convidado, Pergunta, Resposta


def inicio(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()

        if len(nome) < 2:
            messages.error(request, "Digite seu nome.")
            return redirect("inicio")

        convidado = Convidado.objects.create(nome=nome[:100])
        request.session["convidado_id"] = convidado.id
        return redirect("quiz")

    return render(request, "inicio.html")


def quiz(request):
    convidado_id = request.session.get("convidado_id")

    if not convidado_id:
        return redirect("inicio")

    convidado = Convidado.objects.get(id=convidado_id)

    perguntas = list(
        Pergunta.objects.filter(ativa=True)
    )

    respondidas = set(
        Resposta.objects
        .filter(convidado=convidado)
        .values_list("pergunta_id", flat=True)
    )

    pendentes = [
        p for p in perguntas
        if p.id not in respondidas
    ]


    # =====================================
    # RESPONDEU UMA PERGUNTA
    # =====================================

    if request.method == "POST":

        pergunta_id = request.POST.get("pergunta_id")
        alternativa = request.POST.get("alternativa")


        try:

            pergunta = Pergunta.objects.get(
                id=pergunta_id,
                ativa=True
            )

        except Pergunta.DoesNotExist:

            messages.error(
                request,
                "Pergunta inválida."
            )

            return redirect("quiz")


        # Evita responder duas vezes

        if Resposta.objects.filter(
            convidado=convidado,
            pergunta=pergunta
        ).exists():

            return redirect("quiz")


        acertou = (
            alternativa == pergunta.correta
        )


        # =====================================
        # SALVA A RESPOSTA
        # =====================================

        with transaction.atomic():

            Resposta.objects.create(

                convidado=convidado,

                pergunta=pergunta,

                alternativa=alternativa,

                correta=acertou,

            )


            if acertou:

                convidado.pontos += pergunta.pontos

                convidado.save(
                    update_fields=["pontos"]
                )


        # =====================================
        # TELA DE RESULTADO
        # =====================================

        return render(
            request,
            "resultado.html",
            {
                "convidado": convidado,
                "pergunta": pergunta,
                "acertou": acertou,
                "alternativa": alternativa,
            },
        )


    # =====================================
    # TERMINOU TODAS AS PERGUNTAS
    # =====================================

    if not pendentes:

        return render(
            request,
            "final.html",
            {"convidado": convidado}
        )


    pergunta = pendentes[0]

    progresso = len(respondidas) + 1


    return render(
        request,
        "quiz.html",
        {
            "convidado": convidado,

            "pergunta": pergunta,

            "progresso": progresso,

            "total": len(perguntas),
        },
    )


def ranking(request):
    convidados = Convidado.objects.order_by("-pontos", "criado_em")
    return render(request, "ranking.html", {"convidados": convidados})


def qrcode_view(request):
    url = request.build_absolute_uri(reverse("inicio"))
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


def sair(request):
    request.session.flush()
    return redirect("inicio")

def quebra_cabeca(request):
    return render(
        request,
        "quebra_cabeca.html")

def finalizar_quebra_cabeca(request):

    if request.method != "POST":
        return redirect("quebra_cabeca")

    convidado_id = request.session.get("convidado_id")

    if not convidado_id:
        return redirect("inicio")

    convidado = Convidado.objects.get(
        id=convidado_id
    )

    pontos = int(
        request.POST.get("pontos", 0)
    )

    # Garante que o jogo não envie mais de 200 pontos
    pontos = max(0, min(pontos, 200))

    convidado.pontos += pontos

    convidado.save(
        update_fields=["pontos"]
    )

    return redirect("ranking")
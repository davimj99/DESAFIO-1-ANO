from django.db import models


class Convidado(models.Model):
    nome = models.CharField(max_length=100)
    pontos = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pontos", "criado_em"]

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    texto = models.CharField(max_length=255)
    alternativa_a = models.CharField(max_length=150)
    alternativa_b = models.CharField(max_length=150)
    alternativa_c = models.CharField(max_length=150)
    alternativa_d = models.CharField(max_length=150)
    correta = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
    )
    pontos = models.PositiveIntegerField(default=100)
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "id"]

    def __str__(self):
        return self.texto


class Resposta(models.Model):
    convidado = models.ForeignKey(Convidado, on_delete=models.CASCADE, related_name="respostas")
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    alternativa = models.CharField(max_length=1)
    correta = models.BooleanField(default=False)
    respondida_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["convidado", "pergunta"],
                name="uma_resposta_por_pergunta",
            )
        ]

    def __str__(self):
        return f"{self.convidado} - {self.pergunta}"

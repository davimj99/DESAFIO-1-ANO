from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Convidado",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100)),
                ("pontos", models.PositiveIntegerField(default=0)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-pontos", "criado_em"]},
        ),
        migrations.CreateModel(
            name="Pergunta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("texto", models.CharField(max_length=255)),
                ("alternativa_a", models.CharField(max_length=150)),
                ("alternativa_b", models.CharField(max_length=150)),
                ("alternativa_c", models.CharField(max_length=150)),
                ("alternativa_d", models.CharField(max_length=150)),
                ("correta", models.CharField(choices=[("A","A"),("B","B"),("C","C"),("D","D")], max_length=1)),
                ("pontos", models.PositiveIntegerField(default=100)),
                ("ativa", models.BooleanField(default=True)),
                ("ordem", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["ordem", "id"]},
        ),
        migrations.CreateModel(
            name="Resposta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("alternativa", models.CharField(max_length=1)),
                ("correta", models.BooleanField(default=False)),
                ("respondida_em", models.DateTimeField(auto_now_add=True)),
                ("convidado", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="respostas", to="jogos.convidado")),
                ("pergunta", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="jogos.pergunta")),
            ],
        ),
        migrations.AddConstraint(
            model_name="resposta",
            constraint=models.UniqueConstraint(fields=("convidado","pergunta"), name="uma_resposta_por_pergunta"),
        ),
    ]

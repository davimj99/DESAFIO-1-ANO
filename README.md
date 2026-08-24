# Desafio do 1º Ano

Sistema web para festa de 1 ano, com:
- cadastro simples do convidado;
- quiz;
- pontuação;
- ranking;
- painel administrativo do Django;
- QR Code da página inicial;
- layout responsivo para celular.

## Rodar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:
- Jogo: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Cadastrar perguntas

Entre no `/admin/`, crie perguntas em "Perguntas" e marque uma alternativa como correta.

## Publicar

O projeto está preparado para hospedagem com Gunicorn e PostgreSQL. Para uma festa, o ideal é colocar online e gerar o QR Code da URL pública.

Variáveis de ambiente opcionais:
- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `ALLOWED_HOSTS`

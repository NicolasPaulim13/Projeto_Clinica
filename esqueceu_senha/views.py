from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import random

def esqueceu_senha_view(request):
    if request.method == "POST":
        email = request.POST.get("email_paciente")

        # Gere um código de recuperação aleatório
        recovery_code = str(random.randint(100000, 999999))

        # Envie o e-mail com o código de recuperação
        try:
            send_mail(
                'Código de Recuperação de Senha',
                f'Seu código de recuperação de senha é: {recovery_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'O código de recuperação foi enviado para seu e-mail.')
            # Você pode salvar o código para posterior verificação
        except Exception as e:
            messages.error(request, 'Ocorreu um erro ao enviar o e-mail.')

        return redirect('esqueceu_senha')  # Redireciona para a mesma página ou para uma página de verificação

    return render(request, 'esqueceu_senha/esqueceu_senha.html')

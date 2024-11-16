from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now, timedelta
from .models import PasswordRecovery
from cadastro_registro.models import CadastroRegistro  # Importe o modelo correto

import random


def esqueceu_senha_view(request):
    if request.method == "POST":
        email = request.POST.get("email_paciente")

        # Verifique se o e-mail existe no banco de dados
        if not CadastroRegistro.objects.filter(email_paciente=email).exists():
            return render(request, 'esqueceu_senha/esqueceu_senha.html')  # Exibe a mesma página com a mensagem de erro

        # Gere um código de recuperação aleatório
        recovery_code = str(random.randint(100000, 999999))

        # Salve o código no banco de dados com expiração
        PasswordRecovery.objects.create(
            email=email,
            recovery_code=recovery_code,
            expires_at=now() + timedelta(minutes=10)  # Código válido por 10 minutos
        )

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
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao enviar o e-mail: {e}')
            return render(request, 'esqueceu_senha/esqueceu_senha.html')  # Retorne para a página em caso de erro

        return redirect('codigo_senha')  # Redireciona para a página de verificação do código

    return render(request, 'esqueceu_senha/esqueceu_senha.html')


def codigo_senha_view(request):
    if request.method == "POST":
        email = request.POST.get("email_paciente")
        codigo = request.POST.get("codigo")

        try:
            # Verifique o código no banco de dados
            recovery_entry = PasswordRecovery.objects.get(email=email, recovery_code=codigo)

            # Verifique se o código não expirou
            if recovery_entry.expires_at >= now():
                messages.success(request, "Código validado com sucesso! Você pode redefinir sua senha.")
                return redirect('redefinir_senha')  # Redireciona para a página de redefinição de senha
            else:
                messages.error(request, "Código expirado. Solicite um novo código.")

        except PasswordRecovery.DoesNotExist:
            messages.error(request, "Código inválido ou não encontrado. Tente novamente.")

    return render(request, 'esqueceu_senha/codigo_senha.html')


def redefinir_senha_view(request):
    if request.method == "POST":
        # Lógica para redefinir a senha
        redefinir_senha = request.POST.get("redefinir_senha")
        # Aqui você deve salvar a nova senha no banco de dados
        # Certifique-se de usar hashing para senhas (ex: `set_password`)

        return redirect('login')  # Redirecione para a página de login após redefinir a senha
    
    return render(request, 'esqueceu_senha/redefinir_senha.html')

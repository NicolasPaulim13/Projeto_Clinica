from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now, timedelta
from django.contrib.auth.hashers import make_password  # Para hash de senhas
from .models import PasswordRecovery
from cadastro_registro.models import CadastroRegistro  # Importe o modelo correto
import random


def esqueceu_senha_view(request):
    if request.method == "POST":
        email = request.POST.get("email_paciente")

        # Verifica se o e-mail existe no banco de dados
        if not CadastroRegistro.objects.filter(email_paciente=email).exists():
            messages.error(request, "E-mail não encontrado.")
            return render(request, 'esqueceu_senha/esqueceu_senha.html')

        # Gera um código de recuperação aleatório
        recovery_code = str(random.randint(100000, 999999))

        # Salva o código no banco de dados com expiração
        PasswordRecovery.objects.create(
            email=email,
            recovery_code=recovery_code,
            expires_at=now() + timedelta(minutes=10)  # Código válido por 10 minutos
        )

        # Envia o e-mail com o código de recuperação
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
            return render(request, 'esqueceu_senha/esqueceu_senha.html')

        # Armazena o e-mail na sessão para os próximos passos
        request.session['email_recuperacao'] = email

        return redirect('codigo_senha')  # Redireciona para a página de verificação do código

    return render(request, 'esqueceu_senha/esqueceu_senha.html')


def codigo_senha_view(request):
    if request.method == "POST":
        email = request.session.get('email_recuperacao')  # Obtém o e-mail da sessão
        codigo = request.POST.get("codigo")

        if not email:
            messages.error(request, "Sessão expirada. Solicite a recuperação novamente.")
            return redirect('esqueceu_senha')

        try:
            # Verifica o código no banco de dados
            recovery_entry = PasswordRecovery.objects.get(email=email, recovery_code=codigo)

            # Verifica se o código não expirou
            if recovery_entry.expires_at >= now():
                # Código validado com sucesso
                request.session['codigo_recuperacao'] = codigo  # Salva o código na sessão
                messages.success(request, "Código validado com sucesso! Você pode redefinir sua senha.")
                return redirect('redefinir_senha')
            else:
                messages.error(request, "Código expirado. Solicite um novo código.")

        except PasswordRecovery.DoesNotExist:
            messages.error(request, "Código inválido ou não encontrado. Tente novamente.")

    return render(request, 'esqueceu_senha/codigo_senha.html')


def redefinir_senha_view(request):
    if request.method == "POST":
        nova_senha = request.POST.get("nova_senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        # Validação básica para senhas
        if nova_senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return redirect('redefinir_senha')

        # Requisitos de segurança para a senha
        if (
            len(nova_senha) < 8 or
            not any(char.isupper() for char in nova_senha) or
            not any(char.islower() for char in nova_senha) or
            not any(char.isdigit() for char in nova_senha) or
            not any(char in "!@#$%^&*()-_" for char in nova_senha)
        ):
            messages.error(request, "A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.")
            return redirect('redefinir_senha')

        # Obtém informações da sessão
        email = request.session.get('email_recuperacao')
        codigo = request.session.get('codigo_recuperacao')

        if not email or not codigo:
            messages.error(request, "Sessão expirada. Solicite a recuperação novamente.")
            return redirect('esqueceu_senha')

        try:
            # Atualiza a senha no banco de dados
            paciente = CadastroRegistro.objects.get(email_paciente=email)
            paciente.senha_paciente = make_password(nova_senha)  # Gera o hash da senha
            paciente.save()

            # Remove o registro de recuperação
            PasswordRecovery.objects.filter(email=email, recovery_code=codigo).delete()

            # Limpa a sessão
            request.session.pop('email_recuperacao', None)
            request.session.pop('codigo_recuperacao', None)

            messages.success(request, "Senha redefinida com sucesso! Faça login com sua nova senha.")
            return redirect('login')

        except CadastroRegistro.DoesNotExist:
            messages.error(request, "Erro ao redefinir a senha. Usuário não encontrado.")
            return redirect('esqueceu_senha')

    return render(request, 'esqueceu_senha/redefinir_senha.html')

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from cadastro_registro.models import CadastroRegistro
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group

def login_page(request):
    if request.method == 'POST':
        email_paciente = request.POST.get('email_paciente', '').strip()
        senha_paciente = request.POST.get('senha_paciente', '').strip()

        if not email_paciente or not senha_paciente:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'cadastro/cadastro.html')

        try:
            cadastro = CadastroRegistro.objects.get(email_paciente=email_paciente)

            # Verifica se o usuário é paciente e a senha está correta
            if check_password(senha_paciente, cadastro.senha_paciente) and cadastro.user.groups.filter(name='paciente').exists():
                user = cadastro.user
                auth.login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Acesso restrito a pacientes ou senha incorreta.')
        except CadastroRegistro.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'cadastro/cadastro.html')


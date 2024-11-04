# cadastro_adm/views.py
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from cadastro_registro.models import CadastroRegistro
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group

def login_medico(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        if not email or not senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'cadastro_adm/cadastro_adm.html')

        try:
            cadastro = CadastroRegistro.objects.get(email_paciente=email)
            user = cadastro.user

            # Verifica se o usuário é médico e se a senha está correta
            if check_password(senha, cadastro.senha_paciente) and user.groups.filter(name='medico').exists():
                auth.login(request, user)
                return redirect('index')  # Redireciona para uma página específica após login
            else:
                messages.error(request, 'Acesso restrito a médicos ou senha incorreta.')
        except CadastroRegistro.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'cadastro_adm/cadastro_adm.html')


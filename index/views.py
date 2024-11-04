from django.shortcuts import render, redirect
from django.contrib.auth import logout

def index(request):
    # Lógica existente para renderizar a página inicial
    return render(request, 'index/index.html')

def logout_view(request):
    logout(request)  # Faz o logout do usuário
    return redirect('index')  # Redireciona para a página inicial após o logout

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastro_registro.models import CadastroRegistro
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastro_registro.models import CadastroRegistro
from django.contrib import messages

@login_required
def edit_profile(request):
    if request.method == 'POST':
        cadastro = request.user.cadastroregistro
        nome_paciente = request.POST.get('nome_paciente')
        imagem_fundo = request.FILES.get('imagem_fundo')
        imagem_perfil = request.FILES.get('imagem_perfil')

        if nome_paciente:
            cadastro.nome_paciente = nome_paciente

        if imagem_fundo:
            cadastro.imagem_fundo = imagem_fundo

        if imagem_perfil:
            cadastro.imagem_perfil = imagem_perfil

        cadastro.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('index')

    return render(request, 'edit_profile.html', {})

    
    
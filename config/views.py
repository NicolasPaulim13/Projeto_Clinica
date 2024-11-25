from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from cadastro_registro.models import CadastroRegistro
from .models import Perfil
from .forms import PerfilForm

@login_required
def config(request):
    try:
        # Recupera ou cria CadastroRegistro associado ao usuário logado
        cadastro, _ = CadastroRegistro.objects.get_or_create(
            user=request.user,
            defaults={
                'nome_paciente': request.user.username,
                'email_paciente': request.user.email,
                'cpf_paciente': '000.000.000-00',
                'data_nascimento_paciente': '2000-01-01',
                'sexo_paciente': 'O',
            }
        )

        # Recupera ou cria Perfil associado ao CadastroRegistro
        perfil, _ = Perfil.objects.get_or_create(
            config_user=request.user,
            cadastro_registro=cadastro,
            defaults={'imagem_perfil': None}
        )
    except Exception as e:
        messages.error(request, f"Erro ao carregar perfil: {e}")
        return redirect('home')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Identifica qual formulário foi enviado

        if form_type == 'editar_perfil':
            # Formulário de edição de perfil
            nome_paciente = request.POST.get('nome_paciente', cadastro.nome_paciente)
            imagem_perfil = request.FILES.get('imagem_perfil', None)

            cadastro.nome_paciente = nome_paciente
            cadastro.save()  # Salva o nome no CadastroRegistro

            if imagem_perfil:
                perfil.imagem_perfil = imagem_perfil
            perfil.save()  # Salva a imagem no Perfil

            messages.success(request, "Perfil atualizado com sucesso!")

        elif form_type == 'editar_informacoes':
            # Formulário de informações pessoais
            cadastro.email_paciente = request.POST.get('email_paciente', cadastro.email_paciente)
            cadastro.cpf_paciente = request.POST.get('cpf_paciente', cadastro.cpf_paciente)
            
            # Atualiza a data de nascimento
            data_nascimento_paciente = request.POST.get('data_nascimento_paciente', cadastro.data_nascimento_paciente)
            if data_nascimento_paciente:
                cadastro.data_nascimento_paciente = data_nascimento_paciente
            
            cadastro.sexo_paciente = request.POST.get('sexo_paciente', cadastro.sexo_paciente)
            cadastro.save()  # Salva alterações no CadastroRegistro

            messages.success(request, "Informações pessoais atualizadas com sucesso!")
        else:
            messages.error(request, "Formulário inválido enviado.")

        return redirect('config')

    # Inicialização dos formulários
    return render(request, 'config/config.html', {
        'perfil': perfil,
        'cadastro': cadastro,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil
from .forms import PerfilForm
from django.contrib import messages
from cadastro_registro.models import CadastroRegistro


@login_required
def config(request):
    try:
        perfil = Perfil.objects.get(config_user=request.user)
    except Perfil.DoesNotExist:
        cadastro_registro, created = CadastroRegistro.objects.get_or_create(user=request.user)
        if created:
            # Preencha os campos obrigatórios para evitar erros de integridade
            cadastro_registro.nome_paciente = "Nome padrão"
            cadastro_registro.email_paciente = "email@padrao.com"
            cadastro_registro.cpf_paciente = "00000000000"
            cadastro_registro.data_nascimento_paciente = "2000-01-01"
            cadastro_registro.sexo_paciente = "O"
            cadastro_registro.save()
        perfil = Perfil.objects.create(config_user=request.user, cadastro_registro=cadastro_registro)

    cadastro = perfil.cadastro_registro

    if request.method == 'POST':
        if 'submit_perfil' in request.POST:
            # Atualiza os dados do Perfil
            form = PerfilForm(request.POST, request.FILES, instance=perfil)
            if form.is_valid():
                form.save()
                messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            else:
                messages.error(request, 'Houve um erro ao salvar o perfil.')
        elif 'submit_info' in request.POST:
            # Atualiza os dados de CadastroRegistro
            email = request.POST.get('email_paciente')
            cpf = request.POST.get('cpf_paciente')
            sexo = request.POST.get('sexo_paciente')
            data_nascimento = request.POST.get('data_nascimento_paciente')

            # Validações de dados obrigatórios
            if not cpf:
                messages.error(request, 'O CPF é obrigatório.')
                return redirect('config')

            if not data_nascimento:
                messages.error(request, 'A data de nascimento é obrigatória.')
                return redirect('config')

            # Atualiza o objeto CadastroRegistro
            cadastro.email_paciente = email
            cadastro.cpf_paciente = cpf
            cadastro.sexo_paciente = sexo
            cadastro.data_nascimento_paciente = data_nascimento

            try:
                cadastro.save()
                messages.success(request, 'Suas informações pessoais foram atualizadas com sucesso!')
            except Exception as e:
                messages.error(request, f'Houve um erro ao salvar as informações: {e}')

        return redirect('config')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'config/config.html', {
        'form': form,
        'perfil': perfil,
        'cadastro': cadastro,
    })

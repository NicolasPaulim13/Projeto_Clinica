from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil
from .forms import PerfilForm
from django.contrib import messages
from cadastro_registro.models import CadastroRegistro


@login_required
def config(request):
    try:
        # Tenta buscar o perfil do usuário logado
        perfil = Perfil.objects.get(config_user=request.user)
    except Perfil.DoesNotExist:
        # Cria o CadastroRegistro padrão caso não exista
        cadastro_registro, created = CadastroRegistro.objects.get_or_create(user=request.user)
        if created:
            cadastro_registro.nome_paciente = "Nome padrão"
            cadastro_registro.email_paciente = "email@padrao.com"
            cadastro_registro.cpf_paciente = "000.000.000-00"
            cadastro_registro.data_nascimento_paciente = "2000-01-01"
            cadastro_registro.sexo_paciente = "O"
            cadastro_registro.save()
        # Cria o perfil vinculado ao CadastroRegistro
        perfil = Perfil.objects.create(config_user=request.user, cadastro_registro=cadastro_registro)

        if request.method == 'POST':
            form = PerfilForm(request.POST, request.FILES, instance=perfil)
            if form.is_valid():
                try:
                    # Salva os dados do formulário
                    form.save()
                    messages.success(request, "Perfil e informações pessoais atualizados com sucesso!")
                except Exception as e:
                    messages.error(request, f"Erro ao salvar o perfil: {e}")
            else:
                print("Erros do formulário:", form.errors)
                messages.error(request, "Erro ao atualizar o perfil.")
            return redirect('config')

        

        # Atualização manual de informações pessoais diretamente do request
        cadastro = perfil.cadastro_registro
        if cadastro:
            cadastro.email_paciente = request.POST.get('email_paciente', cadastro.email_paciente)
            cadastro.cpf_paciente = request.POST.get('cpf_paciente', cadastro.cpf_paciente)
            cadastro.sexo_paciente = request.POST.get('sexo_paciente', cadastro.sexo_paciente)
            cadastro.data_nascimento_paciente = request.POST.get('data_nascimento_paciente', cadastro.data_nascimento_paciente)
            try:
                cadastro.save()
                messages.success(request, "Informações pessoais atualizadas com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao salvar informações pessoais: {e}")

        return redirect('config')  # Redireciona para evitar resubmissão do formulário
    else:
        # Instancia o formulário com os dados existentes do perfil
        form = PerfilForm(instance=perfil)

    return render(request, 'config/config.html', {
        'form': form,
        'perfil': perfil,
        'cadastro': perfil.cadastro_registro,  # Passa as informações do CadastroRegistro para o template
    })

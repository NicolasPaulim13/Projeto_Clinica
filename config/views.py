from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cadastro_registro.models import CadastroRegistro
from .forms import PerfilForm
from django.contrib import messages

@login_required  # Certifique-se de que o usuário está autenticado
def config(request):
    try:
        perfil = CadastroRegistro.objects.get(user=request.user)
    except CadastroRegistro.DoesNotExist:
        perfil = CadastroRegistro(user=request.user)
        perfil.save()

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu nome foi atualizado com sucesso!')
            return redirect('config')  # Redireciona de volta para a página de configuração
        else:
            messages.error(request, 'Houve um erro ao salvar suas informações.')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'config/config.html', {'form': form})

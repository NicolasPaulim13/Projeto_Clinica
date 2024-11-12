from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil
from .forms import PerfilForm
from django.contrib import messages
from cadastro_registro.models import CadastroRegistro

# views.py
@login_required
def config(request):
    try:
        perfil = Perfil.objects.get(config_user=request.user)
    except Perfil.DoesNotExist:
        cadastro_registro, _ = CadastroRegistro.objects.get_or_create(user=request.user)
        perfil = Perfil.objects.create(config_user=request.user, cadastro_registro=cadastro_registro)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('config')
        else:
            messages.error(request, 'Houve um erro ao salvar suas informações.')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'config/config.html', {
        'form': form,
        'perfil': perfil  # Passa o perfil para o template
    })
    
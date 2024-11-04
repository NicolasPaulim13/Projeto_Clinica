# consulta/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group  # Importa o modelo Group
from .forms import ConsultaForm
from .models import Consulta
from cadastro_registro.models import CadastroRegistro  # Importe o modelo CadastroRegistro
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group  # Adicione esta linha



@login_required(login_url='login')
def agendar_consulta(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        paciente = CadastroRegistro.objects.get(user=request.user)
    except CadastroRegistro.DoesNotExist:
        return redirect('erro_paciente_nao_encontrado')  # Redireciona para uma view de erro

    # Obtém todos os médicos do grupo "medico"
    grupo_medico = Group.objects.get(name='medico')
    medicos = User.objects.filter(groups=grupo_medico)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente  
            consulta.nome = paciente.nome_paciente
            consulta.email = paciente.email_paciente  # Acesse o e-mail do modelo CadastroRegistro
            consulta.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    # Passa a lista de médicos para o template
    return render(request, 'consulta/consulta.html', {'form': form, 'medicos': medicos})

@login_required(login_url='login')
def listar_consultas(request):
    grupos_do_usuario = request.user.groups.values_list('name', flat=True)

    if 'administrador' in grupos_do_usuario:
        consultas = Consulta.objects.all()
    elif 'medico' in grupos_do_usuario:
        consultas = Consulta.objects.filter(medico=request.user)
    else:
        try:
            paciente = CadastroRegistro.objects.get(user=request.user)
            consultas = Consulta.objects.filter(paciente=paciente)
        except CadastroRegistro.DoesNotExist:
            return redirect('index')

    return render(request, 'consulta/consulta_list.html', {'consultas': consultas})

@login_required(login_url='login')
def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'consulta/consulta_edit.html', {'form': form, 'consulta': consulta})

@login_required(login_url='login')
def deletar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    # Verifique se a consulta pertence ao paciente atual
    try:
        paciente = CadastroRegistro.objects.get(user=request.user)
        if consulta.paciente != paciente:
            return HttpResponseForbidden("Você não tem permissão para excluir esta consulta.")
    except CadastroRegistro.DoesNotExist:
        return HttpResponseForbidden("Paciente não encontrado.")

    if request.method == 'POST':
        consulta.delete()  # Exclui apenas essa consulta específica
        return redirect('consulta_list')  # Redireciona para a lista de consultas após a exclusão

    return render(request, 'consulta/consulta_delete.html', {'consulta': consulta})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from .forms import ConsultaForm
from .models import Consulta
from cadastro_registro.models import CadastroRegistro

@login_required(login_url='login')
def agendar_consulta(request):
    # Verifica se o usuário está autenticado e obtém o paciente associado
    try:
        paciente = CadastroRegistro.objects.get(user=request.user)
    except CadastroRegistro.DoesNotExist:
        return redirect('erro_paciente_nao_encontrado')

    # Obtém todos os médicos do grupo "medico"
    try:
        grupo_medico = Group.objects.get(name='medico')
        medicos = User.objects.filter(groups=grupo_medico)
    except Group.DoesNotExist:
        medicos = []

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente  # Associa a consulta ao paciente logado
            consulta.nome = paciente.nome_paciente  # Preenche com o nome do paciente
            consulta.email = paciente.email_paciente  # Preenche com o email do paciente
            consulta.medico = form.cleaned_data.get('medico')  # Associa o médico selecionado
            consulta.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    return render(request, 'consulta/consulta.html', {'form': form, 'medicos': medicos})


@login_required(login_url='login')
def listar_consultas(request):
    # Obtém os grupos do usuário autenticado
    grupos_do_usuario = request.user.groups.values_list('name', flat=True)

    if 'administrador' in grupos_do_usuario:
        consultas = Consulta.objects.all()
    elif 'medico' in grupos_do_usuario:
        consultas = Consulta.objects.filter(medico=request.user)
    else:
        # Se o usuário é um paciente, exibe apenas suas consultas
        try:
            paciente = CadastroRegistro.objects.get(user=request.user)
            consultas = Consulta.objects.filter(paciente=paciente)
        except CadastroRegistro.DoesNotExist:
            return redirect('index')

    return render(request, 'consulta/consulta_list.html', {'consultas': consultas})


@login_required(login_url='login')
def editar_consulta(request, id):
    # Obtém a consulta pelo ID, verificando se existe
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
    # Obtém a consulta pelo ID e verifica se o paciente tem permissão para excluí-la
    consulta = get_object_or_404(Consulta, id=id)
    try:
        paciente = CadastroRegistro.objects.get(user=request.user)
        if consulta.paciente != paciente:
            return HttpResponseForbidden("Você não tem permissão para excluir esta consulta.")
    except CadastroRegistro.DoesNotExist:
        return HttpResponseForbidden("Paciente não encontrado.")

    if request.method == 'POST':
        consulta.delete()
        return redirect('consulta_list')

    return render(request, 'consulta/consulta_delete.html', {'consulta': consulta})

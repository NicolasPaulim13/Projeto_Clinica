from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from .forms import ConsultaForm
from .models import Consulta
from django.http import HttpResponse
from cadastro_registro.models import CadastroRegistro
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

@login_required(login_url='login')
def agendar_consulta(request):
    try:
        paciente = CadastroRegistro.objects.get(user=request.user)
    except CadastroRegistro.DoesNotExist:
        return redirect('erro_paciente_nao_encontrado')

    try:
        grupo_medico = Group.objects.get(name='medico')
        medicos = User.objects.filter(groups=grupo_medico)
    except Group.DoesNotExist:
        medicos = []

    print(f"Médicos encontrados: {[str(medico) for medico in medicos]}")  # Debug

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.nome = paciente.nome_paciente
            consulta.email = paciente.email_paciente
            consulta.medico = form.cleaned_data.get('medico')
            consulta.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    context = {
        'form': form,
        'medicos': medicos,
        'mensagem': "Nenhum médico disponível no momento." if not medicos else ""
    }
    return render(request, 'consulta/consulta.html', context)


@login_required(login_url='login')
def listar_consultas(request):
    # Obtém os grupos do usuário autenticado
    grupos_do_usuario = request.user.groups.values_list('name', flat=True)
    user_is_medico = 'medico' in grupos_do_usuario  # Verifica se o usuário é médico

    if 'administrador' in grupos_do_usuario:
        consultas = Consulta.objects.all()
    elif user_is_medico:
        consultas = Consulta.objects.filter(medico=request.user)
    else:
        # Se o usuário é um paciente, exibe apenas suas consultas
        try:
            paciente = CadastroRegistro.objects.get(user=request.user)
            consultas = Consulta.objects.filter(paciente=paciente)
        except CadastroRegistro.DoesNotExist:
            return redirect('index')

    return render(request, 'consulta/consulta_list.html', {
        'consultas': consultas,
        'user_is_medico': user_is_medico
    })


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


@login_required
def relatorio(request):
    return render(request, 'consulta/relatorio.html')


@login_required
def consulta_list(request):
    # Obtém as consultas relacionadas ao usuário
    grupos_do_usuario = request.user.groups.values_list('name', flat=True)
    user_is_medico = 'medico' in grupos_do_usuario  # Verifica se o usuário é médico

    if 'administrador' in grupos_do_usuario:
        consultas = Consulta.objects.all()
    elif user_is_medico:
        consultas = Consulta.objects.filter(medico=request.user)
    else:
        try:
            paciente = CadastroRegistro.objects.get(user=request.user)
            consultas = Consulta.objects.filter(paciente=paciente)
        except CadastroRegistro.DoesNotExist:
            consultas = []

    return render(request, 'consulta/consulta_list.html', {
        'consultas': consultas,
        'user_is_medico': user_is_medico,
    })

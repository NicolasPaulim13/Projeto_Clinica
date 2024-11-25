from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User, Group
from .models import Consulta
from .forms import ConsultaForm, ProntuarioCompletoForm
from cadastro_registro.models import CadastroRegistro
from .models import Prontuario




# Verifica se o usuário pertence ao grupo 'medico'
def is_medico(user):
    return user.groups.filter(name='medico').exists()

@login_required(login_url='login')
def agendar_consulta(request):
    try:
        paciente = CadastroRegistro.objects.get(user=request.user)
    except CadastroRegistro.DoesNotExist:
        return redirect('erro_paciente_nao_encontrado')

    grupo_medico = Group.objects.filter(name='medico').first()
    medicos = User.objects.filter(groups=grupo_medico) if grupo_medico else []

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.nome = paciente.nome_paciente
            consulta.email = paciente.email_paciente
            medico_id = request.POST.get('medico')
            if medico_id:
                try:
                    consulta.medico = User.objects.get(id=medico_id)
                except User.DoesNotExist:
                    consulta.medico = None
            consulta.save()
            return redirect('consulta_list')
    else:
        form = ConsultaForm()

    context = {
        'form': form,
        'medicos': medicos,
        'mensagem': "Nenhum médico disponível no momento." if not medicos else "",
    }
    return render(request, 'consulta/consulta.html', context)

@login_required(login_url='login')
def listar_consultas(request):
    user_grupos = request.user.groups.values_list('name', flat=True)

    if 'administrador' in user_grupos:
        consultas = Consulta.objects.all()
    elif 'medico' in user_grupos:
        consultas = Consulta.objects.filter(medico=request.user)
    elif 'paciente' in user_grupos:
        try:
            paciente = CadastroRegistro.objects.get(user=request.user)
            consultas = Consulta.objects.filter(paciente=paciente)
        except CadastroRegistro.DoesNotExist:
            consultas = []
    else:
        consultas = []

    return render(request, 'consulta/consulta_list.html', {
        'consultas': consultas,
        'user_is_medico': 'medico' in user_grupos,
        'user_is_paciente': 'paciente' in user_grupos,
    })

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

    horas_disponiveis = ['09:00', '10:00', '11:00', '14:00', '15:00']

    context = {
        'form': form,
        'consulta': consulta,
        'horas_disponiveis': horas_disponiveis,
    }
    return render(request, 'consulta/consulta_edit.html', context)

@login_required(login_url='login')
def deletar_consulta(request, id):
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

@login_required(login_url='login')
def relatorio(request):
    return render(request, 'consulta/relatorio.html')

@login_required
def prontuario(request, id):
    # Busca o prontuário relacionado ao ID fornecido
    prontuario = get_object_or_404(Prontuario, id=id)
    return render(request, 'consulta/prontuario.html', {'prontuario': prontuario})

@login_required(login_url='login')
@user_passes_test(is_medico)
def editar_prontuario_completo(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == 'POST':
        form = ProntuarioCompletoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('consulta_list')
    else:
        form = ProntuarioCompletoForm(instance=consulta)

    return render(request, 'consulta/prontuario_edit_completo.html', {'form': form, 'consulta': consulta})

@login_required
def consultas_realizadas(request):
    # Lista todas as consultas realizadas para o usuário atual
    consultas = Consulta.objects.filter(usuario=request.user)
    return render(request, 'consulta/consultas_realizadas.html', {'consultas': consultas})

@login_required(login_url='login')
@user_passes_test(is_medico)
def finalizar_consulta(request, pk):
    try:
        consulta = Consulta.objects.get(pk=pk, medico=request.user)
        consulta.exame_realizado = True
        consulta.save()
        return redirect('consultas_realizadas')
    except Consulta.DoesNotExist:
        return HttpResponseForbidden("Consulta não encontrada ou você não tem permissão.")

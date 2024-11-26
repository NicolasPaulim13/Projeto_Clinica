from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User, Group
from .models import Consulta
from .forms import ConsultaForm, ProntuarioCompletoForm
from cadastro_registro.models import CadastroRegistro
from django.contrib import messages
import re



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


@login_required
def consulta_list(request):
    if request.user.groups.filter(name='paciente').exists():
        consultas = Consulta.objects.filter(paciente__user=request.user)
        user_is_paciente = True
        user_is_medico = False
    elif request.user.groups.filter(name='medico').exists():
        consultas = Consulta.objects.filter(medico=request.user)
        user_is_paciente = False
        user_is_medico = True
    else:
        consultas = []
        user_is_paciente = False
        user_is_medico = False

    context = {
        'consultas': consultas,
        'user_is_paciente': user_is_paciente,
        'user_is_medico': user_is_medico,
    }
    return render(request, 'consulta/consulta_list.html', context)


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


@login_required
def relatorio(request):
    return render(request, 'consulta/relatorio.html')


@login_required
def prontuario(request, id):
    print("DEBUG: View prontuario chamada com id:", id)
    consulta = get_object_or_404(Consulta, id=id)
    print("DEBUG: Consulta carregada:", consulta)

    # Busca os dados do paciente associado
    cadastro_paciente = CadastroRegistro.objects.filter(id=consulta.paciente_id).first()

    # Preenche campos do prontuário automaticamente, caso estejam vazios
    if cadastro_paciente:
        consulta.nome_paciente = consulta.nome_paciente or cadastro_paciente.nome_paciente
        consulta.data_nascimento = consulta.data_nascimento or cadastro_paciente.data_nascimento_paciente
        consulta.genero = consulta.genero or cadastro_paciente.sexo_paciente
        consulta.endereco_contato = consulta.endereco_contato or cadastro_paciente.cidade_paciente or "Cidade não informada"
        consulta.documento_identificacao = (
            consulta.documento_identificacao or cadastro_paciente.cpf_paciente or "Documento não informado"
        )
        consulta.save()

    if request.method == 'POST':
        print("DEBUG: POST recebido:", request.POST)

        # Coleta dados do formulário
        cidade = request.POST.get('cidade', consulta.endereco_contato).strip()
        documento_identificacao = request.POST.get('documento_identificacao', consulta.documento_identificacao).strip()

        # Validações
        if len(cidade) < 3:
            messages.error(request, 'A cidade deve ter pelo menos 3 caracteres.')
            print("DEBUG: Cidade inválida:", cidade)
            return render(request, 'consulta/prontuario.html', {'prontuario': consulta, 'cadastro_paciente': cadastro_paciente})

        if not re.match(r'^\d{2}\.\d{3}\.\d{3}-\d{2}$', documento_identificacao):  # Exemplo para CPF
            messages.error(request, 'O documento de identificação não está no formato correto.')
            print("DEBUG: Documento inválido:", documento_identificacao)
            return render(request, 'consulta/prontuario.html', {'prontuario': consulta, 'cadastro_paciente': cadastro_paciente})

        # Atualiza os campos
        consulta.endereco_contato = cidade
        consulta.documento_identificacao = documento_identificacao
        consulta.condicoes_saude = request.POST.get('condicoes_saude', consulta.condicoes_saude)
        consulta.cirurgias_anteriores = request.POST.get('cirurgias_anteriores', consulta.cirurgias_anteriores)
        consulta.historico_tratamentos = request.POST.get('historico_tratamentos', consulta.historico_tratamentos)
        consulta.avaliacao_cavidade = request.POST.get('avaliacao_cavidade', consulta.avaliacao_cavidade)
        consulta.lesoes_anomalias = request.POST.get('lesoes_anomalias', consulta.lesoes_anomalias)
        consulta.queixas_principais = request.POST.get('queixas_principais', consulta.queixas_principais)
        consulta.diagnostico_detalhado = request.POST.get('diagnostico_detalhado', consulta.diagnostico_detalhado)
        consulta.procedimentos_planejados = request.POST.get('procedimentos_planejados', consulta.procedimentos_planejados)

        # Salvar consulta e verificar sucesso
        try:
            consulta.save()
            print("DEBUG: Consulta salva com sucesso:", consulta)
            messages.success(request, 'Prontuário atualizado com sucesso!')
            return redirect('consultas_realizadas', medico_id=request.user.id)
        except Exception as e:
            print("ERROR: Falha ao salvar consulta:", e)
            messages.error(request, 'Erro ao salvar os dados. Tente novamente.')

    context = {
        'prontuario': consulta,
        'cadastro_paciente': cadastro_paciente,
    }
    return render(request, 'consulta/prontuario.html', context)




@login_required(login_url='login')
@user_passes_test(is_medico)
def editar_prontuario_completo(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    # Verifica se está no contexto correto
    if not consulta.exame_realizado:
        messages.warning(request, 'Finalize a consulta antes de editar o prontuário completo.')
        return redirect('consulta_list')

    if request.method == 'POST':
        form = ProntuarioCompletoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            # Marca como "prontuário completo editado" (opcional)
            consulta.prontuario_completo_editado = True
            consulta.save()

            # Mensagem de sucesso
            messages.success(request, 'Prontuário completo editado com sucesso!')
            # Redireciona para consultas realizadas do médico
            return redirect('consultas_realizadas', medico_id=request.user.id)
        else:
            messages.error(request, 'Erro ao salvar o prontuário. Verifique os dados.')
    else:
        form = ProntuarioCompletoForm(instance=consulta)

    return render(request, 'consulta/prontuario_edit_completo.html', {'form': form, 'consulta': consulta})


@login_required
def consultas_realizadas(request, medico_id=None):
    if medico_id:
        # Filtrar apenas consultas realizadas pelo médico
        consultas = Consulta.objects.filter(medico_id=medico_id, exame_realizado=True)
    else:
        # Filtrar consultas realizadas pelo usuário atual (médico autenticado)
        consultas = Consulta.objects.filter(medico=request.user, exame_realizado=True)

    return render(request, 'consulta/consultas_realizadas.html', {'consultas': consultas})


@login_required(login_url='login')
@user_passes_test(is_medico)
def finalizar_consulta(request, pk):
    try:
        consulta = get_object_or_404(Consulta, pk=pk, medico=request.user)

        consulta.exame_realizado = True
        consulta.save()
        messages.success(request, f"A consulta com {consulta.nome_paciente} foi finalizada com sucesso!")
        return redirect('consultas_realizadas', medico_id=request.user.id)

    except Exception as e:
        messages.error(request, f"Erro ao finalizar a consulta: {str(e)}")
        return redirect('consultas_realizadas', medico_id=request.user.id)

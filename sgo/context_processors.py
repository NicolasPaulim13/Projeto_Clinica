from cadastro_registro.models import CadastroRegistro

def paciente_context(request):
    if request.user.is_authenticated:
        try:
            cadastro = CadastroRegistro.objects.get(user=request.user)
            nome = cadastro.nome_paciente.split()[0]  # Pega o primeiro nome do paciente
        except CadastroRegistro.DoesNotExist:
            nome = None
    else:
        nome = None

    return {'nome_paciente': nome}

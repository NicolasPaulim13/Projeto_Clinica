from cadastro_registro.models import CadastroRegistro

def paciente_context(request):
    if request.user.is_authenticated:
        try:
            cadastro = CadastroRegistro.objects.get(user=request.user)
            nome = cadastro.nome_paciente  # Nome completo
            imagem_perfil = cadastro.imagem_perfil.url if cadastro.imagem_perfil else None
        except CadastroRegistro.DoesNotExist:
            nome = None
            imagem_perfil = None
    else:
        nome = None
        imagem_perfil = None

    return {
        'nome_paciente': nome,
        'imagem_perfil_paciente': imagem_perfil,
    }

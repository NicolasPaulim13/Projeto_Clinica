from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from .forms import CadastroRegistroForm
import re  # Para validar o CPF

def validar_cpf(cpf):
    """Valida o formato do CPF e se ele é válido."""
    # Remove pontos e traços
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        return False

    # Validação dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False

    return True

from django.shortcuts import render
from .forms import CadastroRegistroForm

def cadastro_registro(request):
    if request.method == 'POST':
        form = CadastroRegistroForm(request.POST)
        print(request.POST)  # Debug para ver os dados enviados
        if form.is_valid():
            form.save()
            form = CadastroRegistroForm()  # Limpa o formulário após salvar
            return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form, 'success_message': 'Cadastro realizado com sucesso!'})
        else:
            print(form.errors)  # Mostra os erros no console
    else:
        form = CadastroRegistroForm()

    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})



def cadastro_create_paciente(request):
    if request.method == 'POST':
        form = CadastroRegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email_paciente']
            senha = form.cleaned_data['senha_paciente']
            nome = form.cleaned_data['nome_paciente']
            cpf = form.cleaned_data['cpf_paciente']

            # Validação adicional do CPF
            if form.errors.get('cpf_paciente'):
                messages.error(request, form.errors['cpf_paciente'][0])
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})


            # Verificação de requisitos da senha
            if len(senha) < 8 or not re.search(r'\d', senha) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
                messages.error(request, "A senha deve ter pelo menos 8 caracteres, incluindo números e caracteres especiais.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

            if User.objects.filter(username=email).exists():
                messages.error(request, 'Este email já está em uso. Tente outro.')
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

            try:
                user = User.objects.create_user(username=email, email=email, password=senha)
                paciente_group, created = Group.objects.get_or_create(name='paciente')
                user.groups.add(paciente_group)

                cadastro = form.save(commit=False)
                cadastro.user = user
                cadastro.save()

                assunto = "Bem-vindo ao nosso site!"
                mensagem = f"Olá, {nome}! Obrigado por se cadastrar. Estamos felizes em tê-lo conosco."
                destinatario = [email]

                remetente = request.user.email if request.user.is_authenticated else 'email_padrao@dominio.com'

                send_mail(
                    assunto,
                    mensagem,
                    remetente,
                    destinatario,
                    fail_silently=False,
                )

                messages.success(request, 'Cadastro realizado com sucesso! Você pode agora fazer login.')
                return redirect('login')

            except IntegrityError:
                messages.error(request, "Erro ao criar o usuário: possível duplicidade de dados.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

            except Exception as e:
                print(e)  # Para depuração em caso de erro inesperado
                messages.error(request, "Erro inesperado ao criar o usuário. Tente novamente.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

        else:
            # Log detalhado dos erros
            print(form.errors.as_json())
            messages.error(request, "Erro no preenchimento do formulário.")
            return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

    else:
        form = CadastroRegistroForm()

    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

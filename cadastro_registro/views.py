# cadastro_registro/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from .forms import CadastroRegistroForm
from .models import CadastroRegistro

def cadastro_registro(request):
    form = CadastroRegistroForm()
    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})


def cadastro_create_paciente(request):
    if request.method == 'POST':
        form = CadastroRegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email_paciente']
            senha = form.cleaned_data['senha_paciente']
            nome = form.cleaned_data['nome_paciente']
            
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

                # Utiliza o email do usuário autenticado ou define um padrão
                remetente = request.user.email if request.user.is_authenticated else 'email_padrao@dominio.com'

                send_mail(
                    assunto,
                    mensagem,
                    remetente,  # Remetente dinâmico
                    destinatario,
                    fail_silently=False,
                )

                messages.success(request, 'Cadastro realizado com sucesso! Você pode agora fazer login.')
                return redirect('login')

            except IntegrityError as e:
                messages.error(request, "Erro ao criar o usuário: possível duplicidade de dados.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})
            
            except Exception as e:
                messages.error(request, "Erro inesperado ao criar o usuário. Tente novamente.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

        else:
            messages.error(request, "Erro no preenchimento do formulário.")
            return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})
    
    else:
        form = CadastroRegistroForm()
    
    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

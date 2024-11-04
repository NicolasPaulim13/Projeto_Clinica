from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import CadastroRegistroForm
from .models import CadastroRegistro

def cadastro_registro(request):
    form = CadastroRegistroForm()
    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

# Função para criar um novo paciente
def cadastro_create_paciente(request):
    if request.method == 'POST':
        form = CadastroRegistroForm(request.POST)
        print("Formulário POST recebido")

        if form.is_valid():
            email = form.cleaned_data['email_paciente']
            senha = form.cleaned_data['senha_paciente']

            # Adicionando log detalhado antes da verificação
            print(f"Verificando se o email {email} já existe no banco de dados.")

            # Verifica se já existe um usuário com o mesmo email
            existing_user = User.objects.filter(username=email).exists()
            if existing_user:
                # Adiciona um log se encontrar um usuário existente
                print(f"Email {email} já existe no banco de dados.")
                messages.error(request, 'Este email já está em uso. Tente outro.')
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})
            else:
                # Log caso o email não esteja registrado
                print(f"Email {email} está disponível.")

            # Cria o usuário com o email como username
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=senha
                )
                print("Usuário criado com sucesso")
            except Exception as e:
                print("Erro ao criar usuário:", e)
                messages.error(request, "Erro ao criar o usuário. Tente novamente.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

            # Adiciona o usuário ao grupo "paciente"
            paciente_group, created = Group.objects.get_or_create(name='paciente')
            user.groups.add(paciente_group)
            print("Usuário adicionado ao grupo 'paciente'")

            # Salva a instância de CadastroRegistro associada ao usuário
            cadastro = form.save(commit=False)
            cadastro.user = user  # Associa o cadastro ao usuário
            cadastro.save()  # Salva no banco de dados
            print("Cadastro salvo no banco de dados")

            messages.success(request, 'Cadastro realizado com sucesso! Você pode agora fazer login.')
            return redirect('login')  # Redireciona para a página de login após o cadastro
        else:
            print("Formulário inválido")
    else:
        form = CadastroRegistroForm()

    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import CadastroRegistroForm
from .models import CadastroRegistro

def cadastro_registro(request):
    form = CadastroRegistroForm()
    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

# Função para criar um novo paciente
def cadastro_create_paciente(request):
    if request.method == 'POST':
        form = CadastroRegistroForm(request.POST)
        print("Formulário POST recebido")

        if form.is_valid():
            email = form.cleaned_data['email_paciente']
            senha = form.cleaned_data['senha_paciente']

            # Adicionando log detalhado antes da verificação
            print(f"Verificando se o email {email} já existe no banco de dados.")

            # Verifica se já existe um usuário com o mesmo email
            existing_user = User.objects.filter(username=email).exists()
            if existing_user:
                # Adiciona um log se encontrar um usuário existente
                print(f"Email {email} já existe no banco de dados.")
                messages.error(request, 'Este email já está em uso. Tente outro.')
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})
            else:
                # Log caso o email não esteja registrado
                print(f"Email {email} está disponível.")

            # Cria o usuário com o email como username
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=senha
                )
                print("Usuário criado com sucesso")
            except Exception as e:
                print("Erro ao criar usuário:", e)
                messages.error(request, "Erro ao criar o usuário. Tente novamente.")
                return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

            # Adiciona o usuário ao grupo "paciente"
            paciente_group, created = Group.objects.get_or_create(name='paciente')
            user.groups.add(paciente_group)
            print("Usuário adicionado ao grupo 'paciente'")

            # Salva a instância de CadastroRegistro associada ao usuário
            cadastro = form.save(commit=False)
            cadastro.user = user  # Associa o cadastro ao usuário
            cadastro.save()  # Salva no banco de dados
            print("Cadastro salvo no banco de dados")

            messages.success(request, 'Cadastro realizado com sucesso! Você pode agora fazer login.')
            return redirect('login')  # Redireciona para a página de login após o cadastro
        else:
            print("Formulário inválido")
    else:
        form = CadastroRegistroForm()

    return render(request, 'cadastro_registro/cadastro_registro.html', {'form': form})

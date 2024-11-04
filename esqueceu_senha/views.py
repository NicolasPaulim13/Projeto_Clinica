from django.shortcuts import render

def esqueceu_senha(request):
    return render(request, 'esqueceu_senha/esqueceu_senha.html')  # Renderiza o template home.html

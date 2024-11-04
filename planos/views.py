from django.shortcuts import render

def planos(request):
    return render(request, 'planos/planos.html')  # Renderiza o template home.html

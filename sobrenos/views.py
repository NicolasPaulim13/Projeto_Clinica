from django.shortcuts import render

def sobrenos(request):
    return render(request, 'sobrenos/sobrenos.html')  # Renderiza o template home.html

from django.shortcuts import render



def tratamentos(request):
    return render(request, 'tratamentos/tratamentos.html')  # Renderiza o template home.html

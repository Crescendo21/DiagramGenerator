from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
import json
import openai

# Importez la fonction generate_mind_map_data depuis apps.py
from .apps import generate_mind_map_data

openai.api_key = settings.OPENAI_API_KEY

def index(request):
    return render(request, 'apptest/index.html')

def create_diagram(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        schema_type = request.POST.get('schema_type')

        if not theme or not schema_type:
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
            return render(request, 'apptest/index.html')

        # Utilisez la fonction generate_mind_map_data pour générer le fichier JSON
        json_data = generate_mind_map_data(theme, schema_type)
        request.session['json_data'] = json_data

        return redirect('result')

    return render(request, 'apptest/index.html')

def result(request):
    json_data = request.session.get('json_data', {})
    return render(request, 'apptest/result.html', {'json_data': json.dumps(json_data)})


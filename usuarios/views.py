from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            ''' Pra utilizar a funcao de  mensagens do django precisa "from django.contrib.messages import constants"
             lembrando que em settings.py precisa estar configurado os messages '''
            messages.add_message(request, constants.ERROR, 'As senhas não conicidem ')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR, 'Este usuário já existe')
            return redirect('/usuarios/cadastro')


        user = User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('/usuarios/logar')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        
        '''User vai verificar se existe esse usuario no bando de dados, 
        pra utilizar essa funcao do django precisa importar "from django.contrib import auth'''
        user = auth.authenticate(request, username=username, password=senha)

        ''' Essa funcao auth.login vai autenticar e iniciar a secao do usuario (vulgo logado) '''
        if user:
            auth.login(request, user)
            return redirect('/empresarios/cadastrar_empresa')

        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
        return redirect('/usuarios/logar')

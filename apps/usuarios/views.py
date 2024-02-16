from django.shortcuts import render, redirect
from apps.usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        #pega os dados preenchidos e armazena em outro formulário = form
        form = CadastroForms(request.POST)
        
        #verifica se o formulario é válido
        if form.is_valid():            
            
            #maneira para acessar as informaçoes do formulário
            nome=form["nome_cadastro"].value()
            email=form["email"].value()
            senha=form["senha1"].value()

            #verifica se o usuário já existe cadastrado
            if User.objects.filter(username=nome).exists():
                messages.error(request, "Nome de usuário já cadastrado")
                return redirect('cadastro')
            
            #verifica se o e-mail ja existe no cadastro de outro usuario
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email de usuário já cadastrado")
                return redirect('cadastro')
            
            #cadastra um usuario
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, "Sucesso ao efetuar cadastro")
            return redirect('login')

    return render(request, "usuarios/cadastro.html", {"form":form})

def login(request):

    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome=form["nome_login"].value()
            senha=form["senha"].value()

        #verificar se o usuário existe e valida ele para entrar na pagina
        usuario = auth.authenticate(
            #busca dados do usuario para validação
            request, 
            username=nome,
            password=senha
        )
        if usuario is not None:
            #efetua o login e redireciona
            auth.login(request,usuario)
            messages.success(request, f"{nome} Logado com sucesso")
            return redirect('index')
        else:
            messages.error(request, f"Erro ao efetuar login")
            return redirect('login')            

    return render(request, 'usuarios/login.html', {"form":form})

def logout(request):
    auth.logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')
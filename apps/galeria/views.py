from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.models import Fotografia
from apps.galeria.forms import FotografiaForms
from django.contrib import messages


def index(request):
   #se usuário não estiver com login realizado ent n permite entrar e redireciona pra pag login
   if not request.user.is_authenticated:
       messages.error(request, 'usuário não logado')
       return redirect('login')

   #chamando no banco de dados todos os objetos de fotografia cadastrados
   fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True)                                                
   return render(request, 'galeria/index.html', {"cards":fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def buscar(request):

    #se usuário não estiver com login realizado ent n permite entrar e redireciona pra pag login
    if not request.user.is_authenticated:
       messages.error(request, 'Usuário não logado')
       return redirect('login')
   
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True)    

    if "buscar" in request.GET:
        nome_a_buscar = request.GET["buscar"]
        if nome_a_buscar:
            #iconstains pra fazer filtro 
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(request, 'galeria/index.html', {"cards":fotografias})

def nova_imagem(request):

    #se usuário não estiver com login realizado ent n permite entrar e redireciona pra pag login
    if not request.user.is_authenticated:
       messages.error(request, 'Usuário não logado')
       return redirect('login')

    form = FotografiaForms
    #salvar informacoes do formulario no banco dados
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova fotografia cadastrada')
            return redirect('index')

    return render(request, 'galeria/nova_imagem.html', {'form':form})

def editar_imagem(request, foto_id):
    #pegar dados do banco
    fotografia = Fotografia.objects.get(id=foto_id)    
    #preencher form com os dados preexistentes da imagem = instance
    form = FotografiaForms(instance=fotografia)

    if request.method == 'POST':
        #colocando informações novas
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia editada com sucesso')
            return redirect('index')

    return render(request, 'galeria/editar_imagem.html', {'form':form, 'foto_id':foto_id})

def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request,'Deletado com sucesso')
    return redirect('index')

def filtro(request, categoria):
    #chamando no banco de dados todos os objetos de fotografia cadastrados
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True, categoria=categoria)     
    return render(request, 'galeria/index.html',  {"cards":fotografias})  

from django.shortcuts import render, redirect
from core.models import Usuario, Cartao, Despesas, Relatorio, ContaBancaria, Notificacao
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from core.forms import FormContaBancaria, FormCartao, UsuarioForm
from django.contrib.auth import authenticate, login

# Create your views here.


def apresentacao(request):
    return render(request,'core/apresentacao.html')

class Registrar(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('url_principal')
    template_name = 'registration/registrar.html'

def cadastro_contaBancaria(request):
    form = FormContaBancaria(request.POST, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_cadastro_cartao')
    contexto = {'form': form, 'bancaria': 'Cadastro com sua conta bancária', 'formulario':True}
    return render(request, 'cadastro.html', contexto)

def cadastro_cartao(request):
    form = FormCartao(request.POST or None, request.FILES or None)
    if form.is_valid():
            form.save()
            return redirect('url_login')
    contexto = {'form': form, 'cartao': 'Cadastre seu cartão', 'formulario':False}
    return render(request, 'core/cadastro_cartao.html', contexto)

def login(request):
    if request.method == 'POST':
        conta = request.POST['conta']
        senha = request.POST['senha']
        try:
            user = ContaBancaria.objects.get(conta=conta, senha=senha)
            if conta == user.conta and senha == user.senha:
                context = {'pessoa': user.proprietario}
                return render(request, 'core/home.html', context)  # Redirecionar para a página inicial após o login
        except ContaBancaria.DoesNotExist:
            error_message = 'Nome de usuário ou senha inválidos.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def perfil(request, pessoa):
    usuario = Usuario.objects.get(nome=pessoa)
    contexto = {'nome': usuario.nome, 'foto': usuario.foto}
    return render(request, 'core/perfil.html', contexto)

def editar_perfil(request):
    usuario = request.user  # Obtém o objeto de usuário atualmente autenticado
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redireciona para a página de perfil do usuário após salvar os dados
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

def conta_bancaria(request):
    return render(request, '')

def pagamentos(request):
    return render(request, '')

def logout_view(request):
    return render(request, 'core/apresentacao.html')

def home(request): 
     return render(request, 'core/home.html')

def grafico_gastos(request):
    return render(request, 'core/grafico_gastos.html')

def relatorios(request): 
    return render(request, 'core/relatorios.html')


""" def login_validation(request):
    conta_bancaria = request.POST.get('conta')
    senha = request.POST.get('senha')
    if senha == Usuario.senha and conta_bancaria == Usuario.contaBancaria.numeroConta:
        dados = Usuario.objects.all()
        return redirect('home', dados)
    return render(request, 'login.html') """

    

""" @login_required
def cadastro_usuario(request):
    if request.user.is_staff:
        form = FormUsuario(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário adicionado com sucesso')
            return redirect('url_listagem_cliente')
        contexto = {'form': form, 'txt_title':'cad_cli','txt_descricao':'cadastro de cliente','txt_button':'Cadastrar'}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'core/mensagem.html') """



""" 
@login_required
def listagem_cliente(request):
    if request.user.is_staff:
        if request.POST and request.POST['input_pesquisa']:
            dados = Cliente.objects.filter(nome__contains=request.POST['input_pesquisa'])
        else:
            dados = Cliente.objects.all()
        contexto = {'dados': dados, 'txt': 'Digite nome do cliente'}
        return render(request, 'core/listagem_cliente.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def atualiza_cliente(request, id):
    if request.user.is_staff:
        obj = Cliente.objects.get(id=id)
        form = FormCliente(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso')
            return redirect('url_listagem_cliente')
        contexto = {'form' : form, 'txt_title':'atualizaCliente', 'txt_descricao':'Atualiza Cliente','txt_button':'Atualizar'}
        return render(request,'core/cadastro.html', contexto)
    return render (request, 'core/mensagem.html')

@login_required
def exclui_cliente(request, id):
    if request.user.is_staff:
        obj = Cliente.objects.get(id=id)
        contexto = {'txt_msg': obj.nome, 'txt_url':'/listagem_cliente/'}
        if request.POST:
            obj.delete()
            messages.success(request, 'Cliente excluido com sucesso')
            contexto.update({'txt_tipo':'Cliente'})
            return render(request, 'core/mensagem_exclusao.html', contexto)
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    return render(request, 'core/mensagem.html')


@login_required
def cadastro_tabelaPreco(request):
    if request.user.is_staff:
        form = FormTabelaPreco(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('url_listagem_tabelaPreco')
        contexto = {'form': form, 'txt_title':'cad_tab', 'txt_descricao':'Cadastro de Preco','txt_button':'Cadastrar'}
        return render(request,'core/cadastro.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def listagem_tabelaPreco(request):
    if request.user.is_staff:
        dados = TabelaPreco.objects.all()
        contexto = {'dados': dados}
        return render(request, 'core/listagem_tabelaPreco.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def atualiza_tabelaPreco(request, id):
     if request.user.is_staff:
        obj = TabelaPreco.objects.get(id=id)
        form = FormTabelaPreco(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('url_listagem_tabelaPreco')
        contexto = {'form': form, 'txt_title':'atualizatabelaPreco', 'txt-descricao':'Atualiza Preco','txt_button':'Atualizar'}
        return render(request,'core/cadastro.html', contexto)
     return render(request, 'core/mensagem.html')


@login_required
def exclui_tabelaPreco(request, id):
    if request.user.is_staff:
        obj = TabelaPreco.objects.get(id=id)
        contexto = {'txt_msg': obj.descricao,'txt_url':'/listagem_tabelaPreco/'}
        if request.POST:
            obj.delete()
            contexto.update({'txt_tipo':'TabelaPreco'})
            return render(request, 'core/mensagem_exclusao.html', contexto)
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def cadastro_veiculo(request):
    if request.user.is_staff:
        form = FormVeiculo(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('url_listagem_veiculo')
        contexto = {'form': form, 'txt_title':'cad_veic', 'txt_descricao':'Cadastro de veiculo','txt_button':'Cadastrar'}
        return render(request,'core/cadastro.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def listagem_veiculo(request):
    if request.user.is_staff:
        if request.POST and request.POST['input_pesquisa']:
            dados = Veiculo.objects.filter(modelo__startswith=request.POST['input_pesquisa'])
        else:
            dados = Veiculo.objects.all()
        contexto = {'dados': dados, 'txt': 'Digite o nome do veículo'}
        return render(request, 'core/listagem_veiculo.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def atualiza_veiculo(request, id):
    if request.user.is_staff:
        obj = Veiculo.objects.get(id=id)
        form = FormVeiculo(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('url_listagem_veiculo')
        contexto = {'form': form, 'txt_title':'atualizaveiculo', 'txt-descricao':'Atualiza Veiculo','txt_button':'Atualizar'}
        return render(request,'core/cadastro.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def exclui_veiculo(request, id):
    if request.user.is_staff:
        obj = Veiculo.objects.get(id=id)
        contexto = {'txt_msg': obj.placa,'txt_url':'/listagem_veiculo/'}
        if request.POST:
            obj.delete()
            contexto.update({'txt_tipo':'Veiculo'})
            return render(request, 'core/mensagem_exclusao.html', contexto)
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    return render(request, 'core/mensagem.html')


def cadastro_fabricante(request):
    if request.user.is_staff:
        form = FormFabricante(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('url_cadastro_fabricante')
        contexto= {'form': form, 'txt_title':'cadastro_fabricante', 'txt-descricao' : ' Cadastro Fabricante','txt_button':'Cadastrar'}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'core/mensagem.html')


@login_required
def atualiza_fabricante(request, id):
      if request.user.is_staff:
        obj = Fabricante.objects.get(id=id)
        form = FormFabricante(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('url_listagem_fabricante')
        contexto = {'form': form, 'txt_title': 'atualiza_fabricante', 'txt_descricao': 'Atualiza Fabricante',
                    'txt_button': 'Atualizar'}
        return render(request, 'core/cadastro.html', contexto)
      return render(request, 'core/mensagem.html')

@login_required
def listagem_fabricante(request):
    if request.user.is_staff:
        dados = Fabricante.objects.all()
        contexto = {'dados': dados}
        return render(request, 'core/listagem_fabricante.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def exclui_fabricante(request, id):
    if request.user.is_staff:
        obj = Fabricante.objects.get(id=id)
        contexto = {'txt_msg': obj.nome,'txt_url':'/listagem_fabricante/'}
        if request.POST:
            obj.delete()
            contexto.update({'txt_tipo':'Fabricante'})
            return render(request, 'core/mensagem_exclusao.html', contexto)
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    return render(request, 'core/mensagem.html')

def cadastro_rotativo(request):
    if request.user.is_staff:
        form = FormRotativo(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('url_cadastro_rotativo')
        contexto= {'form': form, 'txt_title':'cadastro_rotativo', 'txt-descricao' : ' Cadastro Rotativo','txt_button':'Cadastrar'}
        return render(request, 'core/cadastro_rotativo_dividido.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def listagem_rotativo(request):
    if request.user.is_staff:
        dados = Rotativo.objects.all()
        contexto = {'dados': dados}
        return render(request, 'core/listagem_rotativo.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def atualiza_rotativo(request, id):
      if request.user.is_staff:
        obj = Rotativo.objects.get(id=id)
        form = FormRotativo(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            obj.calcula_total()
            form.save()
            return redirect('url_listagem_rotativo')
        contexto = {'form': form, 'txt_title': 'atualiza_rotativo', 'txt_descricao': 'Atualiza Rotativo',
                    'txt_button': 'Atualizar'}
        return render(request, 'core/cadastro.html', contexto)
      return render(request, 'core/mensagem.html')

@login_required
def exclui_rotativo(request, id):
    if request.user.is_staff:
        obj = Rotativo.objects.get(id=id)
        contexto = {'txt_msg': obj.id_veiculo,'txt_url':'/listagem_rotativo/'}
        if request.POST:
            obj.delete()
            contexto.update({'txt_tipo':'Rotativo'})
            return render(request, 'core/mensagem_exclusao.html', contexto)
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    return render(request, 'core/mensagem.html')


def cadastro_mensalista(request):
    if request.user.is_staff:
        form = FormMensalista(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('url_cadastro_mensalista')
        contexto= {'form': form, 'txt_title':'cadastro_mensalista', 'txt-descricao' : ' Cadastro Mensalista','txt_button':'Cadastrar'}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'core/mensagem.html')


@login_required
def listagem_mensalista(request):
    if request.user.is_staff:
        dados = Mensalista.objects.all()
        contexto = {'dados': dados}
        return render(request, 'core/listagem_mensalista.html', contexto)
    return render(request, 'core/mensagem.html')

@login_required
def atualiza_mensalista(request, id):
      if request.user.is_staff:
        obj = Mensalista.objects.get(id=id)
        form = FormMensalista(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('url_listagem_mensalista')
        contexto = {'form': form, 'txt_title': 'atualiza_mensalista', 'txt_descricao': 'Atualiza Mensalista',
                    'txt_button': 'Atualizar'}
        return render(request, 'core/cadastro.html', contexto)
      return render(request, 'core/mensagem.html')

@login_required
def exclui_mensalista(request, id):
    if request.user.is_staff:
        obj = Mensalista.objects.get(id=id)
        contexto = {'txt_msg': obj.id_veiculo,'txt_url':'/listagem_mensalista/'}
        if request.POST:
            obj.delete()
            contexto.update({'txt_tipo':'Mensalista'})
            return render(request, 'core/mensagem_exclusao.html', contexto)
        else:
            return render(request, 'core/confirma_exclusao.html', contexto)
    return render(request, 'core/mensagem.html') """
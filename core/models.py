from django.db import models
import math
# Create your models here.

class Cartao(models.Model):
    nomeTitular = models.CharField(max_length=100, verbose_name='Nome do Titular')
    numeroCartao = models.CharField(max_length=30, verbose_name='Número do Cartão')
    validade = models.DateTimeField(auto_now=False, verbose_name='Validade')
    cvv = models.IntegerField(verbose_name='CVV')
    class Meta:
        verbose_name_plural='Cartões'
    def __str__(self):
        return f"{self.numeroCartao} ({self.nomeTitular})"
    

class ContaBancaria(models.Model):
    proprietario = models.CharField(max_length=45, verbose_name='Proprietário')
    agencia = models.IntegerField(verbose_name='Agência')
    conta = models.CharField(max_length=100, verbose_name='Número da Conta')
    cartao = models.ForeignKey('Cartao', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cartão')
    senha = models.CharField(max_length=100, verbose_name='Senha', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Contas Bancárias'

    def __str__(self):
        return self.conta, self.proprietario

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45, null=True, blank=True, verbose_name='Nome')
    foto = models.ImageField(upload_to='foto_cliente',blank=True, null=True, verbose_name='Foto')
    senha = models.CharField(max_length=100, verbose_name='Senha')
    contaBancaria = models.ForeignKey(ContaBancaria, on_delete = models.CASCADE, verbose_name='Número da Conta')
    class Meta:
        verbose_name_plural='Usuários'

    def save(self, *args, **kwargs):
        if not self.nome: 
            self.nome = self.contaBancaria.proprietario
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome if self.nome else str(self.id_usuario)

class FormaPagamento(models.Model):
    tipo = models.CharField(max_length=20, blank=False, null=False, verbose_name='Tipo de pagamento')
    id = models.IntegerField(verbose_name='Id pagamento', primary_key = True, null=False)


class Notificacao(models.Model):
    mensagem = models.CharField(max_length=100, verbose_name='Mensagem')
    notificacoesAtivas = models.BooleanField(blank=True, null=True, verbose_name='Status')
    data_envio = models.DateTimeField(auto_now=False, verbose_name='Entrada')
    notificacaoPagamento = models.BooleanField(blank=True, null=True, verbose_name='Notificação do Pagamento')
    intervaloNotificacoes = models.IntegerField(blank=True, null=True, verbose_name='Intervalo de Notificações')
    diasAntesVencimento = models.IntegerField(blank=True, null=True, verbose_name='diasAntesVencimento')
    class Meta:
        verbose_name_plural = 'Notificações'
    def __str__(self):
        return f'{self.mensagem}:{self.notificacoesAtivas}'    

class Despesas(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    status = models.BooleanField(verbose_name='Status')
    categoria = models.CharField(max_length=100, verbose_name='Categoria')
    dataPagamento = models.DateField(verbose_name='DataPagamento')
    dataVencimento = models.DateField(verbose_name='DataVencimento')
    pagamento = models.ForeignKey(FormaPagamento, on_delete = models.CASCADE, verbose_name='FormaPagamento')
    notificacaoDespesas = models.ForeignKey(Notificacao, on_delete = models.CASCADE, verbose_name='Notificacao')
    class Meta:
        verbose_name_plural = "Despesas"
    def __str__(self):
        return f'{self.id_veiculo}:{self.id_tabela}'

class Relatorio(models.Model):
    nomeItens = models.ForeignKey(Despesas, max_length=100, on_delete=models.CASCADE, verbose_name='Título da conta')
    descricao = models.CharField(max_length=50, verbose_name='Descrição')
    geracaoRelatorio = models.DateField(verbose_name='Relatório gerado')
    class Meta:
        verbose_name_plural = 'Relatorios'

    def __str__(self):
        return f"{self.nomeItens} = {self.descricao}"


"""
    def calcula_total(self):
        obj = TabelaPreco.objects.get(id=self.id_tabela.pk)
        if self.data_hora_saida:
            horas = math.ceil((self.data_hora_saida - self.data_hora_entrada).total_seconds() / 3600)
            if ((self.data_hora_saida - self.data_hora_entrada).total_seconds() / 3600) <= 0.5:
                self.total = (horas * obj.valor) / 2
                return self.total
            else:
                self.total = horas * obj.valor
                return self.total
        return 0.0
"""    

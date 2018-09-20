from random import random
import matplotlib.pyplot as plt

#Classe responsável por criar os produtos e seus atributos
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos #limite usado no caminhão é de 3 metros cúbicos neste exemplo
        self.nota_avaliacao = 0 #Avaliar se o individio é bom ou ruim
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = [] #Vai ser armazenado a solução do individuo, lembrando que temos 14 produtos
        
        #Inicialização aleátoria dos cromossomos usando random que gera numeros entre 0 e 1
        #Seta o que leva ou não com 0 ou 1
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
    
    #Função que vai fazer a avaliação dos cromossomos, ou seja vai somar os valores do produtos que vai levar
    # vai somar os metros cpubicos e avaliar se cabe no caminhão.
    #Individuos que não ultrapassatem de 3 metros cúbicos terão mais chances de evoluir             
    def avaliacao(self):
        nota = 0  #Responsável por somar os valores dos produtos selecionados
        soma_espacos = 0 #Soma espaços ocupados do cromossomo
        for i in range(len(self.cromossomo)):
           if self.cromossomo[i] == '1':
               nota += self.valores[i]
               soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1 #Não usamos 0 ou números negativos pq terá uma tendência de gerar somente soluções com individuos melhores, apesar que isso é o objeto de AG, mas se excluir os individuos com notas muito baixa vai ficar com os valores todos iguais
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
    
    #Operador crossover de um ponto    
    #Reprodução
    def crossover(self, outro_individuo):
        corte = round(random()  * len(self.cromossomo)) #Pega o ponto de corte do cromossomo, multiplica pelo radom de 0 a 1
        
        #Cria os filhos fazendo a mesclagem
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        #Cria a lista de filhos da nova geração e depois seta na posição 0 e 1 
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
    
    #Função que faz mutações nos cromossomos, passando uma taxa de mutação
    def mutacao(self, taxa_mutacao):
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1': #Se a condição for satisfeita muda de 1 para 0
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("Depois %s " % self.cromossomo)
        return self
        
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao): 
        self.tamanho_populacao = tamanho_populacao # Quantos individuos que vai ser criado
        self.populacao = []  #Lista guarda vários objetos do tipo individuo
        self.geracao = 0 
        self.melhor_solucao = 0 #Armazena a melhor solução dentro da população
        self.lista_solucoes = []
    
    #Cria vários individios de acordo com o tamanho da população    
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0] #Melhor solução com a lista dos valores ordenadas
    
    #Ordena o vetor para pegar o melhor individuo    
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
     
    #Seleciona o melhor individuo verificando pela melhor solução já encontrada    
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
    
    #Soma todos as notas de uma determinada população        
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma
   
    #Faz a simulação da roleta viciada e escolhe o melhor pai e retorna o indice
    def seleciona_pai(self, soma_avaliacao):
        pai = -1 #Começa com -1 pq ainda não selecionou nenhum inviduo
        valor_sorteado = random() * soma_avaliacao  #Sortea um valor para a roleta
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    #Print na tela com os dados do melhor individuo(cromossomo)
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
    
    #Resolve todo o algoritmo
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos) #inicializa a população
        
        #Faz a avaliação da população
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0] #
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes() #Necessário para selecionar os pais para o crossover
            nova_populacao = [] #Lista para guardar a nova população
            
            #Escolhe os pais através da roleta viciada
            for individuos_gerados in range(0, self.tamanho_populacao, 2): #20 elementos, pais gera 2 filhos ou seja o for precisa rodar somente 10 vezes
                pai1 = self.seleciona_pai(soma_avaliacao) 
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2]) #Faz a mutação direto com o processo de crossover gera 2 filhos
                
                #Adicona os novos filhos e já faz a mutação
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao) #Descarta a população antiga e recebe a nova
            
            #Recalcula a avaliação dos individuos e refaz os cálculos
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao) #Lista para plotar o gráfico
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo
        
        
if __name__ == '__main__':
    #p1 = Produto("Iphone 6", 0.0000899, 2199.12)
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    
    #Listas responsáveis por armazenar espaços, valores e nomes de todos os produtos para efeito de cálculos
    espacos = []
    valores = []
    nomes = []
    
    #Inicializa a lista com os produtos
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3 #Limite de carga do caminhão
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    
    #Componentes que estão na carga
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
            
    
    #for valor in ag.lista_solucoes:
    #    print(valor)
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show()
    
    

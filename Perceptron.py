# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
import cv2
import os
import imutils
from skimage.feature import hog
import numpy as np
import random
import copy

'''
Descrição do algoritmo:
	1 - entradas
	2 - peso de desvio
	3 - função de entrada
	4 - função de ativação
	5 - função de saida
'''

'''
Função de ativação:
	1 - Soma ponderada das entradas (entrada*peso)
	2 - Colocar a soma na função de ativação
	
	A função pode ser do tipo:
		threshold:
		*se* g(somas) >= ao treshold *é* 1
		*se* g(somas) < treshold *é* 0
		
		sigmoid logistica
		
		tangente hiperbólica
		
Depois aplicar o resultado obtido com o resultado esperado, 
se for diferente utilizar uma função de correção de erro

Erro:
	1 - erro (e) = resultadoObtido - resultadoEsperado
	
	2 - função de custo (c) = 1/(2*(soma de e^2(t)))
	
	3 - função de aprendizado(W) = n(função de aprendizado) * e * valor da entrada
	
	4 - novo peso =  peso + resultado de W
'''

'''
Variáveis necessárias:
	1 - entradas
	2 - pesos
	3 - limiar
	4 - função de aprendizado
'''

# Perceptron com apenas uma camada
class Perceptron:
	# incializa o perceptron
	def __init__(self, epocas, taxa_aprendizagem, entradas, saidas, limiar):
		self.entradas = entradas            # entradas para teste
		self.saidas = saidas                # suas saidas esperadas para cada entrada
		self.epocas = epocas
		self.taxa_aprendizagem = taxa_aprendizagem
		self.pesos = []                         # vetor com os pesos que serão atribuidos a cada entrada
		self.total_entradas = len(entradas)     # quantidade total de entradas que serão testadas
		self.total_variaveis_entrada = len(entradas[0])
		self.limiar = limiar

	def treinar(self):
		# adiciona -1 para cada uma das amostras
		#for amostra in self.entradas:
		#	amostra.insert(0, -1)
		# onde cada posição armazena um vetor com os pesos iniciais
		for i in range(self.total_variaveis_entrada):
			# preencher o vetor que armazena os pesos
			self.pesos.append(np.random.random_sample())

		# insere o limiar no vetor de pesos
		#self.pesos.insert(0, self.limiar)

		# roda o algoritmo ate terminar as eras estabelecidas
		for i in range(self.epocas):
			erro = False
			# repetir o processo a quantidade total de entradas
			for j in range(self.total_entradas):
				somatorio = 0
				# somar os pesos com as variaveis da entrada
				for posicao in range(self.total_variaveis_entrada):
					somatorio += self.pesos[posicao] * self.entradas[j][posicao]

				# função de ativação
				saida = self.ativacao(somatorio)

				if saida != self.saidas[j]:
					erro = True
					erro_auxiliar = self.saidas[j] - saida

					# corrigir o peso agora para cada entrada dessa rodada
					for posicao in range(self.total_variaveis_entrada):
						self.pesos[posicao] = self.pesos[posicao] + \
											  (self.taxa_aprendizagem * erro_auxiliar * self.entradas[j][posicao])

			# se achar os melhores valores antes do fim das eras
			if not erro:
				break

	def testar(self):
		resposta_esperada = []
		amostras = []
		arquivo = teste
		local = os.listdir(arquivo)
		cont = 0
		for im_file in local:
			vetor_caracteristica_aux = []

			im_path = arquivo + im_file

			im = cv2.imread(im_path)
			resized_image = imutils.resize(im, width=80, height=80)

			fd, hog_image = hog(resized_image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(3, 3),
			                    visualize=True, feature_vector=True)

			for i in range(len(fd)):
				teste = float(fd[i])
				vetor_caracteristica_aux.append(teste)

			string_aux = im_file.split('.')[0]
			if 'nodule' == string_aux:
				cont = 1
			elif 'nannodule' == string_aux:
				cont = 0

			resposta_esperada.append(cont)
			amostras.append(vetor_caracteristica_aux)

		resposta = []
		for amostra in amostras:
			# utiliza o vetor de pesos que foi ajustado na fase de treinamento
			u = 0
			for i in range(self.total_variaveis_entrada):
				u += self.pesos[i] * amostra[i]

			# calcula a saída da rede
			y = self.ativacao(u)

			resposta.append(y)

		return resposta, resposta_esperada

	# função de ativação do tipo bipolar (bipolar pq so tem dois valores de saida)
	# +1 ativo e 0 inativo, com 0 como limiar
	def ativacao(self, valor):
		#return 1 if valor >= 0 else -1
		return 1 if valor >= 0 else 0

class hog_gerador:
	def __init__(self):
		self.vetor_caracteristica = []
		self.saidas_esperadas = []
		self.arquivos = treinar

	def gerar_vetor(self):
		local = os.listdir(self.arquivos)
		cont = 0

		for im_file in local:
			vetor_caracteristica_aux = []

			im_path = self.arquivos + im_file

			im = cv2.imread(im_path)
			resized_image = imutils.resize(im, width=80, height=80)

			fd, hog_image = hog(resized_image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(3,3),
									  visualize=True, feature_vector=True)

			for i in range(len(fd)):
				teste = float(fd[i])
				vetor_caracteristica_aux.append(teste)

			string_aux = im_file.split('.')[0]
			if 'nodule' == string_aux:
				cont = 1
			elif 'nannodule' == string_aux:
				cont = 0
			vetor_caracteristica_aux.append(cont)

			self.vetor_caracteristica.append(vetor_caracteristica_aux)

		random.shuffle(self.vetor_caracteristica)

	def retirar_informacoes(self):
		entradas = []
		saidas = []

		for vetor in self.vetor_caracteristica:
			# não utilizar os vetores de caracteristica que só são compostos por 0's
			if vetor[0] != 0:
				aux = len(vetor) - 1
				entradas.append(vetor[0:aux])
				saidas.append(vetor[len(vetor)-1])

		return entradas, saidas

# ---------------------------------------------------------------------------------------------------
# MAIN:
for i in range(5):
	teste = "string_path"+str(i)             #Separar para Teste
	for n in range(5):
		if not n == i:
            treino = "string_path"+str(n)    #Treino da vez

			hogControlador = hog_gerador()
			print 'gerar vetor...'
			hogControlador.gerar_vetor()

			entradas = []
			saidas = []
			print 'retirar_informacoes...'
			entradas, saidas = hogControlador.retirar_informacoes()

			# variando eras e taxa de aprendizado
			perceptronControlador = Perceptron(100, 0.1, entradas, saidas, -1)

			print 'treinar...'
			perceptronControlador.treinar()

			print 'testar...'
			resposta_obtida, resposta_esperada = perceptronControlador.testar()

			similar = 0
			print 'somando...'
			for i in range(len(resposta_obtida)):
				if resposta_obtida[i] == resposta_esperada[i]: similar += 1
			total = len(resposta_obtida)
			accuracy = float(similar)/ float(total)

			print 'acertados ', similar
			print 'total ', total
			print 'acuracia',accuracy
			#200 caracteristicas no hog
			#200 pesos
			#ativacao bipolar
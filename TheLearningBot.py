#-- coding: utf-8 --
import telebot #importar a biblioteca do pyTelegrambotAPI
from telebot import types #selecionar a lib types
import json #valores em json - xml
import urllib.request #tratar urls
from urllib.request import urlopen
import random
from telebot import util
from unicodedata import normalize


API_TOKEN = 'INSIRA O TOKEN AQUI' #@botfather
API_VAGALUME = 'KEY DO VAGALUME AQUI' #registro no Vagalume

bot = telebot.TeleBot(API_TOKEN) #telebot é a biblioteca, TeleBot é o comando para aplicar o Token		  

#COMANDO START

@bot.message_handler(commands=['start']) #receber comando /start
def send_welcome(message): #ações a partir do comando
	msg = bot.reply_to(message,"Oie! \nEu sou o Bot que vai te divertir! Aperte /ajuda para ver mais.") #mensagem enviada para o usuário
	
#COMANDO AJUDA
	
@bot.message_handler(commands=['ajuda']) #receber comando /ajuda
def send_help(message):	#ações a partir do comando
	msg_help = bot.reply_to(message,"Eu sou um bot construído puramente por aprendizado, e estou em constante melhoria!") #mensagem enviada para o usuário
	bot.send_message(message.chat.id,"Os meus comandos você pode ver pela lista de comandos, quando você digita uma barra (/). Divirta-se!") #envia uma segunda mensagem, separada
	
#COMANDO CHOOSE
#é um teste para estudar sobre o Inline Keyboard da API

@bot.message_handler(commands=['choose']) 
def send_category(message):		
	button = types.InlineKeyboardMarkup(row_width = 2) #estilo de mensagem que mostra diversos botões para serem apertados
	btn1 = types.InlineKeyboardButton(text="1", callback_data="um")
	btn2 = types.InlineKeyboardButton(text="2", callback_data="dois")
	button.row(btn1,btn2)
	btn3 = types.InlineKeyboardButton(text="3", callback_data="tres")	
	btn4 = types.InlineKeyboardButton(text="4", callback_data="quatro")
	button.row(btn3,btn4)		
	bot.send_message(message.chat.id,"Escola um dos números:", reply_markup=button) #ler qual botão foi pressionado

#cada callback abaixo é uma resposta para cada botão:

@bot.callback_query_handler(lambda query: query.data == "um")
def send_cat(query):
	get_user = query.from_user.username
	bot.send_message(query.message.chat.id,"@" + get_user + " selecionou o número um!")

@bot.callback_query_handler(lambda query: query.data == "dois")
def send_plant(query):
	get_user = query.from_user.username
	bot.send_message(query.message.chat.id,"@" + get_user + " selecionou o número dois!")
	
@bot.callback_query_handler(lambda query: query.data == "tres")
def send_heli(query):
	get_user = query.from_user.username
	bot.send_message(query.message.chat.id,"@" + get_user + " selecionou o número três!")
	
@bot.callback_query_handler(lambda query: query.data == "quatro")
def send_reptil(query):
	get_user = query.from_user.username
	bot.send_message(query.message.chat.id,"@" + get_user + " selecionou o número quatro!")	
	
#COMANDO CEP
#Digitando o CEP, o bot retorna Logradouro, Rua (caso haja), Cidade e UF

@bot.message_handler(commands=['cep'])
def send_cep(message):	
	a = telebot.util.extract_arguments(message.text) #checa se a pessoa já digitou algo junto ao comando ou não
	if not a:
		bot.send_message(message.chat.id,"Para usar esse comando, envie o CEP que queira pesquisar junto dele, por exemplo: /cep 01311-200.") #se não enviou, ele ensina como o fazer
		return
	else:	
		hifencheck = a #condicional para remover o hífen do CEP caso haja, para encaixar na URL do ViaCEP
		if hifencheck.find('-'):
			removehifen = hifencheck.lstrip("-")
		else:
			removehifen = hifencheck
		
	get_user = message.from_user.username
	info_cep = removehifen 
	
	try:
		url = "https://viacep.com.br/ws/" + removehifen + "/json/"
		response = urllib.request.urlopen(url) #abrir a URL que informa o CEP	
		data = json.loads(response.read()) #carregar o json e ler os valores
	except Exception as e:
		bot.reply_to(message, "Opa... parece que eu não consegui encontrar um CEP existente com esse que você me mandou. Veja se o número está correto e tente novamente!") #retorno caso ele não acha um CEP existente
		print("Bot encontrou um erro em CEP, quando " + get_user + " pesquisou por " + info_cep) #avisa no console que um usuário cometeu um erro, enviando também seu @ do Telegram
		return
				
	try:			
		cep = data['cep'] #escolhendo valores do json
		logradouro = data['logradouro']
		bairro = data['bairro']
		localidade = data['localidade']
		uf = data['uf']
	except Exception as e:
		bot.reply_to(message, "Não pera aí... parece que eu não consegui encontrar um CEP existente com esse que você me mandou. Veja se o número está correto e tente novamente!")
		print("Bot encontrou um erro em CEP, quando " + get_user + " pesquisou por " + info_cep)
		return
		
	print(get_user + " pediu por " + removehifen + ", CEP de " + localidade + " - " + uf)
	bot.send_message(message.chat.id,"CEP: " + cep + "\nLogradouro: " + logradouro + "\nBairro: " + bairro + "\nLocalidade: " + localidade + " - " + uf)
	
#COMANDO VAGALUME
#Usando a API do Vagalume, retorna o perfil do artista pedido
		
@bot.message_handler(commands=['vagalume'])
def send_vagalume(message):	
	a = telebot.util.extract_arguments(message.text) #checa se a pessoa já digitou algo junto ao comando ou não
	if not a:
		if message.chat.type == "private": #se não, verifica se o comando foi feito em um chat privado ou não
			msg = bot.reply_to(message,"Digite o nome do artista que deseja consultar:") #caso foi no PV, ele pede então o artista para o próximo input
			bot.send_message(message.chat.id,"Note que o Vagalume possui fraco suporte com artistas de K-Pop, então muitos deles podem não estar inteiramente disponíveis.")
			bot.register_next_step_handler(msg, send_vagalume_step) #vai pegar a próxima mensagem como o próximo passo do comando 
		else:
			bot.send_message(message.chat.id,"Esse comando não é apropriado para ser usado em grupos. Se ainda quiser usá-lo, peça diretamente junto ao comando, como por exemplo escrevendo: /vagalume Queen.") #caso o comando for feito em um grupo, ele deixa apenas caso envie junto do comando, para evitar conflitos com outras mensagens/outros usuários
			return
	else: #condicionais especiais para ajustar específicos artistas que não são bem colocados no Vagalume
		if a in ['loona','Loona','LOONA']:
			a = 'loo'
		if a in ['april','April','APRIL']:
			a = 'april-k-pop'
		if a in ['florence + the machine', 'Florence + The Machine', 'Florence + the machine']:
			a = 'florence-and-the-machine'
		
		cid = message.chat.id
		get_user = message.from_user.username
		info_vagalume = a #mensagem digitada	
		info_vagalume_low = info_vagalume.lower()
		normalize_vagalume = normalize('NFKD', info_vagalume_low).encode('ASCII','ignore').decode('ASCII')	
		f_vagalume = normalize_vagalume.replace(" ", "-")
			
		try:
			url = "https://www.vagalume.com.br/" + f_vagalume + "/index.js"
			response = urllib.request.urlopen(url) #abrir a URL que informa o perfil	
			data = json.loads(response.read()) #carregar o json e ler os valores	
		except Exception as e:
			bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista que você quer. Confira se você não digitou errado, ou se o artista consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
			print("Bot encontrou um erro em Vagalume, quando " + get_user + " pesquisou por " + f_vagalume)
			return	
			
		#NOME DO ARTISTA
		desc = data['artist']['desc']	

		#Try-Catches abaixo são para verificar se tudo está correto no perfil do artista
		#Isso deve-se ao fato do Vagalume não possuir alguns perfis completos de certos artistas

		try:	
			#FOTO DO ARTISTA					
			pic_medium = "https://www.vagalume.com.br" + data['artist']['pic_medium']	
		except Exception as e:
			bot.reply_to(message, "Ops... parece que esse artista não possui uma imagem registrada no Vagalume.")
		try:		
			#RANKING DO ARTISTA (NO SITE)	
			pos = data['artist']['rank']['pos']	
		except Exception as e:
			bot.reply_to(message, "Ops... parece que esse artista não possui um ranking no Vagalume.")	
		try:
			#LETRAS MAIS PESQUISADAS
			toplyrics1 = data['artist']['toplyrics']['item'][0]['desc']
			toplyrics2 = data['artist']['toplyrics']['item'][1]['desc']
			toplyrics3 = data['artist']['toplyrics']['item'][2]['desc']
		except Exception as e:
			bot.reply_to(message, "Ops... parece que esse artista não possui 3 ou mais músicas registradas no Vagalume...")	
		try:
			#ÁLBUM MAIS PESQUISADO
			albums1 = data['artist']['albums']['item'][0]['desc']
		except Exception as e:
			bot.reply_to(message, "Ops... parece que esse artista não possui um álbum ou EP registrado no Vagalume...")
			
		#Enviar o perfil do artista

		try:
			bot.send_message(cid,"\n-----------------------------\n")
			bot.send_message(cid,"Nome do Artista: " + desc)	
			bot.send_photo(cid,pic_medium)
			bot.send_message(cid,"Este artista é o " + pos + "° artista mais acessado no Vagalume.")
			bot.send_message(cid,"As letras de músicas mais acessadas desse artista são: " + toplyrics1 + ", " + toplyrics2 + " e " + toplyrics3)
			bot.send_message(cid,"O álbum mais pesquisado desse artista é: " + albums1)
		except Exception as e:
			bot.reply_to(message, "Infelizmente, algumas informações para esse artista estão incompletas pelos erros acima. Muitas vezes pode ser porque o Vagalume não possui tudo registrado, então sinto muito :(") #Caso falhe em algum try de cima, avisa de novo que as infos estão incompletas.

#O comando é repetido aqui pois, nesse caso, ele usa quando o usuário fazer do método de input separado no PV
#As limitações da API apenas permitem pegar uma mensagem de usuário por 'step', então é preciso fazer um novo step toda vez

def send_vagalume_step(message):		
	cid = message.chat.id
	get_user = message.from_user.username
	info_vagalume = message.text #mensagem digitada	pelo usuário
	
	#condicionais especiais para ajustar específicos artistas que não são bem colocados no Vagalume
	if info_vagalume in ['loona','Loona','LOONA']:
		info_vagalume = 'loo'
	if info_vagalume in ['april','April','APRIL']:
		info_vagalume = 'april-k-pop'
	if info_vagalume in ['florence + the machine', 'Florence + The Machine', 'Florence + the machine']:
		info_vagalume = 'florence-and-the-machine'
	
	info_vagalume_low = info_vagalume.lower()
	normalize_vagalume = normalize('NFKD', info_vagalume_low).encode('ASCII','ignore').decode('ASCII')	
	f_vagalume = normalize_vagalume.replace(" ", "-")
			
	try:
		url = "https://www.vagalume.com.br/" + f_vagalume + "/index.js"
		response = urllib.request.urlopen(url) #abrir a URL que informa o perfil	
		data = json.loads(response.read()) #carregar o json e ler os valores	
	except Exception as e:
		bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista que você quer. Confira se você não digitou errado, ou se o artista consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
		print("Bot encontrou um erro em Vagalume, quando " + get_user + " pesquisou por " + f_vagalume)
		return	
			
	#NOME DO ARTISTA
	desc = data['artist']['desc']	
					
	try:	
		#FOTO DO ARTISTA					
		pic_medium = "https://www.vagalume.com.br" + data['artist']['pic_medium']	
	except Exception as e:
		bot.reply_to(message, "Ops... parece que esse artista não possui uma imagem registrada no Vagalume.")
	try:			
		#RANKING DO ARTISTA (NO SITE)
		pos = data['artist']['rank']['pos']	
	except Exception as e:
		bot.reply_to(message, "Ops... parece que esse artista não possui um ranking no Vagalume.")	
	try:
		#LETRAS MAIS PESQUISADAS
		toplyrics1 = data['artist']['toplyrics']['item'][0]['desc']
		toplyrics2 = data['artist']['toplyrics']['item'][1]['desc']
		toplyrics3 = data['artist']['toplyrics']['item'][2]['desc']
	except Exception as e:
		bot.reply_to(message, "Ops... parece que esse artista não possui 3 ou mais músicas registradas no Vagalume...")	
	try:
		#ÁLBUM MAIS PESQUISADO
		albums1 = data['artist']['albums']['item'][0]['desc']
	except Exception as e:
		bot.reply_to(message, "Ops... parece que esse artista não possui um álbum ou EP registrado no Vagalume...")
			
	try:
		bot.send_message(cid,"\n-----------------------------\n")
		bot.send_message(cid,"Nome do Artista: " + desc)	
		bot.send_photo(cid,pic_medium)
		bot.send_message(cid,"Este artista é o " + pos + "° artista mais acessado no Vagalume.")
		bot.send_message(cid,"As letras de músicas mais acessadas desse artista são: " + toplyrics1 + ", " + toplyrics2 + " e " + toplyrics3)
		bot.send_message(cid,"O álbum mais pesquisado desse artista é: " + albums1)
	except Exception as e:
		bot.reply_to(message, "Infelizmente, algumas informações para esse artista estão incompletas pelos erros acima. Muitas vezes pode ser porque o Vagalume não possui tudo registrado, então sinto muito :(")								
		
#COMANDO LYRICS
#Usando a API do Vagalume, fornece letras de músicas

@bot.message_handler(commands=['lyrics'])
def send_lyrics_welcome(message):	
	a = telebot.util.extract_arguments(message.text) #checa se a pessoa já digitou algo junto ao comando ou não
	if not a:	
		if message.chat.type == "private": #se não, verifica se o comando foi feito em um chat privado ou não
			msg = bot.reply_to(message, "Digite o nome do artista e a música, separados por uma vírgula (Ex: The Weeknd, Blinding Lights): ") #caso foi no PV, ele pede então o artista para o próximo input
			bot.register_next_step_handler(msg, process_lyrics_step) #vai pegar a próxima mensagem como o próximo passo do comando 
		else:
			bot.send_message(message.chat.id,"Esse comando não é apropriado para ser usado em grupos. Se ainda quiser usá-lo, peça diretamente junto ao comando, como por exemplo escrevendo: /lyrics U2, One.") #caso o comando for feito em um grupo, ele deixa apenas caso envie junto do comando, para evitar conflitos com outras mensagens/outros usuários
			return
				
	else:					
		request = a #O que veio junto ao comando se torna o pedido - request
		get_user = message.from_user.username
		try:
			aux = request.split(",", 1) #Aqui, ele vai separar Artista e Música, que no comando foram escritos com uma vírgula
			separate = aux[1].lstrip(" ") #Aqui, ele tira o expaço extra que fica digitado depois da vírgula, evitando erros
		except Exception as e:
			bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
			return #Se ele não achar, retorna o erro para o usuário e me informa o que tentaram fazer que deu errado, através do terminal

		#condicionais especiais para ajustar específicos artistas que não são bem colocados no Vagalume	
		if aux[0] in ['loona','Loona','LOONA']:
			aux[0] = 'loo'
		if aux[0] in ['april','April','APRIL']:
			aux[0] = 'april-k-pop'	
		if aux[0] in ['florence + the machine', 'Florence + The Machine', 'Florence + the machine']:
			aux[0] = 'florence-and-the-machine'
	
		try:		
			#processo para retirar acentuações e símbolos, tanto no artista quanto na música
			normalize_artist = normalize('NFKD', aux[0]).encode('ASCII','ignore').decode('ASCII')
			normalize_song = normalize('NFKD', separate).encode('ASCII','ignore').decode('ASCII')
			#aqui, vai substituir os espaços (e vírgulas) com hífen, para formar o link igual o da API que dá as letras
			artist = normalize_artist.replace(" ", "-")
			song_step1 = normalize_song.replace(",", "-")
			song_step2 = song_step1.replace(" ", "-")
			song = song_step2.replace("--", "-")
		except Exception as e:
			bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar no modelo dos exemplos (/lyrics Slipknot, Duality), por favor.")
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
			return #se o processo de ajuste do pedido falhar, significa que o usuário o digitou errado.
		
		print(get_user + " pediu por " + artist + " - " + song)
	
		try:
			url = "https://api.vagalume.com.br/search.php" + "?art=" + artist + "&mus=" + song + "&apikey={API_VAGALUME}"
			response = urllib.request.urlopen(url) #abrir a URL que informa as letras	
			data = json.loads(response.read()) #carregar o json e ler os valores
		except Exception as e:
			bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou por " + artist + " e " + song)
			return		
		try:	
			#pega artista, música e letra
			f_artist = data['art']['name']
			f_song = data['mus'][0]['name']	
			f_letra = data['mus'][0]['text']
		except Exception as e:
			bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou por " + artist + " e " + song)
			return	
				
		#condicional para caso a letra for grande demais, excedendo os limites do Telegram (dessa forma, enviando em mensagens divididas)
		if len(f_letra) > 3000:
			letra_split = util.split_string(f_letra, 3000)
			bot.send_message(message.chat.id, "`" + f_artist + " - " + f_song + "`" + "\n\n" + letra_split[0], parse_mode='Markdown')
			for text in letra_split:
				bot.send_message(message.chat.id, text)
		else: 
			bot.send_message(message.chat.id, "`" + f_artist + " - " + f_song + "`" + "\n\n" + f_letra, parse_mode='Markdown')		
	
def process_lyrics_step(message):	
	request = message.text
	get_user = message.from_user.username
				
	try:
		aux = request.split(",", 1)
		separate = aux[1].lstrip(" ")
	except Exception as e:
		bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
		return
	
	if aux[0] in ['loona','Loona','LOONA']:
		aux[0] = 'loo'
	if aux[0] in ['april','April','APRIL']:
		aux[0] = 'april-k-pop'
	if aux[0] in ['florence + the machine', 'Florence + The Machine', 'Florence + the machine']:
		aux[0] = 'florence-and-the-machine'
	
	try:		
		normalize_artist = normalize('NFKD', aux[0]).encode('ASCII','ignore').decode('ASCII')
		normalize_song = normalize('NFKD', separate).encode('ASCII','ignore').decode('ASCII')
		artist = normalize_artist.replace(" ", "-")
		song_step1 = normalize_song.replace(",", "-")
		song_step2 = song_step1.replace(" ", "-")
		song = song_step2.replace("--", "-")	
	except Exception as e:
		bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
		return	
		
	print(get_user + " pediu por " + artist + " - " + song)
	
	try:
		url = "https://api.vagalume.com.br/search.php" + "?art=" + artist + "&mus=" + song + "&apikey={API_VAGALUME}"
		response = urllib.request.urlopen(url) #abrir a URL que informa as letras	
		data = json.loads(response.read()) #carregar o json e ler os valores
	except Exception as e:
		bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou por " + artist + " e " + song)
		return		
	try:	
		f_artist = data['art']['name']
		f_song = data['mus'][0]['name']	
		f_letra = data['mus'][0]['text']
	except Exception as e:
		bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou por " + artist + " e " + song)
		return	
		
	if len(f_letra) > 3000:
		letra_split = util.split_string(f_letra, 3000)
		bot.send_message(message.chat.id, "`" + f_artist + " - " + f_song + "`" + "\n\n" + letra_split[0], parse_mode='Markdown')
		for text in letra_split:
			bot.send_message(message.chat.id, text)
	else: 
		bot.send_message(message.chat.id, "`" + f_artist + " - " + f_song + "`" + "\n\n" + f_letra, parse_mode='Markdown')		
	
#COMANDO LYRICS_RANDOM
#Ainda na API do Vagalume, é um comando por diversão, que pega apenas um par de versos aleatórios de uma música
#Pode servir para, por exemplo, conseguir uma frase engraçada ou gerar uma legenda para uma foto

@bot.message_handler(commands=['lyrics_random'])
def send_lyricsmin_welcome(message):	
	a = telebot.util.extract_arguments(message.text)
	if not a:	
		if message.chat.type == "private":
			msg = bot.reply_to(message, "Digite o nome do artista e a música, separados por uma vírgula (Ex: The Weeknd, Blinding Lights): ")
			bot.register_next_step_handler(msg, process_lyricsmin_step) 
		else:
			bot.send_message(message.chat.id,"Esse comando não é apropriado para ser usado em grupos. Se ainda quiser usá-lo, peça diretamente junto ao comando, como por exemplo escrevendo: /lyrics_random U2, One.")		
			
	else:		
			
		request = a
		get_user = message.from_user.username
		try:
			aux = request.split(",", 1)
			separate = aux[1].lstrip(" ")
		except Exception as e:
			bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
			return
			
		if aux[0] in ['loona','Loona','LOONA']:
			aux[0] = 'loo'
		if aux[0] in ['april','April','APRIL']:
			aux[0] = 'april-k-pop'
		if a in ['florence + the machine', 'Florence + The Machine', 'Florence + the machine']:
			a = 'florence-and-the-machine'

		try:
			normalize_artist = normalize('NFKD', aux[0]).encode('ASCII','ignore').decode('ASCII')
			normalize_song = normalize('NFKD', separate).encode('ASCII','ignore').decode('ASCII')
			artist = normalize_artist.replace(" ", "-")
			song_step1 = normalize_song.replace(",", "-")
			song_step2 = song_step1.replace(" ", "-")
			song = song_step2.replace("--", "-")	
		except Exception as e:
			bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
			return	
		
		print(get_user + " pediu por " + artist + " " + song + " versão minimalista")
	
		try:
			url = "https://api.vagalume.com.br/search.php" + "?art=" + artist + "&mus=" + song + "&apikey={API_VAGALUME}"
			response = urllib.request.urlopen(url) #abrir a URL que informa as letras	
			data = json.loads(response.read()) #carregar o json e ler os valores
		except Exception as e:
			bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
			print("Bot encontrou um erro em Lyrics Minimalistas, quando " + get_user + " pesquisou por " + artist + " e " + song)
			return	
	
		try:
			f_artist = data['art']['name']
			f_song = data['mus'][0]['name']	
			f_letra = data['mus'][0]['text']
		except Exception as e:
			bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
			print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou por " + artist + " e " + song)
			return	
			
		#essa etapa é para juntar estrofes, já que são divididas por duas quebras de linha
		letra_random = f_letra.replace("\n\n", "\n")	
		#agora, salva numa array cada verso da música, dividindo a cada quebra de linha	
		x = letra_random.split("\n")
		y = len(x)
		#tira 2 para que ele não pegue o último verso da música e não retorne só um
		cont = random.randint(0, y-2)
		cont2 = cont+1	
		bot.send_message(message.chat.id, "`" + f_artist + " - " + f_song + " (Minimalist Version, by TheLearningBot)" + "`" + "\n\n" + x[cont] + "\n" + x[cont2], parse_mode='Markdown')
	
def process_lyricsmin_step(message):
	request = message.text
	get_user = message.from_user.username		
	
	try:
		aux = request.split(",", 1)
		separate = aux[1].lstrip(" ")
	except Exception as e:
		bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
		return
		
	if aux[0] in ['loona','Loona','LOONA']:
		aux[0] = 'loo'
	if aux[0] in ['april','April','APRIL']:
		aux[0] = 'april-k-pop'
	if a in ['florence + the machine', 'Florence + The Machine', 'Florence + the machine']:
			a = 'florence-and-the-machine'

	try:
		normalize_artist = normalize('NFKD', aux[0]).encode('ASCII','ignore').decode('ASCII')
		normalize_song = normalize('NFKD', separate).encode('ASCII','ignore').decode('ASCII')
		artist = normalize_artist.replace(" ", "-")
		song_step1 = normalize_song.replace(",", "-")
		song_step2 = song_step1.replace(" ", "-")
		song = song_step2.replace("--", "-")
				
	except Exception as e:
		bot.reply_to(message, "Eita... parece que você não fez corretamente seu pedido. Tente digitar igual ao exemplo, por favor.")
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou errado por " + request)
		return	
		
	print(get_user + " pediu por " + artist + " " + song + " versão minimalista")
	
	try:
		url = "https://api.vagalume.com.br/search.php" + "?art=" + artist + "&mus=" + song + "&apikey={API_VAGALUME}"
		response = urllib.request.urlopen(url) #abrir a URL que informa as letras	
		data = json.loads(response.read()) #carregar o json e ler os valores
	except Exception as e:
		bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
		print("Bot encontrou um erro em Lyrics Minimalistas, quando " + get_user + " pesquisou por " + artist + " e " + song)
		return	
	
	try:
		f_artist = data['art']['name']
		f_song = data['mus'][0]['name']	
		f_letra = data['mus'][0]['text']
	except Exception as e:
		bot.reply_to(message, "Uepa! Parece que eu não consegui encontrar o artista ou a música que você quer. Confira se você não digitou errado, ou se o artista/música consta no site do Vagalume, e tente novamente. É preciso digitar o nome exatamente como ele consta lá!")	
		print("Bot encontrou um erro em Lyrics, quando " + get_user + " pesquisou por " + artist + " e " + song)
		return	
			
	letra_random = f_letra.replace("\n\n", "\n")		
	x = letra_random.split("\n")
	y = len(x)
	cont = random.randint(0, y-2)
	cont2 = cont+1	
	bot.send_message(message.chat.id, "`" + f_artist + " - " + f_song + " (Minimalist Version, by TheLearningBot)" + "`" + "\n\n" + x[cont] + "\n" + x[cont2], parse_mode='Markdown')	

#faz com que o bot não pare caso haja muitos pedidos, porém espere um pouco
bot.polling(none_stop=True, timeout=20)
























































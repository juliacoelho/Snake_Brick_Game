#Python 2.7.6
from Tkinter import *
import random

class Cobra:
    def __init__(self, canvas):
        self.canvas = canvas
        self.L = [[170,200],[180,200],[190,200]]
        self.C = [200,200]
        self.dircabeca = PhotoImage(file = "cabecinhadireita.gif")
        self.corpo = PhotoImage(file = "corpocobra.gif")
        self.direita = PhotoImage(file = "cabecinhadireita.gif")
        self.esquerda = PhotoImage(file = "cabecinhaesquerda.gif")
        self.baixo = PhotoImage(file = "cabecinhabaixo.gif")
        self.cima = PhotoImage(file = "cabecinhacima.gif")
    def andar(self, direcao, coordenadas, imagemcomida, coordenadasinimigo, imageminimigo, inimigonatela):
        self.inimigonatela = inimigonatela
        self.coordenadasinimigo = coordenadasinimigo
        self.imageminimigo = imageminimigo
        self.direcao = direcao
        self.coordenadas = coordenadas
        self.imagemcomida = imagemcomida
        self.canvas.delete(ALL)
        if self.inimigonatela:
            f = self.canvas.create_image(self.coordenadasinimigo[0], self.coordenadasinimigo[1], image = self.imageminimigo)
        for e in range(len(self.L)):
            a = self.canvas.create_image(self.L[e][0], self.L[e][1], image = self.corpo)
        b = self.canvas.create_image(self.C[0],self.C[1], image = self.dircabeca)
        if not self.C == self.coordenadas:
            e = self.canvas.create_image(self.coordenadas[0], self.coordenadas[1], image = self.imagemcomida)
            self.L.pop(0)
        if (self.C[0] > 390) or (self.C[0] < 10) or (self.C[1] > 390) or (self.C[1] < 10):
            aplicativo.gameover()
        if self.C in self.L:
            aplicativo.gameover()
        if self.C == self.coordenadasinimigo:
            aplicativo.gameover()
        self.L.append([self.C[0],self.C[1]])
        if self.C == self.coordenadas:
            aplicativo.comidanatela = False
        if self.direcao == "Direita":
            self.C[0] += 10
            self.dircabeca = self.direita
        if self.direcao == "Esquerda":
            self.C[0] -= 10
            self.dircabeca = self.esquerda
        if self.direcao == "Baixo":
            self.C[1] += 10
            self.dircabeca = self.baixo
        if self.direcao == "Cima":
            self.C[1] -= 10
            self.dircabeca = self.cima
        
  
class Game(Frame):
    def __init__(self):
        self.direcao = "Direita"
        self.tk = Tk()
        self.tk.geometry("400x400+100+100")     
        self.tk.title("Snake")
        self.inicio = PhotoImage(file = "snake_abertura.gif")
        self.over = PhotoImage(file = "gameover.gif")
        self.canvas = Canvas(self.tk,width=400,height=400,bg = "Green")
        self.canvas.pack()
        self.pausa = True
        self.comidanatela = False
        self.inimigonatela = False
        self.coordenadasinimigo = [300, 300]
        self.imageminimigo = PhotoImage(file = "fantasma.gif")
        self.iniciado = False
        self.rodando = False
    def start(self):
        self.rodando = True
        #self.root = self.tk
        self.cobra = Cobra(self.canvas)
        self.comida = Comidinha()
        self.inimigo = Comidinhadomal()
        self.gameloop()
        self.tk.after(500, self.apareceinimigo)
        self.iniciado = True
    def novojogo(self, e):
        if not self.rodando:
            if self.iniciado == False:
                self.start()
                self.iniciado = True
                #print "if"
            else:
                self.pausa = True
                self.cobra = Cobra(self.canvas)
                self.comida = Comidinha()
                self.inimigo = Comidinhadomal()
                self.rodando = True
                self.gameloop()
                #print "else"
            #print "nada"
    def apareceinimigo(self):
        self.coordenadasinimigo = self.inimigo.inimigoaparece()
        self.imageminimigo = self.inimigo.inimigoqualimagem()
        if not (self.coordenadasinimigo == self.cobra.C or self.coordenadasinimigo in self.cobra.L):
            self.inimigonatela = True
        self.tk.after(8000, self.someinimigo)
    def someinimigo(self):
        self.inimigonatela =  False
        self.tk.after(5000, self.apareceinimigo)
    def prabaixo(self, e):
        if self.direcao != "Cima":
            self.direcao = "Baixo"
    def pradireita(self, e):
        if self.direcao != "Esquerda":
            self.direcao = "Direita"
    def praesquerda(self, e):
        if self.direcao != "Direita":
            self.direcao = "Esquerda"
    def pracima(self, e):
        if self.direcao != "Baixo":
            self.direcao = "Cima"
    def gameloop(self):
        if self.comidanatela == False:
            self.coordenadas = self.comida.aparece()
            self.imagemcomida = self.comida.qualimagem()
            self.comidanatela = True
        self.cobra.andar(self.direcao, self.coordenadas, self.imagemcomida, self.coordenadasinimigo, self.imageminimigo, self.inimigonatela)
        self.canvas.bind_all("<Down>", self.prabaixo)
        self.canvas.bind_all("<Right>", self.pradireita)
        self.canvas.bind_all("<Left>", self.praesquerda)
        self.canvas.bind_all("<Up>", self.pracima)
        self.canvas.bind_all("<space>", self.pausar)
        self.canvas.bind_all("<Escape>", self.fechar)
        if self.pausa:
            self.tk.after(80, self.gameloop)
    def pausar(self, e):
        self.pausa = not self.pausa
        if self.pausa:
            self.gameloop()
    def abertura(self):
        a = self.canvas.create_image(200, 200, image = self.inicio)
        self.canvas.bind_all("<Return>", self.novojogo)
    def fechar(self, e):
        self.tk.destroy()
    def gameover (self):
        self.pausar(self)
        self.canvas.delete(ALL)
        c = self.canvas.create_image(200, 200, image = self.over)
        self.direcao = "Direita"
        self.rodando = False
            
class Comidinha:
    def __init__(self):
        self.banana = PhotoImage(file = "banana.gif")
        self.coracao = PhotoImage(file = "coracao.gif")
        self.maca = PhotoImage(file = "maca.gif")
        self.melancia = PhotoImage(file = "melancia.gif")
        self.moeda = PhotoImage(file = "moeda.gif")
    def aparece(self):
        self.coordenadax = random.choice(range(10,400,10))
        self.coordenaday = random.choice(range(10,400,10))
        return [self.coordenadax, self.coordenaday]
    def qualimagem(self):
        self.imagem = random.choice([self.banana, self.coracao, self.maca, self.melancia, self.moeda])
        return self.imagem

class Comidinhadomal:
    def __init__(self):
        self.fantasma = PhotoImage(file = "fantasma.gif")
        self.caveira = PhotoImage(file = "caveira.gif")
        self.bomba = PhotoImage(file = "bomba.gif")
    def inimigoaparece(self):
        self.coordenadax = random.choice(range(10,400,10))
        self.coordenaday = random.choice(range(10,400,10))
        return [self.coordenadax, self.coordenaday]
    def inimigoqualimagem(self):
        self.imagem = random.choice([self.fantasma, self.caveira, self.bomba])
        return self.imagem


aplicativo = Game()
aplicativo.abertura()
mainloop()




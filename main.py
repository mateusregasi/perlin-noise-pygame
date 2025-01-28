import pygame as pg
from pygame.locals import *
from grid import Perlin

# Variáveis
TAM = 1000
SCALE = 5
PIXEL = 20
JUMP = 0.04
SEED = 10
HEIGHT, WIDTH = DIM = (TAM, TAM)


# Janela
pg.init()
window = pg.display.set_mode(DIM)
pg.display.set_caption("PerlinNoise")

# Instância do frid do Perlin Noise
grid = Perlin(WIDTH, HEIGHT, SCALE, PIXEL,JUMP, SEED)

# Game Loop
while True:

	# Sair da janela
	for event in pg.event.get():
		if event.type == QUIT: 
			pg.quit()
			exit

	# Pinta a tela de preto
	window.fill((0,0,0))

	# Desenha o grid
	grid.draw(window)

	# Atualiza a tela
	pg.display.update()
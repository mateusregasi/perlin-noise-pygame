from math import floor, sin, cos, pi
import random

import pygame as pg
from pygame.locals import *

# Classe do Perlin Noise
class Perlin:
    def __init__ (self, width, height, scale=1, pixel=1, jump=0.1, seed=1):
        self.w = width
        self.h = height
        self.wg = width // pixel
        self.hg = height // pixel
        self.scale = scale
        self.pixel = pixel
        self.jump = jump
        self.seed = seed
        self.factor = 0.67
        self.generate_angles(seed)
        self.generate_perlin_noise(self.wg, self.hg, self.scale)

    # Gera os ângulos para os vetores gradiente
    def generate_angles(self, seed):
        self.angles = []
        random.seed = seed
        for y in range(self.hg):
            row = []
            for x in range(self.wg):
                row.append(2*random.random())
            self.angles.append(row)

    # Gera o grid do perlin noise
    def generate_perlin_noise(self, width, height, scale):
        self.noise = []
        for y in range(height):
            row = []
            for x in range(width):
                nx = x / scale
                ny = y / scale
                row.append(self.perlin_noise(nx, ny))
            self.noise.append(row)
    
    # Altera o grid do Perlin Noise
    def alter_perlin_noise(self, x, y):
        self.noise[x][y] = self.perlin_noise(x / self.scale, y / self.scale)
    
    # Função principal de Perlin Noise
    def perlin_noise(self, x, y):

        # Define os vértices da grade
        x0 = floor(x)
        x1 = x0 + 1
        y0 = floor(y)
        y1 = y0 + 1
        
        # Pega os vetores dos vértices
        vec0 = self.angles[x0][y0]
        vec1 = self.angles[x1][y0]
        vec2 = self.angles[x0][y1]
        vec3 = self.angles[x1][y1]

        # Produto escalar dos vetores gradiente com vetores de deslocamento
        n00 = Perlin.dot_product_gradient(x0, y0, x, y, Perlin.getVector(vec0,1))
        n10 = Perlin.dot_product_gradient(x1, y0, x, y, Perlin.getVector(vec1,1))
        n01 = Perlin.dot_product_gradient(x0, y1, x, y, Perlin.getVector(vec2,1))
        n11 = Perlin.dot_product_gradient(x1, y1, x, y, Perlin.getVector(vec3,1))
        
        # Aplicar a função fade (suavizar o vetor do canto superior esquerdo até o ponto)
        u = Perlin.fade(x - x0)
        v = Perlin.fade(y - y0)
        
        # # Interpolação linear
        nx0 = Perlin.lerp(n00, n10, u)
        nx1 = Perlin.lerp(n01, n11, u)

        return Perlin.lerp(nx0, nx1, v)
    
    # Função de interpolação suave (fade)
    def fade(t): return t*t*t*(t*(t*6-15)+10)

    # Função para interpolação linear entre dois valores
    def lerp(a, b, t): return a + t * (b - a)
    
    # Pega o vetor à partir de um raio e um ângulo
    def getVector(a, r): return (cos(a*pi)*r, sin(a*pi)*r)

    # Função para calcular o produto escalar entre o vetores gradiente e de deslocamento
    def dot_product_gradient(ix, iy, x, y, vec): return vec[0]*(x-ix) + vec[1]*(y-iy)

    def draw_grid(self, surface):
        for x in range(0, self.wg):
            pg.draw.rect(surface, (255,255,255), (self.pixel*x, 0, 1, self.h))
        for y in range(0, self.hg):
            pg.draw.rect(surface, (255,255,255), (0, self.pixel*y, self.w, 1))

    # Desenha o Perlin Noise
    def draw(self, surface):
        for x in range(self.wg):
            for y in range(self.hg):

                # Define a cor
                c = (self.factor + self.noise[x][y])/(2*self.factor) * 255

                # Desenha o pixel
                pg.draw.rect(surface, (c,c,c), (x*self.pixel, y*self.pixel, (x+1)*self.pixel, (y+1)*self.pixel))

                # Atualiza o Perlin
                self.angles[x][y] = (self.angles[x][y] + self.jump) % 2
                self.alter_perlin_noise(x,y)
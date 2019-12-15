import pygame 
import random

class Balle:
    
    def __init__(self, x, y, rayon, direction):
        
        self.x = x 
        self.y = y 
        self.rayon = rayon 
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, self.rayon, self.rayon)
        self.random_direction = random.randint(1, 4)
        
    def mouvement(self, vitesse_x, vitesse_y):
        self.rect.x = (self.rect.x + vitesse_x * self.direction)
        self.rect.y += self.random_direction * vitesse_y
    
    def afficher(self, surface):
        
        pygame.draw.rect(surface, (230, 230, 230), self.rect)

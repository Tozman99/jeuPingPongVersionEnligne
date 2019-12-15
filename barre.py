import pygame 


class Barre:
    
    def __init__(self, x, y, taille):
        
        self.x = x 
        self.y = y 
        self.taille = taille 
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])
        
    def mouvement(self, vitesse):
        
        self.rect.y += vitesse 
        
    def afficher(self, surface):
        
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        
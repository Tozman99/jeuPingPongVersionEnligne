import pygame
import sys
import random
import math
import socket
import threading
from barre import Barre
from balle import Balle


class Jeu:

	def __init__(self):
		self.resolution = (900, 500)
		self.ecran = pygame.display.set_mode(self.resolution)
		pygame.display.set_caption('Ping Pong')
		self.jeu_encours = True
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ip, self.port = '127.0.0.1', 9999
		self.joueur_1_x, self.joueur_1_y = 20, 250
		self.joueur_2_x, self.joueur_2_y = 860, 250
		self.joueur_taille = [20, 80]
		self.vitesse_y_1, self.vitesse_y_2 = 0, 0
		self.joueur_1 = Barre(self.joueur_1_x, self.joueur_1_y, self.joueur_taille)
		self.joueur_2 = Barre(self.joueur_2_x, self.joueur_2_y, self.joueur_taille)
		self.direction_balle = [-1, 1]
		self.rect = pygame.Rect(0, 0, self.resolution[0], self.resolution[1])
		self.balle = Balle(450, 250, 10, random.choice(self.direction_balle))
		self.collision = False
		self.balle_vitesse_x, self.balle_vitesse_y = 15, 2
		self.balle_tire = False
		self.score_1, self.score_2 = 0, 0
		self.balle_x, self.balle_y = None, None
		self.joueur_1_position = 250
		self.reception_donnees = False

	def boucle_principale(self):

		self.client.connect((self.ip, self.port))
		self.creer_un_thread(self.recevoir_donnees)

		while self.jeu_encours:

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						self.vitesse_y_2 = -10
					if event.key == pygame.K_s:
						self.vitesse_y_2 = 10
					if event.key == pygame.K_SPACE:
						self.balle_tire = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_w:
						self.vitesse_y_2 = 0
					if event.key == pygame.K_s:
						self.vitesse_y_2 = 0

			if self.reception_donnees:
				self.balle.rect.x = self.balle_x
				self.balle.rect.y = self.balle_y
				self.joueur_1.rect.y = self.joueur_1_position

			self.joueur_1.mouvement(self.vitesse_y_1)
			self.joueur_2.mouvement(self.vitesse_y_2)
			position_y_joueur_2 = f"{self.joueur_2.rect.y}"
			self.client.send(position_y_joueur_2.encode('utf-8'))
			self.joueur_1.rect.clamp_ip(self.rect)
			self.joueur_2.rect.clamp_ip(self.rect)
			self.reception_donnees = True
			self.ecran.fill((50, 50, 50))
			self.creer_message('moyenne', 'Jeu Pong', [330, 50, 20, 20], (255, 255, 255))
			self.creer_message('grande', f" {self.score_1}", [300, 200, 50, 50], (255, 255, 255))
			self.creer_message('grande', f" {self.score_2}", [485, 200, 50, 50], (255, 255, 255))
			self.joueur_1.afficher(self.ecran)
			self.joueur_2.afficher(self.ecran)
			self.balle.afficher(self.ecran)
			pygame.display.flip()

	def changement_balle_direction(self, vitesse, angle):
		vitesse = -(vitesse * math.cos(angle))

		return vitesse

	def creer_message(self, font, message, message_rectangle, couleur):

		"""
		:param: font
		:param: message
		:param: message_rectangle
		:param: couleur
		"""
		if font == 'petite':
			font = pygame.font.Font('/Users/karimsadiki/PycharmProjects/Ping_Pong_Game/ATARCC__.TTF', 20)

		elif font == 'moyenne':
			font = pygame.font.Font('/Users/karimsadiki/PycharmProjects/Ping_Pong_Game/ATARCC__.TTF', 30)

		elif font == 'grande':
			font = pygame.font.Font('/Users/karimsadiki/PycharmProjects/Ping_Pong_Game/ATARCC__.TTF', 40)

		message = font.render(message, True, couleur)

		self.ecran.blit(message, message_rectangle)

	def creer_un_thread(self, cible):

		thread = threading.Thread(target=cible)
		thread.daemon = True
		thread.start()

	def recevoir_donnees(self):

		while True:
			donnees_recus = self.client.recv(128).decode('utf-8')
			donnees_recus = donnees_recus.split(',')
			self.joueur_1_position = int(donnees_recus[0])
			self.balle_x = int(donnees_recus[1])
			self.balle_y = int(donnees_recus[2])
			self.score_1, self.score_2 = int(donnees_recus[3]), int(donnees_recus[4])



if __name__ == '__main__':
	pygame.init()
	Jeu().boucle_principale()
	pygame.quit()
import pygame, sys, os, math
from pygame.locals import *

class Character(pygame.sprite.Sprite):
	def load_sliced_sprites(self,w,h,image_name):
		images = []
		try:
			master_image = pygame.image.load(image_name)
		except pygame.error, message:
			print "Cannot load image: " + image_name
			raise SystemExit, message
		master_width, master_height = master_image.get_size()
		for i in xrange(int(master_width/w)):
			images.append(master_image.subsurface((i*w,0,w,h)))
			print i
		return images

	def __init__(self, screen, img_filename, init_x, init_y):
		pygame.sprite.Sprite.__init__(self) 
		self.screen = screen

		self.image = self.load_sliced_sprites(20,20,img_filename)

		self.image_w, self.image_h = self.image[0].get_size()

		self.x = init_x
		self.y = init_y
		self.hspeed = 0
		self.image_index = 0
		self.image_timer = 0

	def run(self,direction):
		if abs(self.hspeed) <= 5:
			self.hspeed += .5*direction 

	def decelerate(self):
		if abs(self.hspeed) > .1:
			self.hspeed /= 1.2
		else:
			self.hspeed = 0

	def update(self):
		keystate = pygame.key.get_pressed()

		if keystate[K_LEFT] and not keystate[K_RIGHT]:
    			self.run(-1)
		elif keystate[K_RIGHT] and not keystate[K_LEFT]:
			self.run(1)			
		else:
			self.decelerate()

		self.x += self.hspeed
			

	def draw(self):	
		if abs(self.hspeed) > 0:
			self.image_timer += abs(self.hspeed)
			if self.image_timer > 30:
				self.image_index += 1
				self.image_timer = 0
			if self.image_index > 7: 
				self.image_index = 0
		else:
			self.image_index = 8

		draw_pos = self.image[self.image_index].get_rect().move(self.x - self.image_w / 2, self.y - self.image_h / 2)
		self.image[self.image_index] = pygame.transform.scale(self.image[self.image_index],(3*self.image_w,3*self.image_h))
		self.screen.blit(self.image[self.image_index], draw_pos)

if __name__ == "__main__":
	pygame.init()
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	screenDimensions = (SCREEN_WIDTH,SCREEN_HEIGHT)
	window = pygame.display.set_mode(screenDimensions)
	pygame.display.set_caption('Barbarian?!')
	screen = pygame.display.get_surface()

	FPS = 60
	BACKGROUND_COLOR = (130,130,130)
	barbara = Character(screen,'runstrip.gif',SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
	facing = 1
	pygame.mixer.music.load('killertomato.mod')
	pygame.mixer.music.play(1)
	while True:
		pygame.time.Clock().tick(FPS)	
		screen.fill(BACKGROUND_COLOR)
		
		barbara.update()
		
		barbara.draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_LEFT and facing == 1:
					for frame in range(9):
						barbara.image[frame] = pygame.transform.flip(barbara.image[frame],1,0)
						facing = 0
				
				if event.key == K_RIGHT and facing == 0:
					for frame in range(9):
						barbara.image[frame] = pygame.transform.flip(barbara.image[frame],1,0)
						facing = 1
					
			
		

		pygame.display.flip()



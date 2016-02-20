import pygame
from pygame.locals import *

##
def blurTrans(clock,screen,oldScreen,newScreen):
	time = 0
	trans = True
	
	while trans:
		tick = clock.tick()/1000.0
		if time < .5:
			temp = pygame.transform.scale(pygame.transform.scale(oldScreen,(int(160-(310*time)),int(120-(230*time)))),(320,240))
			screen.blit(temp,(0,0))
			time+=tick
			screen.update()
			pygame.display.update()
		elif time < 1:
			temp = pygame.transform.scale(pygame.transform.scale(newScreen,(int(5+(630*(time-.5))),int(5+(470*(time-.5))))),(320,240))
			screen.blit(temp,(0,0))
			time+=tick
			screen.update()
			pygame.display.update()
		else:
			trans = False

def fadeBlackTrans(screen,oldScreen,newScreen,fadeTime,pauseTime):
	time = 0
	trans = True
	clock = pygame.time.Clock()
	
	while trans:
		tick = clock.tick()/1000.0
		if time < fadeTime:
			screen.blit(oldScreen,[0,0])
			screen.fill([255-(255*(time/fadeTime))]*3,special_flags=BLEND_RGB_MULT)
			time+=tick
			screen.update()
			pygame.display.update()
		elif time < fadeTime+pauseTime:
			screen.fill([0,0,0])
			time+=tick
			screen.update()
			pygame.display.update()
		elif time < (2*fadeTime)+pauseTime:
			screen.blit(newScreen,[0,0])
			screen.fill([(255*((time-(fadeTime+pauseTime))/fadeTime))]*3,special_flags=BLEND_RGB_MULT)
			time+=tick
			screen.update()
			pygame.display.update()
		else:
			trans = False

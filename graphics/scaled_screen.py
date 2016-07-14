import pygame

import config

## A window that emulates a smaller python window.
class ScaledScreen(object):
	
	## Constructor.
	#  @param screen Reference to pygame screen object.
	#  @param actualResX Horizontal resolution of pygame window.
	#  @param actualResY Vertical resolution of pygame window.
	#  @param smoothing
	#  @parblock
	#  Smoothing type to use.
	#
	#       Smoothing Types:
	#         0 = No smoothing.
	#         1 = 2x smoothing.
	#         2 = Full smoothing.
	#
	#  @endparblock
	def __init__(self,screen,actualResX,actualResY):
		self.scaledScreen=screen
		self.aResX=actualResX
		self.aResY=actualResY
		self.screen=pygame.surface.Surface((320,240))
		if config.Smoothing==1:
			self.aResX=640
			self.aResY=480
	
	## Updates the pygame screen by scaling the internal screen.
	def update(self):
		if config.Smoothing==0:
			pygame.transform.scale(self.screen,(self.aResX,self.aResY),self.scaledScreen)
		elif config.Smoothing==1:
			pygame.transform.scale2x(self.screen,self.scaledScreen)
		elif config.Smoothing==2:
			pygame.transform.smoothscale(self.screen,(self.aResX,self.aResY),self.scaledScreen)
	
	## Functions the same as pygame.Surface.fill().
	#  @param color Color to fill screen.
	#  @param rect Rectangle to fill within, if @c None then fill entire screen.
	#  @param special_flags Fill mode, see Pygame documentation.
	def fill(self,color,rect=None,special_flags=0):
		if rect!=None:
			if rect[0]<0:
				rect[2]-=abs(rect[0])
			if rect[1]<0:
				rect[3]-=abs(rect[1])
		self.screen.fill(color,rect,special_flags)
	
	## Functions the same as pygame.Surface.fill().
	#  @param source Source image to copy
	#  @param dest Destination location to copy image to on screen.
	#  @param area Area of source to copy, if @c None then copy entire image.
	#  @param special_flags Copy mode, see Pygame documentation.
	def blit(self,source,dest,area=None,special_flags=0):
		self.screen.blit(source,dest,area,special_flags)
	
	## Functions the same as pygame.Surface.copy().
	def copy(self,*args):
		return self.screen.copy(*args)

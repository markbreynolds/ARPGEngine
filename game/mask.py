import pygame

## Uses a threshold in order to create a mask from a surface.
def maskFromSurface(surface,mustBeAbove=127):
	surface.lock()
	mask = pygame.mask.Mask(surface.get_size())
	for x in range(surface.get_width()):
		for y in range(surface.get_height()):
			if surface.get_at((x,y))[0]>mustBeAbove:
				mask.set_at((x,y),1)
	return mask

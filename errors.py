## @package errors
#  Documentation for the Errors Module.
#
#  This module contains the code related to custom game errors and logging
#

import logging

## This variable ensures that only one ErrorEngine is created.
errorEngineSingleton = None

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

def getLogger():
	return errorEngineSingleton.getLogger()

## This class handles all errors and warnings.
#
#  It will also ensure that all errors and warnings logged to their appropiate destinations.
class ErrorEngine(object):
	
	## Constructor
	#
	#  @param screen A reference to the screen to be used in case of a fatal error.
	def __init__(self,screen,level=logging.WARNING,logToFile=False,quiet=True):
		global errorEngineSingleton
		if errorEngineSingleton != None:
			errorEngineSingleton.error("Attempted to create more than one ErrorEngine.",level="Warning")
			return errorEngineSingleton
		errorEngineSingleton = self
		self.screen = screen
		self.logger = logging.getLogger("GameLogger")
		if not quiet:
			self.sHandler=logging.StreamHandler()
			self.sHandler.setFormatter(logging.Formatter(fmt="File '%(filename)s', line %(lineno)s, in %(funcName)s\n  %(levelname)s: %(msg)s"))
			self.logger.addHandler(self.sHandler)
		else:
			self.sHandler = logging.NullHandler()
		if logToFile:
			self.fHandler=logging.StreamHandler()
			self.fHandler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(msg)s at %(filename)s:%(funcName)s: %(lineno)s"))
			self.logger.addHandler(self.fHandler)
		else:
			self.fHandler = logging.NullHandler()
		self.logger.setLevel(level)
	
	def getLogger(self):
		return self.logger
	
#	def criticalGameError(self):
#		while True:
#			self.screen.fill((0,0,0))
			

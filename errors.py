## @package errors
#  Documentation for the Errors Module.
#
#  This module contains the code related to custom game errors and logging
#

import logging

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

Logger = None
Screen = None

def genericError(msg,*args,**kwargs):
	print "Generic Error: "+msg

critical = genericError
error = genericError
warning = genericError
info = genericError
debug = genericError


## Initialization code
#
#  @param screen A reference to the screen to be used in case of a fatal error.
def init(screen,level=logging.WARNING,logToFile=False,quiet=True):
	global Screen, Logger
	Screen = screen
	Logger = logging.getLogger("GameLogger")
	if not quiet:
		sHandler=logging.StreamHandler()
		#sHandler.setFormatter(logging.Formatter(fmt="File '%(filename)s', line %(lineno)s, in %(funcName)s\n  %(levelname)s: %(msg)s"))
		sHandler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(msg)s"))
		Logger.addHandler(sHandler)
	else:
		sHandler = logging.NullHandler()
	if logToFile:
		fHandler=logging.StreamHandler()
		#fHandler.setFormatter(logging.Formatter(fmt="File '%(filename)s', line %(lineno)s, in %(funcName)s\n  %(levelname)s: %(msg)s"))
		fHandler.setFormatter(logging.Formatter(fmt="%(levelname)s: %(msg)s"))
		Logger.addHandler(fHandler)
	else:
		fHandler = logging.NullHandler()
	Logger.setLevel(level)

	global critical, error, warning, info, debug
	critical = Logger.critical
	error = Logger.error
	warning = Logger.warning
	info = Logger.info
	debug = Logger.debug

#def getLogger():
#	return Logger

#	def criticalGameError():
#		while True:
#			self.screen.fill((0,0,0))

"""
def critical(msg,*args,**kwargs):
	Logger.critical(msg,*args,**kwargs)

def error(msg,*args,**kwargs):
	Logger.error(msg,*args,**kwargs)

def warning(msg,*args,**kwargs):
	Logger.warning(msg,*args,**kwargs)

def info(msg,*args,**kwargs):
	Logger.info(msg,*args,**kwargs)

def debug(msg,*args,**kwargs):
	Logger.debug(msg,*args,**kwargs)
"""

## @package config
#  Documentation for the Configuration Module.
#
#  This module contains the code related configuration of the game.

## The directory that game assets are contained in.
AssetPath = "assets/"

## Background color of windows.
Color = (0,0,255)

## Outline color of windows.
ColorDark = (0,0,64)

## Color of text.
ColorFont = (255,255,255)

## Color of selected text.
ColorSel = (255,255,0)

## Color of bolded text.
ColorBold = (255,0,0)

## Color of disabled options.
ColorDisable = (127,127,127)

## How hard the game will be on a scale from 1-5 (easy to hard).
#
#  Affects various factors including:
#   + How often random battles occur. (Not implemented)
#   + How much stronger enemies will be than you. (Not implemented)
#
#  A difficulty of 0 can be used for test to make random battles not occur.
Difficulty = 1

## How much information should be put into logs.
#
# Here are the values for each level:
# CRITICAL = 50
# ERROR	= 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0
#
LogVerbosity = 20

## The size of the actual window.
ScreenSize = [640,480]

## Smoothing mode to use.
#
#  See ScaledScreen for more information.
Smoothing = 0

VersionString = "0.3.0a"

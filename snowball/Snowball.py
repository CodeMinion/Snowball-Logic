from FsmOwner import FsmOwner
from Fsm import Fsm 
from SbStateInitial import SbStateInitial

from KeyframeAnimations import *
from os import listdir
from os.path import isfile,

import json

class Snowball(FsmOwner):
	
	mPygameInstance = None
	mAnimationDict = {}
	
	def __init__(self, pygame):
		snowballFsm = Fsm(self, SbStateInitial())
		FsmOwner.__init__(self, snowballFsm)
		self.mPygameInstance = pygame
		
	def init(self):
		# Do any resource loading needed for Snowball
		for animFile in os.listdir("/assets/animations"):
			if animFile.endswith(".anim"):
				loadedAnimation = readJsonAnimFile(animFile)
				# Store animation in animation dictionary.
				mAnimationDict[loadedAnimation.getId()] = loadedAnimation
		pass
		

	def readJsonAnimFile(self, animFilePath):
		jsonFile = open(animFilePath)
		jsonAnimData = json.load(jsonFile)
		
		animId = jsonAnimData['id']
		spriteSheetSrc = jsonAnimData['spriteSheetSrc']
		frameLength = jsonAnimData['frameLength']
		isLooping = jsonAnimData['isLooping']
		keyframeList = jsonAnimData['keyframes']
		
		animKeyframeListOut = []
		for keyframe in keyframeList:
			sourceX = keyframe['sourceX']
			sourceY = keyframe['sourceY']
			sourceWidth = keyframe['sourceWidth']
			sourceHeight = keyframe['sourceHeight']
			
			animKeyframeOut = Keyframe(sourceX, sourceY, sourceWidth, sourceHeight)
			# Store in keyframe list. 
			animKeyframeListOut.append(animKeyframeOut)
		
		spriteSheet = self.mPygameInstance.image.load(spriteSheetSrc)
		outAnimation = AnimationStrip(animId, spriteSheet, animKeyframeListOut, frameLength, isLooping)
		
		return outAnimation

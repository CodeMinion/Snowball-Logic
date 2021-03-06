class Keyframe:
	
	mSourceY = 0
	mSourceX = 0
	mSourceWidth = 0
	mSourceHeight = 0
	
	def __init__(self, sourceX, sourceY, sourceWidth, sourceHeight):
		self.mSourceX = sourceX
		self.mSourceY = sourceY
		self.mSourceWidth = sourceWidth
		self.mSourceHeight = sourceHeight
		pass

	'''
	Returns the keyframe source information as 
	a tuple (x,y,width,height)
	'''
	def getSource(self):
		return (self.mSourceX, self.mSourceY, self.mSourceWidth, self.mSourceHeight)


########################################################
class AnimationStrip:
	
	mId = None
	mCurrentFame = -1
	mNextFrameUpdateTimeMillis = 0
	mIsLooping = False
	mKeyframesList = None
	mFrameLength = 0
	mSpriteSheet = None
	mIsFinished = False
	
	'''
	@param keyframeList: List of keyframes
	@param frameLength: Lenght in milliseconds of a single frame.
	@param loops: True if the animation will restart when it reaches the end.
	'''
	def __init__(self, animId, spriteSheet, keyframeList, frameLength, loops = False):
		self.mId = animId
		self.mKeyframesList = keyframeList
		self.mFrameLength = frameLength
		self.mIsLooping = loops
		self.mSpriteSheet = spriteSheet
		pass
		
	def start(self):
		self.mCurrentFame = -1
		self.mNextFrameUpdateTimeMillis = 0
		self.mIsFinished = False
	'''
	Updates the animation by moving stepping the current frame forward
	if it's time.
	'''
	def update(self, timeMillis):
		
		if timeMillis > self.mNextFrameUpdateTimeMillis:
			# Update keyframe forward
			self.mCurrentFame = self.mCurrentFame + 1
			
			if self.mCurrentFame >= len(self.mKeyframesList):
				if self.mIsLooping:
					self.mCurrentFame = 0
				else: 
					self.mCurrentFame = len(self.mKeyframesList) -1
					self.mIsFinished = True
			
			# Prepare next update
			self.mNextFrameUpdateTimeMillis = timeMillis + self.mFrameLength
			pass
		
		pass
	
	'''
	Returns the current frame of the animation or None if the animation
	has not started yet. 
	'''	
	def getCurrentFrame(self):
		if self.mCurrentFame < 0 : 
			return None
			 
		return self.mKeyframesList[self.mCurrentFame]		
		
	'''
	Returns the spriteSheet for this animation resource for this animation.
	'''
	def getSpriteSheet(self):
		return self.mSpriteSheet
		
	'''
	Identifier of this animation
	'''
	def getId(self):
		return self.mId

	'''
	Returns whether the animation is finished playing or not. 
	Note: Animations with isLooping = True will always return False.
	'''
	def isFinished(self):
		return self.mIsFinished

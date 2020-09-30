class Game_status:
	"""Class contains game status"""
	def __init__(self,gsets):
		self.gsets = gsets
		self.game_active = False
		self.score = 0
		self.high_score = gsets.saved_high_score
		self.level = 1
		self.reset_status()

	def reset_status(self):
		"""Reset the ship count"""
		self.ships_left = self.gsets.ship_limit


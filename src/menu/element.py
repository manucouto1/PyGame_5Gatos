
class ElementGUI:

	def __init__(self, screen, rectangle):
		# save reference to screen and position it's belong
		self.screen = screen
		self.rect = rectangle

	def set_position(self, position):
		# method for situate the element on screen
		(position_x, position_y) = position
		self.rect.left = position_x
		self.rect.bottom = position_y

	def position_elem(self, position):
		# method that says if it's been clicked
		(position_x, position_y) = position
		if (position_x >= self.rect.left) and (position_x <= self.rect.right) and (position_y >= self.rect.top) and (position_y <= self.rect.bottom):
			return True
		else:
			return False

	# abstract methods
	def draw(self, screen):
		raise NotImplemented("You have to implement method draw.")

	def action(self):
		raise NotImplemented("You have to implement method action.")
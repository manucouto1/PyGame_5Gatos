
class ElementGUI:
	"""
	Class to create screen interaction elements

	:param screen: reference to the screen that the element belongs to
	:param rectangle: position of the element (x, y)
	"""
	def __init__(self, screen, rectangle):
		# save reference to screen and position it's belong
		self.screen = screen
		self.rect = rectangle

	def set_position(self, position):
		"""
		Method to place the element on the screen

		:param position: position of the element (x, y)
		"""
		(position_x, position_y) = position
		self.rect.left = position_x
		self.rect.bottom = position_y

	def position_elem(self, position):
		"""
		Method that tells if the element has been clicked

		:param position: position of the element (x, y)
		"""
		(position_x, position_y) = position
		if (position_x >= self.rect.left) and (position_x <= self.rect.right) and (position_y >= self.rect.top) and (position_y <= self.rect.bottom):
			return True
		else:
			return False

	"""
	Abstract methods
	"""
	def draw(self, screen):
		"""
		Method to draw the element on screen

		:param screen: reference to the screen that the element belongs to
		"""
		raise NotImplemented("You have to implement method draw.")

	def action(self):
		"""
		Method to indicate the action triggered by clicking on the element

		"""
		raise NotImplemented("You have to implement method action.")

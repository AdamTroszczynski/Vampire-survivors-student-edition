class Enemy:
  def __init__(self, position, type):
    self.position = position
    self.type = type
    if type == 1:
      self.speed = 100
      self.hp = 30
    elif type == 2:
      self.speed = 50
      self.hp = 60
    elif type == 3:
      self.speed = 250
      self.hp = 10
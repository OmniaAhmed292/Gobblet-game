class Rock:
  size: int # 1 = small, 2 = medium, 3 = large
  id: int # refer to the player own this rock
  def __init__(self, size: int, id) -> None:
    self.size = size
    self.id = id
class Rock:
  size: int # 1 = small, 2 = medium, 3 = large
  id: int # refer to the player own this rock
  pile_no: int # refer to the number of pile
  def __init__(self, size: int, id,pile_no=0) -> None:
    self.size = size
    self.id = id
    self.pile_no = pile_no
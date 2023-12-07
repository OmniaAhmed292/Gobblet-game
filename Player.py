import Pile


class Player:
  name: str
  piles: list[Pile]
  id: int

  def __init__(self, name, id) -> None:
    self.name = name
    self.id = id
    self.piles = [Pile(True, id),Pile(True, id),Pile(True, id),Pile(True, id)]
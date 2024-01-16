from Pile import Pile


class Player:
  name: str
  piles: list[Pile]
  id: int
  turns: int

  def __init__(self, name, id) -> None:
    self.name = name
    self.id = id
    self.piles = [Pile(0,True, id),Pile(1,True, id),Pile(2,True, id)]
    self.turns = 0
from Pile import Pile


class Player:
  """
  Represents a player in the Gobblet game.
  """
  name: str
  piles: list[Pile]
  id: int

  """""
  Initializes a new instance of the Player class.
  Args:
    name (str): The name of the player.
    id (int): The ID of the player.
  """""
  def __init__(self, name, id) -> None:
    self.name = name
    self.id = id
    self.piles = [Pile(True, id),Pile(True, id),Pile(True, id)]

  """
  checks if the player's pile is empty
  returns:
    bool: True if the player's pile is empty, False otherwise
  """
  def is_pile_empty(self):
    for pile in self.piles:
      if pile.size() != 0:
        return False
    return True
    
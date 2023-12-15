from Rock import Rock


class Pile:
  """
  Represents a pile of rocks in the Gobblet game.
  """

  rocks: list[Rock]   # stack of rocks sorted from large to small

  def __init__(self, is_player=False, id=None) -> None:
    """
    Initializes a new instance of the Pile class.

    Args:
      is_player (bool, optional): Indicates if the pile belongs to a player. Defaults to False.
      id (any, optional): Identifier for the pile. Defaults to None.
    """
    self.rocks = []
    if is_player:
      self.rocks.append(Rock(1, id))
      self.rocks.append(Rock(2, id))
      self.rocks.append(Rock(3, id))
      self.rocks.append(Rock(4, id))

  def push(self, rock: Rock) -> None:
    """
    Pushes a rock onto the pile.

    Args:
      rock (Rock): The rock to be pushed onto the pile.

    Raises:
      Exception: If the rock being added is smaller than the rocks already in the pile.
    """
    if not self.rocks or self.rocks[-1].size < rock.size:
      self.rocks.append(rock)
    else:
      raise Exception("Cannot add small rock into larger ones")

  def pop(self) -> Rock:
    """
    Removes and returns the topmost rock from the pile.

    Returns:
      Rock: The topmost rock from the pile.

    Raises:
      Exception: If the pile is empty and there are no rocks to remove.
    """
    if self.rocks:
      return self.rocks.pop()
    else:
      raise Exception("Cannot remove from empty space")

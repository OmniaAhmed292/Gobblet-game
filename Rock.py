class Rock:
  
  """
  Represents a rock in the Gobblet game.
  """

  size: int  # 1 = small, 2 = medium, 3 = large
  id: int  # refers to the player who owns this rock

  def __init__(self, size: int, id: int, pile_no: int) -> None:
    """
    Initializes a new Rock object.

    Args:
      size (int): The size of the rock (1 = small, 2 = medium, 3 = large).
      id (int): The ID of the player who owns this rock.
    """
    self.size = size
    self.id = id
    self.pile_no = pile_no
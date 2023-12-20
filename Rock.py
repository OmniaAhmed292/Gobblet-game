class Rock:
  """
  Represents a rock in the Gobblet game.

  Attributes:
    size (int): The size of the rock (1 = small, 2 = medium, 3 = large).
    id (int): The ID of the player who owns this rock.

  methods:
    __init__(self, size: int, id: int) -> None:
      Initializes a new Rock object.
  """

  size: int  # 1 = small, 2 = medium, 3 = large
  id: int  # refers to the player who owns this rock

  def __init__(self, size: int, id: int) -> None:
    """
    Initializes a new Rock object.

    Args:
      size (int): The size of the rock (1 = small, 2 = medium, 3 = large).
      id (int): The ID of the player who owns this rock.
    """
    if size < 1 or size > 3:
      raise Exception("Invalid rock size")
    self.size = size
    self.id = id

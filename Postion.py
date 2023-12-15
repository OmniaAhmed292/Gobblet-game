class Postion:
  """
  Represents a position with x and y coordinates.
  """

  x: int
  y: int

  def __init__(self, x, y) -> None:
    """
    Initializes a new instance of the Position class.

    Args:
      x (int): The x coordinate.
      y (int): The y coordinate.
    """
    self.x = x
    self.y = y
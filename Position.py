class Position:
  """
  Represents a position with x and y coordinates.
  """
  
  _x: int
  _y: int

  def __init__(self, x, y) -> None:
    """
    Initializes a new instance of the Position class.

    Args:
      x (int): The x coordinate.
      y (int): The y coordinate.

    """
    if(x<0 or x>3 or y<0 or y>3):
      raise Exception("Invalid position")
    self.x = x
    self.y = y
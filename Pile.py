from Rock import Rock


class Pile:
  # stack of rocks sorted from large to small
  rocks: list[Rock]

  def __init__(self,pile_no,is_player=False, id=None) -> None:
    self.rocks = []
    if is_player:
      self.rocks.append(Rock(1, id, pile_no))
      self.rocks.append(Rock(2, id, pile_no))
      self.rocks.append(Rock(3, id, pile_no))
      self.rocks.append(Rock(4, id, pile_no))

  def push(self, rock: Rock) -> None:
    if not self.rocks or self.rocks[-1].size < rock.size:
      self.rocks.append(rock)
    else:
      raise Exception("can not add small rock into larger ones")

  def pop(self) -> Rock:
    if self.rocks:
      return self.rocks.pop()
    else:
      raise Exception("can not remove from empty space")
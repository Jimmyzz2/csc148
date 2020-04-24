from typing import Any
class Stack :
     """
     _Item:
     """
     _item: list

     def __init__ (self) -> None:
         self._item = []

     def push(self, item) -> None:
         self._item.append(item)

     def pop(self) -> Any:

         if not self.is_empty():
             return self._item.pop()
         else:
             raise EmptyPopErrorDoc

     def is_empty(self)-> bool:
          return self._item == []
















class EmptyPopError(Exception):
  pass


class EmptyPopErrorDoc(Exception):
 def __str__(self):
  return 'You cannot pop from empty list'

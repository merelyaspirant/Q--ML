import threading
from Tkinter import Tk, Button
from tkFont import Font
from time import sleep

class Board:

  def __init__(self,other=None):
    self.player = 'X'
    self.opponent = 'O'
    self.empty = '.'
    self.size = 3
    self.fields = {}
    for x in range(self.size):
      for y in range(self.size):
        self.fields[x,y] = self.empty

  def move(self,turn, x,y):
    self.fields[x,y] = turn
    return self

  def tied(self):
    for (x,y) in self.fields:
      if self.fields[x,y]==self.empty:
        return False
    return True

  def won(self, turn):
    # horizontal
    for x in range(self.size):
      winning = []
      for y in range(self.size):
        if self.fields[x,y] == turn:
          winning.append((x,y))
      if len(winning) == self.size:
#        print "win horizontal\n"
        return winning
    # vertical
    for y in range(self.size):
      winning = []
      for x in range(self.size):
        if self.fields[x,y] == turn:
          winning.append((x,y))
      if len(winning) == self.size:
#        print "win vertical"
        return winning
    # diagonal
    winning = []
    for x in range(self.size):
      y = x
      if self.fields[x,y] == turn:
        winning.append((x,y))
    if len(winning) == self.size:
#      print "win 1 diagonal"
#      print winning
      return winning
    # other diagonal
    winning = []
    for x in range(self.size):
      y = self.size-1-x
      if self.fields[x,y] == turn:
        winning.append((x,y))
    if len(winning) == self.size:
#      print "win 2 diagonal\n"
      return winning
    # default
    return None

class GUI:

  def __init__(self, todo):
    self.app = Tk()
    self.todo = todo
    self.app.title('TicTacToe')
    self.app.resizable(width=False, height=False)
    self.board = Board()
    self.font = Font(family="Helvetica", size=32)
    self.buttons = {}
    for x,y in self.board.fields:
      handler = lambda x=x,y=y: self.move(x,y)
      button = Button(self.app, command=handler, font=self.font, width=2, height=1)
      button.grid(row=x, column=y)
      self.buttons[x,y] = button
    handler = lambda: self.reset()
    button = Button(self.app, text='reset', command=handler)
    button.grid(row=self.board.size+1, column=0, columnspan=self.board.size, sticky="WE")
    turn = 'X'
    self.update(turn)

  def reset(self):
    self.board = Board()
    turn = 'X'
    self.update(turn)

  def move(self,turn,x,y):
    self.board.move(turn,x,y)
    res = self.update(turn)
    return res

  def update(self, turn):
    for (x,y) in self.board.fields:
      text = self.board.fields[x,y]
      self.buttons[x,y]['text'] = text
      self.buttons[x,y]['disabledforeground'] = 'black'
      if text==self.board.empty:
        self.buttons[x,y]['state'] = 'normal'
      else:
        self.buttons[x,y]['state'] = 'disabled'

    winning = self.board.won(turn)
    if winning:

      for x,y in winning:
        self.buttons[x,y]['disabledforeground'] = 'red'
      for x,y in self.buttons:
        self.buttons[x,y]['state'] = 'disabled'
      for (x,y) in self.board.fields:
        self.buttons[x,y].update()
      self.reset()
      return 'won'

    elif self.board.tied():
      self.reset()
      return 'tied'

    return 'done'
    

  def mainloop(self):
    self.app.mainloop()



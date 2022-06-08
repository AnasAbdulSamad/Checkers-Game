import pygame
from board import *
from constants import *
from pygame import *

class Game:

     def __init__(self, win):

          self.selected = None                                          #stores the selected piece
          self.board = Board()                                          #calls the Board Class from board.py
          self.turn = RED                                                  #the first turn is for RED
          self.valid_moves = {}                                         #a dictionary that contains the valid moves for the selected piece
          self.win = win
          pygame.init()
    

     def update(self):

          """Updates the screen after the moves"""

          self.board.draw(self.win)
          self.draw_valid_moves(self.valid_moves)
          pygame.display.update()

     def winner(self):
          return self.board.winner()

     def reset(self):

          """Resets the screen after the game is over"""

          self.selected = None                                          #stores the selected piece
          self.board = Board()                                          #calls the Board Class from board.py
          self.turn = RED                                                  #the first turn is for RED
          self.valid_moves = {}                                         #a dictionary that contains the valid moves for the selected piece

     def select(self, row, col):

          if self.selected:                                                #if a piece is selected (the click is not on empty space)
               result = self._move(row, col)                        #then move the piece to the required position                    

               if not result:                                                 #if a piece is not slected then call the same function again
                    self.selected = None
                    self.select(row, col)
        
          piece = self.board.get_piece(row, col)
          if piece != 0 and piece.color == self.turn:
               self.selected = piece
               self.valid_moves = self.board.get_valid_moves(piece)
               return True
            
          return False

     def _move(self, row, col):

          """Moves the piece tothe required position"""
         
          piece = self.board.get_piece(row, col)
          if self.selected and piece == 0 and (row, col) in self.valid_moves:
               self.board.move(self.selected, row, col)
               mixer.music.load('final.mp3')
               mixer.music.play()
               skipped = self.valid_moves[(row, col)]
               if skipped:
                    self.board.remove(skipped)
               self.change_turn()
          else:
               return False

          return True

     def draw_valid_moves(self, moves):

          """Draws a blue circle where the piece can move"""

          for move in moves:
               row, col = move
               pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

     def change_turn(self):

          """Changes the turn one after the other"""
         
          self.valid_moves = {}                                    #an empty dictionary
          if self.turn == RED:                                     #if the last turn was for RED
               self.turn = WHITE                                  #then next turn would be of WHITE
          else:
               self.turn = RED                                        #else would be of RED

     def get_board(self):
          return self.board

     def ai_move(self, board):

          """After the computer makes it moves it return us the new board"""
          
          self.board = board
          self.change_turn()
          

     

import pygame
from constants import *
from piece import *

class Board:

     def __init__(self):

          self.board = []                                           # a 2d list
          self.red_left = 12                                     #the remaining pieces (if piece is removed we decrese the count)
          self.white_left = 12                                  #the remaining pieces (if piece is removed we decrese the count)
          self.red_kings  = 0                                   #the count of kings (initally 0)
          self.white_kings = 0                                 #the count of kings (initally 0)
          self.create_board()

     def draw_squares (self , win):

          """Draws the checker board pattern on the screen window"""

          win.fill(BLACK)                                    #fills the full screen with black colour

          for row in range (ROWS):                   # ROWS defined in the constants file
               for col in range (row%2 , COLS , 2):             #using a step 2 as board follows an alternate pattern
                    pygame.draw.rect(win , RED , (row*SQUARE_SIZE , col*SQUARE_SIZE , SQUARE_SIZE , SQUARE_SIZE))
                    #Syntax (Window in which to draw rectangle, colour, ( x , y , width , height))

     def evaluate(self):

          """Evaluates the score of each position for our AI"""
          
          return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
          #the bracket is prioritizing the move to become king

     def get_all_pieces (self , color):

          """Loops through the whole board and get all the pieces of the required color"""
          
          pieces = []
          for row in self.board:
               for piece in row:
                    if piece!=0 and piece.color == color:
                         pieces.append(piece)
          return pieces

     def move( self , piece , row , col ):
          self.board[piece.row][piece.col] , self.board[row][col]  = self.board[row][col] , self.board[piece.row][piece.col]              #swapping the position
          piece.move( row, col )

          if row == ROWS - 1 or row == 0 :                                   #checking if the piece has become king by moving to the last or first row
               piece.make_king()

               if piece.color == WHITE:                                    #checking which piece has become king(White or Red)
                    self.white_kings += 1                                        #incrementing the white kings

               else: 
                    self.red_kings += 1                                           #incrementing the red kings

     def get_piece (self , row , col ):
          return self.board[row][col]
               
     def create_board(self):

          """Placing the pieces (white and red) in their respective positions"""

          for row in range(ROWS):
               self.board.append([])                                 #the interior list of the 2d list

               for col in range(COLS):

                    if col%2 == ((row+1)%2):                          #the condition as we have to draw pieces by leaving one box after the other

                         if row < 3:                                            # as only first three rows contains WHITE pieces (Iteration 0,1 & 2)
                              self.board[row].append( Piece ( row , col , WHITE ) )                    # placing the white pieces

                         elif row > 4:                                                            #the RED pieces are placed in 6th, 7th & 8th rows (Iteration 5,6 & 7)
                              self.board[row].append( Piece ( row , col , RED ) )                          #placing the red pieces

                         else:
                              self.board[row].append(0)                                   #blank piece

                    else:
                         self.board[row].append(0)                                        #blank piece

     def draw(self, win ):

          """Will draw all the squares and the pieces"""

          self.draw_squares(win)

          for row in range (ROWS):

               for col in range (COLS):
                    piece = self.board[row][col]

                    if piece != 0:
                         piece.draw(win)

     def remove(self, pieces):

          """ Removes the piece or pieces that are jummed over"""
         
          for piece in pieces:
               self.board[piece.row][piece.col] = 0
               if piece != 0:
                    if piece.color == RED:      
                         self.red_left -= 1                                #decrease the number of the red pieces left
                    else:
                         self.white_left -= 1                             #deccrease the number of white pieces left


     def winner(self):

          """Checks if someone has won the game"""
          
          if self.red_left <= 0:                            #if number of red pieces are not left WHITE is the winner
               return WHITE
          elif self.white_left <= 0:                    #if number of white pieces are not left RED is the winner
               return RED

          return None

     def get_valid_moves(self, piece):

          """If the moves are valid then moves the piece"""

          moves = {}
          left = piece.col - 1
          right = piece.col + 1
          row = piece.row

          if piece.color == RED or piece.king:
               moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
               moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))

          if piece.color == WHITE or piece.king:
               moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
               moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

          return moves

     def _traverse_left(self, start, stop, step, color, left, skipped=[]):

          """Treaverse for all the valid moves in the left diagonal"""
          
          moves = {}
          last = []
          for r in range(start, stop, step):
               if left < 0:
                    break

               current = self.board[r][left]
               if current == 0:                      # if it is an empty square
                    if skipped and not last:                     #if we jump over a piece and can not move anywhere then end the turn
                         break
                    elif skipped:                                                    #if a double jump is possible then       
                         moves[(r, left)] = last + skipped
                    else:                                                     #if we dont jump over a piece then simply move to the left or right diagonal
                         moves[(r, left)] = last

                    if last:                                                             
                         if step == -1:
                              row = max(r-3, 0)
                         else:
                              row = min(r+3, ROWS)
                              moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))                     #updates the moves
                              moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))                   #updates the moves
                    break
               elif current.color == color:                                      #if it is not an empty square and same colour piece is present
                    break                                                                  #then we can not move
               else:                                                                         #but a different colour piece is present
                    last = [current]                                                  #then jump over it

               left -= 1

          return moves

     def _traverse_right(self, start, stop, step, color, right, skipped=[]):

          """Treavers for all the valid moves in the right diagonal"""
          
          moves = {}
          last = []
          for r in range(start, stop, step):
               if right >= COLS:
                    break

               current = self.board[r][right]
               if current == 0:                                           # if it is an empty square
                    if skipped and not last:                          #if we jump over a piece and can not move anywhere then end the turn
                         break
                    elif skipped:                                                 #if a double jump is possible then 
                         moves[(r,right)] = last + skipped
                    else:                                                            #if we dont jump over a piece then simply move to the left or right diagonal
                         moves[(r, right)] = last

                    if last:
                         if step == -1:
                              row = max(r-3, 0)
                         else:
                              row = min(r+3, ROWS)
                              moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))                   #updates the moves
                              moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))                 #updates the moves
                    break
               elif current.color == color:                                                   #if it is not an empty square and same colour piece is present
                    break                                                                               #then we can not move
               else:                                                                                      #but a different colour piece is present
                    last = [current]                                                                #then jump over it

               right += 1

          return moves
          
                    
                    
     
          
          

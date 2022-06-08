from constants import *
import pygame

class Piece:
     PADDING = 10
     OUTLINE = 2

     def __init__(self , row , col  ,color):
          self.row = row
          self.col = col
          self.color = color
          self.king = False
          self.x = 0                     #position of the  piece
          self.y = 0                     # position of the piece
          self.calc_pos()

     def calc_pos (self):
          self.x = SQUARE_SIZE * self.col +SQUARE_SIZE//2             #the center point of the piece from where the circle is drawn
          self.y  = SQUARE_SIZE * self.row + SQUARE_SIZE//2          #the center point of the piece from where the circle is drawn
          
     def make_king(self):
          self.king = True

     def draw(self , win):
          radius = SQUARE_SIZE//2 - self.PADDING                             # the radius of the piece
          pygame.draw.circle(win , GREY, (self.x , self.y) , radius + self.OUTLINE)                       #drawing the border of the piece with grey color
          pygame.draw.circle(win , self.color, (self.x , self.y) , radius )                          # drawing the piece

          if self.king:
               win.blit(CROWN , (self.x - CROWN.get_width()//2 , self.y - CROWN.get_height()//2 )  )      #placing in the crown at the center of the piece  

     def move(self , row , col ):
          self.row = row
          self.col  =col
          self.calc_pos()

               
     def __repr__ (self):
          return str(self.color)





          

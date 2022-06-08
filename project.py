import pygame
from pygame import mixer
from constants import *
from piece import *
from board import *
from game import *
from minimax import *

class Project:

     def __init__(self):
          
          self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))                    #setting the window size
          pygame.display.set_caption("CHECKERS")                    #setting the title
          pygame.init()

     def get_row_col_from_mouse(self,pos):

          """Gets the row and coloumn at which our mouse is placed"""

          x , y = pos
          row = y // SQUARE_SIZE
          col = x // SQUARE_SIZE
          return row , col

     def main(self):
          run = True
          clock = pygame.time.Clock()                             
          game = Game(self.WIN)

          while run:
               clock.tick(FPS)                        #FPS=Frames per Second
                    
               if game.turn == WHITE:
                    value , new_board = minimax(game.get_board(), 4,  WHITE , game)
                    mixer.music.load('final.mp3')
                    mixer.music.play()
                    game.ai_move(new_board)
                    
               if game.winner() != None:
                    print(game.winner())
                    run = False

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:                           #if mouse button is pressed move the piece
                         pos = pygame.mouse.get_pos()
                         row , col = Project.get_row_col_from_mouse(self,pos)                         #get the row and coloumn at which the mouse button is pressed
                         game.select(row , col )
                         
                         
               game.update()
               
          pygame.quit()

p=Project()
p.main()


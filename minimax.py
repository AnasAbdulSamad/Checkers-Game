from copy import deepcopy
import pygame
from pygame import mixer
from constants import *

pygame.init()
    
def minimax(position, depth, max_player, game):

    #position = the current position in which our piece is
    #depth = how long you want to make the recursive call
    #max_player = tells whether we are maximizing or minmizing the value

    if depth == 0 or position.winner() != None:                            #if we have not won the game
        return position.evaluate(), position
    
    if max_player:                                                          #if it is white player turn
        maxEval = float('-inf')                                         #least value
        best_move = None                                                #currently the best move is set to None
        for move in get_all_moves(position, WHITE, game):                               #get all the posssible moves for White player
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)                                   #check if the new score is greater then change it 
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):

    """If we make this move return the new board and remove the piece if it is skipped"""
    
    board.move(piece, move[0], move[1])
    
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):

    moves = []

    for piece in board.get_all_pieces(color):                                    #get all the pieces of certain color
        valid_moves = board.get_valid_moves(piece)                          #get all the valid moves for the pieces

        for move, skip in valid_moves.items():                                     #valid_move is a dictionary      
            temp_board = deepcopy(board)                                           #a temporary board
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves




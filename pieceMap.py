#!/usr/bin/python3

import chess
from chess import Board
import math
import pieceMap

# Adjusts evaluation of piece positions according hard-coded heat map
def pieceLocationModifier(board=None):
    modifier = 0

    # These are arrays representing piece locations on the board
    # and the value associated with those locations
    pawnMap = [
        0,  0,  0,  0,  0,  0,  0,  0,
	50, 50, 50, 50, 50, 50, 50, 50,
       	10, 10, 20, 30, 30, 20, 10, 10,
	5,  5, 10, 25, 25, 10,  5,  5,
	0,  0,  0, 20, 20,  0,  0,  0,
	5, -5,-10,  0,  0,-10, -5,  5,
	5, 10, 10,-20,-20, 10, 10,  5,
	0,  0,  0,  0,  0,  0,  0,  0
    ]

    knightMap = [
        -50,-40,-30,-30,-30,-30,-40,-50,
       	-40,-20,  0,  0,  0,  0,-20,-40,
       	-30,  0, 10, 15, 15, 10,  0,-30,
	-30,  5, 15, 20, 20, 15,  5,-30,
	-30,  0, 15, 20, 20, 15,  0,-30,
	-30,  5, 10, 15, 15, 10,  5,-30,
	-40,-20,  0,  5,  5,  0,-20,-40,
	-50,-40,-30,-30,-30,-30,-40,-50,
    ]

    bishopMap = [
        -20,-10,-10,-10,-10,-10,-10,-20,
	-10,  0,  0,  0,  0,  0,  0,-10,
	-10,  0,  5, 10, 10,  5,  0,-10,
	-10,  5,  5, 10, 10,  5,  5,-10,
	-10,  0, 10, 10, 10, 10,  0,-10,
	-10, 10, 10, 10, 10, 10, 10,-10,
	-10,  5,  0,  0,  0,  0,  5,-10,
	-20,-10,-10,-10,-10,-10,-10,-20,
    ]

    rookMap = [
        0,  0,  0,  0,  0,  0,  0,  0,
	5, 10, 10, 10, 10, 10, 10,  5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	0,  0,  0,  5,  5,  0,  0,  0
    ]

    queenMap = [
        -20,-10,-10, -5, -5,-10,-10,-20,
	-10,  0,  0,  0,  0,  0,  0,-10,
	-10,  0,  5,  5,  5,  5,  0,-10,
	-5,  0,  5,  5,  5,  5,  0, -5,
	0,  0,  5,  5,  5,  5,  0, -5,
	-10,  5,  5,  5,  5,  5,  0,-10,
	-10,  0,  5,  0,  0,  0,  0,-10,
	-20,-10,-10, -5, -5,-10,-10,-20
    ]

    # Loop for each piece type and adds their value to the returning modifier
    for p in board.pieces(chess.PAWN, chess.BLACK):
        modifier = modifier - pawnMap[p]
    for p in board.pieces(chess.KNIGHT, chess.BLACK):
        modifier = modifier - knightMap[p]
    for p in board.pieces(chess.BISHOP, chess.BLACK):
        modifier = modifier - bishopMap[p]
    for p in board.pieces(chess.ROOK, chess.BLACK):
        modifier = modifier - rookMap[p]
    for p in board.pieces(chess.QUEEN, chess.BLACK):
        modifier = modifier - queenMap[p]

    # The index here is reversed to 'flip' the board around for the opposing color
    for p in board.pieces(chess.PAWN, chess.WHITE):
        modifier = modifier + pawnMap[abs(p - 63)]
    for p in board.pieces(chess.KNIGHT, chess.WHITE):
        modifier = modifier + knightMap[abs(p - 63)]
    for p in board.pieces(chess.BISHOP, chess.WHITE):
        modifier = modifier + bishopMap[abs(p - 63)]
    for p in board.pieces(chess.ROOK, chess.WHITE):
        modifier = modifier + rookMap[abs(p - 63)]
    for p in board.pieces(chess.QUEEN, chess.WHITE):
        modifier = modifier + queenMap[abs(p - 63)]    
        
    return modifier

def kingLocationModifier(board=None):
    kingMap = [
        -30,-40,-40,-50,-50,-40,-40,-30,
	-30,-40,-40,-50,-50,-40,-40,-30,
	-30,-40,-40,-50,-50,-40,-40,-30,
	-30,-40,-40,-50,-50,-40,-40,-30,
	-20,-30,-30,-40,-40,-30,-30,-20,
	-10,-20,-20,-20,-20,-20,-20,-10,
	20, 20,  0,  0,  0,  0, 20, 20,
	20, 30, 10,  0,  0, 10, 30, 20
    ]

    modifier = 0

    for p in board.pieces(chess.KING, chess.BLACK):
        modifier = modifier - kingMap[p]
    for p in board.pieces(chess.KING, chess.WHITE):
        modifier = modifier + kingMap[abs(p - 63)]

    return modifier

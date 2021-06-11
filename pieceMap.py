#!/usr/bin/python3

import chess
from chess import Board
import math
import pieceMap

def pieceLocationModifier(b=None):
    mod = 0

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

    for p in b.pieces(chess.PAWN, chess.BLACK):
        mod = mod - pawnMap[p]
    for p in b.pieces(chess.KNIGHT, chess.BLACK):
        mod = mod - knightMap[p]
    for p in b.pieces(chess.BISHOP, chess.BLACK):
        mod = mod - bishopMap[p]
    for p in b.pieces(chess.ROOK, chess.BLACK):
        mod = mod - rookMap[p]
    for p in b.pieces(chess.QUEEN, chess.BLACK):
        mod = mod - queenMap[p]

    for p in b.pieces(chess.PAWN, chess.WHITE):
        mod = mod + pawnMap[abs(p - 63)]
    for p in b.pieces(chess.KNIGHT, chess.WHITE):
        mod = mod + knightMap[abs(p - 63)]
    for p in b.pieces(chess.BISHOP, chess.WHITE):
        mod = mod + bishopMap[abs(p - 63)]
    for p in b.pieces(chess.ROOK, chess.WHITE):
        mod = mod + rookMap[abs(p - 63)]
    for p in b.pieces(chess.QUEEN, chess.WHITE):
        mod = mod + queenMap[abs(p - 63)]    
        
    return mod

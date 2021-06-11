#!/usr/bin/python3

import chess
from chess import Board
import math
import pieceMap

board = chess.Board()
board2 = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")

def boardValue(b=None):
    eva = 0
    whitePieces = 0
    blackPieces = 0
    if b.is_checkmate():
        if b.turn == chess.WHITE:
            return -1000000
        else:
            return 1000000
    
    for c in b.board_fen():
        if c == "p":
            eva -= 100
            blackPieces += 1
        if c == "n" or c == "b":
            eva -= 300
            blackPieces += 1
        if c == "r":
            eva -= 500
            blackPieces += 1
        if c == "q":
            eva -= 900
            blackPieces += 1
        if c == "P":
            eva += 100
            whitePieces += 1
        if c == "N" or c == "B":
            eva += 300
            whitePieces += 1
        if c == "R":
            eva += 500
            whitePieces += 1
        if c == "Q":
            eva += 900
            whitePieces += 1

    if whitePieces < 6 or blackPieces < 6:
        whiteKing = int(str(b.king(chess.WHITE)))
        blackKing = int(str(b.king(chess.BLACK)))
        wkr = int(whiteKing / 8)
        wkf = int(whiteKing % 8)
        bkr = int(blackKing / 8)
        bkf = int(blackKing % 8)
        wdfc = max(3 - wkr, wkr - 4)
        wdfc += max(3 - wkf, wkf - 4)
        bdfc = max(3 - bkr, bkr - 4)
        bdfc += max(3 - bkf, bkf - 4)
        dbkf = abs(wkf - bkf)
        dbkr = abs(wkr - bkr)
        if eva > 0:
            eva += 14 - (dbkr + dbkf)
            eva += bdfc * 5
        else:
            eva -= 14 - (dbkr + dbkf)
            eva -= wdfc * 5

    eva += pieceMap.pieceLocationModifier(b)
            
    return(eva)

def moveSearch(b=None, depth=0, alpha=0, beta=0):
    if depth == 0:
        return boardValue(b)
        #capMoves = moveSearchCaptures(b, alpha, beta)
        #bv = boardValue(b)
        #if capMoves > bv and b.turn == chess.WHITE:
        #    return capMoves
        #elif capMoves < bv and b.turn == chess.BLACK:
        #    return capMoves
        #else:
        #    return bv
    if b.turn == chess.WHITE:
        value = -math.inf
        for m in getOrderMoves(b):
            b.push_san(str(m))
            value = max(value, moveSearch(b, depth - 1, alpha, beta))
            b.pop()
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = math.inf
        for m in getOrderMoves(b):
            b.push_san(str(m))
            value = min(value, moveSearch(b, depth - 1, alpha, beta))
            b.pop()
            if value <= alpha:
                break
            beta = min(beta, value)
        return value

def moveSearchCaptures(b=None, alpha=0, beta=0):
    capMoves = []
    for m in getOrderMoves(b):
        if b.is_capture(m):
            capMoves.append(m)
    if len(capMoves) == 0:
        return boardValue(b)
    
    if b.turn == chess.WHITE:
        value = -math.inf
        for m in capMoves:
            b.push_san(str(m))
            value = max(value, moveSearchCaptures(b, alpha, beta))
            b.pop()
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = math.inf
        for m in capMoves:
            b.push_san(str(m))
            value = min(value, moveSearchCaptures(b, alpha, beta))
            b.pop()
            if value <= alpha:
                break
            beta = min(beta, value)
        return value
    
def regMoveSearch(b=None, depth=0):
    if depth == 0:
        return boardValue(b)

    eva = -math.inf
    if b.turn == chess.BLACK:
        eva = eva * -1

    for m in b.legal_moves:
        b.push_san(str(m))
        ev = regMoveSearch(b, depth - 1)
        if b.turn == chess.BLACK:
            eva = max(eva, ev)
        else:
            eva = min(eva, ev)
        b.pop()

    return eva
    
def getOrderMoves(b=None):
    result = []
    for m in b.legal_moves:
        result.append(m)
    board.set_fen(b.fen())
    return sorted(result, key=weightMoves)

def weightMoves(m=None):
    weight = 0

    from_square = str(board.piece_at(m.from_square)).lower()
    to_square = str(board.piece_at(m.to_square)).lower()
    
    if board.is_capture(m):
        weight -= 10 * pieceValue(to_square) - pieceValue(from_square)
    if len(str(m)) > 4:
        weight -= 100
    if board.gives_check(m):
        weight -= 5
    return weight

def pieceValue(p=""):
    if p == "p":
        return 1
    if p == "b":
        return 3
    if p == "n":
        return 3
    if p == "r":
        return 5
    if p == "q":
        return 9
    if p == "k":
        return 4
    if p == "none":
        return 1

def getMove(b=None):
    board = b.copy()
    depth = 0
    totalPieces = 0
    highIdx = str(getOrderMoves(b)[0])
    lowIdx = str(getOrderMoves(b)[0])
    lowEva = math.inf
    highEva = -math.inf
    for p in b.board_fen():
        if p in "pPnNbBrRqQkK":
            totalPieces += 1
    if totalPieces > 20:
        depth = 2
    else:
        depth = 3
    for m in getOrderMoves(b):
        b.push_san(str(m))
        move = moveSearch(b, depth, highEva, lowEva)
        print("move: {} | value: {}".format(str(m), move))
        b.pop()
        if move > highEva:
            highEva = move
            highIdx = str(m)
        if move < lowEva:
            lowEva = move
            lowIdx = str(m)
    if b.turn == chess.WHITE:
        print(highIdx)
        return highIdx
    else:
        print(lowIdx)
        print("???")
        return lowIdx
    
if __name__ == "__main__":
    print(boardValue(board2))

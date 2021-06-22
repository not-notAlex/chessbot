#!/usr/bin/python3

import chess
from chess import Board
import math
import pieceMap

localBoard = chess.Board()
testBoard = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")

# Evaluates a board position and returns inetger
def boardValue(board=None):

    evaluation = 0
    whitePieces = 0
    blackPieces = 0

    # Evaluate checkmate
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1000000
        else:
            return 1000000

    # Count piece material
    for c in board.board_fen():
        if c == "p":
            evaluation -= 100
            blackPieces += 1
        if c == "n" or c == "b":
            evaluation -= 300
            blackPieces += 1
        if c == "r":
            evaluation -= 500
            blackPieces += 1
        if c == "q":
            evaluation -= 900
            blackPieces += 1
        if c == "P":
            evaluation += 100
            whitePieces += 1
        if c == "N" or c == "B":
            evaluation += 300
            whitePieces += 1
        if c == "R":
            evaluation += 500
            whitePieces += 1
        if c == "Q":
            evaluation += 900
            whitePieces += 1

    # During endgame scenarios evaluate king positions
    if whitePieces < 6 or blackPieces < 6:
        whiteKing = int(str(board.king(chess.WHITE)))
        blackKing = int(str(board.king(chess.BLACK)))
        whiteKingRank = int(whiteKing / 8)
        whiteKingFile = int(whiteKing % 8)
        blackKingRank = int(blackKing / 8)
        blackKingFile = int(blackKing % 8)
        whiteDistanceFromCenter = max(3 - whiteKingRank, whiteKingRank - 4)
        whiteDistanceFromCenter += max(3 - whiteKingFile, whiteKingFile - 4)
        blackDistanceFromCenter = max(3 - blackKingRank, blackKingRank - 4)
        blackDistanceFromCenter += max(3 - blackKingFile, blackKingFile - 4)
        distanceBetweenKingFile = abs(whiteKingFile - blackKingFile)
        distanceBetweenKingRank = abs(whiteKingRank - blackKingRank)
        if evaluation > 0:
            evaluation += 14 - (distanceBetweenKingRank + distanceBetweenKingFile)
            evaluation += blackDistanceFromCenter * 5
        else:
            evaluation -= 14 - (distanceBetweenKingRank + distanceBetweenKingFile)
            evaluation -= whiteDistanceFromCenter * 5

    # Piece location heatmap
    evaluation += pieceMap.pieceLocationModifier(board)
            
    return(evaluation)

# Searches for recommended move up to a given depth
def moveSearch(board=None, depth=0, alpha=0, beta=0):
    if depth == 0:
        return boardValue(board)

    # Alpha-Beta Pruning
    if board.turn == chess.WHITE:
        value = -math.inf
        for m in getOrderMoves(board):
            board.push_san(str(m))
            value = max(value, moveSearch(board, depth - 1, alpha, beta))
            board.pop()
            # Prune unnecessary branch
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = math.inf
        for m in getOrderMoves(board):
            board.push_san(str(m))
            value = min(value, moveSearch(board, depth - 1, alpha, beta))
            board.pop()
            # Prune unnecessary branch
            if value <= alpha:
                break
            beta = min(beta, value)
        return value

# Unused function created for testing future feature
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

# Unused function for regular minimax algorithm
# Used for testing alpha-beta pruning having same result
def regMoveSearch(board=None, depth=0):
    if depth == 0:
        return boardValue(board)

    eva = -math.inf
    if board.turn == chess.BLACK:
        eva = eva * -1

    for m in board.legal_moves:
        board.push_san(str(m))
        ev = regMoveSearch(board, depth - 1)
        if board.turn == chess.BLACK:
            eva = max(eva, ev)
        else:
            eva = min(eva, ev)
        board.pop()

    return eva

# Returns list of legal moves in a predicted order
def getOrderMoves(board=None):
    result = []
    
    for m in board.legal_moves:
        result.append(m)
        
    # Copy position from argument to global variable to use in weightMoves function
    localBoard.set_fen(board.fen())
    
    return sorted(result, key=weightMoves)

# Function that assigns weight to a particular move
def weightMoves(m=None):
    weight = 0

    from_square = str(localBoard.piece_at(m.from_square)).lower()
    to_square = str(localBoard.piece_at(m.to_square)).lower()

    # Weight move in terms of valuable capture
    if localBoard.is_capture(m):
        weight -= 10 * pieceValue(to_square) - pieceValue(from_square)
    # Increase weight of pawn promotion
    if len(str(m)) > 4:
        weight -= 100
    # Slightly increase weight of checks
    if localBoard.gives_check(m):
        weight -= 5
    return weight

# Simple function to convert string of piece to integer value
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

# Prime function that takes a board state as argument and returns reccomended move
def getMove(board=None):
    depth = 0
    totalPieces = 0
    highIdx = str(getOrderMoves(board)[0])
    lowIdx = str(getOrderMoves(board)[0])
    lowEva = math.inf
    highEva = -math.inf
    
    for p in board.board_fen():
        if p in "pPnNbBrRqQkK":
            totalPieces += 1
            
    # Adjust depth to number of pieces on the board
    if totalPieces > 20:
        depth = 2
    else:
        depth = 3

    # Loop through legal moves and perform alpha-beta pruning
    for m in getOrderMoves(board):
        board.push_san(str(m))
        move = moveSearch(board, depth, highEva, lowEva)
        # Print evaluation of all moves
        print("move: {} | value: {}".format(str(m), move))
        board.pop()
        if move > highEva:
            highEva = move
            highIdx = str(m)
        if move < lowEva:
            lowEva = move
            lowIdx = str(m)
            
    if board.turn == chess.WHITE:
        print(highIdx)
        return highIdx
    else:
        print(lowIdx)
        return lowIdx
    
if __name__ == "__main__":
    print(boardValue(testBoard))

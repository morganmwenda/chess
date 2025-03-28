# Description: This file contains the GameState class which represents the current state of the chess game. It contains the board configuration and the current player's turn.


class GameState:
    def __init__(self):
        # Board is an 8x8 2D list, each element has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'.
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', or 'p'.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.moveFunctions = {'p': self.getPawnMoves,
                              'R': self.getRookMoves,
                              'N': self.getKnightMoves,
                              'B': self.getBishopMoves,
                              'Q': self.getQueenMoves,
                              'K': self.getKingMoves
                              }
        
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        
    #won't work for castling, pawn promotion, and en-passant
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players
        
        #update the king's location if needed
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
            
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
        
            #update the king's location if needed   
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
        

            
    #all moves considering checks


    #get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1): #go through all the pins
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--":  # 2 square pawn advance
                        moves.append(Move((r,c),(r-2,c),self.board))
            
            #captures to the left
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
            #captures to the right
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
                    
        else:  # Black pawn moves
            if self.board[r+1][c] == "--":  # 1 square pawn advance
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # 2 square pawn advance
                   moves.append(Move((r, c), (r+2, c), self.board))

            # Captures to the left
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':  # Enemy piece to capture
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))
            # Captures to the right
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':  # Enemy piece to capture
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))

    
    #get all the rook moves for the rook located at row, col and add these moves to the list
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1): #go through all the pins
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != 'Q': #can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
            
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #friendly piece invalid
                            break
                else: #off board invalid
                    break

    #get all the knight moves for the knight located at row, col and add these moves to the list
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1): #go through all the pins
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
            
        knightMoves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    #get all the bishop moves for the bishop located at row, col and add these moves to the list
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1): #go through all the pins
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break
 
    #get all the queen moves for the queen located at row, col and add these moves to the list
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    #get all the king moves for the king located at row, col and add these moves to the list
    def getKingMoves(self, r, c, moves):
        rowMoves = [-1, -1, -1, 0, 0, 1, 1, 1]
        colMoves = [-1, 0, 1, -1, 1, -1, 0, 1]
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    #place king on end square and check for checks
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))    
                        #place king back on original location
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)


    def checkForPinsAndChecks(self):
        pins = [] # squares where the allied pinned piece is and direction it's pinned from
        checks = [] # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":  # ally piece, not king
                        if possiblePin == ():  # first pinned piece found
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break  # stop checking in this direction
                        
                    elif endPiece[0] == enemyColor:  # enemy piece
                        type = endPiece[1]
                        # 5 possibilities in this complex conditional
                        # 1. orthogonally away from king and piece is a rook
                        # 2. diagonally away from king and piece is a bishop
                        # 3. 1 square away diagonally from king and piece is a pawn
                        # 4. any direction and piece is a queen
                        # 5. any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and type == 'R') or \
                              (4 <= j <= 7 and type == 'B') or \
                              (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                              (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking, so check is still valid
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # there is a piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:
                    break #off board
                
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking the king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks
       
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
       
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = [] # squares that the king can move to
                
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # get rid of any moves that don't get the king out of check or move into check
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: #double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)        
        else:
            moves = self.getAllPossibleMoves()
        
        # Check if any move leaves the king in check
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck:
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            
        return moves
    
class Move():

    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol #unique id for each move
        
    
    #overriding the equals method
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        #making to real chess notation
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

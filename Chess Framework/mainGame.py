from chessPieces import *

board = [["  " for x in range(8)] for y in range(8)]

def playGame():
    turn = "w"
    setBoard()
    printBoard()
    dict = {
        0: "w",
        1: "b"
    }
    n = 0
    while True:
        turn = dict.get(n%2)
        print(f"Current Turn: {turn}")
        win = checkmate(turn)
        # 0 for continue
        # 1 for checkmate
        # 2 for stalemate
        if win == 0:
            # no checkamte or stalemate
            pass
        elif win == 1 and turn == "w":
            print("Checkmate! Black has won, White is in check and has no legal moves remaining.")
            break
        elif win == 1 and turn == "b":
            print("Checkmate! White has won, Black is in check and has no legal moves remaining.")
            break
        elif win == 2 and turn == "w":
            print("Stalemate! White is not is check but has no legan moves remaining.")
        elif win == 2 and turn == "b":
            print("Stalemate! Black is not is check but has no legan moves remaining.")
        if check(turn):
            print("Your king is in check!")
        (r, c) = getValid(turn)
        if len(validMove(r, c)) == 0:
            print("This piece has no valid moves. Please choose another. (Ex. f7)")
            continue
        (y, x) = convert(input("Where would you like to move your piece? (Ex. f7)\n").lower())
        if (y, x) in validMove(r, c):
            while True:
                if isinstance(board[y][x], Piece):
                    alias = Piece(y, x, board[y][x].getType(), board[y][x].getColor())
                else:
                    alias = "  "
                movePiece(r, c, y, x)
                if check(turn):
                    movePiece(y, x, r, c)
                    board[y][x] = alias
                    print("This move is invalid as your king would be in check. Please try a different move.")
                    # must reset y x and ask for new r c before breaking from loop.
                    (r,c) = getValid(turn)
                    if len(validMove(r, c)) == 0:
                        print("This piece has no valid moves. Please choose another. (Ex. f7)")
                        continue
                    (y, x) = convert(input("Where would you like to move your piece? (Ex. f7)\n").lower())
                else:
                    promote(y, x)
                    break
        else:
            while True:
                (y, x) = convert(input("That move is invalid. Please try another. (Ex. f7)\n").lower())
                if (y, x) not in validMove(r, c):
                    continue
                else:
                    movePiece(r, c, y, x)
                    promote(y, x)
                    break
        printBoard()
        n +=1
    print("Good Game! I hope you play again.")

def setBoard():
    for i in range(8):
        board[1][i] = Piece(1, i, "P", "b")
        board[6][i] = Piece(6, i, "P", "w")

    board[0][0] = Piece(0, 0, "R", "b")
    board[7][0] = Piece(7, 0, "R", "w")
    board[0][7] = Piece(0, 7, "R", "b")
    board[7][7] = Piece(7, 7, "R", "w")

    board[0][1] = Piece(0, 1, "N", "b")
    board[7][1] = Piece(7, 1, "N", "w")
    board[0][6] = Piece(0, 6, "N", "b")
    board[7][6] = Piece(7, 6, "N", "w")

    board[0][2] = Piece(0, 2, "B", "b")
    board[7][2] = Piece(7, 2, "B", "w")
    board[0][5] = Piece(0, 5, "B", "b")
    board[7][5] = Piece(7, 5, "B", "w")

    board[0][3] = Piece(0, 3, "Q", "b")
    board[7][3] = Piece(7, 3, "Q", "w")
    board[0][4] = Piece(0, 4, "K", "b")
    board[7][4] = Piece(7, 4, "K", "w")

def printBoard():
    print("\n"+"-"+"----"*(len(board)+2))
    for i in range(8):
        for j in range(8):
            if j == 0:
                print("| "+ str(board[i][j]), end = "")
            else:
                print(" | "+ str(board[i][j]), end = "")
            if j == 7:
                print(" |", 8-i)
        print("-"+"----"*(len(board)+2))
    for x in range (65, 73, 1):
        if x == 65:
            print("", end="")
        print("  ", chr(x), end = " ")
    print("\n")

def check(turn):
    bigList = []
    for row in range(8):
        for col in range(8):
            if isinstance(board[row][col], str):
                continue
            elif board[row][col].getColor() != turn and board[row][col].getType() != "K":
                bigList.extend(validMove(row, col))
    for r in range(8):
        for c in range(8):
            if isinstance(board[r][c], Piece):
                if board[r][c].getType() == "K" and board[r][c].getColor() == turn:
                    return (board[r][c].getPosition() in bigList)

def movePiece(y, x, newY, newX):
    board[newY][newX] = board[y][x]
    board[y][x].move(newY, newX)
    board[y][x] = "  "

def promote(y, x):
    if not ((board[y][x].getColor() == "b" and y == 7) or (board[y][x].getColor() == "w" and y == 0)) or board[y][x].getType() != "P":
        return None
    promotion = ''
    while promotion not in ["N", "B", "R", "Q"]:
        promotion = input("What piece would you like to promote your pawn to? 'N' for Knight, 'B' for Bishop, 'R' for Rook, and 'Q' for Queen.\n").upper()
        if promotion not in ["N", "B", "R", "Q"]:
            print(f"'{promotion}' is not an accepted value. Please try again.")
    board[y][x].setType(promotion)

def convert(loc):
    # expects a 2 character string such as "e3" and returns the corresponding location on the board in the form of (row, column) 
    while True:
        if (ord(loc[0]) >= 97 and ord(loc[0]) <= 104) and (int(loc[1]) >= 1 and int(loc[1]) <= 8) and (len(loc) == 2):
            break
        else:
            loc = input("The value you entered is invalid. Please enter a different value. (Ex. f7)\n").lower()
    dict = {
        "h": 7,
        "g": 6,
        "f": 5,
        "e": 4,
        "d": 3,
        "c": 2,
        "b": 1,
        "a": 0
        }
    row = 8-int(loc[1])
    col = dict.get(loc[0])
    return (row, col)
    
def getValid(turn):
    while True:
        (row, col) = convert(input("Please enter the board location of the piece you would like to move. (ex. f7)\n").lower())
        if type(board[row][col]) != str:
            if board[row][col].getColor() != turn:
                print("This piece not yours. Please choose another.")
                continue
            else:
                # it is a valid location
                break
        else:
            print("There is no piece at this position. Please choose another.")
            continue
    return (row, col)
    # if outside of while loop, you have correctly selected your piece.

def validMove(row, col):
    # parameters are y and x location of the piece to be moved
    # returns a list of possible moves for the selected piece
    possibleMoves = []
    obj = board[row][col]
    if obj.getType() == "R":
        count = (row, 7-col, 7-row, col)
        for l in range(col+1):
            if l == 0:
                continue
            if isinstance(board[row][col-l], str):
                possibleMoves.append((row, col-l))
            else:
                if board[row][col-l].getColor() != obj.getColor():
                    possibleMoves.append((row, col-l))
                break
        for r in range(8-col):
            if r == 0:
                continue
            if isinstance(board[row][col+r], str):
                possibleMoves.append((row, col+r))
            else:
                if board[row][col+r].getColor() != obj.getColor():
                    possibleMoves.append((row, col+r))
                break
        for u in range(row+1):
            if u == 0:
                continue
            if isinstance(board[row-u][col], str):
                possibleMoves.append((row-u, col))
            else:
                if board[row-u][col].getColor() != obj.getColor():
                    possibleMoves.append((row-u, col))
                break
        for d in range(8-row):
            if d == 0:
                continue
            if isinstance(board[row+d][col], str):
                possibleMoves.append((row+d, col))
            else:
                if board[row+d][col].getColor() != obj.getColor():
                    possibleMoves.append((row+d, col))
                break
    elif obj.getType() == "N":
        try:
            if isinstance(board[row+2][col+1], str):
                if row+2 >= 0 and col+1 >= 0:
                    possibleMoves.append((row+2, col+1))
            elif isinstance(board[row+2][col+1], Piece):
                if board[row+2][col+1].getColor() == obj.getColor():
                    pass
                else:
                    if row+2 > 0 and col+1 > 0:
                        possibleMoves.append((row+2, col+1))
        except IndexError:
            pass
        try:
            if isinstance(board[row+2][col-1], str):
                if row+2 >= 0 and col-1 >= 0:
                    possibleMoves.append((row+2, col-1))
            elif isinstance(board[row+2][col-1], Piece):
                if board[row+2][col-1].getColor() == obj.getColor():
                    pass
                else:
                    if row+2 >= 0 and col-1 >= 0:
                        possibleMoves.append((row+2, col-1))
        except IndexError:
            pass
        try:
            if isinstance(board[row-2][col+1], str):
                if row-2 >= 0 and col+1 >= 0:
                    possibleMoves.append((row-2, col+1))
            elif isinstance(board[row-2][col+1], Piece):
                if board[row-2][col+1].getColor() == obj.getColor():
                    pass
                else:
                    if row-2 > 0 and col+1 > 0:
                        possibleMoves.append((row-2, col+1))
        except IndexError:
            pass
        try:
            if isinstance(board[row-2][col-1], str):
                if row-2 >= 0 and col-1 >= 0:
                    possibleMoves.append((row-2, col-1))
            elif isinstance(board[row-2][col-1], Piece):
                if board[row-2][col-1].getColor() == obj.getColor():
                    pass
                else:
                    if row-2 >= 0 and col-1 >= 0:
                        possibleMoves.append((row-2, col-1))
        except IndexError:
            pass
        try:
            if isinstance(board[row+1][col+2], str):
                if row+1 >= 0 and col+2 >= 0:
                    possibleMoves.append((row+1, col+2))
            elif isinstance(board[row+1][col+2], Piece):
                if board[row+1][col+2].getColor() == obj.getColor():
                    pass
                else:
                    if row+1 >= 0 and col+2 >= 0:
                        possibleMoves.append((row+1, col+2))
        except IndexError:
            pass
        try:
            if isinstance(board[row+1][col-2], str):
                if row+1 >= 0 and col-2 >= 0:
                    possibleMoves.append((row+1, col-2))
            elif isinstance(board[row+1][col-2], Piece):
                if board[row+1][col-2].getColor() == obj.getColor():
                    pass
                else:
                    if row+1 >= 0 and col-2 >= 0:
                        possibleMoves.append((row+1, col-2))
        except IndexError:
            pass
        try:
            if isinstance(board[row-1][col+2], str):
                if row-1 >= 0 and col+2 >= 0:
                    possibleMoves.append((row-1, col+2))
            elif isinstance(board[row-1][col+2], Piece):
                if board[row-1][col+2].getColor() == obj.getColor():
                    pass
                else:
                    if row-1 >= 0 and col+2 >= 0:
                        possibleMoves.append((row-1, col+2))
        except IndexError:
            pass
        try:
            if isinstance(board[row-1][col-2], str):
                if row-1 >= 0 and col-2 >= 0:
                    possibleMoves.append((row-1, col-2))
            elif isinstance(board[row-1][col-2], Piece):
                if board[row-1][col-2].getColor() == obj.getColor():
                    pass
                else:
                    if row-1 >= 0 and col-2 >= 0:
                        possibleMoves.append((row-1, col-2))
        except IndexError:
            pass
    elif obj.getType() == "B":
        n = 1
        while((row-n >= 0 and col-n >= 0) and (row != 0 and col != 0)):
            if isinstance(board[row-n][col-n], str):
                possibleMoves.append((row-n, col-n))
            else:
                if board[row-n][col-n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row-n, col-n))
                    break
            n +=1
        n = 1
        while((row-n >= 0 and col+n <= 7) and (row != 0 and col != 7)):
            if isinstance(board[row-n][col+n], str):
                possibleMoves.append((row-n, col+n))
            else:
                if board[row-n][col+n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row-n, col+n))
                    break
            n +=1
        n = 1
        while((row+n <= 7 and col-n >= 0) and (row != 7 and col != 0)):
            if isinstance(board[row+n][col-n], str):
                possibleMoves.append((row+n, col-n))
            else:
                if board[row+n][col-n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row+n, col-n))
                    break
            n +=1
        n = 1
        while((row+n <= 7 and col+n <= 7) and (row != 7 and col != 7)):
            if isinstance(board[row+n][col+n], str):
                possibleMoves.append((row+n, col+n))
            else:
                if board[row+n][col+n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row+n, col+n))
                    break
            n +=1
    elif obj.getType() == "P":
        if obj.getColor() == "w":
            if isinstance(board[row-1][col], str):
                possibleMoves.append((row-1, col))
                if obj.getFirstMove():
                    if isinstance(board[row-2][col], str):
                        possibleMoves.append((row-2, col))
                    elif isinstance(board[row-2][col], Piece):
                        pass
                else:
                    pass
            elif isinstance(board[row-1][col], Piece):
                pass
            try:
                if isinstance(board[row-1][col-1], Piece):
                    if board[row-1][col-1].getColor() == "w":
                        pass
                    else:
                        possibleMoves.append((row-1,col-1))
            except IndexError:
                pass
            try:
                if isinstance(board[row-1][col+1], Piece):
                    if board[row-1][col+1].getColor() == "w":
                        pass
                    else:
                        possibleMoves.append((row-1,col+1))
            except IndexError:
                pass
        else:
            if isinstance(board[row+1][col], str):
                possibleMoves.append((row+1, col))
                if obj.getFirstMove():
                    if isinstance(board[row+2][col], str):
                        possibleMoves.append((row+2, col))
                    elif isinstance(board[row+2][col], Piece):
                        pass
                else:
                    pass
            elif isinstance(board[row+1][col], Piece):
                pass
            try:
                if isinstance(board[row+1][col-1], Piece):
                    if board[row+1][col-1].getColor() == "b":
                        pass
                    else:
                        possibleMoves.append((row+1,col-1))
            except IndexError:
                pass
            try:
                if isinstance(board[row+1][col+1], Piece):
                    if board[row+1][col+1].getColor() == "b":
                        pass
                    else:
                        possibleMoves.append((row+1,col+1))
            except IndexError:
                pass
    elif obj.getType() == "Q":
        for l in range(col+1):
            if l == 0:
                continue
            if isinstance(board[row][col-l], str):
                possibleMoves.append((row, col-l))
            else:
                if board[row][col-l].getColor() != obj.getColor():
                    possibleMoves.append((row, col-l))
                break
        for r in range(8-col):
            if r == 0:
                continue
            if isinstance(board[row][col+r], str):
                possibleMoves.append((row, col+r))
            else:
                if board[row][col+r].getColor() != obj.getColor():
                    possibleMoves.append((row, col+r))
                break
        for u in range(row+1):
            if u == 0:
                continue
            if isinstance(board[row-u][col], str):
                possibleMoves.append((row-u, col))
            else:
                if board[row-u][col].getColor() != obj.getColor():
                    possibleMoves.append((row-u, col))
                break
        for d in range(8-row):
            if d == 0:
                continue
            if isinstance(board[row+d][col], str):
                possibleMoves.append((row+d, col))
            else:
                if board[row+d][col].getColor() != obj.getColor():
                    possibleMoves.append((row+d, col))
                break
        n = 1
        while((row-n >= 0 and col-n >= 0) and (row != 0 and col != 0)):
            if isinstance(board[row-n][col-n], str):
                possibleMoves.append((row-n, col-n))
            else:
                if board[row-n][col-n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row-n, col-n))
                    break
            n +=1
        n = 1
        while((row-n >= 0 and col+n <= 7) and (row != 0 and col != 7)):
            if isinstance(board[row-n][col+n], str):
                possibleMoves.append((row-n, col+n))
            else:
                if board[row-n][col+n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row-n, col+n))
                    break
            n +=1
        n = 1
        while((row+n <= 7 and col-n >= 0) and (row != 7 and col != 0)):
            if isinstance(board[row+n][col-n], str):
                possibleMoves.append((row+n, col-n))
            else:
                if board[row+n][col-n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row+n, col-n))
                    break
            n +=1
        n = 1
        while((row+n <= 7 and col+n <= 7) and (row != 7 and col != 7)):
            if isinstance(board[row+n][col+n], str):
                possibleMoves.append((row+n, col+n))
            else:
                if board[row+n][col+n].getColor() == obj.getColor():
                    break
                else:
                    possibleMoves.append((row+n, col+n))
                    break
            n +=1
    elif obj.getType() == "K":
        # append all possible options. Place king in each position and see if king is in check (make alias of object in that location if there is one). 
        # Remove moves that put king in check.
        if row > 0:
            if isinstance(board[row-1][col], str):
                possibleMoves.append((row-1, col))
            else:
                if board[row-1][col].getColor() == obj.getColor():
                    pass
                else:
                    possibleMoves.append((row-1, col))
            if col > 0:
                if isinstance(board[row-1][col-1], str):
                    possibleMoves.append((row-1, col-1))
                else:
                    if board[row-1][col-1].getColor() == obj.getColor():
                        pass
                    else:
                        possibleMoves.append((row-1,col-1))
            if col < 7:
                if isinstance(board[row-1][col+1], str):
                    possibleMoves.append((row-1, col+1))
                else:
                    if board[row-1][col+1].getColor() == obj.getColor():
                        pass
                    else:
                        possibleMoves.append((row-1,col+1))
        if row < 7:
            if isinstance(board[row+1][col], str):
                possibleMoves.append((row+1, col))
            else:
                if board[row+1][col].getColor() == obj.getColor():
                    pass
                else:
                    possibleMoves.append((row+1, col))
            if col > 0:
                if isinstance(board[row+1][col-1], str):
                    possibleMoves.append((row+1, col-1))
                else:
                    if board[row+1][col-1].getColor() == obj.getColor():
                        pass
                    else:
                        possibleMoves.append((row+1,col-1))
            if col < 7:
                if isinstance(board[row+1][col+1], str):
                    possibleMoves.append((row+1, col+1))
                else:
                    if board[row+1][col+1].getColor() == obj.getColor():
                        pass
                    else:
                        possibleMoves.append((row+1,col+1))
        if col > 0:
            if isinstance(board[row][col-1], str):
                possibleMoves.append((row, col-1))
            else:
                if board[row][col-1].getColor() == obj.getColor():
                    pass
                else:
                    possibleMoves.append((row,col-1))
        if col < 7:
            if isinstance(board[row][col+1], str):
                possibleMoves.append((row, col+1))
            else:
                if board[row][col+1].getColor() == obj.getColor():
                    pass
                else:
                    possibleMoves.append((row,col+1))
        someList = [x for x in possibleMoves]
        flag = False
        for (y, x) in someList:
            if isinstance(board[y][x], str):
                # if spot is empty, flag is true
                flag = True
            else:
                flag = False # redundant
                someObj = Piece(y, x, board[y][x].getType(), board[y][x].getColor()) 
            movePiece(row, col, y, x)
            if check(obj.getColor()):
                possibleMoves.remove((y,x))
            movePiece(y, x, row, col)
            if flag:
                board[y][x] = "  "
            else:
                board[y][x] = someObj
    return possibleMoves

def checkmate(turn):
    currentCheck = False
    for r in range(8):
        for c in range(8):
            if isinstance(board[r][c], Piece):
                if board[r][c].getColor() == turn:
                    if board[r][c].getType() == "K" and check(turn):
                        currentCheck = True
                    moveList = validMove(r, c)
                    for (y, x) in moveList:
                        if isinstance(board[y][x], Piece):
                            alias = Piece(y, x, board[y][x].getType(), board[y][x].getColor())
                        elif isinstance(board[y][x], str):
                            alias = "  "
                        movePiece(r, c, y, x)
                        inCheck = check(turn)
                        movePiece(y, x, r, c)
                        board[y][x] = alias
                        if not inCheck:
                            return 0 
    # if program makes it here, there are no possible moves
    if currentCheck:
        # king is in check, checkmate
        return 1
    else:
        # king is not in check, stalemate
        return 2

def main():
    playGame()

if __name__ == "__main__":
    main()
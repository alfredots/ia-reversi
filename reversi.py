# -*- coding: utf-8 -*-
# Reversi
import random
import sys
n = 8 #tamanho do coisa

def drawBoard(board):
    # Essa funcao desenha o tabuleiro
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)

    for y in range(8):
        print(VLINE)
        print(y + 1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)


def resetBoard(board):
    # Essa funcao esvazia o tabuleiro
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
    # Pecas iniciais:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Criar um tabuleiro novo
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board

def isTerminalNode(board, player):
    for y in range(n):
        for x in range(n):
            if isValidMove(board, player, x, y):
                return False
    return True

def isValidMove(board, tile, xstart, ystart):
    # Retorna False se o movimento em xstart, ystart é invalido
    # Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    board[xstart][ystart] = tile
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = ' '
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Retorna True se a casa está no tabuleiro.
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def getBoardWithValidMoves(board, tile):
    # Retorna um tabuleiro com os movimentos validos
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Retorna uma lista de movimentos validos
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determina o score baseado na contagem de 'X' e 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    # Permite que o player escolha ser X ou O
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Escolha suas peças: X ou O?')
        tile = input().upper()
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Escolhe aleatóriamente quem começa.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # Retorna True se o player quer jogar novamente
    print('Quer jogar novamente? (yes ou no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
    # Retorna False se for um movimento invalido
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Faz uma cópia do tabuleiro e retorna a cópia
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def goodMove(x, y):
    # Retorna True se a posição x, y é um dos cantos do tabuleiro
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7) or (x == 0 and y == 2) or (x == 0 and y == 3) or (x == 0 and y == 4) or (x == 0 and y == 5) or (x == 2 and y == 0) or (x == 3 and y == 0) or (x == 4 and y == 0) or (x == 5 and y == 0) or (x == 7 and y == 2) or (x == 7 and y == 3) or (x == 7 and y == 4) or (x == 7 and y == 5) or (x == 2 and y == 7) or (x == 3 and y == 7) or (x == 4 and y == 7) or (x == 5 and y == 7)

def opponent(player):
    if player == computerTile:
        return playerTile
    else:
        return computerTile
    
 
def getPlayerMove(board, playerTile):
    # Permite que o player insira sua jogada
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                print('Essa não é uma jogada válida')
                continue
            else:
                break
        else:
            print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
            print('Por exemplo, 81 será o canto superior direito.')
    return [x, y]


def getComputerMove(board, computerTile):
    # Permite ao computador executar seu movimento
    possibleMoves = getValidMoves(board, computerTile)
    # randomiza a ordem dos possíveis movimentos
    random.shuffle(possibleMoves)
    # se for possivel, joga no canto

    for x, y in possibleMoves:
        if goodMove(x, y):
            print("esse foi um good move x:" + str(x) + " y:" + str(y))
            return [x, y]

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Escolhe a jogada que resulta em mais pontos
    bestScore = -1
    bestMove = []

    # itera sobre as jogadas possiveís
    for x, y in possibleMoves:
        # cria cópia do tabuleiro
        dupeBoard = getBoardCopy(board)
        # faz primeira previsão do tabuleiro ao jogar
        makeMove(dupeBoard, computerTile, x, y)
        # chama minmax
        #temp = minimaxDecision(dupeBoard, computerTile, 5, True)

        #bestMove = minimax(board, computerTile, 15)
        alpha = float('-inf')
        beta = float('inf')
        temp = podaAlphaBetaNEW(board, computerTile, alpha, beta, 5, True)

        if temp > bestScore:
            bestMove = [x, y]
            bestScore = temp
    return bestMove

def min_play(board, player, depth):
  if isTerminalNode(board, player) or depth == 0:
    return getScoreOfBoard(board)[player]
  moves = getValidMoves(board, player)
  best_score = float('inf')
  opp = opponent(player)
  for x, y in moves:
    newBoard = getBoardCopy(board)
    makeMove(newBoard, player, x, y)
    #drawBoard(newBoard)
    score = max_play(newBoard, opp, depth-1)
    if score < best_score:
      best_move = [x, y]
      best_score = score
  return best_score

def max_play(board, player, depth):
  if isTerminalNode(board, player) or depth == 0:
    return getScoreOfBoard(board)[player]
  moves = getValidMoves(board, player)
  best_score = float('inf')
  opp = opponent(player)
  for x, y in moves:
    newBoard = getBoardCopy(board)
    makeMove(newBoard, player, x, y)
    #drawBoard(newBoard)
    score = min_play(newBoard, opp, depth-1)
    if score > best_score:
      best_move = move
      best_score = score
  return best_score


def minimax(board, player, depth):
  moves = getValidMoves(board, player)
  best_move = moves[0]
  best_score = float('-inf')
  opp = opponent(player)
  for x, y in moves:
    newBoard = getBoardCopy(board)
    makeMove(newBoard, player, x, y)
    #drawBoard(newBoard)
    score = min_play(newBoard, opp, depth -1)
    if score > best_score:
      best_move = [x, y]
      best_score = score
  return best_move

def podaAlphaBeta(board, player, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or isTerminalNode(board, player):
        return getScoreOfBoard(board)[player]
    bestValue = 0
    if maximizingPlayer:
        bestValue = -1
        for y in range(n):
            for x in range(n):
                if isValidMove(board, player, x, y):
                    newBoard = getBoardCopy(board)
                    makeMove(newBoard, player, x, y)
                    bestValue = max(bestValue, podaAlphaBeta(newBoard, player, depth - 1, alpha, beta, False))
                    alpha = max(alpha, bestValue)
                    if beta <= alpha:
                        break # beta cut-off
        return bestValue
    else: # minimizingPlayer
        bestValue = 1000
        for y in range(n):
            for x in range(n):
                if isValidMove(board, player, x, y):
                    newBoard = getBoardCopy(board)
                    makeMove(newBoard, player, x, y)
                    bestValue = min(bestValue, podaAlphaBeta(newBoard, player, depth - 1, alpha, beta, True))
                    beta = min(beta, bestValue)
                    if beta <= alpha:
                        break # alpha cut-off
        return bestValue

def showPoints(playerTile, computerTile):
    # Mostra o score atual
    scores = getScoreOfBoard(mainBoard)
    print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

def podaAlphaBetaNEW(board, player, alpha, beta, depth, maximizingPlayer):
    if depth == 0 or isTerminalNode(board, player):
        return getScoreOfBoard(board)[player]

    moves = getValidMoves(board, player)
    opp = opponent(player)

    if maximizingPlayer:
        value = float('-inf')
        for x,y in moves:
            newBoard = getBoardCopy(board)
            makeMove(newBoard, player, x, y)
            value = max(value, podaAlphaBeta(newBoard, opp, alpha, beta, depth-1, False))
            alpha = max(alpha, value)
            if alpha > beta:
                break
        return value

    else:
        value = float('inf')
        for x, y in moves:
            newBoard = getBoardCopy(board)
            makeMove(newBoard, player, x, y)
            value = min(value, podaAlphaBeta(newBoard, opp, alpha, beta, depth-1, True))
            beta = min(beta, value)
            if alpha > beta:
                break
        return value

#
# Código principal
#
print('Welcome to Reversi!')
while True:
    # Reseta o jogo e o tabuleiro
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('O ' + turn + ' começa o jogo.')
    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Obrigado por jogar!')
                sys.exit()  # terminate the program
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])
            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'
        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Pressione Enter para ver a jogada do computador.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)
            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'
    # Mostra o resultado final.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))

    if scores[playerTile] > scores[computerTile]:
        print('Você venceu o computador por %s ponto(s)! \nParabéns!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('Você perdeu!\nO computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
    else:
        print('Empate!')
    if not playAgain():
        break
 #-------------------------------------------------------------------------
 def minimaxDecision(board, player, depth, maximizingPlayer):

    if depth == 0 or isTerminalNode(board, player):
        return getScoreOfBoard(board)[player]
    
    if maximizingPlayer:
        bestValue = -1
        moves = getValidMoves(board, player)
        for x,y in moves:
            #criar cópia do tabuleiro
            newBoard = getBoardCopy(board)
            #faz previsão de jogada
            makeMove(newBoard, player, x, y)
            #return minimaxDecision(newBoard, player, depth -1, False)
            #recursão
            v = minimaxDecision(newBoard, player, depth -1, False)
            #retorna o maior valor
            bestValue = max(bestValue, v)    
    
    else:
        bestValue = 1000
        moves = getValidMoves(board, playerTile)
        for x,y in moves:
            newBoard = getBoardCopy(board)
            makeMove(newBoard, playerTile, x, y)
            #return minimaxDecision(newBoard, player, depth -1, True)
            v = minimaxDecision(newBoard, player, depth -1, True)
            #retorna o menor valor
            bestValue = min(bestValue, v)
    return bestValue

boardHeuristics = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 100, -10,  10,   3,   3,  10, -10, 100,   0,
    0, -10, -20,  -3,  -3,  -3,  -3, -20, -10,   0,
    0,  10,  -3,   8,   1,   1,   8,  -3,  10,   0,
    0,   3,  -3,   1,   1,   1,   1,  -3,   3,   0,
    0,   3,  -3,   1,   1,   1,   1,  -3,   3,   0,
    0,  10,  -3,   8,   1,   1,   8,  -3,  10,   0,
    0, -10, -20,  -3,  -3,  -3,  -3, -20, -10,   0,
    0, 100, -10,  10,   3,   3,  10, -10, 100,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]


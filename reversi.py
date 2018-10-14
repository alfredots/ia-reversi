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


def isOnCorner(x, y):
    # Retorna True se a posição x, y é um dos cantos do tabuleiro
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


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
        if isOnCorner(x, y):
            return [x, y]
    # Escolhe a jogada que resulta em mais pontos
#----------------------------------------------	
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        #score = getScoreOfBoard(dupeBoard)[computerTile]
        temp = minimaxDecision(dupeBoard, computerTile, 5, True)
        if temp > bestScore:
            bestMove = [x,y]
            bestScore = temp
    return bestMove
#-----------------------------------------------

    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def minimaxDecision(board, player, depth, maximizingPlayer):

    if depth == 0 or isTerminalNode(board, player):
        return getScoreOfBoard(board)[player]

    if maximizingPlayer:
        bestValue = -1
        for y in range(n):
            for x in range(n):
                if isValidMove(board, player, x, y):
                    newBoard = getBoardCopy(board)
                    v = minimaxDecision(newBoard, player, depth-1, False)
                    bestValue = max(bestValue, v)
    else:
        bestValue = 1000
        for y in range(n):
            for x in range(n):
                if isValidMove(board, player, x, y):
                    newBoard = getBoardCopy(board)
                    #(boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = minimaxDecision(newBoard, player, depth -1, True)
                    bestValue = min(bestValue, v)
                    #best
    return bestValue

def showPoints(playerTile, computerTile):
    # Mostra o score atual
    scores = getScoreOfBoard(mainBoard)
    print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

#
#Minha IA
#
class NodeTree:
	def __init__(self, board):
		self.peso = 0
		self.pai = ""
		self.board = board
		self.profundidade = 0
		self.tile = ""
		self.nodes = []

	def addNode(self,node):
		node.pai = self
		self.nodes.append(node)

#função determina peso
def calculaPeso(node):
    #verifica de quem é o turno
	tile = node.tile
	board = node.board
    #calcula o total peças minhas quando executada a jogada
	pecas_x = 0
	pecas_o = 0
	for x in range(8):
		for y in range(8):
			if board[x][y] == "X":
				pecas_x = pecas_x + 1
			else:
				pecas_o = pecas_o + 1		
	#retorna o peso
	if tile == "X":
		return pecas_x
	else:
		return pecas_o
#fim função calculaPeso

#Responsável por montar árvore de busca
def buildTree(board, tile, enemyTile):
	
	#Pegar board no estado atual
	boardCopy = getBoardCopy(board)
	for x in range(8):
		print(boardCopy[x])
	#Criar nó para board raiz
	root = NodeTree(boardCopy)
	root.tile = tile
	root.peso = calculaPeso(root)	
	print("peso: "+str(root.peso))
	root.profundidade = 0
	root.pai = None
	#pega jogadas boas jogadas
	vmoves = getValidMoves(boardCopy, tile)
	print("movimentos válidos pra máquina")
	print(vmoves)
	#
	atual = root
	for j in range(len(vmoves)):
		print("para jogada "+str(j))
		boardCopy2 = getBoardCopy(boardCopy)
		x,y = vmoves[j]
		print("x:"+str(x)+" y:"+str(y))
		makeMove(boardCopy2, tile, x, y)
		#criando novo nó
		novo = NodeTree(boardCopy2)
		novo.tile = tile
		novo.peso = calculaPeso(novo)	
		print("peso: "+str(novo.peso))
		novo.profundidade = 0
		novo.pai = atual
		atual.addNode(novo)
		print(atual.nodes)
		for x in range(8):
			print(boardCopy2[x])
	#agora prevendo a jogadas do humano
	for j in range(len(atual.nodes)):
		atual = atual.nodes[j]
		boardCopy3 = getBoardCopy(atual.board)
		vmoves2 = getValidMoves(boardCopy3, tile)
		print("movimentos válidos pra humano")
		print(vmoves2)
		for k in range(len(vmoves2)):
			print("para jogada "+str(j))
			boardCopy4 = getBoardCopy(boardCopy3)
			x,y = vmoves2[k]
			print("x:"+str(x)+" y:"+str(y))
			makeMove(boardCopy4, tile, x, y)
			#criando novo nó
			novo = NodeTree(boardCopy4)
			novo.tile = tile
			novo.peso = calculaPeso(novo)	
			print("peso: "+str(novo.peso))
			novo.profundidade = 0
			novo.pai = atual
			atual.addNode(novo)
			print(atual.nodes)
			for x in range(8):
				print(boardCopy4[x])
#fim função buildTree

#def minmax():
	#monta árvore:

#fim função minax

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
            buildTree(mainBoard, computerTile, playerTile)
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

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import _thread as thread
import random
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
root = Builder.load_string("""
<Block>:
	size_hint:None, None
	size:"45dp", "45dp"
	block_image_object:block_image
	id:block_image
	background_normal:"icons/None"
	background_down:"icons/0_162_232.png"
<EmptyBlock>:
	current_box_object:current_box
	id:current_box
	size_hint:None, None
	size:"45dp", "45dp"
	padding:5
<BlocksBox>:
	pieces_layout_object:pieces_layout
	green_layout_object:green_layout
	black_layout_object:black_layout
	canvas:
		Color:
			rgb:230/float(255), 230/float(255), 230/float(255)
		Rectangle:
			size:self.size
			pos:self.pos
	FloatLayout:
		BoxLayout:
			orientation:"vertical"
			BoxLayout:
			BoxLayout:
				size_hint_y:None
				height:"360dp"
				BoxLayout:
				BlocksGrid:
					size_hint:None, None
					size:"360dp", "360dp"
					cols:8
					rows:8
				BoxLayout:
			BoxLayout:
		BoxLayout:
			orientation:"vertical"
			BoxLayout:
				orientation:"vertical"
				BoxLayout:
				BoxLayout:
					size_hint_y:None
					height:"45dp"
					BoxLayout:
					GridLayout:
						id:green_layout
						canvas:
							Color:
								rgb:23/float(255), 234/float(255), 137/float(255)
							Rectangle:
								size:self.size
								pos:self.pos
						cols:8
						size_hint_x:None
						width:"360dp"
					BoxLayout:
				BoxLayout:
			BoxLayout:
				size_hint_y:None
				height:"360dp"
				BoxLayout:
				PiecesBlocksLayout:
					size_hint:None, None
					size:"360dp", "360dp"
					id:pieces_layout
					cols:8
					rows:8
				BoxLayout:
			BoxLayout:
				orientation:"vertical"
				BoxLayout:
				BoxLayout:
					size_hint_y:None
					height:"45dp"
					BoxLayout:
					GridLayout:
						id:black_layout
						canvas:
							Color:
								rgb:195/float(255), 195/float(255), 195/float(255)
							Rectangle:
								size:self.size
								pos:self.pos
						cols:8
						size_hint_x:None
						width:"360dp"
					BoxLayout:
				BoxLayout:
""")
def getRootBox(starting_box, specified_root_box = None):
    parent_box = starting_box.parent
    box = True
    while box:
        print(parent_box)
        parent_box = parent_box.parent
        core = parent_box.parent
        if specified_root_box != None:
            if specified_root_box in str(parent_box):
                root_box = parent_box
                return root_box
        elif core == parent_box:
            box = False
        else:
            root_box = parent_box
    return root_box
class BlocksBox(BoxLayout):
	pass
class Block(Button):
	pass
class EmptyBlock(BoxLayout):
	pass		
class BlocksGrid(GridLayout):
	def __init__(self, **kwargs):
		super(BlocksGrid, self).__init__(**kwargs)
		block_one = "icons/0_162_232.png"
		block_two = "icons/230_230_230.png"
		counter = 0
		for i in range(1, 65):
			block = Block()
			block.bind(on_press = self.pressBlock)
			if counter == 8:
				temp = block_one
				block_one = block_two
				block_two = temp
				counter = 0
			if (i%2 == 0):
				block.block_image_object.background_normal  = block_two
				block.block_image_object.background_down = block_two
			else:
				block.block_image_object.background_normal = block_one
				block.block_image_object.background_down = block_one
			counter = counter + 1
			self.add_widget(block)
	def pressBlock(self, block):
		parent = getRootBox(self)
		block_pos = (self.children.index(block)//8, self.children.index(block)%8)
		block_index = block_pos[0] * 8 + block_pos[1]
		if block_pos in parent.pieces_layout_object.possible_moves:
			parent.pieces_layout_object.movePiece(block_index)
class PiecesBlocksLayout(GridLayout):
	def __init__(self, **kwargs):
		super(PiecesBlocksLayout, self).__init__(**kwargs)
		self.pieces = [("R", 2), ("N", 2), ("B", 2), ("Q", 1), ("K", 1), ("P", 8)]
		self.incrementer = 0
		self.piece_class = dict()
		self.grid_blocks = self.generateGridBlocks()
		self.possible_moves = []
		self.piece_pos = []
		self.bot_play = 0
		self.user_play = 1
		self.bot_color = "black"
		self.player_color = "white"
		chess_bot = ChessBot(self)
		thread.start_new_thread(chess_bot.main, (self,))
		self.decrementer = len(self.children) - 1
		self.down_counter = 7
		for i in range(1, 65):
			empty_block = EmptyBlock()
			self.add_widget(empty_block)
		for piece in self.pieces:
			if piece[1] == 1:
				black_button = Button()
				white_button = Button()
				self.piece_class[black_button] = "black"
				self.piece_class[white_button] = "white"
				black_button.text = piece[0]
				white_button.text = piece[0]
				black_button.color = [23/float(255), 234/float(255), 137/float(255), 1]
				if piece[0] == "Q":
					black_button.bind(on_press = self.pieceEater)
					white_button.bind(on_press = self.detectQueenMove)
				elif piece[0] == "K":	
					black_button.bind(on_press = self.pieceEater)
					white_button.bind(on_press = self.detectKingMove)
				self.children[self.incrementer].current_box_object.add_widget(white_button)
				self.children[self.decrementer].current_box_object.add_widget(black_button)
			elif piece[1] == 2:
				print(piece[0])
				black_button_one = Button()
				black_button_one.text = piece[0]
				black_button_one.bind(on_press = self.pieceEater)
				black_button_one.color = [23/float(255), 234/float(255), 137/float(255), 1]
				black_button_two = Button()
				black_button_two.text = piece[0]
				black_button_two.bind(on_press = self.pieceEater)
				black_button_two.color = [23/float(255), 234/float(255), 137/float(255), 1]
				white_button_one = Button()
				white_button_one.text = piece[0]
				white_button_two = Button()
				white_button_two.text = piece[0]
				self.piece_class[white_button_one] = "white"
				self.piece_class[white_button_two] = "white"
				self.piece_class[black_button_one] = "black"
				self.piece_class[black_button_two] = "black"
				white_button_one  = self.addButtonsFunction(white_button_one, piece)
				white_button_two  = self.addButtonsFunction(white_button_two, piece)
				self.children[self.incrementer].current_box_object.add_widget(white_button_one)
				self.children[7 - self.incrementer].current_box_object.add_widget(white_button_two)
				self.children[self.decrementer].current_box_object.add_widget(black_button_one)
				self.children[self.decrementer - self.down_counter].current_box_object.add_widget(black_button_two)
				self.down_counter -= 2
			else:
				self.incrementer += 3
				self.decrementer -= 3
				for i in range(8):
					black_button = Button()
					black_button.text = piece[0]
					black_button.bind(on_press = self.pieceEater)
					black_button.color = [23/float(255), 234/float(255), 137/float(255), 1]
					white_button = Button()
					white_button.bind(on_press = self.detectPawnMove)
					white_button.text = piece[0]
					self.piece_class[black_button]  = "black"
					self.piece_class[white_button] = "white"
					self.children[self.incrementer].current_box_object.add_widget(white_button)
					self.children[self.decrementer].current_box_object.add_widget(black_button)
					self.decrementer -= 1
					self.incrementer += 1
			self.incrementer += 1	
			self.decrementer -= 1
	def addButtonsFunction(self, button_one, _piece):
		if _piece[0] == "R":
			button_one.bind(on_press = self.detectRoockMove)
		elif _piece[0] == "N":
			button_one.bind(on_press = self.detectKnightMove)
		elif _piece[0] == "B":
			button_one.bind(on_press = self.detectBishopMove)
		return button_one
	def generateGridBlocks(self):
		grid = []
		for i in range(8):
			sub_list = list()
			for j in range(8):
				if (i > 1) and (i < 6):
					sub_list.append(0)
				else:
					sub_list.append(1)
			grid.append(sub_list)
		return grid
	def checkPieceExistence(self, pos):
		try:
			piece_indicator = self.grid_blocks[pos[0]][pos[1]]
			return piece_indicator
		except:
			return 1
	def eatBlackPawn(self, pawn):
		pawn_block = pawn.parent
		pawn_block_pos = self.children.index(pawn_block)
		pawn_pos = (pawn_block_pos//8, pawn_block_pos%8)
		if pawn_pos in self.possible_moves:
			self.children[pawn_block_pos].remove_widget(pawn)
			self.piece_class.pop(pawn)
			self.movePiece(pawn_block_pos)
	def pieceEater(self, piece):
		piece_block = piece.parent
		piece_block_pos = self.children.index(piece_block)
		piece_pos = (piece_block_pos//8, piece_block_pos%8)
		parent = getRootBox(self)
		if piece_pos in self.possible_moves:
			print("piece eater after if condition")
			self.children[piece_block_pos].remove_widget(piece)
			self.piece_class.pop(piece)
			box = BoxLayout(size_hint= (None, None), size = ("45dp", "45dp"))
			box.add_widget(piece)
			parent.green_layout_object.add_widget(box)
			self.movePiece(piece_block_pos) 
	def detectKingMove(self, king, bot_play = 0):
		king_parent = king.parent
		king_parent_pos = self.children.index(king_parent)
		king_pos = (king_parent_pos//8, king_parent_pos%8)
		self.piece_pos = list(king_pos)
		if (self.user_play):
			open_blocks = self.findKingMoves(king_pos)
			self.possible_moves = open_blocks
		elif (bot_play == 1) or (bot_play == 0):
			open_blocks = self.findKingMoves(king_pos)
			self.possible_moves = open_blocks
	def detectQueenMove(self, queen, bot_play = 0):
		queen_parent = queen.parent
		queen_parent_pos = self.children.index(queen_parent)
		queen_pos = (queen_parent_pos//8, queen_parent_pos%8)
		self.piece_pos = list(queen_pos)
		if (self.user_play):
			open_blocks = self.findQueenMoves(queen_pos)
			self.possible_moves = open_blocks
		elif (bot_play == 1) or (bot_play == 0):
			open_blocks = self.findQueenMoves(queen_pos)
			self.possible_moves = open_blocks
		print("queen moves:", self.possible_moves)
	def detectBishopMove(self, bishop, bot_play = 0):
		bishop_parent = bishop.parent
		bishop_parent_pos = self.children.index(bishop_parent)
		bishop_pos = (bishop_parent_pos//8, bishop_parent_pos%8)
		self.piece_pos = list(bishop_pos)
		if (self.user_play):
			open_blocks = self.findBishopMoves(bishop_pos)
			self.possible_moves = open_blocks
		elif (bot_play == 1) or (bot_play == 0):
			open_blocks = self.findBishopMoves(bishop_pos)
			self.possible_moves = open_blocks
		print("bishop moves:", self.possible_moves)
	def detectKnightMove(self, knight, bot_play = 0):
		knight_parent = knight.parent
		knight_parent_pos = self.children.index(knight_parent)
		knight_pos = (knight_parent_pos//8, knight_parent_pos%8)
		self.piece_pos = list(knight_pos)
		if (self.user_play):
			open_blocks = self.findKnightOpenMovesBlocks(knight_pos)
			self.possible_moves = open_blocks
		elif (bot_play == 1) or (bot_play == 0):
			open_blocks = self.findKnightOpenMovesBlocks(knight_pos)
			self.possible_moves = open_blocks
		print("Night moves:", self.possible_moves)	
	def detectRoockMove(self, roock, bot_play = 0):
		roock_parent = roock.parent
		roock_parent_pos = self.children.index(roock_parent)
		roock_pos = (roock_parent_pos//8, roock_parent_pos%8)
		self.piece_pos = list(roock_pos)
		if (self.user_play):
			open_blocks = self.findRoockOpenBlocks(roock_pos)
			self.possible_moves = open_blocks
		elif (bot_play == 1) or (bot_play == 0):
			open_blocks = self.findRoockOpenBlocks(roock_pos)
			self.possible_moves = open_blocks
		print("Roock:", self.possible_moves)
	def detectPawnMove(self, pawn, bot_play = 0):
		pawn_parent = pawn.parent
		pawn_parent_pos = self.children.index(pawn_parent)
		pawn_pos = (pawn_parent_pos//8, pawn_parent_pos%8)
		self.piece_pos = list(pawn_pos)
		if self.user_play:
			open_blocks = self.findPawnOpenBlock(pawn_pos)
			if (pawn_pos[0] == 1) and (open_blocks):
				open_blocks.append((3, pawn_pos[1]))
			self.possible_moves = open_blocks
		elif (bot_play == 1) or (bot_play == 0):
			open_blocks = self.findPawnOpenBlock(pawn_pos)
			if (pawn_pos[0] == 1) and (self.grid_blocks[pawn_pos[0]][pawn_pos[1]]==0):
				open_blocks.append((3, pawn_pos[1]))
			self.possible_moves = open_blocks
	def detectOppositePawnMove(self, pawn):
		pawn_parent = pawn.parent
		pawn_parent_pos = self.children.index(pawn_parent)
		pawn_pos = (pawn_parent_pos//8, pawn_parent_pos%8)
		self.piece_pos = list(pawn_pos)
		open_blocks = self.findOppositePawnOpenBlock(pawn_pos)
		if (pawn_pos[0] == 6) and (self.grid_blocks[pawn_pos[0]][pawn_pos[1]]==0):
			open_blocks.append((4, pawn_pos[1]))
		self.possible_moves = open_blocks
	def movePiece(self, new_block_index):
		index = self.piece_pos[0] * 8 + self.piece_pos[1]
		piece_block = self.children[index]
		new_block_pos = (new_block_index//8, new_block_index%8)
		if new_block_index != index:
			try:
				piece = piece_block.children[0]
				piece_block.remove_widget(piece)
				self.grid_blocks[self.piece_pos[0]][self.piece_pos[1]] = 0
				self.children[new_block_index].add_widget(piece)
				self.grid_blocks[new_block_pos[0]][new_block_pos[1]] = 1
			except:
				pass
		self.user_play = 0
		self.bot_play = 1
	def getPiecesAttacking(self, piece, opponent_move, layout_object):
		piece_index = layout_object.children.index(piece)
		piece_pos = [piece_index//8, piece_index%8]
		attacking_pieces = []
		for open_place in opponents_move:
			if piece_pos in open_place[1]:
				attacking_pieces.append(open_place)
		return attacking_pieces
	def checkIfPiecesAreSameKind(self, piece_one_index, piece_two_index):
		try:
			piece_one_block = self.children[piece_one_index]
			piece_two_block = self.children[piece_two_index]
			piece_two = piece_two_block.children[0]
			if self.piece_class[piece_one_block.children[0]] != self.piece_class[piece_two]:
				return True
		except:
			return False
		return False
	def findOppositePawnOpenBlock(self, pawn_pos):
		if pawn_pos[0] == 0:
			return []
		opening_moves = []
		try:
			opening_moves + self.findDownBlock(opening_moves, pawn_pos)
		except:
			opening_moves = opening_moves + []
		try:
			open_blocks = self.findDownLeftDiagnalBlock([], pawn_pos)
			if len(open_blocks) == 0:			
				piece_block = self.children[(pawn_pos[0] -1) * 8 + (pawn_pos[1] - 1)]
				current_piece_block = self.children[pawn_pos[0] * 8  + pawn_pos[1]]
				current_piece = current_piece_block.children[0]
				if self.piece_class[piece_block.children[0]] != self.piece_class[current_piece]:
					opening_moves.append((pawn_pos[0] -1, pawn_pos[1] - 1))
		except:
			opening_moves = opening_moves + []
		try:
			open_blocks = self.findDownRightDiagnalBlock([], pawn_pos)
			if len(open_blocks) == 0:
				piece_block = self.children[(pawn_pos[0] - 1) * 8 + (pawn_pos[1] +1)]
				current_piece_block = self.children[pawn_pos[0] * 8 + pawn_pos[1]]
				current_piece = current_piece_block.children[0]
				if self.piece_class[piece_block.children[0]] != self.piece_class[current_piece]:
					opening_moves.append((pawn_pos[0] - 1, pawn_pos[1] + 1))
		except:
			opening_moves = opening_moves + []
		return opening_moves
	def findPawnOpenBlock(self, pawn_pos):
		opening_moves = []
		try:
			opening_moves + self.findForwardBlock(opening_moves, pawn_pos)
		except:
			opening_moves = opening_moves + []
		try:
			open_blocks = self.findLeftDiagnalBlock([], pawn_pos)
			if len(open_blocks) == 0:			
				piece_block = self.children[(pawn_pos[0] + 1) * 8 + (pawn_pos[1] + 1)]
				current_piece_block = self.children[pawn_pos[0] * 8  + pawn_pos[1]]
				current_piece = current_piece_block.children[0]
				if self.piece_class[piece_block.children[0]] != self.piece_class[current_piece]:
					opening_moves.append((pawn_pos[0] + 1, pawn_pos[1] + 1))
		except:
			opening_moves = opening_moves + []
		try:
			open_blocks = self.findRightDiagnalBlock([], pawn_pos)
			if len(open_blocks) == 0:
				piece_block = self.children[(pawn_pos[0] + 1) * 8 + (pawn_pos[1] - 1)]
				current_piece_block = self.children[pawn_pos[0] * 8 + pawn_pos[1]]
				current_piece = current_piece_block.children[0]
				if self.piece_class[piece_block.children[0]] != self.piece_class[current_piece]:
					opening_moves.append((pawn_pos[0] + 1, pawn_pos[1] - 1))
		except:
			opening_moves = opening_moves + []
		return opening_moves
	def findRoockOpenBlocks(self, roock_pos):
		opening_moves = []
		try:
		 	blocks = self.findHorizontalBlocks(1, roock_pos)
		 	opening_moves = opening_moves + blocks
		except:
		 	opening_moves + []
		try:
		 	blocks = self.findHorizontalBlocks(-1, roock_pos)
		 	opening_moves = opening_moves + blocks
		except:
		 	opening_moves + []
		try:
		 	blocks = self.findVerticalBlocks(1, roock_pos)
		 	opening_moves = opening_moves + blocks
		except:
		 	opening_moves + []
		try:
		 	blocks = self.findVerticalBlocks(-1, roock_pos)
		 	opening_moves = opening_moves + blocks
		except:
		 	opening_moves + []
		return opening_moves
	def findKnightOpenMovesBlocks(self, piece_pos):
		open_blocks = []
		blocks_options = [[2, 1], [2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
		for block in blocks_options:
			if (((piece_pos[0] + block[0]) >= 0) and ((piece_pos[0] + block[0]) < 8)) and (((piece_pos[1] + block[1]) >= 0) and ((piece_pos[1] + block[1]) < 8)):
				if not self.checkPieceExistence((piece_pos[0] +block[0], piece_pos[1] + block[1])):
					open_blocks.append((piece_pos[0] + block[0], piece_pos[1] + block[1]))
				else:
					piece_index = piece_pos[0] * 8 + piece_pos[1]
					piece_two_index = (piece_pos[0] + block[0]) * 8 + (block[1] + piece_pos[1])
					not_same_kind = self.checkIfPiecesAreSameKind(piece_index, piece_two_index)
					if not_same_kind:
						open_blocks.append((piece_pos[0] + block[0], piece_pos[1] + block[1]))
		return open_blocks
	def findVerticalBlocks(self, operator, piece_pos):
		blocks = []
		counter = piece_pos[0]
		piece_index = piece_pos[0] * 8 + piece_pos[1]
		if operator > 0:
			while counter < 8:
				block = self.findForwardBlock([], (counter, piece_pos[1]))
				if len(block) > 0:
					blocks.append(block[0])
				else:
					counter = counter + 1
					piece_two_index = counter * 8 + piece_pos[1]
					not_same_kind = self.checkIfPiecesAreSameKind(piece_index, piece_two_index)
					if not_same_kind:
						blocks.append((counter, piece_pos[1]))
					break	
				counter = counter + 1
		else:
			while counter > 0:
				block = self.findDownBlock([], (counter, piece_pos[1]))
				if len(block) > 0:
					blocks.append(block[0])
				else:
					counter = counter - 1
					piece_two_index = counter * 8 + piece_pos[1]
					not_same_kind = self.checkIfPiecesAreSameKind(piece_index, piece_two_index)
					if not_same_kind:
						blocks.append((counter, piece_pos[1]))
					break
				counter = counter - 1
		return blocks
	def findHorizontalBlocks(self, operator, piece_pos):
		blocks = []
		piece_index = piece_pos[0] * 8 + piece_pos[1]
		counter = piece_pos[1]
		if operator > 0:
			while counter < 8:
				block = self.findLeftBlock([], (piece_pos[0], counter))
				if len(block) > 0:
					blocks.append(block[0])
				else:
					counter = counter + 1
					piece_two_index = counter + piece_pos[0] * 8
					not_same_kind = self.checkIfPiecesAreSameKind(piece_index, piece_two_index)
					if not_same_kind:
						blocks.append((piece_pos[0], counter))
					break
				counter = counter + 1
		else:
			while counter > 0:
				block = self.findRightBlock([], (piece_pos[0], counter))
				if len(block) > 0:
					blocks.append(block[0])
				else:
					counter = counter - 1
					piece_two_index = counter + piece_pos[0] * 8
					not_same_kind = self.checkIfPiecesAreSameKind(piece_index, piece_two_index)
					if not_same_kind:
						blocks.append((piece_pos[0], counter))
					break
				counter = counter - 1
		return blocks
	def findDiagnalBlock(self, piece_pos, operator_list):
		blocks_list = []
		if (operator_list[0] < 0) and (operator_list[1] > 0):
			blocks_list = self.findRightDiagnalBlock([], piece_pos)
		elif (operator_list[0] > 0) and (operator_list[1] < 0):
			blocks_list = self.findDownRightDiagnalBlock([], piece_pos)
		elif (operator_list[0] > 0) and (operator_list[1] > 0):
			blocks_list = self.findLeftDiagnalBlock([], piece_pos)
		elif (operator_list[0] < 0) and (operator_list[1] < 0):
			blocks_list = self.findDownLeftDiagnalBlock([], piece_pos)
		return blocks_list
	def getCondition(self, x, y, operator_list):
		if (operator_list[0] > 0) and (operator_list[1] < 0):
			if (x < 8) and (y > 0 ):
				return True
		elif (operator_list[0] < 0) and (operator_list[1] > 0):
			if (x > 0) and (y < 8):
				return True
		elif (operator_list[0] > 0) and (operator_list[1] > 0):
			if (x < 8) and (y < 8):
				return True
		elif (operator_list[0] < 0) and (operator_list[1] < 0):
			if (x > 0) and (y > 0):
				return True
		return False
	def findBishopOpenBlocks(self, piece_pos, operator_list):
		x_counter = piece_pos[1]
		y_counter = piece_pos[0]
		blocks = []
		while (self.getCondition(x_counter, y_counter, operator_list)):
			 blocks_list = self.findDiagnalBlock((y_counter, x_counter), operator_list)
			 if len(blocks_list):
			 	blocks.append(blocks_list[0])
			 else:
			 	piece_two_index = (y_counter + operator_list[1])*8 + (x_counter + operator_list[0])
			 	piece_index = piece_pos[0]*8 + piece_pos[1]
			 	not_same_kind = self.checkIfPiecesAreSameKind(piece_index, piece_two_index)
			 	if not_same_kind:
			 		blocks.append((y_counter + operator_list[1], x_counter + operator_list[0]))
			 	break
			 x_counter = x_counter + operator_list[0]
			 y_counter = y_counter + operator_list[1]
		return blocks
	def findBishopMoves(self, piece_pos):
		open_moves = []
		blocks = self.findBishopOpenBlocks(piece_pos, [1, 1])
		open_moves = open_moves + blocks
		blocks = self.findBishopOpenBlocks(piece_pos, [-1, -1])
		open_moves = open_moves + blocks
		blocks = self.findBishopOpenBlocks(piece_pos, [-1, 1])
		open_moves = open_moves + blocks
		blocks = self.findBishopOpenBlocks(piece_pos, [1, -1])
		open_moves = open_moves + blocks
		return open_moves
	def findQueenMoves(self, piece_pos):
		open_moves = []
		bishop_blocks = self.findBishopMoves(piece_pos)
		roock_blocks = self.findRoockOpenBlocks(piece_pos)
		return bishop_blocks + roock_blocks
	def generateNeighboringBlocks(self, piece_pos):
		blocks = []
		ops = [[1, 0], [-1, 0], [0, -1], [0, 1], [1, 1], [1, -1], [-1, -1], [-1, 1]]
		for op in ops:
			if (((piece_pos[0] + op[0]) >= 0) and ((piece_pos[1] + op[1]) >=0)):
				blocks.append(((piece_pos[0] + op[0]), (piece_pos[1] + op[1]) ))
		return blocks
	def findKingMoves(self, piece_pos):
		king_blocks = []
		generated_blocks = self.generateNeighboringBlocks(piece_pos)
		queen_blocks = self.findQueenMoves(piece_pos)
		for block in queen_blocks:
			if block in generated_blocks:
				king_blocks.append(block)
		return king_blocks
	def findForwardBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0] + 1,  piece_pos[1])):
			opening_moves.append((piece_pos[0] + 1, piece_pos[1]))
		return opening_moves
	def findDownBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0] - 1, piece_pos[1])):
			opening_moves.append((piece_pos[0] - 1, piece_pos[1]))
		return opening_moves
	def findLeftBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0], piece_pos[1] + 1)):
			opening_moves.append((piece_pos[0] , piece_pos[1] + 1))
		return opening_moves
	def findRightBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0], piece_pos[1] - 1)):
			opening_moves.append((piece_pos[0], piece_pos[1] - 1))
		return opening_moves
	def findLeftDiagnalBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0] + 1, piece_pos[1] + 1)):
			opening_moves.append((piece_pos[0] + 1, piece_pos[1] + 1))
		return opening_moves
	def findDownLeftDiagnalBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0] - 1, piece_pos[1] - 1)):
			opening_moves.append((piece_pos[0] - 1, piece_pos[1] - 1))
		return opening_moves
	def findRightDiagnalBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0] + 1,  piece_pos[1] - 1)):
			opening_moves.append((piece_pos[0] + 1, piece_pos[1] - 1))
		return opening_moves
	def findDownRightDiagnalBlock(self, opening_moves, piece_pos):
		if not self.checkPieceExistence((piece_pos[0] - 1, piece_pos[1] + 1)):
			opening_moves.append((piece_pos[0] - 1, piece_pos[1] + 1))
		return opening_moves
class ChessBot:
	def __init__(self, layout_grid):
		self.layout_grid = layout_grid
		self.back_up_table = {"K":["P", "N", "B", "R", "Q"], "Q":["P", "N", "B", "R"], "R":["P", "N", "B"], "N":["P"], "P":["P"]}
	def getMoves(self, piece, layout_grid, player = 1):
		if piece.text =="K":
			layout_grid.detectKingMove(piece, player)
		elif piece.text =="Q":
			layout_grid.detectQueenMove(piece, player)
		elif piece.text == "R":
			layout_grid.detectRoockMove(piece, player)
		elif piece.text == "B":
			layout_grid.detectBishopMove(piece, player)
		elif piece.text == "N":
			layout_grid.detectKnightMove(piece, player)
		elif (piece.text == "P") and player:
			layout_grid.detectOppositePawnMove(piece)
		else:
			layout_grid.detectPawnMove(piece, player)
		return layout_grid.possible_moves
	def getOpponentsPossibleMove(self, layout_grid, opponent_color):
		opponent_moves = []
		counter =0
		for piece_object in layout_grid.piece_class:
			if layout_grid.piece_class[piece_object] == opponent_color:
				piece_moves = self.getMoves(piece_object, layout_grid, 0)
				opponent_moves.append((piece_object, piece_moves))
				counter += 1
		return opponent_moves
	def getPiecesAttacking(self, piece, opponent_moves, layout_grid):
		piece_index = layout_grid.children.index(piece.parent)
		piece_pos = [piece_index//8, piece_index%8]
		attacking_pieces = []
		for open_place in opponent_moves:
			if piece_pos in open_place[1]:
				attacking_pieces.append(open_place)
		return attacking_pieces
	def checkPieceVulnarability(self, piece_pos, opponent_moves):
		for opponent_piece_moves in opponent_moves:
			if piece_pos in opponent_piece_moves[1]:
				return True
		return False
	def getOccupiedMoves(self, list_of_possible_moves, board_grid):
		occupied_moves = []
		for piece_pos in list_of_possible_moves:
			if board_grid[piece_pos[0]][piece_pos[1]] == 1:
				occupied_moves.append(piece_pos)
		return occupied_moves
	def getSafeAttacks(self, piece, layout_grid, opponent_color):
		safe_attacks = []
		possible_moves = self.getMoves(piece, layout_grid)
		occupied_moves = self.getOccupiedMoves(possible_moves, layout_grid.grid_blocks)
		opponents_moves = self.getOpponentsPossibleMove(self.layout_grid, self.layout_grid.player_color)
		for piece_pos in occupied_moves:
			layout_grid.grid_blocks[piece_pos[0]][piece_pos[1]] = 0
			exist = self.checkPieceVulnarability(piece_pos, opponents_moves)
			if not exist:
				safe_attacks.append(piece_pos)
			layout_grid.grid_blocks[piece_pos[0]][piece_pos[1]] = 1
		return safe_attacks
	def getBackUp(self, piece, layout_grid, back_up_table, attacking_pieces, color):
		back_up_list = back_up_table[piece.text]
		if len(back_up_list) >= 1:
			for piece_name in back_up_list:
				for fellow_piece in layout_grid.piece_class:
					if (fellow_piece.text == piece_name) and (layout_grid.piece_class[fellow_piece] == color):
						fellow_piece_moves = self.getMoves(fellow_piece, layout_grid)
						for move in fellow_piece_moves:
							if move in attacking_pieces:
								return move, fellow_piece
		return [], None
	def getSafeBlocks(self, piece, layout_grid, opponents_moves):
		possible_moves = self.getMoves(piece, layout_grid)
		safe_moves_list = []
		for move in possible_moves:
			if layout_grid.grid_blocks[move[0]][move[1]] == 0:
				piece_safe = True
				for open_place in opponents_moves:
					if move in open_place[1]:
						piece_safe = False
						break
				if piece_safe:
					safe_moves_list.append(move)
		return safe_moves_list
	def collectPiecePossibleNextMove(self, piece_object):
		piece = piece_object.children[0]
		piece_index = self.layout_grid.children.index(piece.parent)
		piece_pos = (piece_index//8, piece_index%8)
		opponents_moves = self.getOpponentsPossibleMove(self.layout_grid, self.layout_grid.player_color)
		vulnarable = self.checkPieceVulnarability(piece_pos, opponents_moves)
		safe_attacks = self.getSafeAttacks(piece, self.layout_grid, self.layout_grid.player_color)
		safe_blocks = self.getSafeBlocks(piece, self.layout_grid, opponents_moves)
		attacking_pieces = self.getPiecesAttacking(piece, opponents_moves, self.layout_grid)
		back_up, fellow_piece = self.getBackUp(piece, self.layout_grid, self.back_up_table, attacking_pieces, self.layout_grid.player_color)
		if len(safe_attacks) > 0:
			next_move = random.choice(safe_attacks)
			print("opponents_moves : ", opponents_moves)
			print(piece.text, "-- is attacking", next_move, "at", piece_pos, "vulnerability :", vulnarable)
			return next_move, piece, True
		elif len(safe_blocks) > 0:
			next_move = random.choice(safe_blocks)
			return next_move, piece, vulnarable
		elif back_up:
			return back_up, fellow_piece, vulnarable
	def calculateNextMove(self, layout_grid):
		checked_objects = []
		possible_move = []
		counter = 1
		for key in self.back_up_table:
			if counter == 1:
				print("KEY:", key)
			if (key == "P"):
				counter = 8
			elif (key == "R") or (key == "N"):
				counter = 2
			for i in range(counter):
				for piece in layout_grid.piece_class:
					if (piece.text == key) and (piece not in checked_objects) and (layout_grid.piece_class[piece] == layout_grid.bot_color):
						checked_objects.append(piece)
						move_list = self.collectPiecePossibleNextMove(piece.parent)
						try:
							if move_list[2] == True:
								return move_list[0], move_list[1]
							else:
								if move_list[0]:
									possible_move.append((move_list[0], move_list[1]))
						except:
							pass
		return random.choice(possible_move)
	def isButtonObjectPresent(self, layout_grid, block_pos):
		if (layout_grid.grid_blocks[block_pos[0]][block_pos[1]] == 1):
			return True
		else:
			return False
	def botEatPiece(self, piece, layout_grid):
		parent = getRootBox(layout_grid)
		piece_block = piece.parent
		piece_block_pos = layout_grid.children.index(piece_block)
		piece_pos = (piece_block_pos//8, piece_block_pos%8)
		layout_grid.children[piece_block_pos].remove_widget(piece)
		layout_grid.piece_class.pop(piece)
		box = BoxLayout(size_hint= (None, None), size = ("45dp", "45dp"))
		box.add_widget(piece)
		parent.black_layout_object.add_widget(box)
		layout_grid.movePiece(piece_block_pos)
	def main(self, layout_grid):
		while True:
			if layout_grid.bot_play:
				next_move, _object = self.calculateNextMove(layout_grid)
				pos_index = layout_grid.children.index(_object.parent)
				layout_grid.piece_pos = [pos_index//8, pos_index%8]
				next_move_index = next_move[0] * 8 + next_move[1]
				button_presence = self.isButtonObjectPresent(layout_grid, next_move)
				next_block = layout_grid.children[next_move_index]
				if button_presence:
					self.botEatPiece(next_block.children[0], layout_grid)
				else:
					layout_grid.movePiece(next_move_index)
				layout_grid.bot_play = 0
				layout_grid.user_play = 1
class TestApp(App):
	def build(self):
		root = BlocksBox()
		return root
if __name__ =="__main__":
	TestApp().run()
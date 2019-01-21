import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
from random import randint


class Vector2D:
	def __init__(self, x, y):
		self.x, self.y = x, y
	def __init__(self, t):
		self.x, self.y = t
	def __add__(self, vector2d):
		return Vector2D(self.x + vector2d.x, self.y + vector2d.y)
	def __sub__(self, vector2d):
		return Vector2D(self.x - vector2d.x, self.y - vector2d.y)
	def __eq__(self, vector2d):
		return self.x == vector2d.x and self.y == vector2d.y
	def __len__(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5
	def __str__(self):
		return str(self.x) + ", " + str(self.y)
	def __repr__(self):
		return str(self)
	def __mul__(self, vector2d):
		return self.x * vector2d.x + self.y * vector2d.y
	def __getitem__(self, index):
		return (self.x, self.y)[index]


class GameJudge:
	_DX = [-1, +1, 0, 0]
	_DY = [0, 0, -1, +1]
	_MAXIMUM_TURNS_COUNT = 250
	_COW_CELL = 'C'
	_STABLE_CELL = 'S'
	_WOLF_CELL = 'W'
	_FLAG_CELL = 'F'
	_EMPTY_CELL = 'E'
	_PLAYER_CELL = 'P'

	_MAP_WIDTH = 10
	_MAP_HEIGHT = 10

	_COWS_COUNT = 5
	_WOLVES_COUNT = 1
	_FLAGS_COUNT = 1
	_STABLES_COUNT = 1

	_COW_IMAGE_PATH = 'cow.png'
	_PLAYER_IMAGE_PATH = 'player.png'
	_FLAG_IMAGE_PATH = 'flag.png'
	_STABLE_IMAGE_PATH = 'stable.png'
	_WOLF_IMAGE_PATH = 'wolf.png'
	_EMPTY_IMAGE_PATH = 'empty.png'
	_IMAGES_PATH = {}

	def _is_move_valid(self, move_direction):
		pass

	def _put_cell_on_map(self, cell):
		x, y = randint(0, self._MAP_WIDTH - 1), randint(0, self._MAP_HEIGHT - 1)
		while self._map[y][x] != self._EMPTY_CELL:
			x, y = randint(0, self._MAP_WIDTH - 1), randint(0, self._MAP_HEIGHT - 1)
		self._map[y][x] = cell
		return x, y

	def __init__(self, player=None):
		self._turns_count = 0
		self._player_score = 0.0
		self._map = [[self._EMPTY_CELL for j in range(self._MAP_WIDTH)] for i in range(self._MAP_HEIGHT)]
		self._player_has_flag = False
		self._player_position = Vector2D(self._put_cell_on_map(self._PLAYER_CELL))
		self._stable_position = self._put_cell_on_map(self._STABLE_CELL)
		for i in range(self._WOLVES_COUNT):
			self._put_cell_on_map(self._WOLF_CELL)
		for i in range(self._FLAGS_COUNT):
			self._put_cell_on_map(self._FLAG_CELL)
		for i in range(self._COWS_COUNT):
			self._put_cell_on_map(self._COW_CELL)
		self._player = player
		self._IMAGES_PATH[self._COW_CELL] = self._COW_IMAGE_PATH
		self._IMAGES_PATH[self._PLAYER_CELL] = self._PLAYER_IMAGE_PATH
		self._IMAGES_PATH[self._STABLE_CELL] = self._STABLE_IMAGE_PATH
		self._IMAGES_PATH[self._FLAG_CELL] = self._FLAG_IMAGE_PATH
		self._IMAGES_PATH[self._WOLF_CELL] = self._WOLF_IMAGE_PATH
		self._IMAGES_PATH[self._EMPTY_CELL] = self._EMPTY_IMAGE_PATH
		
	def _do_turn(self):
		x, y = self._player_position.x, self._player_position.y
		player_neighbors = []
		for x2 in range(x - 1, x + 2):
			for y2 in range(y - 1, x + 2):
				if _is_inside_map(x2, y2) and self._map[y2][x2] not in player_neighbors:
					player_neighbors.append(self._map[y2][x2])
		player_move_direction = self.player.move(player_position=self._player_position, stable_position=self._stable_position, player_neighbors=player_neighbors)
		if self._is_move_valid(player_move_direction):
			_update_map(player_move_direction)

	def run(self):
		for i in range(_MAXIMUM_TURNS_COUNT):
			_do_turn()
			self._turns_count = i + 1

	def show_map(self):
		plt.figure(figsize=(8, 8))
		for y in range(self._MAP_HEIGHT):
			for x in range(self._MAP_WIDTH):
				plt.subplot(self._MAP_HEIGHT, self._MAP_WIDTH, y * self._MAP_WIDTH + x + 1,)
				plt.imshow(cv2.imread(self._IMAGES_PATH[self._map[y][x]], cv2.IMREAD_COLOR))
				plt.xticks([])
				plt.yticks([])
		plt.subplots_adjust(wspace=0, hspace=0)
		plt.show()
		# plt.pause()


game_judge = GameJudge()

game_judge.show_map()
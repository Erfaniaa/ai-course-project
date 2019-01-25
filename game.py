import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
from random import randint


COW_CELL = 'C'
STABLE_CELL = 'S'
WOLF_CELL = 'W'
FLAG_CELL = 'F'
EMPTY_CELL = 'E'
PLAYER_CELL = 'P'


class Vector2D:
	def __init__(self, x, y):
		self.x, self.y = x, y
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


class Player:
	_DX = [-1, +1, 0, 0]
	_DY = [0, 0, -1, +1]

	_MAP_WIDTH = 10
	_MAP_HEIGHT = 10

	def __init__(self):
		self._cells_score = {}
		self._cells_visits_count = {}
		self._player_last_position = Vector2D(0, 0)
		self._last_move_direction = None

	def _is_inside_map(self, position):
		if position.x < 0 or position.x >= self._MAP_WIDTH:
			return False
		if position.y < 0 or position.y >= self._MAP_HEIGHT:
			return False
		return True

	def _is_cell_available(self, cell_position):
		if not self._is_inside_map(cell_position):
			return False
		if cell_position == Vector2D(self.stable_position[0], self.stable_position[1]):
			return False
		wolf_cell = self._find_cell_with_max_score(WOLF_CELL)
		if wolf_cell is not None:
			for x2 in range(-1, +2):
				for y2 in range(-1, +2):
					x3, y3 = cell_position.x + 2 * x2, + cell_position.y + 2 * y2
					if self._cells_score.get((wolf_cell.x, wolf_cell.y, WOLF_CELL), 0) == self._cells_score.get((x3, y3, WOLF_CELL), 0):
						return False
		return True

	def _distance(self, position1, position2):
		return abs(position1.x - position2.x) + abs(position1.y - position2.y)

	def _find_cell_with_max_score(self, cell):
		mx = 0
		choices = []
		for y in range(self._MAP_HEIGHT):
			for x in range(self._MAP_WIDTH):
				if self._cells_score.get((x, y, cell)) and self._cells_score.get((x, y, cell)) == mx and mx > 0:
					choices.append(Vector2D(x, y))
				elif self._cells_score.get((x, y, cell)) and self._cells_score.get((x, y, cell)) > mx:
					mx = self._cells_score[(x, y, cell)]
					choices = [Vector2D(x, y)]
		if mx > 0:
			random_idx = randint(0, len(choices) - 1)
			return choices[random_idx]
		else:
			return None

	def move(self, map_width, map_height, player_position, stable_position, player_has_flag, player_neighbors):
		x, y = player_position.x, player_position.y
		self._player_last_position = Vector2D(x, y)
		self.stable_position = stable_position
		if self._cells_visits_count.get((x, y)): 
			self._cells_visits_count[(x, y)] += 1
		else:
			self._cells_visits_count[(x, y)] = 1
		if WOLF_CELL in player_neighbors:
			if self._cells_visits_count[(x, y)] == 1:
				tmp_cnt = 0
				for x2 in range(x - 1, x + 2):
					for y2 in range(y - 1, y + 2):
						if self._is_inside_map(Vector2D(x2, y2)) and (x2, y2) != stable_position and (x, y) != (x2, y2) and (x2, y2) != (self._player_last_position.x, self._player_last_position.y):
							tmp_cnt += 1
				for x2 in range(x - 1, x + 2):
					for y2 in range(y - 1, y + 2):
						if self._is_inside_map(Vector2D(x2, y2)) and (x2, y2) != stable_position and (x, y) != (x2, y2) and (x2, y2) != (self._player_last_position.x, self._player_last_position.y):
							if self._cells_score.get((x2, y2, WOLF_CELL)):
								self._cells_score[(x2, y2, WOLF_CELL)] += 1.0 / tmp_cnt
							else:
								self._cells_score[(x2, y2, WOLF_CELL)] = 1.0 / tmp_cnt
			if self._last_move_direction is not None:
				self._last_move_direction = Vector2D(0, 0) - self._last_move_direction
				return self._last_move_direction
		if FLAG_CELL in player_neighbors:
			if self._cells_visits_count[(x, y)] == 1:
				tmp_cnt = 0
				for x2 in range(x - 1, x + 2):
					for y2 in range(y - 1, y + 2):
						if self._is_inside_map(Vector2D(x2, y2)) and (x2, y2) != stable_position and (x, y) != (x2, y2) and (x2, y2) != (self._player_last_position.x, self._player_last_position.y):
							tmp_cnt += 1
				for x2 in range(x - 1, x + 2):
					for y2 in range(y - 1, y + 2):
						if self._is_inside_map(Vector2D(x2, y2)) and (x2, y2) != stable_position and (x, y) != (x2, y2) and (x2, y2) != (self._player_last_position.x, self._player_last_position.y):
							if self._cells_score.get((x2, y2, FLAG_CELL)):
								self._cells_score[(x2, y2, FLAG_CELL)] += 1.0 / tmp_cnt
							else:
								self._cells_score[(x2, y2, FLAG_CELL)] = 1.0 / tmp_cnt
		if not player_has_flag:
			flag_cell = self._find_cell_with_max_score(FLAG_CELL)
			if flag_cell is not None:
				min_idx = randint(0, 3)
				mn = 10 * self._MAP_WIDTH * self._MAP_WIDTH
				for i in range(4):
					new_position = Vector2D(self._DX[i], self._DY[i]) + Vector2D(x, y)
					if self._distance(flag_cell, new_position) < mn and self._is_cell_available(new_position):
						mn = self._distance(flag_cell, new_position)
						min_idx = i
				self._last_move_direction = Vector2D(self._DX[min_idx], self._DY[min_idx])
				return Vector2D(self._DX[min_idx], self._DY[min_idx])

			min_idx = randint(0, 3)
			new_position = Vector2D(self._DX[min_idx], self._DY[min_idx]) + Vector2D(x, y)
			mn = self._cells_visits_count.get((new_position.x, new_position.y), 0)
			tmp_cnt = 0

			while not self._is_cell_available(new_position) and tmp_cnt < 20:
				min_idx = randint(0, 3)
				new_position = Vector2D(self._DX[min_idx], self._DY[min_idx]) + Vector2D(x, y)
				mn = self._cells_visits_count.get((new_position.x, new_position.y), 0)
				tmp_cnt += 1

			for i in range(4):
				new_position = Vector2D(self._DX[i], self._DY[i]) + Vector2D(x, y)
				if self._cells_visits_count.get((new_position.x, new_position.y), 0) < mn and self._is_cell_available(new_position):
					mn = self._cells_visits_count.get((new_position.x, new_position.y), 0)
					min_idx = i
			self._last_move_direction = Vector2D(self._DX[min_idx], self._DY[min_idx])
			return Vector2D(self._DX[min_idx], self._DY[min_idx])

		else:
			min_idx = randint(0, 3)
			new_position = Vector2D(self._DX[min_idx], self._DY[min_idx]) + Vector2D(x, y)
			mn = self._cells_visits_count.get((new_position.x, new_position.y), 0)
			tmp_cnt = 0

			while not self._is_cell_available(new_position) and tmp_cnt < 20:
				min_idx = randint(0, 3)
				new_position = Vector2D(self._DX[min_idx], self._DY[min_idx]) + Vector2D(x, y)
				mn = self._cells_visits_count.get((new_position.x, new_position.y), 0)
				tmp_cnt += 1

			for i in range(4):
				new_position = Vector2D(self._DX[i], self._DY[i]) + Vector2D(x, y)
				if self._cells_visits_count.get((new_position.x, new_position.y), 0) < mn and self._is_cell_available(new_position):
					mn = self._cells_visits_count.get((new_position.x, new_position.y), 0)
					min_idx = i
			self._last_move_direction = Vector2D(self._DX[min_idx], self._DY[min_idx])
			return Vector2D(self._DX[min_idx], self._DY[min_idx])

class GameJudge:
	_DX = [-1, +1, 0, 0]
	_DY = [0, 0, -1, +1]
	_MAXIMUM_TURNS_COUNT = 250

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

	def _is_inside_map(self, position):
		if (position.x < 0 or position.x >= self._MAP_WIDTH):
			return False
		if (position.y < 0 or position.y >= self._MAP_HEIGHT):
			return False
		return True

	def _is_move_valid(self, player_move_direction):
		if abs(player_move_direction.x) + abs(player_move_direction.y) != 1:
			return False
		player_new_position = self._player_position + player_move_direction
		if not self._is_inside_map(player_new_position):
			return False
		return self._map[player_new_position.y][player_new_position.x] in [EMPTY_CELL, FLAG_CELL, WOLF_CELL]

	def _put_cell_on_map(self, cell):
		x, y = randint(0, self._MAP_WIDTH - 1), randint(0, self._MAP_HEIGHT - 1)
		while self._map[y][x] != EMPTY_CELL:
			x, y = randint(0, self._MAP_WIDTH - 1), randint(0, self._MAP_HEIGHT - 1)
		self._map[y][x] = cell
		return x, y

	def _update_map(self, player_move_direction):
		if not self._is_move_valid(player_move_direction):
			return
		player_new_position = self._player_position + player_move_direction
		if self._map[player_new_position.y][player_new_position.x] == WOLF_CELL:
			self._is_game_finished = True
		elif self._map[player_new_position.y][player_new_position.x] == FLAG_CELL:
			self._player_has_flag = True
		self._map[self._player_position.y][self._player_position.x] = EMPTY_CELL
		if self._map[player_new_position.y][player_new_position.x] != WOLF_CELL:
			self._map[player_new_position.y][player_new_position.x] = PLAYER_CELL
		self._show_map([self._player_position, player_new_position])
		self._player_position = player_new_position
		if self._player_has_flag:
			x, y = player_new_position.x, player_new_position.y
			for x2 in range(x - 1, x + 2):
				for y2 in range(y - 1, y + 2):
					if (x2, y2) == (x, y):
						continue
					if self._is_inside_map(Vector2D(x2, y2)) and self._map[y2][x2] == COW_CELL:
						self._move_cow(Vector2D(x2, y2))


	def _move_cow(self, cow_position):
		if not self._is_inside_map(cow_position) or self._map[cow_position.y][cow_position.x] != COW_CELL:
			return
		player_is_adjacent = True
		while player_is_adjacent:
			player_is_adjacent = False
			x, y = cow_position.x, cow_position.y
			loop_break_flag = False
			for x2 in range(x - 1, x + 2):
				if loop_break_flag:
					break
				for y2 in range(y - 1, y + 2):
					if loop_break_flag:
						break
					if (x2, y2) == (x, y):
						continue
					if self._is_inside_map(Vector2D(x2, y2)) and self._map[y2][x2] == PLAYER_CELL:
						player_is_adjacent = True
						cow_new_position = cow_position - Vector2D(x2 - x, y2 - y)
						if self._is_inside_map(cow_new_position):
							if self._map[cow_new_position.y][cow_new_position.x] == EMPTY_CELL:
								self._map[cow_position.y][cow_position.x] = EMPTY_CELL
								self._map[cow_new_position.y][cow_new_position.x] = COW_CELL
								self._show_map([cow_position, cow_new_position])
								cow_position = cow_new_position
								loop_break_flag = True
								break
							elif self._map[cow_new_position.y][cow_new_position.x] == STABLE_CELL:
								self._map[cow_position.y][cow_position.x] = EMPTY_CELL
								self._show_map([cow_position])
								self._cows_in_stables += 1
								return
							elif self._map[cow_new_position.y][cow_new_position.x] == WOLF_CELL:
								self._map[cow_position.y][cow_position.x] = EMPTY_CELL
								self._show_map([cow_position])
								self._cows_eaten_by_wolves += 1
								return
							else:
								while True:
									if loop_break_flag:
										break
									cow_new_position = cow_position + Vector2D(randint(-1, +1), randint(-1, +1))
									if cow_new_position == cow_position:
										continue
									if self._is_inside_map(cow_new_position):
										if self._map[cow_new_position.y][cow_new_position.x] == EMPTY_CELL:
											self._map[cow_position.y][cow_position.x] = EMPTY_CELL
											self._map[cow_new_position.y][cow_new_position.x] = COW_CELL
											self._show_map([cow_position, cow_new_position])
											cow_position = cow_new_position
											loop_break_flag = True
											break
										elif self._map[cow_new_position.y][cow_new_position.x] == STABLE_CELL:
											self._map[cow_position.y][cow_position.x] = EMPTY_CELL
											self._show_map([cow_position])
											self._cows_in_stables += 1
											return
										elif self._map[cow_new_position.y][cow_new_position.x] == WOLF_CELL:
											self._map[cow_position.y][cow_position.x] = EMPTY_CELL
											self._show_map([cow_position])
											self._cows_eaten_by_wolves += 1
											return
						else:
							while True:
								if loop_break_flag:
									break
								cow_new_position = cow_position + Vector2D(randint(-1, +1), randint(-1, +1))
								if cow_new_position == cow_position:
									continue
								if self._is_inside_map(cow_new_position):
									if self._map[cow_new_position.y][cow_new_position.x] == EMPTY_CELL:
										self._map[cow_position.y][cow_position.x] = EMPTY_CELL
										self._map[cow_new_position.y][cow_new_position.x] = COW_CELL
										self._show_map([cow_position, cow_new_position])
										cow_position = cow_new_position
										loop_break_flag = True
										break
									elif self._map[cow_new_position.y][cow_new_position.x] == STABLE_CELL:
										self._map[cow_position.y][cow_position.x] = EMPTY_CELL
										self._show_map([cow_position])
										self._cows_in_stables += 1
										return
									elif self._map[cow_new_position.y][cow_new_position.x] == WOLF_CELL:
										self._map[cow_position.y][cow_position.x] = EMPTY_CELL
										self._show_map([cow_position])
										self._cows_eaten_by_wolves += 1
										return

	def calculate_player_score(self):
		return self._cows_in_stables * 2 - (self._cows_eaten_by_wolves + self._turns_count * 0.01)

	def _get_cell_neighbors(self, position):
		x, y = position.x, position.y
		cell_neighbors = []
		for x2 in range(x - 1, x + 2):
			for y2 in range(y - 1, y + 2):
				if (x2, y2) == (x, y):
					continue
				if self._is_inside_map(Vector2D(x2, y2)) and self._map[y2][x2] != EMPTY_CELL and self._map[y2][x2] not in cell_neighbors:
					cell_neighbors.append(self._map[y2][x2])
		return cell_neighbors

	def __init__(self, player=None):
		self._is_game_finished = False
		self._turns_count = 0
		self._cows_in_stables = 0
		self._cows_eaten_by_wolves = 0
		self._map = [[EMPTY_CELL for j in range(self._MAP_WIDTH)] for i in range(self._MAP_HEIGHT)]
		self._player_has_flag = False
		self._player_position = Vector2D(0, 0)
		self._player_position.x, self._player_position.y = self._put_cell_on_map(PLAYER_CELL)
		self._stable_position = self._put_cell_on_map(STABLE_CELL)
		for i in range(self._FLAGS_COUNT):
			self._put_cell_on_map(FLAG_CELL)
		for i in range(self._COWS_COUNT):
			self._put_cell_on_map(COW_CELL)
		for i in range(self._WOLVES_COUNT):
			self._put_cell_on_map(WOLF_CELL)
		self._player = player
		self._IMAGES_PATH[COW_CELL] = self._COW_IMAGE_PATH
		self._IMAGES_PATH[PLAYER_CELL] = self._PLAYER_IMAGE_PATH
		self._IMAGES_PATH[STABLE_CELL] = self._STABLE_IMAGE_PATH
		self._IMAGES_PATH[FLAG_CELL] = self._FLAG_IMAGE_PATH
		self._IMAGES_PATH[WOLF_CELL] = self._WOLF_IMAGE_PATH
		self._IMAGES_PATH[EMPTY_CELL] = self._EMPTY_IMAGE_PATH
		plt.figure(figsize=(6, 6))
		
	def _do_turn(self):
		player_neighbors = self._get_cell_neighbors(self._player_position)
		player_move_direction = self._player.move(map_width=self._MAP_WIDTH, map_height=self._MAP_HEIGHT, player_position=self._player_position, stable_position=self._stable_position, player_has_flag=self._player_has_flag, player_neighbors=player_neighbors)
		if player_move_direction is not None and self._is_move_valid(player_move_direction):
			self._update_map(player_move_direction)

	def run(self):
		self._show_map()
		for i in range(self._MAXIMUM_TURNS_COUNT):
			self._do_turn()
			self._turns_count = i + 1
			if self._is_game_finished is not None and self._is_game_finished == True:
				break
		print("Your score: " + str(self.calculate_player_score()))
		plt.pause(60)

	def _show_map(self, positions=None):
		if positions:
			for position in positions:
				plt.subplot(self._MAP_HEIGHT, self._MAP_WIDTH, position.y * self._MAP_WIDTH + position.x + 1,)
				plt.imshow(cv2.imread(self._IMAGES_PATH[self._map[position.y][position.x]], cv2.IMREAD_COLOR))
				plt.xticks([])
				plt.yticks([])
		else:
			for y in range(self._MAP_HEIGHT):
				for x in range(self._MAP_WIDTH):
					plt.subplot(self._MAP_HEIGHT, self._MAP_WIDTH, y * self._MAP_WIDTH + x + 1,)
					plt.imshow(cv2.imread(self._IMAGES_PATH[self._map[y][x]], cv2.IMREAD_COLOR))
					plt.xticks([])
					plt.yticks([])

		plt.subplots_adjust(wspace=0, hspace=0)
		plt.draw()
		plt.pause(0.01)


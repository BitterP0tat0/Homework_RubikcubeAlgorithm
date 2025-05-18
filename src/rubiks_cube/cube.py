import random
import numpy as np
from enum import Enum

class Face(Enum):
    FRONT = 0
    BACK = 1
    LEFT = 2
    RIGHT = 3
    UP = 4
    DOWN = 5

class Move(Enum):
    F = "F"
    F_PRIME = "F'"

COLORS = {
    Face.FRONT: 'R',
    Face.BACK: 'O',
    Face.LEFT: 'B',
    Face.RIGHT: 'G',
    Face.UP: 'W',
    Face.DOWN: 'Y',
}

def inverse_move(move: Move) -> Move:
    if move == Move.F:
        return Move.F_PRIME
    elif move == Move.F_PRIME:
        return Move.F

class RubiksCube:
    def __init__(self, size=3):
        self.size = size
        self.faces = {face: np.full((size, size), COLORS[face]) for face in Face}

    def is_solved(self):
        for face in self.faces.values():
            if not np.all(face == face[0,0]):
                return False
        return True

    def apply_move(self, move: Move):
        if move == Move.F:
            self._rotate_face_clockwise(Face.FRONT)
            self._rotate_front_adjacent_clockwise()
        elif move == Move.F_PRIME:
            self._rotate_face_counterclockwise(Face.FRONT)
            self._rotate_front_adjacent_counterclockwise()

    def _rotate_face_clockwise(self, face: Face):
        self.faces[face] = np.rot90(self.faces[face], -1)

    def _rotate_face_counterclockwise(self, face: Face):
        self.faces[face] = np.rot90(self.faces[face], 1)

    def _rotate_front_adjacent_clockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = up[-1, :].copy()
        up[-1, :] = left[:, -1][::-1]
        left[:, -1] = down[0, :]
        down[0, :] = right[:, 0][::-1]
        right[:, 0] = tmp

    def _rotate_front_adjacent_counterclockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = up[-1, :].copy()
        up[-1, :] = right[:, 0]
        right[:, 0] = down[0, :][::-1]
        down[0, :] = left[:, -1]
        left[:, -1] = tmp[::-1]
    def get_state(self):
        state = ""
        for face in Face:
            state += "".join(self.faces[face].flatten())
        return state
    def scramble(self, moves_count: int):
        last_move = None
        for _ in range(moves_count):
            move = random.choice(list(Move))
            while last_move and move == inverse_move(last_move):
                move = random.choice(list(Move))
            self.apply_move(move)
            last_move = move

    def __str__(self):
        s = ""
        for face in Face:
            s += f"{face.name} face:\n{self.faces[face]}\n\n"
        return s
    


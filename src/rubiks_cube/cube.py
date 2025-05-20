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
    B = "B"
    B_PRIME = "B'"
    L = "L"
    L_PRIME = "L'"
    R = "R"
    R_PRIME = "R'"
    U = "U"
    U_PRIME = "U'"
    D = "D"
    D_PRIME = "D'"

COLORS = {
    Face.FRONT: 'R',
    Face.BACK: 'O',
    Face.LEFT: 'B',
    Face.RIGHT: 'G',
    Face.UP: 'W',
    Face.DOWN: 'Y',
}

def inverse_move(move: Move) -> Move:
    inverses = {
        Move.F: Move.F_PRIME, Move.F_PRIME: Move.F,
        Move.B: Move.B_PRIME, Move.B_PRIME: Move.B,
        Move.L: Move.L_PRIME, Move.L_PRIME: Move.L,
        Move.R: Move.R_PRIME, Move.R_PRIME: Move.R,
        Move.U: Move.U_PRIME, Move.U_PRIME: Move.U,
        Move.D: Move.D_PRIME, Move.D_PRIME: Move.D,
    }
    return inverses[move]

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
        face_map = {
            Move.F: (Face.FRONT, True),
            Move.F_PRIME: (Face.FRONT, False),
            Move.B: (Face.BACK, True),
            Move.B_PRIME: (Face.BACK, False),
            Move.L: (Face.LEFT, True),
            Move.L_PRIME: (Face.LEFT, False),
            Move.R: (Face.RIGHT, True),
            Move.R_PRIME: (Face.RIGHT, False),
            Move.U: (Face.UP, True),
            Move.U_PRIME: (Face.UP, False),
            Move.D: (Face.DOWN, True),
            Move.D_PRIME: (Face.DOWN, False),
        }
        face, clockwise = face_map[move]
        if clockwise:
            self._rotate_face_clockwise(face)
        else:
            self._rotate_face_counterclockwise(face)
        self._rotate_adjacent(face, clockwise)

    def _rotate_face_clockwise(self, face: Face):
        self.faces[face] = np.rot90(self.faces[face], -1)

    def _rotate_face_counterclockwise(self, face: Face):
        self.faces[face] = np.rot90(self.faces[face], 1)

    def _rotate_adjacent(self, face: Face, clockwise: bool = True):
        if face == Face.FRONT:
            if clockwise:
                self._rotate_front_adjacent_clockwise()
            else:
                self._rotate_front_adjacent_counterclockwise()
        elif face == Face.BACK:
            if clockwise:
                self._rotate_back_adjacent_clockwise()
            else:
                self._rotate_back_adjacent_counterclockwise()
        elif face == Face.LEFT:
            if clockwise:
                self._rotate_left_adjacent_clockwise()
            else:
                self._rotate_left_adjacent_counterclockwise()
        elif face == Face.RIGHT:
            if clockwise:
                self._rotate_right_adjacent_clockwise()
            else:
                self._rotate_right_adjacent_counterclockwise()
        elif face == Face.UP:
            if clockwise:
                self._rotate_up_adjacent_clockwise()
            else:
                self._rotate_up_adjacent_counterclockwise()
        elif face == Face.DOWN:
            if clockwise:
                self._rotate_down_adjacent_clockwise()
            else:
                self._rotate_down_adjacent_counterclockwise()

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

    def _rotate_back_adjacent_clockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = up[0, :].copy()
        up[0, :] = right[:, -1]
        right[:, -1] = down[-1, :][::-1]
        down[-1, :] = left[:, 0]
        left[:, 0] = tmp[::-1]

    def _rotate_back_adjacent_counterclockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = up[0, :].copy()
        up[0, :] = left[:, 0][::-1]
        left[:, 0] = down[-1, :]
        down[-1, :] = right[:, -1][::-1]
        right[:, -1] = tmp

    def _rotate_left_adjacent_clockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        tmp = up[:, 0].copy()
        up[:, 0] = back[:, -1][::-1]
        back[:, -1] = down[:, 0][::-1]
        down[:, 0] = front[:, 0]
        front[:, 0] = tmp

    def _rotate_left_adjacent_counterclockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        tmp = up[:, 0].copy()
        up[:, 0] = front[:, 0]
        front[:, 0] = down[:, 0]
        down[:, 0] = back[:, -1][::-1]
        back[:, -1] = tmp[::-1]

    def _rotate_right_adjacent_clockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        tmp = up[:, -1].copy()
        up[:, -1] = front[:, -1]
        front[:, -1] = down[:, -1]
        down[:, -1] = back[:, 0][::-1]
        back[:, 0] = tmp[::-1]

    def _rotate_right_adjacent_counterclockwise(self):
        up = self.faces[Face.UP]
        down = self.faces[Face.DOWN]
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        tmp = up[:, -1].copy()
        up[:, -1] = back[:, 0][::-1]
        back[:, 0] = down[:, -1][::-1]
        down[:, -1] = front[:, -1]
        front[:, -1] = tmp

    def _rotate_up_adjacent_clockwise(self):
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = back[0, :].copy()
        back[0, :] = right[0, :]
        right[0, :] = front[0, :]
        front[0, :] = left[0, :]
        left[0, :] = tmp

    def _rotate_up_adjacent_counterclockwise(self):
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = back[0, :].copy()
        back[0, :] = left[0, :]
        left[0, :] = front[0, :]
        front[0, :] = right[0, :]
        right[0, :] = tmp

    def _rotate_down_adjacent_clockwise(self):
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = back[-1, :].copy()
        back[-1, :] = left[-1, :]
        left[-1, :] = front[-1, :]
        front[-1, :] = right[-1, :]
        right[-1, :] = tmp

    def _rotate_down_adjacent_counterclockwise(self):
        front = self.faces[Face.FRONT]
        back = self.faces[Face.BACK]
        left = self.faces[Face.LEFT]
        right = self.faces[Face.RIGHT]
        tmp = back[-1, :].copy()
        back[-1, :] = right[-1, :]
        right[-1, :] = front[-1, :]
        front[-1, :] = left[-1, :]
        left[-1, :] = tmp

    def scramble(self, moves_count: int):
        last_move = None
        for _ in range(moves_count):
            attempts = 0
            move = random.choice(list(Move))
            while last_move and (move == inverse_move(last_move) or move.name[0] == last_move.name[0]):
                move = random.choice(list(Move))
                attempts += 1
                if attempts > 50:
                    break
            self.apply_move(move)
            last_move = move

    def get_state(self):
        state = ""
        for face in Face:
            state += "".join(self.faces[face].flatten())
        return state

    def __str__(self):
        s = ""
        for face in Face:
            s += f"{face.name} face:\n{self.faces[face]}\n\n"
        return s

import heapq
from collections import deque
from typing import List, Optional, Set
from src.rubiks_cube.cube import RubiksCube, Move, inverse_move

class Node:
    def __init__(self, cube: RubiksCube, parent=None, move=None, cost=0):
        self.cube = cube
        self.parent = parent
        self.move = move
        self.cost = cost
        self.estimated_cost = 0

    def __lt__(self, other):
        return (self.cost + self.estimated_cost) < (other.cost + other.estimated_cost)

    def path(self) -> List[Move]:
        node, moves = self, []
        while node.move is not None:
            moves.append(node.move)
            node = node.parent
        moves.reverse()
        return moves


def dfs(start_cube: RubiksCube, max_depth=15) -> Optional[List[Move]]:
    stack = [Node(start_cube)]
    visited: Set[str] = set()

    while stack:
        node = stack.pop()
        state = node.cube.get_state()
        if state in visited:
            continue
        visited.add(state)

        if node.cube.is_solved():
            print(f"DFS found solution at depth {node.cost}, path length: {len(node.path())}")
            print("DFS path:", node.path())
            return node.path()

        if node.cost >= max_depth:
            continue

        if node.move:
            print(f"DFS depth {node.cost}, move {node.move}")

        for move in Move:
            if node.move and move == inverse_move(node.move):
                continue
            new_cube = copy_cube(node.cube)
            new_cube.apply_move(move)
            stack.append(Node(new_cube, node, move, node.cost + 1))

    print("DFS: no solution found within max depth")
    return None

def bfs(start_cube: RubiksCube, max_depth=15) -> Optional[List[Move]]:
    queue = deque([Node(start_cube)])
    visited: Set[str] = set()

    while queue:
        node = queue.popleft()
        state = node.cube.get_state()
        if state in visited:
            continue
        visited.add(state)

        if node.cube.is_solved():
            print(f"BFS found solution at depth {node.cost}, path length: {len(node.path())}")
            print("BFS path:", node.path())
            return node.path()

        if node.cost >= max_depth:
            continue

        if node.move:
            print(f"BFS depth {node.cost}, move {node.move}")

        for move in Move:
            if node.move and move == inverse_move(node.move):
                continue
            new_cube = copy_cube(node.cube)
            new_cube.apply_move(move)
            queue.append(Node(new_cube, node, move, node.cost + 1))

    print("BFS: no solution found within max depth")
    return None

def a_star(start_cube: RubiksCube, max_depth=15) -> Optional[List[Move]]:
    def heuristic(cube: RubiksCube) -> int:
        h = 0
        for face in cube.faces.values():
            center = face[cube.size // 2, cube.size // 2]
            h += sum((face != center).flatten())
        return h

    open_heap = []
    start_node = Node(start_cube)
    start_node.estimated_cost = heuristic(start_cube)
    heapq.heappush(open_heap, start_node)
    visited: Set[str] = set()

    while open_heap:
        node = heapq.heappop(open_heap)
        state = node.cube.get_state()
        if state in visited:
            continue
        visited.add(state)

        if node.cube.is_solved():
            print(f"A* found solution at depth {node.cost}, path length: {len(node.path())}")
            print("A* path:", node.path())
            return node.path()

        if node.cost >= max_depth:
            continue

        if node.move:
            print(f"A* depth {node.cost}, move {node.move}, heuristic {heuristic(node.cube)}")

        for move in Move:
            if node.move and move == inverse_move(node.move):
                continue
            new_cube = copy_cube(node.cube)
            new_cube.apply_move(move)
            new_node = Node(new_cube, node, move, node.cost + 1)
            new_node.estimated_cost = heuristic(new_cube)
            heapq.heappush(open_heap, new_node)

    print("A*: no solution found within max depth")
    return None

def copy_cube(cube: RubiksCube) -> RubiksCube:
    new_cube = RubiksCube(cube.size)
    for face in cube.faces:
        new_cube.faces[face] = cube.faces[face].copy()
    return new_cube

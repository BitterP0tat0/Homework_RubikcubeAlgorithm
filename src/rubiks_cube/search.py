import heapq
import time
from collections import deque
from typing import List, Optional, Set
from .cube import RubiksCube, Move, inverse_move

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
def dfs(start_cube: RubiksCube, max_depth) -> Optional[tuple[List[Move], float, int]]:
    start_time = time.time()

    def dfs_limited(node: Node, depth_limit: int, visited: Set[str]) -> Optional[Node]:
        if node.cube.is_solved():
            return node
        if node.cost >= depth_limit:
            return None

        state = node.cube.get_state()
        visited.add(state)

        for move in Move:
            if node.move and move == inverse_move(node.move):
                continue
            new_cube = copy_cube(node.cube)
            new_cube.apply_move(move)
            new_state = new_cube.get_state()
            if new_state in visited:
                continue
            new_node = Node(new_cube, node, move, node.cost + 1)
            result = dfs_limited(new_node, depth_limit, visited)
            if result is not None:
                return result
        visited.remove(state)
        return None

    for depth in range(1, max_depth + 1):
        visited: Set[str] = set()
        result = dfs_limited(Node(start_cube), depth, visited)
        if result is not None:
            time_taken = time.time() - start_time
            print(f"DFS found solution at depth {depth}, time: {time_taken:.4f} seconds")
            return result.path(), time_taken, depth
        print(f"DFS depth {depth} finished without solution")

    time_taken = time.time() - start_time
    return None


def bfs(start_cube: RubiksCube, max_depth) -> Optional[tuple[List[Move], float, int]]:
    start_time = time.time()
    queue = deque([Node(start_cube)])
    visited: Set[str] = set()

    while queue:
        node = queue.popleft()
        state = node.cube.get_state()
        if state in visited:
            continue
        visited.add(state)

        if node.cube.is_solved():
            time_taken = time.time() - start_time
            print(f"BFS found solution at depth {node.cost}, time: {time_taken:.4f} seconds")
            return node.path(), time_taken, node.cost

        if node.cost >= max_depth:
            continue

        for move in Move:
            if node.move and move == inverse_move(node.move):
                continue
            new_cube = copy_cube(node.cube)
            new_cube.apply_move(move)
            queue.append(Node(new_cube, node, move, node.cost + 1))

    time_taken = time.time() - start_time
    return None

def a_star(start_cube: RubiksCube, max_depth) -> Optional[tuple[List[Move], float, int]]:
    start_time = time.time()

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
            time_taken = time.time() - start_time
            print(f"A* found solution at depth {node.cost}, time: {time_taken:.4f} seconds")
            return node.path(), time_taken, node.cost

        if node.cost >= max_depth:
            continue

        for move in Move:
            if node.move and move == inverse_move(node.move):
                continue
            new_cube = copy_cube(node.cube)
            new_cube.apply_move(move)
            new_node = Node(new_cube, node, move, node.cost + 1)
            new_node.estimated_cost = heuristic(new_cube)
            heapq.heappush(open_heap, new_node)

    time_taken = time.time() - start_time
    return None


def copy_cube(cube: RubiksCube) -> RubiksCube:
    new_cube = RubiksCube(cube.size)
    for face in cube.faces:
        new_cube.faces[face] = cube.faces[face].copy()
    return new_cube

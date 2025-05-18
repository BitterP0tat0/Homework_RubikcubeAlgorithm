from src.rubiks_cube.search import dfs, bfs, a_star
from src.rubiks_cube.cube import RubiksCube

def test_search_algorithms():
    cube = RubiksCube()
    cube.scramble(5)
    print("Scrambled Cube:")
    print(cube)

    dfs_solution = dfs(cube, max_depth=10)
    print("DFS solution:", dfs_solution)

    bfs_solution = bfs(cube, max_depth=10)
    print("BFS solution:", bfs_solution)

    a_star_solution = a_star(cube, max_depth=10)
    print("A* solution:", a_star_solution)

if __name__ == "__main__":
    test_search_algorithms()

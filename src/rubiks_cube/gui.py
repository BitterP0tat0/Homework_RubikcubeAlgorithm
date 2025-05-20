import tkinter as tk
from tkinter import messagebox
from cube import RubiksCube, Move, Face
from search import a_star,dfs,bfs
import threading

COLOR_MAP = {
    'R': 'red',
    'O': 'orange',
    'B': 'blue',
    'G': 'green',
    'W': 'white',
    'Y': 'yellow',
}

FACE_POS = {
    'UP': (3, 0),
    'LEFT': (0, 3),
    'FRONT': (3, 3),
    'RIGHT': (6, 3),
    'BACK': (9, 3),
    'DOWN': (3, 6),
}

class RubiksCubeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rubik's Cube Solver")
        self.cube = RubiksCube(3)
        self.solution_moves = []
        self.current_step = 0
        self.square_size = 30

        self.canvas = tk.Canvas(self, width=12*self.square_size, height=9*self.square_size)
        self.canvas.pack()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Scramble", command=self.scramble).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Solve (A*)", command=self.solve_Astar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Solve DFS", command=self.solve_Astar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Solve BFS", command=self.solve_Astar).pack(side=tk.LEFT, padx=5)


        self.next_btn = tk.Button(btn_frame, text="Next Step", command=self.next_step, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.draw_cube()
    def draw_cube(self):
        self.canvas.delete("all")
        for face_name, (start_x, start_y) in FACE_POS.items():
            face_enum = getattr(Face, face_name)  
            face_colors = self.cube.faces[face_enum]
            for i in range(self.cube.size):
                for j in range(self.cube.size):
                    color_char = face_colors[i, j]
                    color = COLOR_MAP.get(color_char, "gray")
                    x0 = (start_x + j) * self.square_size
                    y0 = (start_y + i) * self.square_size
                    x1 = x0 + self.square_size
                    y1 = y0 + self.square_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")


    def scramble(self):
        self.cube = RubiksCube(3)
        self.cube.scramble(10)
        self.solution_moves = []
        self.current_step = 0
        self.next_btn.config(state=tk.DISABLED)
        self.draw_cube()

    def solve_Astar(self):
        self.next_btn.config(state=tk.DISABLED)
        def run_solver():
            moves = a_star(self.cube, max_depth=15)
            if moves is None:
                messagebox.showinfo("No solution", "No solution found within max depth.")
                return
            self.solution_moves = moves
            self.current_step = 0
            self.next_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Solution found", f"Solution length: {len(moves)} moves.")

        threading.Thread(target=run_solver).start()

    def solve_Dfs(self):
        self.next_btn.config(state=tk.DISABLED)
        def run_solver():
            moves = dfs(self.cube, max_depth=15)
            if moves is None:
                messagebox.showinfo("No solution", "No solution found within max depth.")
                return
            self.solution_moves = moves
            self.current_step = 0
            self.next_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Solution found", f"Solution length: {len(moves)} moves.")
    def solve_Bfs(self):
        self.next_btn.config(state=tk.DISABLED)
        def run_solver():
            moves = bfs(self.cube, max_depth=15)
            if moves is None:
                messagebox.showinfo("No solution", "No solution found within max depth.")
                return
            self.solution_moves = moves
            self.current_step = 0
            self.next_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Solution found", f"Solution length: {len(moves)} moves.")
        threading.Thread(target=run_solver).start()
    def next_step(self):
        if self.current_step < len(self.solution_moves):
            move = self.solution_moves[self.current_step]
            self.cube.apply_move(move)
            self.current_step += 1
            self.draw_cube()
        if self.current_step == len(self.solution_moves):
            self.next_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Solved", "Cube solved!")

if __name__ == "__main__":
    app = RubiksCubeGUI()
    app.mainloop()

# Rubik's Cube Solver

This project implements various search algorithms to solve the Rubik's Cube puzzle. It includes implementations of Depth-First Search (DFS), Breadth-First Search (BFS), and A\* search algorithms.

## Requirement

The structure of project is based on Poetry, before you run it and make sure that you already installed poetry in your PC

If you use VScode , do ctrl + shift + p and go through the Python interpreter, make sure the environment isn't from Microsoft python but from the python which you downloaded from Python Official

Then run <poetry env use " your python path in interpreter"> for example "C:\Users\BitterP0TAT0\AppData\Local\Programs\Python\Python312\python.exe"

Again, go back to Python interpreter and change the path to your venv

And you should run command <poetry update package> for getting packages from dependencies which the project needs

In Poetry, all libs are inside of dependencies of Poetry. So if you wanna add anything, type and run poetry add <your library name> eg. poetry add <numpy>

## Run Gui

run <poetry run python -m src.rubiks_cube.gui>

## Run test case

If you wanna run your test case in poetry, type <poetry run pytest -s tests/"your test name .py">
e

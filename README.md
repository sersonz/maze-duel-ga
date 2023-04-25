# Applications of Dueling Genetic Algorithms to Maze Problems 

## About

This project uses duelling genetic algorithms that simultaneously optimize a maze-solving algorithm and a maze-generation
algorithm. The two algorithms will evolve in parallel and aim to challenge each other in order to learn and grow alongside
one another. The fitness of individuals in each algorithm is evaluated based on their respective fields as parents and survivors
are chosen using different methods. We compare the results using DFS and BFS as the control and evaluate the duelling
algorithms’ performance against the performance of the control

## Getting Started

To run the code, you will need Python 3.10+ installed on your machine. You can clone the repository by running:

```
git clone https://github.com/<your-username>/maze-evolution.git
```

Once the repository is cloned, you can navigate to the root directory and run the main file:

```
cd maze
python CoEvolution.py
```

## Project Structure

The project is structured as follows:

```
.
├── common/                # directory for storing common code and constants
├── maze/                  # directory for storing maze-generator code
│   ├── Maze.py            # code for generating mazes
│   ├── Solver.py          # code for generating DFS and BFS solvers
│   └── CoEvolution.py     # code for running the dueling genetic algorithms
├── solver/                # directory for storing maze-solvers code
│   └── GeneticSolver.py   # code for generating genetic solvers
├── README.md              # this file
└── LICENSE                # license file  
```

Authors: Zedrick Serson, Youngjun Lee, Benjamin Hui, Zarrin Tasnim


# Problem-Solving-with-MicroPython

Repo for the book Problem Solving with MicroPython. A short introductory text for problem solvers and engineers to learn how to use MicroPython.

Built with jupyter-book. To build:

```
jb build Problem-Solving-with-MicroPython-Book
```

Each push to master initiates a build and publish to GitHub Pages using a GitHub Action.

To build a .pdf of the book from latex

```
jb build Problem-Solving-with-MicroPython-Book/ --builder pdflatex
```

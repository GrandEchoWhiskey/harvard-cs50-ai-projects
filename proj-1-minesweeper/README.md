[<- Back to course](../README.md)

<p align="center"><a href="https://cs50.harvard.edu/ai/2020">
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/course/harvard100.png" /><br>
</a></p>
<h1 align="center">CS50’s Introduction to Artificial Intelligence with Python<br><br>Minesweeper</h1>

<p align="center"><a href="#">
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/programming/python.png" />
</a></p>

### Background:
Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

### Getting Started:
Export this directory using SVN.
```
svn export https://github.com/GrandEchoWhiskey/harvard-cs50-ai-projects/trunk/proj-1-minesweeper
```
Change directory
```
cd proj-1-minesweeper
```
Install requirements
```
pip3 install -r requirements.txt
```
Now run the script
```
python runner.py
```

import tkinter

from game_of_life.game import GameOfLife


if __name__ == '__main__':
    root = tkinter.Tk()
    g = GameOfLife(50, 50, 100, master=root)
    root.mainloop()

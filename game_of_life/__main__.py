import tkinter

from game_of_life.presenter import GameOfLifePresenter


if __name__ == '__main__':
    root = tkinter.Tk()
    g = GameOfLifePresenter(50, 50, 100, master=root)
    root.mainloop()

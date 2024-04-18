import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.game_over = False

        # ゲームボードの作成
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(master, width=2, command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

        # 地雷の配置
        self.place_mines()

    def place_mines(self):
        '''
        地雷の配置
        '''
        self.mine_coords = set()
        total_cells = self.rows * self.cols
        mine_indices = random.sample(range(total_cells), self.mines)

        for index in mine_indices:
            row = index // self.cols
            col = index % self.cols
            self.mine_coords.add((row, col))

    def click(self, row, col):
        '''
        セルをクリックした時の処理
        Args:
            row (int): 行
            col (int): 列
        '''
        if self.game_over:
            return

        if (row, col) in self.mine_coords:
            self.game_over = True
            self.reveal_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine! Game over.")
        else:
            adjacent_mines = self.count_adjacent_mines(row, col)
            self.buttons[row][col].config(text=str(adjacent_mines))
            self.set_num_color(row, col, adjacent_mines)
            if adjacent_mines == 0:
                self.reveal_empty_cells(row, col)

    def count_adjacent_mines(self, row, col):
        '''
        指定されたセルの周囲にある地雷の数を数える
        Args:
            row (int): 行
            col (int): 列
        '''
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) in self.mine_coords:
                    count += 1
        return count

    def reveal_empty_cells(self, row, col):
        '''
        セルが空の場合に周囲のセルを再帰的に開示する
        '''
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.buttons[r][c]["text"] == "":
                    self.click(r, c)

    def reveal_mines(self):
        '''
        ゲームが終了したときにすべての地雷を表示
        '''
        for row, col in self.mine_coords:
            self.buttons[row][col].config(text="*")

    def set_num_color(self, row, col, text):
        '''
        数字に色を付ける
        Args:
            row (int): 行
            col (int): 列
            text (str): テキスト
        '''
        button = self.buttons[row][col]
        button.config(text=text)

        if text == 1:
            button.config(fg="blue")
        elif text == 2:
            button.config(fg="green")
        elif text >= 3:
            button.config(fg="red")


def main():
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()

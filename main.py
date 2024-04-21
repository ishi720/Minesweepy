import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    """
    マインスイーパークラス
    """
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.game_over = False
        self.cells_to_open = rows * cols - mines
        self.open_cells = 0

        # ゲームボードの作成
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(master, width=2)
                button.grid(row=row, column=col)
                button.bind('<Button-1>', lambda event, r=row, c=col: self.left_click(event, r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.right_click(event, r, c))
                button_row.append(button)
            self.buttons.append(button_row)

        # 地雷の配置
        self.place_mines()

    def place_mines(self):
        """
        地雷の配置
        """
        self.mine_coords = set()
        total_cells = self.rows * self.cols
        mine_indices = random.sample(range(total_cells), self.mines)

        for index in mine_indices:
            row = index // self.cols
            col = index % self.cols
            self.mine_coords.add((row, col))

    def left_click(self, event, row, col):
        """
        左クリック時の処理
        Args:
            row (int): 行
            col (int): 列
        """
        if self.game_over:
            return

        if (row, col) in self.mine_coords:
            self.game_over = True
            self.reveal_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine! Game over.")
        else:
            adjacent_mines = self.count_adjacent_mines(row, col)
            self.buttons[row][col].config(text=str(adjacent_mines), bg="#ccc")
            self.set_num_color(row, col, adjacent_mines)
            self.open_cells += 1
            if adjacent_mines == 0:
                self.reveal_empty_cells(row, col)

            # ゲームクリアの処理
            if self.open_cells == self.cells_to_open:
                self.game_over = True
                messagebox.showinfo("Game Clear", "Congratulations! You have cleared the game.")

    def right_click(self, event, row, col):
        """
        右クリック時の処理
        Args:
            row (int): 行
            col (int): 列
        """
        if self.game_over:
            return

        button = self.buttons[row][col]
        if button.cget("text") == "":
            button.config(text="🚩")

    def count_adjacent_mines(self, row, col):
        """
        指定されたセルの周囲にある地雷の数を数える
        Args:
            row (int): 行
            col (int): 列
        Returns:
            int: カウント
        """
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) in self.mine_coords:
                    count += 1
        return count

    def reveal_empty_cells(self, row, col):
        """
        セルが空の場合に周囲のセルを再帰的に開示する
        """
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.buttons[r][c]["text"] == "":
                    self.left_click(None, r, c)

    def reveal_mines(self):
        """
        ゲームが終了したときにすべての地雷を表示
        """
        for row, col in self.mine_coords:
            self.buttons[row][col].config(text="*")

    def set_num_color(self, row, col, text):
        """
        数字に色を付ける
        Args:
            row (int): 行
            col (int): 列
            text (str): テキスト
        """
        button = self.buttons[row][col]
        button.config(text=text)

        if text == 1:
            button.config(fg="#0000ff") # 青
        elif text == 2:
            button.config(fg="#008727") # 緑
        elif text == 3:
            button.config(fg="#ff0000") # 赤
        elif text == 4:
            button.config(fg="#223a70") # 紺
        elif text == 5:
            button.config(fg="#b4533c") # 茶
        elif text == 6:
            button.config(fg="#00ffff") # シアン
        elif text == 7:
            button.config(fg="#000000") # 黒
        elif text == 8:
            button.config(fg="#666666") # 灰色




def main():
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()

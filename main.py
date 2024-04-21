import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    """
    マインスイーパークラス
    """
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows # 列数
        self.cols = cols # 行数
        self.mines = mines # 地雷の数
        self.buttons = [] # セルの配列
        self.game_over = False # ゲームオーバーのフラグ
        self.cells_to_open = rows * cols - mines # 開いていないセルの数
        self.open_cells = 0 # 開かれたセルの数
        self.flags = set() # 設置されたフラグのセット

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

        cell = (row, col)
        if cell in self.flags:
            self.flags.remove(cell)
            self.buttons[row][col].config(text="")
        elif self.buttons[row][col]["text"] == "":
            self.flags.add(cell)
            self.buttons[row][col].config(text="🚩")

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

        color_map = {
            1: "#0000ff",  # 青
            2: "#008727",  # 緑
            3: "#ff0000",  # 赤
            4: "#223a70",  # 紺
            5: "#b4533c",  # 茶
            6: "#00ffff",  # シアン
            7: "#000000",  # 黒
            8: "#666666"   # 灰色
        }

        if text in color_map:
            button.config(fg=color_map[text])

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    _ = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()

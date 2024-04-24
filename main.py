import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class StartMenu:
    """
    スタート画面クラス
    """
    def __init__(self, master):
        self.master = master
        master.title("Minesweeper")
        master.geometry("300x200")

        self.title_label = tk.Label(master, text="Minesweeper", font=("Helvetica", 20))
        self.title_label.pack(pady=20)  # タイトルを配置

        self.label = tk.Label(master, text="地雷の数を指定")
        self.label.pack()

        self.default_mines = tk.StringVar(value="10")  # デフォルトの地雷の数を設定
        self.spin = tk.Spinbox(master, from_=1, to=100, textvariable=self.default_mines)
        self.spin.pack()

        self.start_button = ttk.Button(master, text="ゲームスタート", command=self.start_game, style='TButton')
        self.start_button.place(relx=0.5, rely=0.7, anchor='center')

    def start_game(self):
        try:
            mines = int(self.spin.get())
            self.master.destroy()  # スタート画面を閉じる
            root = tk.Tk()
            root.title("Minesweeper")
            _ = Minesweeper(root, mines=mines)
            root.mainloop()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for mines.")

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
        self.first_click = True # 最初のクリックかどうかのフラグ
        self.start_time = None  # ゲーム開始時刻

        # ゲーム開始時刻を設定
        self.start_time = time.time()

        # タイマーを表示するラベルを作成
        self.timer_label = tk.Label(master, text="Time: 0")
        self.timer_label.grid(row=self.rows + 1, columnspan=self.cols)

        # タイマーを更新する関数を定期的に呼び出す
        self.update_timer()

        # 残りのセルの数を表示するラベルを作成
        self.remaining_cells_label = tk.Label(master, text=f"残: {self.cells_to_open}")
        self.remaining_cells_label.grid(row=self.rows + 1, columnspan=self.cols, sticky="e")

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

        self.flags_left = mines  # 残りの旗の数

        # 旗の数を表示するラベルを作成
        self.flags_label = tk.Label(master, text=f"🚩: {self.flags_left}")
        self.flags_label.grid(row=self.rows + 1, column=0, columnspan=self.cols, sticky="w")  # 左揃えにする

    def place_mines(self, first_click_row, first_click_col):
        """
        地雷の配置
        """
        self.mine_coords = set()
        total_cells = self.rows * self.cols
        safe_cells = set(self.get_surrounding_cells(first_click_row, first_click_col))
        safe_cells.add((first_click_row, first_click_col))
        available_cells = [cell for cell in range(total_cells) if (cell // self.cols, cell % self.cols) not in safe_cells]
        mine_indices = random.sample(available_cells, self.mines)

        for index in mine_indices:
            row = index // self.cols
            col = index % self.cols
            self.mine_coords.add((row, col))

    def get_surrounding_cells(self, row, col):
        """
        指定されたセルの周囲のセルをセットに追加する
        Args:
            row (int): 行
            col (int): 列
        Returns:
            set: 周囲のセルのセット
        """
        surrounding_cells = set()

        # 行と列の範囲を指定
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                # セルをセットに追加
                surrounding_cells.add((r, c))

        return surrounding_cells

    def left_click(self, event, row, col):
        """
        左クリック時の処理
        Args:
            row (int): 行
            col (int): 列
        """
        if self.game_over:
            return

        if (row, col) in self.flags:
            return

        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False

        if (row, col) in self.mine_coords:
            # ゲームオーバーの処理
            self.game_over = True
            self.reveal_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine! Game over.")
            self.master.destroy()
            self.return_to_start_menu()
        else:
            adjacent_mines = self.count_adjacent_mines(row, col)
            self.buttons[row][col].config(text=str(adjacent_mines), bg="#ccc")
            self.set_num_color(row, col, adjacent_mines)
            self.open_cells += 1
            if adjacent_mines == 0:
                self.reveal_empty_cells(row, col)

            # 残りのセルの数を更新
            self.update_remaining_cells()

            # ゲームクリアの処理
            if self.open_cells == self.cells_to_open:
                self.game_over = True
                elapsed_time = round(time.time() - self.start_time)
                messagebox.showinfo("Game Clear", f"Congratulations! You have cleared the game in {elapsed_time} seconds.")
                self.master.destroy()
                self.return_to_start_menu()

        # イベントハンドラを削除してセルをクリック後に無効にする
        self.buttons[row][col].unbind('<Button-1>')

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
            self.flags_left += 1  # 旗の数を増やす
        elif self.buttons[row][col]["text"] == "":
            if self.flags_left > 0:
                self.flags.add(cell)
                self.buttons[row][col].config(text="🚩")
                self.flags_left -= 1  # 旗の数を減らす

        # 旗の数を更新
        self.flags_label.config(text=f"🚩: {self.flags_left}")

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

    def update_timer(self):
        """
        タイマーの更新
        """
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)
        if not self.game_over:
            self.master.after(1000, self.update_timer)

    def update_remaining_cells(self):
        """
        残りのセルの数を更新する
        """
        remaining_cells = self.cells_to_open - self.open_cells
        self.remaining_cells_label.config(text=f"残: {remaining_cells}")

    def return_to_start_menu(self):
        """
        ゲーム終了後にゲーム開始画面に戻る
        """
        root = tk.Tk()
        root.title("Minesweeper")
        _ = StartMenu(root)
        root.mainloop()

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    _ = StartMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
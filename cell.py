from tkinter import Button
from tkinter import Label
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_opened = False
        self.is_mine = is_mine
        self.is_flag = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append Object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)  # Left Click
        btn.bind('<Button-3>', self.right_click_actions)  # Right Click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"Cells Left:{Cell.cell_count}",
            bg="black",
            fg='white',
            width=12,
            height=4,
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If Mine COunt === Cells Left, player wins
            if Cell.cell_count == settings.NUM_MINES:
                ctypes.windll.user32.MessageBoxW(
                    0, "Congratulations! You won the game!", "Game Over", 0)

        # Cancel Left and Right click events if cell is_opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        # Return a cell object based on x, y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(
                text=self.surrounded_cells_mines_length)
            # Update text of cell count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # Revert back to original background color
            self.cell_btn_object.configure(
                bg="SystemButtonFace"
            )

        # Mark the cell as opened
        self.is_opened = True

    def show_mine(self):
        # Interrupt Game and Display Message
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(
            0, "You clicked on a mine", "Game Over", 0)
        # Second zero configures type of buttons
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_flag:
            self.cell_btn_object.configure(
                bg='orange'
            )
            self.is_flag = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_flag = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.NUM_MINES
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

from tkinter import Button, Label
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        Cell.all.append(self)
    
    def __repr__(self):
        return f"Cell ({self.x}, {self.y})"
    
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=2,
            height=1,
        
        )
        btn.bind("<Button-1>", self.left_click_actions) # Left Click
        btn.bind("<Button-3>", self.right_click_actions) #Right Click
        self.cell_btn_object = btn
    
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location, 
            bg = "black",
            fg = "white",
            text=f"Cells Left: {Cell.cell_count}"
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
            #if mines count is equal to the cells left count, player won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "Congratulations, you won.", "Game Over", 0 )
                sys.exit()


        #cancel left and right click events if cell is already open 
        self.cell_btn_object.unbind("<Button-1>")
        self.cell_btn_object.unbind("<Button-3>")
    
    def get_cell_by_axis(self, x, y):
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
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1),

        ]
        
        cells = [cell for cell in cells if cell is not None]
        return cells
    
    @property
    def surrounded_cells_mines_length(self):
        counter = 0 
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter +=1
        
        return counter


    
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text = f"Cells Left: {Cell.cell_count}"
                )
            self.cell_btn_object.configure(
                bg = "SystemButtonFace"
            )
            #mark the cell as opened
            self.is_opened = True 

    def show_mine(self):
        self.cell_btn_object.configure(bg= "red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine", "Game Over", 0 )
        sys.exit()

    
    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg="DodgerBlue2"
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg= "SystemButtonFace"
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomise_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    
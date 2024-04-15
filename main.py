from tkinter import *
from cell import Cell
import settings
import utils



root = Tk()
#OVerride the settings of the window
root.configure(bg="black")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title("Mandisweeper")
root.resizable(False, False)

top_frame = Frame(
    root, 
    bg= "black", 
    width= settings.WIDTH,
    height = utils.height_prct(25)

)
top_frame.place(x=0, y=0)
game_title = Label(
    top_frame,
    bg= "black",
    fg="white",
    text = "Mandisweeper",
    font= ("Courier New", 24)
)
game_title.place(
    x=utils.width_prct(12),
    y= 0
)


centre_frame = Frame(
    root, 
    bg="black",
    width=utils.width_prct(75),
    height=utils.height_prct(75),
)
centre_frame.place(
    x=utils.width_prct(26),
    y=utils.height_prct(30)
    )

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c=Cell(x, y)
        c.create_btn_object(centre_frame)
        c.cell_btn_object.grid(
            column=x, row=y
        )

Cell.create_cell_count_label(top_frame)
Cell.cell_count_label_object.place(
    x=utils.width_prct(38), y=35
)

Cell.randomise_mines()


#Run the window
root.mainloop()
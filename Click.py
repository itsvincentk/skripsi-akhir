from Cell import Cell
def clickBoard (board, tiles):
    i = 1
    for row in board:
        for cell in row:
            if (cell.type == Cell.LAMP):
                tiles[i].click()
            i+=1
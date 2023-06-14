from . import Board
from . import Environment
from Cell import Cell
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pickle

# Light-up base url for board gathering
BASE_URL = 'https://www.puzzle-light-up.com/'

# Light-up end url according to each level and difficulties
LEVEL_7_EASY = ''
LEVEL_7_NORMAL = '?size=1'
LEVEL_7_HARD = '?size=2'
LEVEL_10_EASY = '?size=3'
LEVEL_10_NORMAL = '?size=4'
LEVEL_10_HARD = '?size=5'
LEVEL_14_EASY = '?size=6'
LEVEL_14_NORMAL = '?size=7'
LEVEL_14_HARD = '?size=8'
LEVEL_25_EASY = '?size=9'
LEVEL_25_NORMAL = '?size=10'
LEVEL_25_HARD = '?size=11'
LEVEL_DAILY = '?size=13'
LEVEL_WEEKLY = '?size=12'
LEVEL_MONTHLY = '?size=14'

# Cell component identification for web scraping
WHITE_EMPTY = 'cell selectable cell-off'
BLACK_NUMBER = 'light-up-task-cell'
BLACK_WALL = 'light-up-task-cell wall'

# Open selenium using Chrome Profile
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={Environment.USER_DATA}")
options.add_argument(f"--profile-directory={Environment.PROFILE_DIRECTORY}")

# Assign chrome web driver and profile, because we will use Chrome Browser for web scraping
# driver = webdriver.Chrome(Environment.CHROME_DRIVER_PATH, chrome_options=options)
driver = webdriver.Chrome(Environment.CHROME_DRIVER_PATH)

boardInventory = []

def login ():
    # TODO Login using email and username with selenium
    ''

def gatherBoard (level, size):
    # URL for web scraping target
    url = '{}{}'.format(BASE_URL, level)

    # Let selenium open the target URL for scraping
    driver.get(url)

    # Get all tiles from the board on web
    tiles = driver.find_element(By.CLASS_NAME, value = 'board-back').find_elements(By.TAG_NAME, value = 'div')

    # Get every board cell information
    board = getCellsFromBoard(tiles, size)

    # Add board to inventory for writing pickle purposes
    addBoardToInventory(board)


def getCellsFromBoard (tiles, colSize):
    # Variable initialization
    tileClass = ''  # used for temporary class information
    tileText = ''   # used for temporary child text information
    board = []      # returned 2d list
    row = []        # used for temporary row list
    i = 0

    # Iterate trough every tile on the tiles
    for tile in tiles:
        tileClass = tile.get_attribute('class')
        tileText = tile.text

        # Assigning correct cell value, and add it to the temp board
        if tileClass == WHITE_EMPTY:
            row.append(Cell.WHITE_EMPTY)
        if tileClass == BLACK_WALL:
            row.append(Cell.BLACK_ANY)
        if tileClass == BLACK_NUMBER:
            if tileText == '0':
                row.append(Cell.BLACK_ZERO)
            if tileText == '1':
                row.append(Cell.BLACK_ONE)
            if tileText == '2':
                row.append(Cell.BLACK_TWO)
            if tileText == '3':
                row.append(Cell.BLACK_THREE)
            if tileText == '4':
                row.append(Cell.BLACK_FOUR)

        # Move to the next row on the board
        if i == colSize:
            board.append(row)
            row = []
            i = 0
        
        i += 1

    # Return the temporary board
    return board

def printBoard (board):
    # Print the board in matrix 2d display
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))
    print('\n')

def makeEmptyInputFiles ():
    nums = [7, 10, 14, 25, 'DAILY', 'WEEKLY', 'MONTHLY']
    for num in nums:
        open (f"Dataset/{num}.txt", 'w').close()

def addBoardToInventory(board):
    boardInventory.append(board)

def writeInventory (size, difficulty):
    filename = f"Dataset2/{size}_{difficulty}.pkl"
    pickle.dump(boardInventory, open(filename, 'wb'))
    boardInventory.clear()

# Main
if __name__ == "__main__":
    levels7 = [LEVEL_7_EASY, LEVEL_7_NORMAL, LEVEL_7_HARD]
    levels10 = [LEVEL_10_EASY, LEVEL_10_NORMAL, LEVEL_10_HARD]
    levels14 = [LEVEL_14_EASY, LEVEL_14_NORMAL, LEVEL_14_HARD]
    levels25 = [LEVEL_25_EASY, LEVEL_25_NORMAL, LEVEL_25_HARD]
    sizes = [Board.SIZE_LEVEL_7, Board.SIZE_LEVEL_10, Board.SIZE_LEVEL_14, Board.SIZE_LEVEL_25]
    difficulties = [Board.DIFF_EASY, Board.DIFF_NORMAL, Board.DIFF_HARD]


    size = sizes[0]
    for i, level in enumerate(levels7):
        difficulty = difficulties[i]
        for j in range (100):
            gatherBoard(level, size)
        writeInventory(size, difficulty)
        print(f"PAPAN {size}-{difficulty} SELESAI!")
    
    # size = sizes[1]
    # for i, level in enumerate(levels10):
    #     difficulty = difficulties[i]
    #     for j in range (100):
    #         gatherBoard(level, size)
    #     writeInventory(size, difficulty)
    #     print(f"PAPAN {size}-{difficulty} SELESAI!")
    
    # size = sizes[2]
    # for i, level in enumerate(levels14):
    #     difficulty = difficulties[i]
    #     for j in range (100):
    #         gatherBoard(level, size)
    #     writeInventory(size, difficulty)
    #     print(f"PAPAN {size}-{difficulty} SELESAI!")
    
    # size = sizes[3]
    # for i, level in enumerate(levels25):
    #     difficulty = difficulties[i]
    #     for j in range (100):
    #         gatherBoard(level, size)
    #     writeInventory(size, difficulty)
    #     print(f"PAPAN {size}-{difficulty} SELESAI!")

        
    
    # level = LEVEL_7_EASY
    # size = Board.SIZE_LEVEL_7
    # difficulty = Board.DIFF_EASY

    # for i in range (100):
    #     gatherBoard(level, size)

    # writeInventory(size, difficulty)

    # inventory = pickle.load(open('Dataset2/7_easy.pkl', 'rb'))
    # for inv in inventory:
    #     print (inv)
    
    
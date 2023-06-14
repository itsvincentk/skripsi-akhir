from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from Cell import Cell
from Game import Game
import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains

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
            row.append(Cell.WHITE)
        if tileClass == BLACK_WALL:
            row.append(Cell.ANY)
        if tileClass == BLACK_NUMBER:
            if tileText == '0':
                row.append(Cell.ZERO)
            if tileText == '1':
                row.append(Cell.ONE)
            if tileText == '2':
                row.append(Cell.TWO)
            if tileText == '3':
                row.append(Cell.THREE)
            if tileText == '4':
                row.append(Cell.FOUR)
        # Move to the next row on the board
        if i == colSize:
            board.append(row)
            row = []
            i = 0
        i += 1

    # Return the temporary board
    return board

def playBoard (boardType):
    tiles = driver.find_element(By.CLASS_NAME, value = 'board-back').find_elements(By.TAG_NAME, value = 'div')
    firstBoard = getCellsFromBoard(tiles, boardType[1])
    print (firstBoard)
    game = Game(seed, population, punishment, epoch, rank, preproc)
    game.play(firstBoard, tiles, ActionChains(driver))
    driver.find_element(By.ID, value='btnReady').click()
    #take result screenshot
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"ResultPlay/result_{date_string}.png"
    driver.execute_script('window.scrollTo(0, 0);')
    driver.save_screenshot(filename)
    time.sleep(5)
    if boardType[0] < 12:
        driver.find_element(By.ID, value='btnNew').click()

if __name__ == '__main__':

    LEVEL_7_EASY = [0, 7]
    LEVEL_7_NORMAL = [1, 7]
    LEVEL_7_HARD = [2, 7]
    LEVEL_10_EASY = [3, 10]
    LEVEL_10_NORMAL = [4, 10]
    LEVEL_10_HARD = [5, 10]
    LEVEL_14_EASY = [6, 14]
    LEVEL_14_NORMAL = [7, 14]
    LEVEL_14_HARD = [8, 14]
    LEVEL_25_EASY = [9, 25]
    LEVEL_25_NORMAL = [10, 25]
    LEVEL_25_HARD = [11, 25]
    LEVEL_DAILY = [12, 30]
    LEVEL_WEEKLY = [13, 30]
    LEVEL_MONTHLY = [14, 40]

    WHITE_EMPTY = 'cell selectable cell-off'
    BLACK_NUMBER = 'light-up-task-cell'
    BLACK_WALL = 'light-up-task-cell wall'

    seed = 180820
    population = 200
    base = 2
    punishment = [5*base, 20*base, 1*base, 100*base, 100*base, 100*base]
    epoch = 500
    rank = 0.1
    preproc = True

    levelToPlay = [LEVEL_7_EASY]
    playCount = 5


    # Set the path to the Chrome profile
    chrome_profile_path = 'C:\\Users\\itsvi\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

    # Set the path to the Chrome WebDriver executable
    chrome_driver_path = 'C:\\Users\\itsvi\\OneDrive\\Documents\\Unpar\\Skripsi\\recreate\\ChromeDriver\\chromedriver.exe'

    # Create Chrome options and specify the profile path
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    #chrome_options.add_argument('--user-data-dir=' + chrome_profile_path)

    # Create a new instance of the Chrome driver with the specified options and driver path
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    driver.maximize_window()

    board = ['', '?size=1', '?size=2', '?size=3', 
             '?size=4', '?size=5', '?size=6', 
             '?size=7', '?size=8', '?size=9', 
             '?size=10', '?size=11', '?size=13', 
             '?size=12', '?size=14']

    # Use the driver to perform actions
    for level in levelToPlay:
        driver.get(f"https://www.puzzle-light-up.com/{board[level[0]]}")
        #time.sleep(5)
        #time.sleep(10)
        for _ in range (playCount):
            playBoard(level)

    # Close the browser window
    driver.quit()

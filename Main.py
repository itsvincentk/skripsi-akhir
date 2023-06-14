import pickle as pc
from Game import Game
import datetime
import sys
from tabulate import tabulate
import statistics

if __name__ == "__main__":
    # get current date and time
    now = datetime.datetime.now()

    # format date and time as a string
    date_string = now.strftime("%Y-%m-%d-%H-%M-%S")

    # create output file with date and time in the name
    #filename = f"Log/output_{date_string}.txt"

    # Open the file in write mode
    #log_file = open(filename, 'w')

    # Redirect the standard output to the file
    #sys.stdout = log_file
    dataset = ['7_easy', '7_normal', '7_hard',
               '10_easy', '10_normal', '10_hard',
               '14_easy', '14_normal', '14_hard',
               '25_easy', '25_normal', '25_hard',
               '30_daily', '30_weekly', '40_monthly']
    seed = 180820
    population = [200]
    base = 1
    punishment = [5*base, 20*base, 1*base, 100*base, 100*base, 100*base]
    epoch = [500]
    rank = [0.1]
    preproc = [True]
    boardCount = 10
    datasetToTest = [dataset[-4], dataset[-5], dataset[-6]]
    headers = ['Preprocessing', 'Tingkat kesulitan', 'Nomor papan', 'Nilai fitness akhir', 'Pelanggaran']
    final_result = []
    filename = f"output_{date_string}"
    with open(f"ResultEXP/{filename}.txt", 'a') as f:
        for d in datasetToTest:
            for pop in population:
                for e in epoch:
                    for r in rank:
                        for prep in preproc:
                            jumlahPapanSelesai = 0
                            fitness = []
                            if d == dataset[-1] or d == dataset[-2] or d == dataset[-3]: boardCount = 1
                            else: boardCount = 100
                            for i in range (0, 10):
                                inventory = pc.load(open(f"Dataset/{d}.pkl", 'rb'))
                                firstBoard = inventory[i]
                                game = Game(seed, pop, punishment, e, r, prep)
                                ans = game.experiment(firstBoard)
                                violation = ','.join(map(str, ans.violation))
                                result = [preproc, d, i, ans.fitness, violation]
                                final_result.append(result)
                                fitness.append(ans.fitness)
                                if ans.fitness == 0: jumlahPapanSelesai+=1
                                #ans.board.printBoard()
                                print(d, i, ans.fitness, ans.violation)
                            avg = sum(fitness) / boardCount
                            std_dev = statistics.stdev(fitness)
                            print (sum(fitness))
                            print(f"{d}-{punishment}-{pop}-{e}-{r}-{prep}: avg = {avg:.4f} | std = {std_dev} | selesai = {jumlahPapanSelesai}/{boardCount}\n")
                            f.write(f"{d}-{punishment}-{pop}-{e}-{r}-{prep}: avg = {avg:.4f} | std = {std_dev} | selesai = {jumlahPapanSelesai}/{boardCount}\n")
    f.close()
    table = tabulate(final_result, headers=headers, tablefmt='latex')
    filename = f"output_{date_string}"
    with open(f"ResultTEX/{filename}.tex", 'w') as f:
        f.write(table)
    

    
    
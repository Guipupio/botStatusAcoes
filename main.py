from argparse import ArgumentParser
from datetime import datetime
from os import getcwd as pwd
from os import listdir

from fundsExplorer.manager import analisa_fiis, generate_csv_current_data

parser = ArgumentParser()

parser.add_argument("-gf", "--get-fiis", type=int, dest="get_fiis",
                    help="Busca Rank de FIIs no FundsExplorer (default: 0)", metavar='', default=0)

parser.add_argument("-pf", "--plot-fiis", type=int, dest="plot_analise_fiis",
                    help="Plota dos fiis (default: analise do ultimo csv obtido)", metavar='', default=0)

parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

if __name__ == '__main__':
    args = parser.parse_args()
    
    PATH_FIIS = '/'.join([pwd(), 'csvs', 'fiis'])
    filename = datetime.now().strftime("%Y-%m-%d")

    if args.get_fiis:
        # Gera CSV dos dados do FundsExplorer
        generate_csv_current_data(path_save_csv=f"{PATH_FIIS}/{filename}.csv")

    if args.plot_analise_fiis:
        filenames = listdir(PATH_FIIS)
        filenames.sort()

        analisa_fiis(filenames[-1])
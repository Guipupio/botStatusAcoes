from argparse import ArgumentParser
from datetime import datetime

from fundsExplorer.manager import generate_csv_current_data

parser = ArgumentParser()
parser.add_argument("-gf", "--get-fiis", type=int, dest="get_fiis",
                    help="Busca Rank de FIIs no FundsExplorer (default: 0)", metavar='', default=0)

parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

if __name__ == '__main__':
    args = parser.parse_args()
    
    if args.get_fiis:
        # Gera CSV dos dados do FundsExplorer
        generate_csv_current_data(path_save_csv="{data}_fiis.csv".format(data=datetime.now().strftime("%Y-%m-%d")))
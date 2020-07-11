from argparse import ArgumentParser
from datetime import datetime
from os import getcwd as pwd
from os import listdir

from fundsExplorer.manager import plota_fiis, generate_csv_current_data
from constantes import SEP_DIR

parser = ArgumentParser()

parser.add_argument("-gf", "--get-fiis", type=int, dest="get_fiis",
                    help="Busca Rank de FIIs no FundsExplorer (default: 0)", metavar='', default=0)

parser.add_argument("-pf", "--plot-fiis", type=int, dest="plot_analise_fiis",
                    help="Plota grafico do indice passado. Ex: -1 plota ultimos dados obtidos (default: None)", metavar='', default=None)

parser.add_argument("-auto-fit", "--auto-fit", type=int, dest="setor_auto_fit",
                    help="Ajusta cada subplot isolamente sem considerar os demais. (default: 0)", metavar='', default=0)

parser.add_argument("-only-mine", "--only-mine", type=int, dest="only_mine",
                    help="Plota apenas os FIIs definidos em user.properties. (default: 0)", metavar='', default=0)

parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

if __name__ == '__main__':
    args = parser.parse_args()
    
    PATH_FIIS = SEP_DIR.join([pwd(), 'csvs', 'fiis'])
    filename = datetime.now().strftime("%Y-%m-%d")

    if args.get_fiis:
        # Gera CSV dos dados do FundsExplorer
        generate_csv_current_data(path_save_csv=f"{PATH_FIIS}{SEP_DIR}{filename}.csv")

    if args.plot_analise_fiis is not None:
        filenames = listdir(PATH_FIIS)
        filenames.sort()

        plota_fiis(
            path_to_csv=f"{PATH_FIIS}{SEP_DIR}{filenames[args.plot_analise_fiis]}",
            setor_auto_fit=args.setor_auto_fit,
            only_mine=args.only_mine,
        )
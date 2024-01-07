from glob import glob
from os.path import basename,dirname,realpath
from pandas import read_csv
import logging
import re

columnTypes = {'Before breakfast': 'Int64',
               '2h after breakfast': 'Int64',
               'Before lunch': 'Int64',
               '2h after lunch': 'Int64',
               'Before dinner': 'Int64',
               '2h after dinner': 'Int64',
               'Extra': 'Int64'}
dayMapping = {'seg': 'Mon',
              'ter': 'Tue',
              'qua': 'Wed',
              'qui': 'Thu',
              'sex': 'Fri',
              'sáb': 'Sat',
              'dom': 'Sun'}
monthMapping = {'jan': 'Jan',
                'fev': 'Feb',
                'mar': 'Mar',
                'abr': 'Apr',
                'mai': 'May',
                'jun': 'Jun',
                'jul': 'Jul',
                'ago': 'Aug',
                'set': 'Sep',
                'out': 'Oct',
                'nov': 'Nov',
                'dez': 'Dec'}

def formatCSV():
    dataDir = dirname(realpath(__file__)).replace("project/util","data/formatted/")
    files = [f for f in glob(''.join([dataDir,'*.csv']))]
    pattern = re.compile(r'^(([^,]*,){8}[^,]*)')
    logging.info(f"{len(files)} files found. Formatting data...")
    for file in files:
        year = basename(file).replace('.csv','')
        with open(file, 'r') as fileContent:
            lines = fileContent.readlines()
        if "manhã" in lines[0]:
            logging.info(f"Formatting {year} file.")
            lines = [pattern.match(line).group(1) + '\n' if pattern.match(line) else line for line in lines]
            lines[:2] = ["Date,Before breakfast,2h after breakfast,Before lunch,2h after lunch,Before dinner,2h after dinner,Extra,Comment\n"]
            with open(file, 'w') as fileContent:
                fileContent.writelines(lines)
            data = read_csv(file, sep=',', dtype=columnTypes)
            for portugueseDay, englishDay in dayMapping.items():
                data['Date'] = data['Date'].str.replace(portugueseDay, englishDay)
            for portugueseMonth, englishMonth in monthMapping.items():
                data['Date'] = data['Date'].str.replace(portugueseMonth, englishMonth)
            data.to_csv(file, index=False)
            logging.info(f"{year} formatted successfully.")
        else:
            logging.info(f"{year} already formatted.")

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='[%(threadName)s:%(filename)s:%(funcName)s:%(lineno)d]|[%(asctime)s]|[%(levelname)s]: %(message)s')
    formatCSV()
from glob import glob
from os.path import dirname,realpath
from pandas import read_csv

def mapPortugueseToEnglish():
    dataDir = dirname(realpath(__file__)).replace("project/util","data/")
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
    for file in [f for f in glob(''.join([dataDir,'*.csv']))]:
        data = read_csv(file, sep=',', dtype=columnTypes)
        if data['Date'].str.contains('sáb').any():
            for portugueseDay, englishDay in dayMapping.items():
                data['Date'] = data['Date'].str.replace(portugueseDay, englishDay)
            for portugueseMonth, englishMonth in monthMapping.items():
                data['Date'] = data['Date'].str.replace(portugueseMonth, englishMonth)
            data.to_csv(file, index=False)
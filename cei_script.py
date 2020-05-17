class Calculator:

    def __init__(self, archive):
        """directory "str" from archive(xsl)"""
        self.__archive = archive

    def import_archive(self):
        """import archive:
        usecols=('B:K') and "header=10" will be the same everytime ?
        exclude rows with all values == NaN
        exclude columns with all values == NaN
        converting the index (axis=column) to date"""
        from pandas import read_excel, to_datetime
        self.__archive_cei_records = read_excel(self.__archive, index_col=0, usecols='B:K', header=10)
        self.__archive_cei_records.dropna(axis='columns', how='all', inplace=True)
        self.__archive_cei_records.dropna(axis='rows', how='all', inplace=True)
        self.__archive_cei_records.index = to_datetime(self.__archive_cei_records.index)

    @property
    def df_records(self):
        """show a df from archive formated, after import and cleanned"""
        print(self.__archive_cei_records)

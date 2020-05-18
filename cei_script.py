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
        self.__archive_cei_records['Category'] = self.insert_type_column()

    @property
    def df_records(self):
        """show a df from archive formated, after import and cleanned"""
        print(self.__archive_cei_records)
        
    def check_type(self, value):
        """look for a pattern and categorize in a type (acao ou fii_etf) CI = FII or ETF"""
        import re
        pattern = "(\s){1}[C]{1}[I]{1}(\b){,1}"
        try:
            validate = re.search(pattern, value)
            validate.group()[1:3] == 'CI'
            return 'FII-ETF'
        except:
            return 'ACAO'

    def insert_type_column(self):
        """loop to include one column with the category in df_formated"""
        column_type = []
        for i in range(0, len(self.__archive_cei_records)):
            row = self.__archive_cei_records.iloc[i, 3]
            type_found = self.check_type(row)
            column_type.append(type_found)
        return column_type

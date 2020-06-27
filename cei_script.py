from typing import Dict, Any, Union

from pandas import to_datetime, Series, DataFrame


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
        # self.__archive_cei_records.index = to_datetime(self.__archive_cei_records.index)
        self.__archive_cei_records.reset_index(inplace=True)
        self.__archive_cei_records['Category'] = self.insert_type_column()
        self.__archive_cei_records.rename(columns={'Data Negócio': 'Data',
                                                   'Especificação do Ativo': 'Empresa',
                                                   'Código': 'Ticker',
                                                   'Valor Total (R$)': 'ValorTotal',
                                                   'Preço (R$)': 'Preço'},
                                          inplace=True)
        self.__archive_cei_records['Data'] = to_datetime(self.__archive_cei_records['Data'], format='   %d/%m/%y')
        self.__archive_cei_records['C/V'] = [i.replace(i, i.strip())
                                             for i in self.__archive_cei_records['C/V']]

    @property
    def df_records(self):
        """show a df from archive formated, after import and cleanned"""
        print(self.__archive_cei_records)

    def df_records_csv(self):
        """show a df(csv) from archive formated, after import and cleanned"""
        return self.__archive_cei_records.to_csv('df_formated.csv', encoding='latin-1', index=False)

    def dfs_records_csv(self):
        """show two dfs(csv) from archive formated, after import and cleanned,
        one with ['Category'] == 'FII-ETF'
         another ['Category'] == 'ACAO'"""
        df1 = self.fii_etf()
        df2 = self.stocks()
        return df1.to_csv('df_formated_fii_etf.csv', encoding='latin-1', index=False), \
               df2.to_csv('df_formated_stocks.csv', encoding='latin-1', index=False)

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
            row = self.__archive_cei_records.iloc[i, 4]
            type_found = self.check_type(row)
            column_type.append(type_found)
        return column_type

    def month_sell_amount(self, output=1):
        """at first, call for two inputs, month and year, filter df by ['C/V] == 'V'
        output == 'df' == new df by input range and sum all sell ('V') values ;
        output != 'df' == sum of all sell values at range"""
        month = input('Month: ')
        year = input('Year: ')
        df_sell = self.__archive_cei_records[self.__archive_cei_records['C/V'].str.contains('V')]
        df_sell = df_sell[df_sell['Data'].dt.strftime('%m').str.contains(month)]
        df_sell = df_sell[df_sell['Data'].dt.strftime('%Y').str.contains(year)]
        if output != 'df':
            return df_sell['ValorTotal'].sum()
        else:
            return df_sell

    def fii_etf(self):
        """show a new df from archive formated, after import and cleanned, with fii_etf"""
        df_fii_etf = self.__archive_cei_records[self.__archive_cei_records['Category'] == 'FII-ETF']
        return df_fii_etf

    def stocks(self):
        """show a new df from archive formated, after import and cleanned, with stocks"""
        df_stocks = self.__archive_cei_records[self.__archive_cei_records['Category'] == 'ACAO']
        return df_stocks

    # def find_tickers_byrange(self):
    #     """find tickers by all sells in range inputed"""
    #     ticker_all = self.month_sell_amount('df')
    #     return ticker_all['Ticker'].unique()

    def amount_amountprice_averageprice(self, df):
        """look for a df (just with one Ticker) and calculate: number, amount_price and average_price"""
        number = 0
        amount_price = 0
        average_price = 0
        for i in range(0, df.shape[0]):
            if df.iloc[i, 1] == 'C':
                number_up = df.iloc[i, 5]
                number += round(number_up, 3)
                amount_price_up = round(df.iloc[i, 7], 3)
                amount_price += amount_price_up
                average_price = round(amount_price / number, 3)
            else:
                number_up = round(df.iloc[i, 5], 3)
                amount_price_up = round(average_price * number_up, 3)
                amount_price -= amount_price_up
                number -= number_up
        return [number, amount_price, average_price]

    def profit_loss_unique(self, df_records, df_month):
        """Look for two dfs, one with all records by one ticker,
                another with df_sell (self.month_sell_amount('df')).
            Find one range, using df_sell's index (just one row),
                and create a new df, using the range in df_records[0:index].
            After, take df_sell['ValorTotal'], take averageprice of self.amount_amountprice_averageprice,
                multiply by df_sell['Quantidade'], find profit or loss row by row for one ticker"""
        profit_loss_unique = 0
        for i in df_month.axes[0]:
            index_start = df_records.iloc[0:1].index[0]
            index_end = i
            new_df = df_records.loc[index_start:index_end]
            amount_sell = df_month.loc[i, 'ValorTotal']
            amount_buy = df_month.loc[i, 'Quantidade'] * self.amount_amountprice_averageprice(new_df)[2]
            profit_loss_unique += amount_sell - amount_buy
        return profit_loss_unique

    def profit_loss_month(self):
        """Take all tickers of df_sell and use self.profit_loss_unique() for them,
                after, sum all profits or loss of them, finding the result of month"""
        profit_loss_month = 0
        df_sell = self.month_sell_amount('df')
        for i in df_sell['Ticker'].unique():
            df_records = self.__archive_cei_records[self.__archive_cei_records['Ticker'] == i]
            df_month = df_sell[df_sell['Ticker'] == i]
            profit_loss_month += float(self.profit_loss_unique(df_records, df_month))
        return float(profit_loss_month)

from cei_script import Calculator

relatorio = Calculator(r'C:\Users\bsimm\Downloads\InfoCEI(5).xls')

relatorio.import_archive()

# relatorio.df_records
# print(relatorio.month_sell_amount())
# relatorio.df_records_csv()
# relatorio.dfs_records_csv()
# relatorio.find_tickers_byrange()
relatorio.profit_loss_month()
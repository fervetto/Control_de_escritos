#def xlsx_to_csv_pd():
#    data_xls = pd.read_excel('grid_dbo_vConsultaProveidosFirmadosTodos.xlsx', index_col=0)
#    return data_xls.to_csv('grid_dbo_vConsultaProveidosFirmadosTodos.csv', encoding='utf-8')
    
 
 
#if __name__ == '__main__':
#    xlsx_to_csv_pd()

from os import sep
import pandas as pd
pd.read_excel('grid_dbo_vConsultaProveidosFirmadosTodos.xlsx').to_csv('grid_dbo_vConsultaProveidosFirmadosTodos.csv', encoding='utf-8',header=False , index=False, sep=";")
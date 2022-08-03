import json
import os
import glob
import pandas as pd
from numpy import arange
from openpyxl import load_workbook



                
from loghandler import Log
import logtools


logs_path = "GRR"



def main():

    df = pd.DataFrame({'Name': ['E','F','G','H'],
                   'Age': [100,70,40,60]})
    writer = pd.ExcelWriter('demo.xlsx', engine='openpyxl')
    # try to open an existing workbook
    writer.book = load_workbook('demo.xlsx')
    # copy existing sheets
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    # read existing file
    reader = pd.read_excel(r'demo.xlsx')
    # write out the new sheet
    df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)

    writer.close()
    pass




if __name__ == "__main__":
    main()




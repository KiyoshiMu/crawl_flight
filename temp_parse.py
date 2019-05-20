import pandas as pd
import ast
import os

def info_refine(info_dict, bound=21):
    df = pd.DataFrame.from_dict(info_dict, orient='index')
    df.reset_index(inplace=True)
    df.columns="date, plane, depart_time, depart_loc, \
arrive_loc, arrive_time, note, price".split(', ')
    temp = df['price'].str.extract(r'(?P<currency>\D*)(?P<price>\d+)')
    df['price'] = pd.to_numeric(temp['price'])
    df['currency'] = temp['currency']
    return df.nsmallest(bound, 'price').reset_index(drop=True)

def txt_dict():
    with open('temp.txt', 'r', encoding='utf-8') as temp:
        df = pd.concat([info_refine(ast.literal_eval(line)) for line in temp.readlines()]
        , ignore_index=True)
    df.to_excel('temp.xlsx')

if __name__ == "__main__":
    txt_dict()
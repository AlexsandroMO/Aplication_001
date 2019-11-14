#from tinymongo import TinyMongoClient
import pandas as pd
import xlrd
from tinydb import TinyDB, Query
import openpyxl

db = TinyDB('DB_JSON/db.json')

#===============================
#Cadastro Usuários
#===============================

def registerDB(firstname, lastname, email1, password1):
    return db.insert({'FIRST_NAME':firstname,'LAST_NAME':lastname,'EMAIL':email1,'PASSWORD':password1})

    print(db.all())

Ft = Query()

def query_email_confere(email, password):
    new_db = db.search(Ft.EMAIL == email and Ft.PASSWORD == password)
  
    return new_db

#===================
## DONWLOAD
#==================

def create_list():

    cc = pd.read_excel('static/INT_DELNT_CRTL_META_REV.xlsx')
    RAI = pd.read_excel('static/rai.xlsx')

    df = cc[['CC', 'NCR_RAI', 'STATUS']]
    df.rename(columns={'NCR_RAI': 'RAI'}, inplace=True)

    df = df.fillna('-')

    df['STATUS_LIBERA'] = '-'

    lista = []
    for a in range(len(df)):
        x = df['RAI'][a]
        y = x.split('/')
        if len(y) > 1:
            for b in y:
                lista.append([df['CC'][a], b, df['STATUS'][a], df['STATUS_LIBERA'][a]])
        else:
            lista.append([df['CC'][a], x, df['STATUS'][a], df['STATUS_LIBERA'][a]])

    new_df = pd.DataFrame(data=lista, columns=['CC', 'NCR_RAI', 'STATUS', 'STATUS_LIBERA'])
    new_df.sort_values(by=['NCR_RAI'], inplace=True)

    for i in range(len(new_df)):
        a = new_df['NCR_RAI'].loc[i]
        if a != '-':
            b = new_df[new_df['NCR_RAI'] == new_df['NCR_RAI'].loc[i]]
            e = []
            for c in b['STATUS']:
                if c == 'Publicado':
                    e.append(c)
                if len(e) == len(b['STATUS']):
                    new_df['STATUS_LIBERA'].loc[i] = 'Todos Cadernos Publicados'

    new_df.sort_values(by=['NCR_RAI'], inplace=True)
    df2 = RAI[['RAI', 'DISCIPLINA', 'COS', 'STATUS', 'ACAO_DELINEAMENTO']]

    df2 = df2[df2['STATUS'] == 'Em Delineamento | Analisado']

    analize_rai = new_df[new_df['STATUS_LIBERA'] == 'Todos Cadernos Publicados'][['NCR_RAI', 'STATUS_LIBERA']]
    analize_rai = analize_rai[analize_rai['NCR_RAI'] != '']

    cont = 0
    for a in analize_rai.index:
        cont += 1
        analize_rai.rename(index={a: cont}, inplace=True)

    lista = []
    cont = 0
    for a in analize_rai['NCR_RAI']:
        for b in df2['RAI']:
            if a == b:
                cont += 1
                lista.append([b, 'Liberar RAI_NCR'])

    NCR_RAI_LIBERAR = pd.DataFrame(data=lista, columns=['NCR_RAI', 'STATUS'])

    LIBERAR = NCR_RAI_LIBERAR[NCR_RAI_LIBERAR['NCR_RAI'] != '']
    NCR_RAI_Libera = LIBERAR.groupby(['NCR_RAI', 'STATUS']).count()

    print('\n\nRealizado!')

    NCR_RAI_Libera.to_excel('static/NCR_RAI_LIBERAR.xlsx', 'NCR_RAI_LIBERAR')

    return 'OK'



#
# def db_query2():
#   return db.update({"nome": "Vitor"}, Ft.senha == 'Eller')
#
# def db_query3():
#   return db.remove(Ft.senha == 'Ell')


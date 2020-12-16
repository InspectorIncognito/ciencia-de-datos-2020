import pandas as pd
import glob
import numpy as np
import calendar
from datetime import datetime
import os
from sklearn.preprocessing import StandardScaler

import _pickle as cPickle

def load_cpickle(file_):
    """
    file: path to pickle file

    return: Dictionary
    """

    with open(file_, 'rb') as output:
        mydict = cPickle.load(output)
    return mydict

def patente(df):
    """
    df: dataframe
    
    return: dataframe filtrado con formato de patente correcto
    (XXXX-00 o XX-0000)
    """
    df = df[df['Patente'].map(lambda x: (x[:4].isalpha() and x[5:].isnumeric()) or (x[:2].isalpha() and x[4:].isnumeric()))]
    return df

#--machine <patente> <servicio> <distancia_en_ruta> <tiempo_medición>
def formatoServicio(servicio):
    """
    servicio: string que indica el servicio
    
    return: True si el servicio cumple el formato, False si no
    """
    
    #ej: B09 00R
    if len(servicio) == 7:
        if servicio[0].isalpha() and servicio[1:3].isnumeric() and servicio[3].isspace() \
        and servicio[4:6].isnumeric() and servicio[6].isalpha():
            return True

        else: 
            return False

    #ej: T201 00I, B04V 00I
    if len(servicio) == 8:
        if servicio[0].isalpha() and servicio[1:4].isnumeric() and servicio[4].isspace() \
        and servicio[5:7].isnumeric() and servicio[7].isalpha():
            return True

        if servicio[0].isalpha() and servicio[1:3].isnumeric() and servicio[3].isalpha() \
        and servicio[4].isspace() and servicio[5:7].isnumeric() and servicio[7].isalpha():
            return True

        else: 
            return False

    #ej: B02 C2 00I
    if len(servicio) == 10:
        if servicio[0].isalpha() and servicio[1:3].isnumeric() and servicio[3].isspace() \
        and servicio[4].isalpha() and servicio[5].isnumeric() and servicio[6].isspace() \
        and servicio[7:9].isnumeric() and servicio[9].isalpha():
            return True
        else: 
            return False

    #ej: T201 E0 00I
    if len(servicio) == 11:
        if servicio[0].isalpha() and servicio[1:4].isnumeric() and servicio[4].isspace() \
        and servicio[5].isalpha() and servicio[6].isnumeric() and servicio[7].isspace() \
        and servicio[8:10].isnumeric() and servicio[10].isalpha():
            return True
        else:
            return False

    else:
        return False


def esServicio(servicio):
    """
    servicio: string que indica el servicio
    
    return: True si el servicio está en la lista, False si no
    """
    servs = np.load('servicios_unicos.npy')
    if servicio in servs:
        return True
    else:
        return False

def servicio(df):
    """
    df: dataframe
    
    return: dataframe servicios que cumplen
    formatoServicio y esServicio
    """
    file_ = list(load_cpickle('servs_onehot.pkl').keys())
    df = df[df['Servicio'].isin(file_)]
    return df


def esCoord(lon, lat):
    """
    lon: int, longitud
    lat: int, latitud
    
    return: True si el par está dentro del rango de 
    coordenadas de Santiago, False si no
    """
    
    if lon < -69 and lon > -71 and \
       lat < -32 and lat > -34:
        return True
    else:
        return False

def coords(df):
    """
    df: dataframe
    
    return: dataframe coordenadas que están
    dentro de Santiago
    """
    df = df[df['Latitud'].map(lambda x: (x < -32) and (x > -34))]
    df = df[df['Longitud'].map(lambda x: (x < -69) and (x > -71))]
    return df

def distancia(df):
    """
    df: dataframe
    
    return: dataframe con distanciainicio y distanciaruta 
    sin outliers (-1)
    """
    df = df[df['DistanciaInicio']>=0]
    df = df[df['DistanciaRuta']>=0]
    return df

def fechas(df):
    """
    df: dataframe
    
    return: dataframe que sólo conserva fechas del mes de Agosto 2019
    """
    df = df[df['GPS_time'].map(lambda x: (x[5:7] == '08') and (x[:4] == '2019'))]
    return df

def gpsDia(GPS): 
    """
    GPS: dataframe con columna de fecha
    
    return: dataframe con una nueva columna que indica el 
    día de la semana de cada fecha
    """
    fecha = pd.to_datetime(GPS["GPS_time"])
    GPS['dias'] = fecha.apply(lambda x: calendar.day_name[x.weekday()])
    return GPS

def habilday(GPS):
    """
    GPS: dataframe
    
    return: columna que contiene un 1 si es dia habil y 0 si no 
    """
    dia_semana=['Monday','Tuesday','Wednesday','Thursday','Friday']
    dias=GPS['dias']
    dia_habil=[]
    for i in dias:
        if i in dia_semana:
            dia_habil.append(1)
        else:
            dia_habil.append(0)
    GPS['dia_habil']=dia_habil
    return GPS

def horarios(hora):
    """
    hora: Atributo con el formato datetime como el presente en la columna GPS_time en gps
    
    return: 0 si la hora pertenece a horario bajo, 1 si la hora es de horario valle, 2 si la hora pertenece a horario punta.
    """
    ##horarios valle
    valle_1=pd.to_datetime('09:00:00').time()
    valle_2=pd.to_datetime('17:59:59').time()
    valle_3=pd.to_datetime('20:00:00').time()
    valle_4=pd.to_datetime('20:44:59').time()
    ##horarios puntas
    punta_1=pd.to_datetime('07:00:00').time()
    punta_2=pd.to_datetime('08:59:59').time()
    punta_3=pd.to_datetime('18:00:00').time()
    punta_4=pd.to_datetime('19:59:59').time()
    
    if hora >= valle_1 and hora <= valle_2:
        return 1
    elif hora >= valle_3 and hora <= valle_4:
        return 1
    elif hora >= punta_1 and hora <= punta_2:
        return 2
    elif hora >= punta_3 and hora <= punta_4:
        return 2
    else:
        return 0

def gpsHorarios(GPS): 
    """
    GPS: dataframe
    
    return: columna con los valores categoricos de los horarios definidos en la funcion horarios. retorna el dataframe con 
    la nueva columna 'horarios'.
    """
    fecha = GPS['GPS_time']
    horario = []
    for i in fecha:
        hora=i.time()
        horario.append(horarios(hora))
    GPS['horario']=horario
    return GPS

def gpsWeekendbajo(gps):
    """
    gps: dataframe gps
    
    return: columna final de los tipos de horarios, considerando los días no habiles como horario bajo durante todo el horario 
    """
    gps['horario']=gps['horario']*gps['dia_habil']
    return gps

def delete_cols(df):
    """
    df: dataframe
    
    return: elimina columnas que no se utilizarán
    """
    df = df.drop(columns=['Unnamed:0','Ind1','Ind2','Ind3','Patente', 'GPS_time', 'dias'])
    return df

def notnull_serv(df):
    """
    df: dataframe

    return: Elimina filas con servicios vacios
    """
    return df[df["Servicio"] != " "]

def cod_dia(df):
    """one-hot encoding de los días de la semana"""
    return pd.get_dummies(df, columns=['dias'], prefix='dia', prefix_sep='_', drop_first=True)

def limpieza(df, target = False):
    """
    df: dataframe que se quiere limpiar
    target: booleano que indica True si ya se creó la columna a predecir, False si no
    """
    if target:
        return delete_cols(df)
    else:
        df = patente(df)
        df = servicio(df)
        df = coords(df)
        df = distancia(df)
        df = notnull_serv(df)
        df = gpsDia(df)
        df = fechas(df)
        df = habilday(df)
        return cod_dia(df)

MEAN_PATH = 'mean.csv'
STD_PATH = 'std.csv'
COLUMNS_NORM = ["DistanciaInicio1", "DistanciaRuta1", "Latitud1", "Longitud1", "DistanciaInicio2", "DistanciaRuta2", "Latitud2", "Longitud2"]

def normalize(df):
    mean = pd.read_csv(MEAN_PATH, sep=',', names=["cols", "values"])
    std = pd.read_csv(STD_PATH, sep=',', names=["cols", "values"])
    mean = mean.set_index(mean["cols"]).drop(columns=["cols"]).T
    std = std.set_index(std["cols"]).drop(columns=["cols"]).T

    df[COLUMNS_NORM] = (df[COLUMNS_NORM] - mean[COLUMNS_NORM].to_numpy()) / std[COLUMNS_NORM].to_numpy()
    return df
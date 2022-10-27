"""
funciones.py
Módulo que implementa las siguientes funciones:

-get_data: Esta función obtiene datos de la red en un rango de tiempo 
especifico y los almacena en listas
-set_data: Ordena los datos ingresados en una lista de diccionarios
"""

import requests 
from bs4 import BeautifulSoup


def get_data(dq_dia, dq_mes, aq_dia, aq_mes, aq_anio, data_limit):
    """
    Esta función obtiene datos de la red en un rango de tiempo 
    especifico y los almacena en listas
    
    Parameters
    ----------
    dqDia : string
        Valor del día en que comenzara la busqueda\n
    dqMes : string
        Valor asociado al mes en el que comenzara la busqueda\n
    aqDia : string
        Valor del día en que terminara la busqueda\n
    aqMes : string
        Valor asociado al mes en el que terminara la busqueda\n
    aqAnio : string
        Valor del año en el que se realizara la busqueda\n
    data_limit : int
    Número de datos a obtener por cada tipo de dato 
    (string y float)

    Returns 
    ----------
    data_string : list
        Lista con los datos almacenados en formato de cadena\n
    data_float : list
        Lista con los datos almacenados en formato de flotante
    
    Raises
    ----------
    ValueError
        Si no se pudo conectar al servidor
    """

    #Listas donde se almacenarán los datos obtenidos
    data_string=[]
    data_float=[]

    #Parametros para contruir el url del que obtendremos información
    params={"Punto": 100, "dqDia": dq_dia, "dqMes":dq_mes, "dqAnio": aq_anio, 
            "aqDia": aq_dia, "aqMes": aq_mes, "aqAnio": aq_anio}
    url="http://www.economia-sniim.gob.mx/Consolidados.asp" 
    response=requests.get(url, params=params)
    
    #Se obtienen los datos de interes, para ser guardados en listas
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_strings=soup.find_all('td', {'class': 'Datos'}, limit= data_limit)
    soup_floats=soup.find_all('td', {'class': 'TotRes'}, limit= data_limit)
    for i in soup_strings: data_string.append(i.text)
    for i in soup_floats: data_float.append(float(i.text))
    
    return data_string, data_float


def set_data(new_flt, new_str, old_flt, old_str, data_limit):
    """
    Esta función ordena los datos ingresados en una lista de diccionarios
    
    Parameters
    ----------
    old_str : list
        Lista con los valores tipo cadena del 2021\n
    old_flt : list
        Lista con los valores tipo flotante del 2021\n
    new_str : list
        Lista con los valores tipo cadena del 2022\n
    new_flt : list
        Lista con los valores tipo flotante del 2022 
    data_limit : int
        Número de datos a obtener por cada tipo de dato 
    (string y float)
    
    Returns
    ----------
    final_list : list
        Lista de directorios con los datos del producto
    """
    #Listas donde se almacenarán los directorios d datos
    final_list=[]
    
    i=0
    while i < data_limit:

        #Flitro de datos para comparar los datos de ambos años
        if (new_flt[i] < old_flt[i]): 
            old_flt[i] = new_flt[i]

        if (new_flt[i+1] > old_flt[i+1]):
            old_flt[i+1] = new_flt[i+1]

        if (old_str[i+1] != new_str[i+1]):
            old_str[i+1] = old_str[i+1] + new_str[i+1]
            
        old_str[i+2] = old_str[i+2] + new_str[i+2]

        #Se obtiene la varicación de los promedios en los 2 años
        var_tiem = old_flt[i+2] - new_flt[i+2]   
        old_flt[i+2] = (old_flt[i+2]*365 + new_flt[i+2]*212) / 577

        final_list.append({'product': old_str[i].replace("\n","").replace("\xa0", ""), 
                         'min_price': old_flt[i], 
                         'max_price': old_flt[i+1],
                         'avg_price': round(old_flt[i+2],2), 
                         'origin': old_str[i+1], 
                         'distr': old_str[i+2], 
                         'var_tiem': var_tiem})
        
        i=i+3
    return final_list
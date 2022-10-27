'''
2-scraping-data.py
Este programa obtiene los datos y precios de productos agrícolas
en un rango de tiempo deseado y realiza un breve análisis estadístico,
guarda los datos en un documento con extensión CSV, imprime una tabla 
con el resumen estadístico del precio promedio de los productos y los
5 productos que tienen más variación en el tiempo en los precios
promedio
'''

import funciones as fc 
import pandas as pd


if __name__ == '__main__':

    data_limit=243
    list_prod=[]
    oldlist_str=[]
    oldlist_flt=[]
    newlist_str=[]
    newlist_flt=[]
  
    oldlist_str, oldlist_flt = fc.get_data('01', '01', '31', '12', '2021',
        data_limit)

    newlist_str, newlist_flt = fc.get_data('01', '01', '31', '07', '2022',
        data_limit)

    list_prod= fc.set_data( newlist_flt,  newlist_str, oldlist_flt, 
        oldlist_str, data_limit)
    
    df_prod=pd.DataFrame(list_prod)
    
    #Guardar información en formato CSV
    df_prod[['product', 'min_price', 'max_price', 'avg_price', 'origin',
        'distr']].to_csv('data_frutas_verduras.csv', encoding='utf-8') 
    
    #Resumen estadistico de los precios promedio
    print('\n Resumen Estadistico')
    print(df_prod['avg_price'].describe())
    
    #Tabla con los productos con más variación en los precios promedio
    print(df_prod[['product', 'var_tiem']].nlargest(5, 'var_tiem'))
    
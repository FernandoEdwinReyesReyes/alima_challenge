"""
1-split-and-join.py
Este programa separa una cadena ingresada por el usuario en un
delimitador " " y la imprime unida por un guion /
"""
def split_and_join(line):
    """
    Esta función separa una cadena en un delimitador " " y la une
    con un guion
    Parameters
    ----------
    line : string
        Cadena a ser separada
    
    Returns
    ----------
    line_join : string
        Cadena unida por guion /
    """

    #Separa la cadena y la guarda en una lista
    line_list=line.split()

    #Une los elementos de la lista con un guion 
    line_join='/'.join(line_list)

    return line_join
    
if __name__ == '__main__':
   line=input()
   result=split_and_join(line)
   print(result)


"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf



def printVideosbyCategory(videos):
    """
    Imprime los libros que han sido clasificados con
    una etiqueta
    """
    if (videos):
        print('Se encontraron: ' + str(lt.size(videos)) + ' Videos.')
        for video in lt.iterator(videos):
            print(video['title'])
        print("\n")
    else:
        print("No se encontraron Videos.\n")

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en el catalogo
    """
    controller.loadData(catalog)

def printMenu():
    print("1- Inicializar el catálogo")
    print("2- Cargar información en el catálogo")
    print('3- Hallar los n videos con más LIKES para un pais y categoría específica')
    print('4- Hallar video que más días ha sido trending para un país específico')
    print('5- Hallar video que más días ha sido trending para una categoria específica')
    print('6- Requerimiento 4')
    print('0- Salir')

catalog = None

"""
Menu principal
"""
menu = True
while menu == True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        cont = controller.initCatalog()
        print('Se ha inicializado el catalogo correctamente')

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ... Espere en linea")
        
        

        
        answer = controller.loadData(cont)
        print('Videos cargados: ' + str(controller.videosSize(cont)))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")


    elif int(inputs[0]) == 3:
        label = input("Categoria a buscar: ")
        country = input("Pais a buscar: ")
        n = int(input("Ingrese el n: "))
        videos = controller.getVideosByCategory(cont, label,country, n)


    elif int(inputs[0]) == 4:
        label = input("Pais a buscar: ")
        f = controller.sacarmasrepetidocountry(cont,label)
        print(f)

    elif int(inputs[0]) == 5:
        label = input("Categoria a buscar: ")
        f = controller.sacarmasrepetidocategory(cont,label)
        print(f)

    elif int(inputs[0]) == 6:
        country = input("Pais a buscar: ")
        tag = input('Tag a buscar: ').lower()
        n = int(input("Ingrese el n: "))
        f = controller.req4(cont,tag,country,n)
        

    elif int(inputs[0]) == 0:
        menu = False


        
        
sys.exit(0)

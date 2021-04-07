"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
                'videos-id': None,
                'categories' : None,
               'category-id': None}
               

    catalog['videos'] = lt.newList('SINGLE_LINKED', compareVideoIds)
    catalog['videos-id'] = mp.newMap(10000,
                                maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapVideoIds)
    catalog['categories'] = mp.newMap(37,
                                     maptype='CHAINING',
                                   loadfactor=6.0 ,
                                   comparefunction=compareCategoriesNames)
    catalog['category-id'] = mp.newMap(37,
                                     maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCategoriesIds)
    
    return catalog  
    
# Funciones para creacion de datos
def newVideoCategory(name, id):
    category = {'name': '',
           'category_id': '',
           'total_videos': 0,
           'videos': None}
    category['name'] = name
    category['category_id'] = id
    category['videos'] = lt.newList()
    return category


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de autores, una referencia
    al libro.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    lt.addLast(catalog['videos'], video)
    mp.put(catalog['videos-id'], video['video_id'], video)
    
    

def addCategory(catalog, category):
    """
    Adiciona un category a la tabla de categorys dentro del catalogo y se
    actualiza el indice de identificadores del category.
    """
    
    newcategory = newVideoCategory(category['name'], category['id'])
    
    mp.put(catalog['categories'], category['name'], newcategory)
    mp.put(catalog['category-id'], category['id'], newcategory)

def addVideoCategory(catalog, category):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    videoid = category['video_id']
    categoryid = category['category_id']
    entry = mp.get(catalog['category-id'], categoryid)

    if entry:
        categoryvideo = mp.get(catalog['categories'], me.getValue(entry)['name'])
        #print(categoryvideo)
        categoryvideo['value']['total_videos'] += 1

        video = mp.get(catalog['videos-id'], videoid)
        if video:
            lt.addLast(categoryvideo['value']['videos'], video['value'])
# Funciones de consulta
def getVideosByCategory(catalog, categoryname,n):
    """
    Retornar la lista de libros asociados a un category
    """
    
    category = mp.get(catalog['categories'], categoryname)
    videos = None
    if category:
        videos = me.getValue(category)['videos']
    sorted_list=merge.sort(videos,cmpVideosByLikes)
    i =0
    for video in lt.iterator(sorted_list):
        if i == n:
            break

        print(video['title'])
        i +=1
       
# Funciones utilizadas para comparar elementos dentro de una lista


def cmpVideosIds(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareCategoriesNames(keyname, category):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    catentry = me.getKey(category)
    if (keyname == catentry):
        return 0
    elif (keyname > catentry):
        return 1
    else:
        return -1

def compareCategoriesIds(id, category):
    categoryentry = me.getKey(category)
    if (int(id) == int(categoryentry)):
        return 0
    elif (int(id) > int(categoryentry)):
        return 1
    else:
        return 0

def compareMapVideoIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareVideoIds(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

# Funciones de ordenamiento

def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])

def sortVideos(catalog):
           
    sorted_list=merge.sort(catalog,cmpVideosByLikes)

    return sorted_list

def cmpVideosByLikes(video1,video2):
    comparison=float(video2['likes'])<float(video1['likes'])
    return comparison
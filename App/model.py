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
import tracemalloc
import time

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
               'category-id': None,
               'countries': None}
               

    catalog['videos'] = lt.newList('ARRAY_LIST', compareVideoIds)
    catalog['videos-id'] = mp.newMap(371299,
                                maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapVideoIds)
    catalog['categories'] = mp.newMap(37,
                                     maptype='CHAINING',
                                   loadfactor=4.0 ,
                                   comparefunction=compareCategoriesNames)
    catalog['category-id'] = mp.newMap(37,
                                     maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCategoriesIds)
    catalog['countries'] =mp.newMap(193,
                                     maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCountries)

    catalog['tags']=mp.newMap(809,
                            maptype='CHAINING',
                            loadfactor=4.0,
                            comparefunction=compareTags)
    
    return catalog  
    
# Funciones para creacion de datos
def newVideoCategory(name, id):
    category = {'name': '',
           'category_id': '',
           'total_videos': 0,
           'videos': None}
    category['name'] = name
    category['category_id'] = id
    category['videos'] = lt.newList('ARRAY_LIST')
    return category

def newVideoCountry(pais,video):
    country = {'country':'',
            'videos': None}
    country['country'] = pais
    country['videos'] = lt.newList('ARRAY_LIST')
    lt.addLast(country['videos'], video)
    return country
    
def newTag(tag,video):
    tag = {'tag':'',
            'videos': None}
    tag['tag'] = tag
    tag['videos'] = lt.newList('ARRAY_LIST')
    lt.addLast(tag)


# Funciones para agregar informacion al catalogo+

    
       
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
            lt.addLast(categoryvideo['value']['videos'], video['value']['title'])

def addVideostoCountry(catalog,pais,video):
    #if catalog['countries']['country'] == pais:
    #lt.addlast(catalog['countries']['country'])
    pass
    """
    if pais == video['country']:
        x = mp.get(catalog['countries'], pais)["videos"]
        print('pruebaaaaaaaaaaa')
        lt.addLast(x,video)"""
    

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
    
    
def addTag(catalog,tag,video):
    tags =  catalog['tags']
    verificador = mp.contains(tags,tag)

    if verificador:
        entrada = mp.get(tags,tag)
        x = me.getValue(entrada)
        lt.addLast(x['videos'],video['title'])
    
    else:
        x = newVideoCountry(tags,video['title'])
        mp.put(tags, tag, x)

def addCountry(catalog,pais,video):
    """
    nuevopais = newVideoCountry(pais)
    mp.put(catalog['countries'],pais,nuevopais)
    """

    paises = catalog['countries']
    verificador = mp.contains(paises,pais)

    if verificador:
        entrada = mp.get(paises, pais)
        x = me.getValue(entrada)
        lt.addLast(x['videos'],video['title'])


    else:

        x = newVideoCountry(pais,video['title'])
        mp.put(paises, pais, x)
        
    


def addCategory(catalog, category):
    """
    Adiciona un category a la tabla de categorys dentro del catalogo y se
    actualiza el indice de identificadores del category.
    """
    newcategory = newVideoCategory(category['name'], category['id'])
    mp.put(catalog['categories'], category['name'], newcategory)
    mp.put(catalog['category-id'], category['id'], newcategory)

# Funciones de consulta
def getVideosByCategory(catalog, categoryname,country,n):
    """
    Retornar la lista de libros asociados a un category
    """
    #CON ESTE CODIGO SE HACE LO MISMO PERO USANDO MERGE SORT y sin country (lab)
    '''
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
    '''

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()


    lista = mp.get(catalog['categories'],categoryname)['value']['videos']['elements']
    todoslosvideos = catalog['videos']
    size = lt.size(todoslosvideos)
    dicpaislikes = dict()
    for i in range(size):
        element = lt.getElement(todoslosvideos,i)
        if element['title'] in lista:
            if element['country'] == country:
                dicpaislikes[element["title"]]=element["views"]
    
    contador = 0
    listafinal = []
    #maximo=max(dicpaislikes, key=dicpaislikes.get)
    


    while contador < n:
        
        values=list(dicpaislikes.values()) 
        v=[]
        for i in values:
            v.append(int(i))
    
        k=list(dicpaislikes.keys()) 
        maximo =  k[v.index(max(v))]

    
        

        
        listafinal.append(maximo)
        
        
        
        dicpaislikes.pop(maximo)
        contador += 1
    
    for titulo in listafinal:
        for i in range(size):
            element = lt.getElement(todoslosvideos,i)
            if element['title'] == titulo:
                print('♥   ♠  ♣  ♦')
                print('Title: ')
                print(element['title'])
                print('-')
                print('Channel title: ')
                print(element['channel_title'])
                print('-')
                print('Publish time: ')
                print(element['publish_time'])
                print('-')
                print('views: ')
                print(element['views'])
                print('-')
                print('likes: ')
                print(element['likes'])
                print('-')
                print('dislikes: ')
                print(element['dislikes'])
                print('-')
                print('tags: ')
                print(element['tags'])
                print('♥   ♠  ♣  ♦')

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('tiempo' , delta_time , '|| memoria' , delta_memory)

       
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

def compareCountries(keyname, country):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    catentry = me.getKey(country)
    if (keyname == catentry):
        return 0
    elif (keyname > catentry):
        return 1
    else:
        return -1

def compareTags(keyname, tag):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    catentry = me.getKey(tag)
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


def sacarmasrepetidocountry(catalog,pais):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    lista = mp.get(catalog['countries'],pais)['value']['videos']['elements']
    
    resultado = {i:lista.count(i) for i in lista}
    maximo=max(resultado, key=resultado.get)
    todoslosvideos = catalog['videos']
    size = lt.size(todoslosvideos)
    for i in range(size):
        element = lt.getElement(todoslosvideos,i)
        if element['title'] == maximo:
            titulo =  element['title']
            canal =  element['channel_title']
            pais =  element['country']
            numero = resultado[maximo]

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    print('tiempo' , delta_time , '|| memoria' , delta_memory)

    return(titulo +'\n'+ canal+'\n'+ pais+'\n'+ str(numero))

def sacarmasrepetidocategory(catalog,category):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    lista = mp.get(catalog['categories'],category)['value']['videos']['elements']
    resultado = {i:lista.count(i) for i in lista}
    maximo=max(resultado, key=resultado.get)
    todoslosvideos = catalog['videos']
    size = lt.size(todoslosvideos)
    for i in range(size):
        element = lt.getElement(todoslosvideos,i)
        if element['title'] == maximo:
            titulo =  element['title']
            canal =  element['channel_title']
            pais =  element['country']
            numero = resultado[maximo]


    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    print('tiempo' , delta_time , '|| memoria' , delta_memory)

    return(titulo +'\n'+ canal+'\n'+ pais+'\n'+ str(numero))

def req4(catalog,tag,country,n):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()


    lista = mp.get(catalog['tags'],tag)['value']['videos']['elements']
    
    todoslosvideos = catalog['videos']
    size = lt.size(todoslosvideos)
    dicpaislikes = dict()
    diccionpabuscar = dict()
    
    for i in range(size):
        element = lt.getElement(todoslosvideos,i)
        if element['title'] in lista and element['country'] == country:
            if element['title'] in dicpaislikes:
                if element['likes']>dicpaislikes[element['title']]:
                    dicpaislikes[element["title"]]=element["likes"]
                    diccionpabuscar[element["title"]]=[element["likes"],element['channel_title'],element['publish_time'],element['views'],element['likes'],element['dislikes'],element['tags']]
            else:
                dicpaislikes[element["title"]]=element["likes"]
                diccionpabuscar[element["title"]]=[element["likes"],element['channel_title'],element['publish_time'],element['views'],element['likes'],element['dislikes'],element['tags']]
    
    contador = 0
    listafinal = []
    
    
    while contador < n:
        
        values=list(dicpaislikes.values()) 
        v=[]
        for i in values:
            v.append(int(i))
    
        k=list(dicpaislikes.keys()) 
        maximo = k[v.index(max(v))]
        
        listafinal.append(maximo)
        
        
        dicpaislikes.pop(maximo)
        contador += 1

    

    for i in listafinal:
        print(i,diccionpabuscar[i][0],diccionpabuscar[i][1],diccionpabuscar[i][2],diccionpabuscar[i][3],diccionpabuscar[i][4],diccionpabuscar[i][5],diccionpabuscar[i][6])
        print("\n")
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    print('tiempo' , delta_time , '|| memoria' , delta_memory)


    '''
    for titulo in listafinal:
        for i in range(size):
            element = lt.getElement(todoslosvideos,i)
            if element['title'] == titulo:
                print('♥   ♠  ♣  ♦')
                print('Title: ')
                print(element['title'])
                print('-')
                print('Channel title: ')
                print(element['channel_title'])
                print('-')
                print('Publish time: ')
                print(element['publish_time'])
                print('-')
                print('views: ')
                print(element['views'])
                print('-')
                print('likes: ')
                print(element['likes'])
                print('-')
                print('dislikes: ')
                print(element['dislikes'])
                print('-')
                print('tags: ')
                print(element['tags'])
                print('♥   ♠  ♣  ♦')
'''
    





def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadVideos(catalog)
    loadCategories(catalog)
    loadVideosCategories(catalog)


def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    videosfile = cf.data_dir + 'videos-small.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    

    for video in input_file:
        
        

        model.addVideo(catalog, video)
        


def loadCategories(catalog):
    """
    Carga todos los categories del archivo e indica al modelo
    que los adicione al catalogo
    """

    categoriesfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(categoriesfile, encoding='utf-8'),delimiter='\t')
    
    for category in input_file:
        category['name'] = category['name'].strip()
        
        model.addCategory(catalog, category)


def loadVideosCategories(catalog):
    """
    Carga la información que asocia categories con libros en el catalogo
    """
    videocategoriesfile = cf.data_dir + 'videos-small.csv'
    input_file = csv.DictReader(open(videocategoriesfile, encoding='utf-8'))
    
    for videocategory in input_file:
        
        
        model.addVideoCategory(catalog, videocategory)
        

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def videosSize(catalog):
    """
    Numero de libros cargados al catalogo
    """
    return model.videosSize(catalog)

def getVideosByCategory(catalog, tagname,n):
    """
    Retorna los libros que han sido marcados con
    una etiqueta
    """
    videos = model.getVideosByCategory(catalog, tagname,n)
    return videos
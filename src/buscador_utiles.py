from collections import Counter, defaultdict

# Conjunto con palabras huecas (se ignoran en las búsquedas, no se indexan)
STOP_WORDS = {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o'}

# Caracteres de puntuación
PUNTUACION = '!¡"#$%&\'()*+,-./:;<=>?¿@[\\]^_`{|}~'

def normalizar_texto(texto: str) -> list[str]:
    """
    Recibe un texto, lo limpia y devuelve una lista de palabras. En el proceso de limpieza, 
    la función:
    1. Convierte el texto a minúsculas.
    2. Quita los signos de puntuación (los caracteres contenidos en PUNTUACION).
    3.Filtra las palabras huecas (las palabras contenidas en STOP_WORDS).
    
    Ejemplo: normalizar_texto("¡Hola, Mundo!") debería devolver ['hola', 'mundo']

    Parámetros:
    texto (str): El texto a normalizar.
    
    Devuelve:
    list[str]: Una lista de palabras normalizadas.
    """    
    #TODO: Ejercicio 1
    
    text_min = texto.lower()

    lista = []
    text_sin_sig = ""
    for c in text_min:
        if c not in PUNTUACION and c.isalpha():
            text_sin_sig += c
        else:
            text_sin_sig += " "
    text_sin_sig = text_sin_sig.strip()

    word = ""
    for s in text_sin_sig:
        if s == " ":
            lista.append(word)
            word = ""
        else:
            word += s
    lista.append(word)

    res = []
    for elementos in lista:
        if elementos not in STOP_WORDS:
            res.append(elementos)
    return res



    


def procesar_url_en_indice(url: str, texto: str, indice: dict[str, set[str]]):
    """
    Recibe la URL, el texto ya extraído de esa URL y un diccionario que indexa
    URLs de páginas web usando las palabras contenidas en la web como clave.
    La función actualiza el diccionario para incluir la URL en los conjuntos asociados
    a las palabras que aparecen en el texto.
    
    Parámetros:
    url (str): La URL de la página web.
    texto (str): El texto extraído de la página web.
    indice (dict[str, set[str]]): El índice de búsqueda a actualizar.
    """
    # TODO: Ejercicio 2
    
    nor = normalizar_texto(texto)

    for palabra in nor:
        if palabra not in indice:
            indice[palabra] = set()
        indice[palabra].add(url)



        


def buscar_palabra_simple(palabra: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una única palabra de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encontró esa palabra.
    Si la palabra no está en el índice, debe devolver un conjunto vacío.
    Antes de buscarla, la palabra será normalizada.

    Parámetros:
    palabra (str): La palabra a buscar.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontró la palabra.
    """    
    # TODO: Ejercicio 3

    norm = normalizar_texto(palabra) #norm[0] habrá que utilizar

    palabra_busqueda = norm[0]
    res = set()

    res = indice.get(palabra_busqueda, set())
    return res

def buscar_palabras_or(frase: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una frase de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encuentren alguna de las palabras de la frase.
    Si ninguna de las palabras están en el índice, debe devolver un conjunto vacío.
    La función normalizará el texto de la frase antes de buscar.

    Parámetros:
    frase (str): La frase de búsqueda.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontraron todas las palabras.
    """    
    # TODO: Ejercicio 4
    
    frase_normalizada = normalizar_texto(frase)
    res = set()

    for palabras in frase_normalizada:
        urls_de_palabras = buscar_palabra_simple(palabras, indice)
        res = res.union(urls_de_palabras)

    return res


def buscar_palabras_and(frase: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una frase de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encuentren todas las palabras de la frase.
    Si ninguna de las palabras están en el índice, debe devolver un conjunto vacío.
    La función normalizará el texto de la frase antes de buscar.

    Parámetros:
    frase (str): La frase de búsqueda.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontraron todas las palabras.
    """
    # TODO: Ejercicio 5
    frase_normalizada = normalizar_texto(frase)

    if frase_normalizada[0] == "":
        return set()
    
    res = set(buscar_palabra_simple(frase_normalizada[0], indice))

    for palabras in frase_normalizada[1:]:
        palabra_actual = buscar_palabra_simple(palabras, indice)
        res = res.intersection(palabra_actual)

    return res


def procesar_url_en_indice_top_n(url: str, texto: str, indice: dict[str, set[str]], top_n: int=1000):
    """
    Recibe la URL, el texto ya extraído de esa URL y un diccionario que indexa
    URLs de páginas web usando las palabras contenidas en la web como clave.
    La función actualiza el diccionario para incluir la URL en los conjuntos asociados
    a las 'top_n' palabras más frecuentes de entre las que aparecen en el texto.

    Parámetros:
    url (str): La URL de la página web.
    texto (str): El texto extraído de la página web.
    indice (dict[str, set[str]]): El índice de búsqueda a actualizar.
    top_n (int): Número de palabras más frecuentes a indexar.
    """
    # TODO: Ejercicio 6
    
    texto_normalizado = normalizar_texto(texto)

    recuentos = Counter(texto_normalizado)
    mayores = recuentos.most_common(top_n)

    for i in range(len(mayores)):
        if mayores[i][0] not in indice:
            indice[mayores[i][0]] = set()
        indice[mayores[i][0]].add(url)
    


def calcula_estadisticas_indice(indice: dict[str, set[str]]) -> tuple[int, int, float]:
    """
    Recibe un índice y calcula estadísticas sobre él.

    Parámetros:
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    tuple[int, int, float]: Una tupla con tres valores:
        - Número total de palabras indexadas.
        - Número total de URLs indexadas (sin duplicados).
        - Promedio de URLs por palabra: cuántas URLs hay indexadas para cada palabra, en promedio.
    """
    # TODO: Ejercicio 7
    num_urls_unicas = set()

    num_palabras = len(indice.keys())

    num_total_urls = 0


    for url in indice.values():
        num_urls_unicas = num_urls_unicas.union(url)
        num_total_urls += len(url)

    num = len(num_urls_unicas)    

    promedio = (num_total_urls / num_palabras)



    return (num_palabras, num, promedio)    

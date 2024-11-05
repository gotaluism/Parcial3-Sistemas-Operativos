import os
import heapq
from collections import defaultdict

def crear_carpeta(ruta):
    if not os.path.exists(ruta):
        print(f"Creando la carpeta '{ruta}'...")
        os.makedirs(ruta)
    else:
        print(f"La carpeta '{ruta}' ya existe.")

# Implementación del algoritmo de Huffman
class Nodo:
    def __init__(self, simbolo, frecuencia):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def calcular_frecuencias(datos):
    frecuencias = defaultdict(int)
    print("\nCalculando frecuencias de los bytes...")
    for byte in datos:
        frecuencias[byte] += 1
    for simbolo, frecuencia in frecuencias.items():
        print(f"Byte: {simbolo} Frecuencia: {frecuencia}")
    return frecuencias

def construir_arbol(frecuencias):
    print("\nConstruyendo el árbol de Huffman...")
    heap = [Nodo(simbolo, frecuencia) for simbolo, frecuencia in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        nodo_izq = heapq.heappop(heap)
        nodo_der = heapq.heappop(heap)
        nuevo_nodo = Nodo(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nuevo_nodo.izquierda = nodo_izq
        nuevo_nodo.derecha = nodo_der
        heapq.heappush(heap, nuevo_nodo)
        print(f"Unidos nodos con frecuencias {nodo_izq.frecuencia} y {nodo_der.frecuencia}")

    return heap[0] if heap else None

def construir_codigos(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return

    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = codigo_actual
        print(f"Byte: {nodo.simbolo} Código: {codigo_actual}")
        return

    construir_codigos(nodo.izquierda, codigo_actual + "0", codigos)
    construir_codigos(nodo.derecha, codigo_actual + "1", codigos)

def comprimir(datos):
    frecuencias = calcular_frecuencias(datos)
    arbol = construir_arbol(frecuencias)
    codigos = {}
    print("\nConstruyendo códigos de Huffman...")
    construir_codigos(arbol, "", codigos)

    print("\nCodificando los datos...")
    cadena_codificada = ""
    for byte in datos:
        cadena_codificada += codigos[byte]
        print(f"Byte: {byte} Código: {codigos[byte]}")

    # Añadir padding para que la longitud sea múltiplo de 8
    extra_padding = 8 - len(cadena_codificada) % 8
    for i in range(extra_padding):
        cadena_codificada += "0"

    padded_info = "{0:08b}".format(extra_padding)
    cadena_codificada = padded_info + cadena_codificada

    # Convertir la cadena binaria a bytes
    datos_comprimidos = bytearray()
    for i in range(0, len(cadena_codificada), 8):
        byte = cadena_codificada[i:i+8]
        datos_comprimidos.append(int(byte, 2))

    return datos_comprimidos, codigos

def descomprimir(datos_comprimidos, codigos):
    print("\nDescomprimiendo los datos...")
    cadena_binaria = ""
    for byte in datos_comprimidos:
        cadena_binaria += "{0:08b}".format(byte)

    # Extraer padding
    extra_padding = int(cadena_binaria[:8], 2)
    cadena_binaria = cadena_binaria[8:]
    cadena_binaria = cadena_binaria[:-extra_padding]

    # Invertir los códigos
    codigos_invertidos = {v: k for k, v in codigos.items()}

    datos_descomprimidos = bytearray()
    codigo_actual = ""
    for bit in cadena_binaria:
        codigo_actual += bit
        if codigo_actual in codigos_invertidos:
            datos_descomprimidos.append(codigos_invertidos[codigo_actual])
            print(f"Código: {codigo_actual} Byte: {codigos_invertidos[codigo_actual]}")
            codigo_actual = ""

    return datos_descomprimidos

# Funciones de cifrado César
def cifrar(datos, desplazamiento):
    datos_cifrados = bytearray()
    print("\n--- Iniciando el proceso de cifrado ---")
    for i, byte in enumerate(datos):
        byte_cifrado = (byte + desplazamiento) % 256
        datos_cifrados.append(byte_cifrado)
        # Imprimir cada paso del cifrado
        print(f"Paso {i+1}: Byte original {byte} + desplazamiento {desplazamiento} -> Byte cifrado {byte_cifrado}")
    print("--- Fin del proceso de cifrado ---\n")
    return datos_cifrados

def descifrar(datos, desplazamiento):
    datos_descifrados = bytearray()
    print("\n--- Iniciando el proceso de descifrado ---")
    for i, byte in enumerate(datos):
        byte_descifrado = (byte - desplazamiento) % 256
        datos_descifrados.append(byte_descifrado)
        # Imprimir cada paso del descifrado
        print(f"Paso {i+1}: Byte cifrado {byte} - desplazamiento {desplazamiento} -> Byte descifrado {byte_descifrado}")
    print("--- Fin del proceso de descifrado ---\n")
    return datos_descifrados

def cargar_codigos(nombre_archivo_codigos):
    codigos = {}
    with open(nombre_archivo_codigos, 'r') as f:
        for linea in f:
            simbolo, codigo = linea.strip().split(':')
            codigos[int(simbolo)] = codigo
    return codigos

def procesar_archivo(ruta_archivo, operacion, desplazamiento=3):
    nombre_archivo = os.path.basename(ruta_archivo)
    carpeta_procesados = 'procesados'
    crear_carpeta(carpeta_procesados)

    if operacion == 'comprimir_cifrar':
        # Leer datos
        with open(ruta_archivo, 'rb') as f:
            datos = f.read()

        # Comprimir
        datos_comprimidos, codigos = comprimir(datos)
        nombre_comprimido = os.path.join(carpeta_procesados, f"comprimido_{nombre_archivo}")
        with open(nombre_comprimido, 'wb') as f:
            f.write(datos_comprimidos)
        print(f"\nArchivo comprimido guardado en '{nombre_comprimido}'.")

        # Guardar los códigos de Huffman
        nombre_codigos = os.path.join(carpeta_procesados, f"codigos_{nombre_archivo}.txt")
        with open(nombre_codigos, 'w') as f:
            for simbolo, codigo in codigos.items():
                f.write(f"{simbolo}:{codigo}\n")
        print(f"Códigos de Huffman guardados en '{nombre_codigos}'.")

        # Cifrar el archivo comprimido
        datos_cifrados = cifrar(datos_comprimidos, desplazamiento)
        nombre_cifrado = os.path.join(carpeta_procesados, f"comprimido_cifrado_{nombre_archivo}")
        with open(nombre_cifrado, 'wb') as f:
            f.write(datos_cifrados)
        print(f"Archivo comprimido y cifrado guardado en '{nombre_cifrado}'.")

    elif operacion == 'cifrar_comprimir':
        # Leer datos
        with open(ruta_archivo, 'rb') as f:
            datos = f.read()

        # Cifrar
        datos_cifrados = cifrar(datos, desplazamiento)
        nombre_cifrado = os.path.join(carpeta_procesados, f"cifrado_{nombre_archivo}")
        with open(nombre_cifrado, 'wb') as f:
            f.write(datos_cifrados)
        print(f"Archivo cifrado guardado en '{nombre_cifrado}'.")

        # Comprimir el archivo cifrado
        datos_comprimidos, codigos = comprimir(datos_cifrados)
        nombre_comprimido = os.path.join(carpeta_procesados, f"cifrado_comprimido_{nombre_archivo}")
        with open(nombre_comprimido, 'wb') as f:
            f.write(datos_comprimidos)
        print(f"Archivo cifrado y comprimido guardado en '{nombre_comprimido}'.")

        # Guardar los códigos de Huffman
        nombre_codigos = os.path.join(carpeta_procesados, f"codigos_cifrado_{nombre_archivo}.txt")
        with open(nombre_codigos, 'w') as f:
            for simbolo, codigo in codigos.items():
                f.write(f"{simbolo}:{codigo}\n")
        print(f"Códigos de Huffman guardados en '{nombre_codigos}'.")

    elif operacion == 'descomprimir_descifrar':
        # Leer datos comprimidos y cifrados
        with open(ruta_archivo, 'rb') as f:
            datos_cifrados = f.read()

        # Descifrar
        datos_descifrados = descifrar(datos_cifrados, desplazamiento)
        nombre_descifrado = os.path.join(carpeta_procesados, f"descifrado_{nombre_archivo}")
        with open(nombre_descifrado, 'wb') as f:
            f.write(datos_descifrados)
        print(f"Archivo descifrado guardado en '{nombre_descifrado}'.")

        # Cargar códigos de Huffman
        nombre_codigos = os.path.join(carpeta_procesados, f"codigos_{nombre_archivo.replace('comprimido_cifrado_', '')}.txt")
        if not os.path.isfile(nombre_codigos):
            print(f"No se encontraron los códigos de Huffman en '{nombre_codigos}'.")
            return
        codigos = cargar_codigos(nombre_codigos)

        # Descomprimir
        datos_descomprimidos = descomprimir(datos_descifrados, codigos)
        nombre_descomprimido = os.path.join(carpeta_procesados, f"descomprimido_{nombre_archivo}")
        with open(nombre_descomprimido, 'wb') as f:
            f.write(datos_descomprimidos)
        print(f"Archivo descomprimido guardado en '{nombre_descomprimido}'.")

    elif operacion == 'descifrar_descomprimir':
        # Leer datos cifrados y comprimidos
        with open(ruta_archivo, 'rb') as f:
            datos_cifrados = f.read()

        # Descifrar
        datos_descifrados = descifrar(datos_cifrados, desplazamiento)
        nombre_descifrado = os.path.join(carpeta_procesados, f"descifrado_{nombre_archivo}")
        with open(nombre_descifrado, 'wb') as f:
            f.write(datos_descifrados)
        print(f"Archivo descifrado guardado en '{nombre_descifrado}'.")

        # Cargar códigos de Huffman
        nombre_codigos = os.path.join(carpeta_procesados, f"codigos_cifrado_{nombre_archivo.replace('cifrado_comprimido_', '')}.txt")
        if not os.path.isfile(nombre_codigos):
            print(f"No se encontraron los códigos de Huffman en '{nombre_codigos}'.")
            return
        codigos = cargar_codigos(nombre_codigos)

        # Descomprimir
        datos_descomprimidos = descomprimir(datos_descifrados, codigos)
        nombre_descomprimido = os.path.join(carpeta_procesados, f"descifrado_descomprimido_{nombre_archivo}")
        with open(nombre_descomprimido, 'wb') as f:
            f.write(datos_descomprimidos)
        print(f"Archivo descifrado y descomprimido guardado en '{nombre_descomprimido}'.")

    elif operacion == 'solo_comprimir':
        # Leer datos
        with open(ruta_archivo, 'rb') as f:
            datos = f.read()

        # Comprimir
        datos_comprimidos, codigos = comprimir(datos)
        nombre_comprimido = os.path.join(carpeta_procesados, f"comprimido_{nombre_archivo}")
        with open(nombre_comprimido, 'wb') as f:
            f.write(datos_comprimidos)
        print(f"\nArchivo comprimido guardado en '{nombre_comprimido}'.")

        # Guardar los códigos de Huffman
        nombre_codigos = os.path.join(carpeta_procesados, f"codigos_{nombre_archivo}.txt")
        with open(nombre_codigos, 'w') as f:
            for simbolo, codigo in codigos.items():
                f.write(f"{simbolo}:{codigo}\n")
        print(f"Códigos de Huffman guardados en '{nombre_codigos}'.")

    elif operacion == 'solo_cifrar':
        # Leer datos
        with open(ruta_archivo, 'rb') as f:
            datos = f.read()

        # Cifrar
        datos_cifrados = cifrar(datos, desplazamiento)
        nombre_cifrado = os.path.join(carpeta_procesados, f"cifrado_{nombre_archivo}")
        with open(nombre_cifrado, 'wb') as f:
            f.write(datos_cifrados)
        print(f"Archivo cifrado guardado en '{nombre_cifrado}'.")

    elif operacion == 'solo_descifrar':
        # Leer datos cifrados
        with open(ruta_archivo, 'rb') as f:
            datos_cifrados = f.read()

        # Descifrar
        datos_descifrados = descifrar(datos_cifrados, desplazamiento)
        nombre_descifrado = os.path.join(carpeta_procesados, f"descifrado_{nombre_archivo}")
        with open(nombre_descifrado, 'wb') as f:
            f.write(datos_descifrados)
        print(f"Archivo descifrado guardado en '{nombre_descifrado}'.")

    elif operacion == 'solo_descomprimir':
        # Leer datos comprimidos
        with open(ruta_archivo, 'rb') as f:
            datos_comprimidos = f.read()

        # Cargar códigos de Huffman
        nombre_codigos = os.path.join(carpeta_procesados, f"codigos_{nombre_archivo.replace('comprimido_', '')}.txt")
        if not os.path.isfile(nombre_codigos):
            print(f"No se encontraron los códigos de Huffman en '{nombre_codigos}'.")
            return
        codigos = cargar_codigos(nombre_codigos)

        # Descomprimir
        datos_descomprimidos = descomprimir(datos_comprimidos, codigos)
        nombre_descomprimido = os.path.join(carpeta_procesados, f"descomprimido_{nombre_archivo}")
        with open(nombre_descomprimido, 'wb') as f:
            f.write(datos_descomprimidos)
        print(f"Archivo descomprimido guardado en '{nombre_descomprimido}'.")

def procesar_carpeta(ruta_carpeta, operacion, desplazamiento=3):
    for root, dirs, files in os.walk(ruta_carpeta):
        for file in files:
            ruta_archivo = os.path.join(root, file)
            print(f"\nProcesando archivo: {ruta_archivo}")
            procesar_archivo(ruta_archivo, operacion, desplazamiento)

def main():
    while True:
        print("\nMenú de opciones:")
        print("1. Comprimir y luego cifrar")
        print("2. Cifrar y luego comprimir")
        print("3. Descomprimir y luego descifrar")
        print("4. Descifrar y luego descomprimir")
        print("5. Solo comprimir")
        print("6. Solo descomprimir")
        print("7. Solo cifrar")
        print("8. Solo descifrar")
        print("9. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '9':
            print("Saliendo del programa...")
            break

        ruta = input("Ingresa el nombre del archivo o carpeta: ")

        if not os.path.exists(ruta):
            print(f"El archivo o carpeta '{ruta}' no existe.")
            continue

        if os.path.isfile(ruta):
            if opcion == '1':
                procesar_archivo(ruta, 'comprimir_cifrar')
            elif opcion == '2':
                procesar_archivo(ruta, 'cifrar_comprimir')
            elif opcion == '3':
                procesar_archivo(ruta, 'descomprimir_descifrar')
            elif opcion == '4':
                procesar_archivo(ruta, 'descifrar_descomprimir')
            elif opcion == '5':
                procesar_archivo(ruta, 'solo_comprimir')
            elif opcion == '6':
                procesar_archivo(ruta, 'solo_descomprimir')
            elif opcion == '7':
                procesar_archivo(ruta, 'solo_cifrar')
            elif opcion == '8':
                procesar_archivo(ruta, 'solo_descifrar')
            else:
                print("Opción no válida. Por favor, selecciona una opción del 1 al 9.")
        elif os.path.isdir(ruta):
            if opcion == '1':
                procesar_carpeta(ruta, 'comprimir_cifrar')
            elif opcion == '2':
                procesar_carpeta(ruta, 'cifrar_comprimir')
            elif opcion == '3':
                procesar_carpeta(ruta, 'descomprimir_descifrar')
            elif opcion == '4':
                procesar_carpeta(ruta, 'descifrar_descomprimir')
            elif opcion == '5':
                procesar_carpeta(ruta, 'solo_comprimir')
            elif opcion == '6':
                procesar_carpeta(ruta, 'solo_descomprimir')
            elif opcion == '7':
                procesar_carpeta(ruta, 'solo_cifrar')
            elif opcion == '8':
                procesar_carpeta(ruta, 'solo_descifrar')
            else:
                print("Opción no válida. Por favor, selecciona una opción del 1 al 9.")

if __name__ == "__main__":
    main()

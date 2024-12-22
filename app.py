# Lista para almacenar los productos
# Hola Soy Claudio Pesaresi#

##################################################################################################
# Importaciones
##################################################################################################
import os  # Liberria de funciones del sistema
import sqlite3 as sql  # Libreria de BAse de Datos
from colorama import init, Fore, Back  # Libreria de manejo de colores ed textos

##################################################################################################
# Declaracion de variables
##################################################################################################
productos = []
cont = ""
BaseDatos = "c:\datos\inventario.db"


##################################################################################################
# Declaracion de funciones
# Las funciones se definen antes de usarlas en el codigo.
##################################################################################################
def db_crear_tabla_productos():
    # Hay que agregar una mejora, el sisetma da error si no existe la carpeta de destino
    # de la base, hay que Verificar / Crear eso primero

    # despues si, crea la base y la tabla
    conexion = sql.connect(BaseDatos)  # conecta con base de datos
    cursor = conexion.cursor()  # crea cursor, cadena a ejecutar
    cursor.execute(
        """ 
            CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
            )
            """
    )
    conexion.commit()
    conexion.close()


def menu_registrar_producto():
    # Pantalla inicial para agregar un producto

    # Clearing the Screen
    os.system("cls")

    print(Fore.CYAN + "ALTA DE PRODUCTO" + Fore.WHITE)
    print("")

    # Pide los datos / Validando

    vl_nomPro = True  # identifica acceso OK
    while vl_nomPro:
        try:
            nomPro = input("Ingrese el nombre del producto: ").upper()
        except Exception:
            print(Fore.RED + "Error de ingreso de dato" + Fore.WHITE)
            vl_nomPro = True
        if len(nomPro) < 1:
            print(Fore.RED + "Debe ingresar un nombre" + Fore.WHITE)
            vl_nomPro = True
        elif len(nomPro) > 20:
            print(Fore.RED + "Maximo 20 caracteres" + Fore.WHITE)
            vl_nomPro = True
        elif buscar_producto(nomPro):  # Validar producto duplicado
            print(Fore.RED + "Producto existente" + Fore.WHITE)
            vl_nomPro = True
        else:
            vl_nomPro = False

    vl_desPro = True  # identifica acceso OK
    while vl_desPro:
        try:
            desPro = input("Ingrese descripcion del producto: ")
        except Exception:
            print(Fore.RED + "Error de ingreso de dato" + Fore.WHITE)
            vl_desPro = True
        if len(desPro) < 1:
            print(Fore.RED + "Debe ingresar una descripcion" + Fore.WHITE)
            vl_desPro = True
        elif len(desPro) > 80:
            print(Fore.RED + "Maximo 80 caracteres" + Fore.WHITE)
            vl_desPro = True
        else:
            vl_desPro = False

    vl_canPro = True  # identifica acceso OK
    while vl_canPro:
        try:
            canPro = int(input("Ingrese el stock deproducto : "))
            if canPro < 0:
                print(Fore.RED + "El stock debe ser cero o positivo" + Fore.WHITE)
                vl_canPro = True
            else:
                vl_canPro = False
        except Exception:
            print(Fore.RED + "Error, Ingrese un valor" + Fore.WHITE)
            vl_canPro = True

    vl_prePro = True  # identifica acceso OK
    while vl_prePro:
        try:
            prePro = float(input("Ingrese el precio del deproducto : "))
            if prePro < 0:
                print(Fore.RED + "El precio debe ser cero o positivo" + Fore.WHITE)
                vl_prePro = True
            else:
                vl_prePro = False
        except Exception:
            print(Fore.RED + "Error, Ingrese un valor" + Fore.WHITE)
            vl_prePro = True

    vl_catPro = True  # identifica acceso OK
    while vl_catPro:
        try:
            catPro = int(input("Ingrese la categoria - 1 a 4 - : "))
            if catPro < 1 or catPro > 4:
                print(Fore.RED + "Categoria de 1 a 4  / UNICAMENTE" + Fore.WHITE)
                vl_catPro = True
            else:
                vl_catPro = False
        except Exception:
            print(Fore.RED + "Error, Ingrese un valor" + Fore.WHITE)
            vl_catPro = True

    # Mostrar producto ingresado y confirmar si esta OK

    mostrar_producto(nomPro, desPro, canPro, prePro, catPro)

    vl_CNFPro = True  # identifica acceso OK
    while vl_CNFPro:
        try:
            CNFPro = input("Confirma carga de producto (S/N) ? ").upper()

        except Exception:
            vl_CNFPro = True
        if CNFPro == "S":

            # Si esta todo OK, los inserta en la base

            agregar_producto(nomPro, desPro, canPro, prePro, catPro)

            print(Fore.GREEN + "\nPRODUCTO REGISTRADO - OK" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_CNFPro = False
        elif CNFPro == "N":
            print(Fore.RED + "\nSALIENDO SIN GRABAR PRODUCTO" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_CNFPro = False
        else:
            vl_CNFPro = True


def mostrar_producto(nomPro, desPro, canPro, prePro, catPro):
    # Pantalla inicial para agregar un producto
    # Clearing the Screen
    os.system("cls")

    print("\nPRODUCTO")
    print("------------")

    print(f"\nNombre       {nomPro} ")
    print(f"Descripcion  {desPro} ")
    print(f"Cantidad     {canPro} ")
    print(f"Precio       {prePro} ")
    print(f"Categoria    {catPro} ")


def agregar_producto(nomPro, desPro, canPro, prePro, catPro):

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()
    instruccion = "INSERT INTO productos(nombre, descripcion, cantidad, precio, categoria ) VALUES( ?, ?, ?, ?, ? )"
    cursor.execute(instruccion, (nomPro, desPro, canPro, prePro, catPro))
    conexion.commit()
    conexion.close()


def actualizar_stock(nomPro, canPro):

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()
    instruccion = "UPDATE productos SET cantidad=? WHERE nombre=?"

    cursor.execute(instruccion, (canPro, nomPro))

    conexion.commit()
    conexion.close()

    # Comprobar si se actualizaron filas
    filas_afectadas = cursor.rowcount
    if filas_afectadas > 0:
        return True
    else:
        return False


def eliminar_producto(nomPro):

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()  # siempre igual

    instruccion = "DELETE FROM productos WHERE nombre = ? "
    placeholders = (nomPro,)

    cursor.execute(instruccion, placeholders)
    conexion.commit()
    conexion.close()

    # Comprobar si se actualizaron filas
    filas_afectadas = cursor.rowcount
    if filas_afectadas > 0:
        return True
    else:
        return False


def buscar_producto(nomPro):

    campo = "nombre"

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()

    instruccion = f"SELECT * FROM productos WHERE {campo} LIKE ? "
    cursor.execute(instruccion, (f"%{nomPro}%",))
    resultados = cursor.fetchall()

    conexion.commit()
    conexion.close()

    if not resultados:
        return False
        # No se encontraron productos
    else:
        return True
        # Producto encontrado


def presentar_producto(nomPro):

    campo = "nombre"

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()

    instruccion = f"SELECT * FROM productos WHERE {campo} LIKE ? "
    cursor.execute(instruccion, (f"%{nomPro}%",))
    resultados = cursor.fetchall()

    conexion.commit()
    conexion.close()

    if not resultados:
        return False
        # No se encontraron productos
    else:

        for i in resultados:
            id, nombre, descripcion, cantidad, precio, categoria = i

            # print(                 f""" {id} -//- {nombre} -//- {descripcion} -//- {cantidad} -//- {precio} -//- {categoria}  """             )

            print(f"Descripcion  {descripcion} ")
            print(f"Cantidad     {cantidad} ")
            print(f"Precio       {precio} ")
            print(f"Categoria    {categoria} ")

        return True
        # Producto encontrado


def menu_listar_productos():

    os.system("cls")

    print("\nINVENTARIO DE PRODUCTOS")
    print("--------------------------")

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()
    instruccion = f" SELECT * FROM productos"
    cursor.execute(instruccion)
    resultados = cursor.fetchall()
    conexion.commit()
    conexion.close()

    if not resultados:

        # Base de datos vacia

        print(Fore.RED + "\nSIN PRODUCTOS EN EL INVENTARIO" + Fore.WHITE)
        cont = input("\nCualquier tecla para continuar")

    else:

        print(
            f"""ID -//- Nombre -//- Descripcion -//- Cantidad -//- Precio -//- Categoria   """
        )

        for i in resultados:
            id, nombre, descripcion, cantidad, precio, categoria = i
            print(
                f""" {id} -//- {nombre} -//- {descripcion} -//- {cantidad} -//- {precio} -//- {categoria}  """
            )
        cont = input("\nCualquier tecla para continuar")


def listado_stock_minimo(canPro):

    conexion = sql.connect(BaseDatos)
    cursor = conexion.cursor()
    instruccion = f" SELECT * FROM productos WHERE cantidad <= ?"
    placeholders = (canPro,)

    cursor.execute(instruccion, placeholders)
    resultados = cursor.fetchall()
    conexion.commit()
    conexion.close()

    if not resultados:

        # Base de datos vacia

        print(Fore.RED + "\nSIN PRODUCTOS PARA LISTAR" + Fore.WHITE)
        cont = input("\nCualquier tecla para continuar")

    else:

        print(
            f"""ID -//- Nombre -//- Descripcion -//- Cantidad -//- Precio -//- Categoria   """
        )

        for i in resultados:
            id, nombre, descripcion, cantidad, precio, categoria = i
            print(
                f""" {id} -//- {nombre} -//- {descripcion} -//- {cantidad} -//- {precio} -//- {categoria}  """
            )
        cont = input("\nCualquier tecla para continuar")


def menu_actualizar_producto():
    # Actualizar Stock de producto

    vl_nomPro = True  # identifica acceso OK
    while vl_nomPro:
        try:
            os.system("cls")

            print("\nACTUALIZAR CANTIDAD DE PRODUCTOS")
            print("----------------------------------")

            nomPro = input("Ingrese el nombre del producto: ").upper()

        except Exception:
            print(Fore.RED + "Error de ingreso de dato" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = True
        if len(nomPro) < 1:
            # print(Fore.RED + "Debe ingresar un nombre" + Fore.WHITE)
            # cont = input("\nCualquier tecla para continuar")
            # vl_nomPro = True
            vl_nomPro = False
        elif len(nomPro) > 20:
            print(Fore.RED + "Maximo 20 caracteres" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = True
        elif buscar_producto(nomPro):  # Validar producto duplicado
            print(Fore.GREEN + "\nProducto EXISTENTE" + Fore.WHITE)

            presentar_producto(nomPro)

            vl_canPro = True  # identifica acceso OK
            while vl_canPro:
                try:
                    canPro = int(input("Ingrese NUEVO stock deproducto : "))
                    if canPro < 0:
                        print(
                            Fore.RED + "El stock debe ser cero o positivo" + Fore.WHITE
                        )
                        vl_canPro = True
                    else:

                        vl_CNFPro = True  # identifica acceso OK
                        while vl_CNFPro:
                            try:
                                CNFPro = input(
                                    "Confirma modificar stock (S/N) ? "
                                ).upper()

                            except Exception:
                                vl_CNFPro = True
                            if CNFPro == "S":

                                # Si esta todo OK, los inserta en la base

                                if actualizar_stock(nomPro, canPro):
                                    print(
                                        Fore.GREEN
                                        + "\nPRODUCTO ACTUALIZADO - OK"
                                        + Fore.WHITE
                                    )
                                else:
                                    print(
                                        Fore.RED
                                        + "\nERROR EN ACTUALIZCION DE DATOS"
                                        + Fore.WHITE
                                    )
                                vl_CNFPro = False
                            elif CNFPro == "N":
                                print(
                                    Fore.RED
                                    + "\nSALIENDO SIN ACTUALIZAR STOCK"
                                    + Fore.WHITE
                                )
                                vl_CNFPro = False
                            else:
                                vl_CNFPro = True
                        vl_canPro = False
                except Exception:
                    print(Fore.RED + "Error, Ingrese un valor" + Fore.WHITE)
                    vl_canPro = True

            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = False

        else:
            print(Fore.RED + "Producto INEXISTENTE" + Fore.WHITE)

            vl_CNFPro = True  # identifica acceso OK
            while vl_CNFPro:
                try:
                    CNFPro = input("Nueva busqueda de producto (S/N) ? ").upper()

                except Exception:

                    vl_CNFPro = True

                if CNFPro == "S":

                    vl_nomPro = True
                    vl_CNFPro = False

                elif CNFPro == "N":

                    vl_nomPro = False
                    vl_CNFPro = False

                else:

                    vl_CNFPro = True


def menu_eliminar_producto():
    # ELIMINAR un producto

    vl_nomPro = True  # identifica acceso OK
    while vl_nomPro:
        try:
            os.system("cls")

            print(Fore.RED + "\nELIMINAR UN PRODUCTO" + Fore.WHITE)
            print(Fore.RED + "-----------------------" + Fore.WHITE)

            nomPro = input("Ingrese el nombre del producto: ").upper()

        except Exception:
            print(Fore.RED + "Error de ingreso de dato" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = True
        if len(nomPro) < 1:
            # print(Fore.RED + "Debe ingresar un nombre" + Fore.WHITE)
            # cont = input("\nCualquier tecla para continuar")
            # vl_nomPro = True
            vl_nomPro = False
        elif len(nomPro) > 20:
            print(Fore.RED + "Maximo 20 caracteres" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = True
        elif buscar_producto(nomPro):  # Validar producto duplicado
            print(Fore.GREEN + "\nProducto EXISTENTE" + Fore.WHITE)

            presentar_producto(nomPro)

            vl_CNFPro = True  # identifica acceso OK
            while vl_CNFPro:
                try:
                    CNFPro = input(
                        Fore.RED + "Confirma ELIMINAR PRODUCTO (S/N) ? " + Fore.WHITE
                    ).upper()

                except Exception:
                    vl_CNFPro = True
                if CNFPro == "S":

                    # Si esta todo OK, ELIMINO PRODUCTO

                    if eliminar_producto(nomPro):
                        print(Fore.GREEN + "\nPRODUCTO ELIMINADO - OK" + Fore.WHITE)
                    else:
                        print(
                            Fore.RED + "\nERROR EN ACTUALIZCION DE DATOS" + Fore.WHITE
                        )
                    vl_CNFPro = False
                elif CNFPro == "N":
                    print(Fore.RED + "\nSALIENDO SIN ACTUALIZAR PRODUCTO" + Fore.WHITE)
                    vl_CNFPro = False
                else:
                    vl_CNFPro = True
                vl_nomPro = False

        else:
            print(Fore.RED + "Producto INEXISTENTE" + Fore.WHITE)

            vl_CNFPro = True  # identifica acceso OK
            while vl_CNFPro:
                try:
                    CNFPro = input("Nueva busqueda de producto (S/N) ? ").upper()

                except Exception:

                    vl_CNFPro = True

                if CNFPro == "S":

                    vl_nomPro = True
                    vl_CNFPro = False

                elif CNFPro == "N":

                    vl_nomPro = False
                    vl_CNFPro = False

                else:

                    vl_CNFPro = True


def menu_buscar_producto():
    # Buscar un producto por nombre

    vl_nomPro = True  # identifica acceso OK
    while vl_nomPro:
        try:
            os.system("cls")

            print("\nBUSCAR UN PRODUCTO")
            print("----------------------")

            nomPro = input("Ingrese el nombre del producto: ").upper()

        except Exception:
            print(Fore.RED + "Error de ingreso de dato" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = True
        if len(nomPro) < 1:
            # print(Fore.RED + "Debe ingresar un nombre" + Fore.WHITE)
            # cont = input("\nCualquier tecla para continuar")
            # vl_nomPro = True
            vl_nomPro = False
        elif len(nomPro) > 20:
            print(Fore.RED + "Maximo 20 caracteres" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            vl_nomPro = True
        elif buscar_producto(nomPro):  # Validar producto duplicado
            print(Fore.GREEN + "\nProducto EXISTENTE" + Fore.WHITE)

            presentar_producto(nomPro)

            vl_CNFPro = True  # identifica acceso OK
            while vl_CNFPro:
                try:
                    CNFPro = input("Nueva busqueda de producto (S/N) ? ").upper()
                except Exception:
                    vl_CNFPro = True
                if CNFPro == "S":
                    vl_nomPro = True
                    vl_CNFPro = False
                elif CNFPro == "N":
                    vl_nomPro = False
                    vl_CNFPro = False
                else:
                    vl_CNFPro = True

        else:
            print(Fore.RED + "Producto INEXISTENTE" + Fore.WHITE)

            vl_CNFPro = True  # identifica acceso OK
            while vl_CNFPro:
                try:
                    CNFPro = input("Nueva busqueda de producto (S/N) ? ").upper()
                except Exception:
                    vl_CNFPro = True
                if CNFPro == "S":
                    vl_nomPro = True
                    vl_CNFPro = False
                elif CNFPro == "N":
                    vl_nomPro = False
                    vl_CNFPro = False
                else:
                    vl_CNFPro = True


def menu_reporte_bajo_stock():
    # Listado de productos de bajo stock

    os.system("cls")

    print("\nLISTADO DE PRODUCTOS DE BAJO STOCK")
    print("-------------------------------------")

    vl_canPro = True  # identifica acceso OK
    while vl_canPro:
        try:
            canPro = int(input("Ingrese el stock minimo "))
            if canPro < 0:
                # print(Fore.RED + "El stock debe ser cero o positivo" + Fore.WHITE)
                vl_canPro = False
            else:

                listado_stock_minimo(canPro)

                vl_canPro = False

        except Exception:
            print(Fore.RED + "Error, Ingrese un valor" + Fore.WHITE)
            vl_canPro = True


##################################################################################################
# MENU
##################################################################################################


# Función principal para el sistema de inventario (NO ELIMINAR)
def main():
    # AQUÍ PUEDES COMENZAR A DESARROLLAR LA SOLUCIÓN

    # Controlo que exista la tabla, sino la creo
    db_crear_tabla_productos()

    # Menu de la aplicacion
    while True:

        # Clearing the Screen
        os.system("cls")

        print(Fore.BLUE + "SISTEMA DE MANEJO DE INVENTARIO" + Fore.WHITE)
        print("")

        print("Opcion 1 - Registrar Producto")
        print("Opcion 2 - Mostrar Productos")
        print("Opcion 3 - Actualizar Stock de Producto")
        print("Opcion 4 - Eliminar Producto")
        print("Opcion 5 - Buscar Producto")
        print("Opcion 6 - Reporte Bajo Stock")
        print("Opcion 7 - Salir")

        # option = input("\nIngrese su opcion ==> ")
        try:
            option = int(input("\nIngrese su opcion ==> "))
        except Exception as error:
            print(
                Fore.RED
                + "Opción inválida. Debe ingresar un número entero."
                + Fore.WHITE
            )
            cont = input("\nCualquier tecla para continuar")
            continue  # Continuamos el bucle si no es un número válido

        if option == 7:
            # Salir
            print(Fore.GREEN + f"\nHasta la vista !!!!" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")
            os.system("cls")
            break

        elif option == 1:
            # Agregar
            menu_registrar_producto()  # Funcionando

        elif option == 2:
            # Listar
            menu_listar_productos()  # Funcionando

        elif option == 3:
            # Listar
            menu_actualizar_producto()  # Funcionando

        elif option == 4:
            # Listar
            menu_eliminar_producto()  # Funcionando

        elif option == 5:
            # Listar
            menu_buscar_producto()

        elif option == 6:
            # Listar
            menu_reporte_bajo_stock()

        else:
            # Ingreso incorrecto
            print(Fore.RED + f"\nIngreso incorrecto - Reintentar" + Fore.WHITE)
            cont = input("\nCualquier tecla para continuar")


# Ejecución de la función main() - (NO ELIMINAR) - Inicia ejecucion Aqui
if __name__ == "__main__":
    main()

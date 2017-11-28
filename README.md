# ExamenParcial-Paradigmas-EDD

PharmaDino
==========

INTRODUCCIÓN:
-------------

El presente es un sistema destinado a poder visualizar la base de datos de la empresa **“PharmaDino”**. En la cual se podrá realizar consultas como: Buscar Clientes por nombres, Buscar Productos por su nombre, Buscar la Cantidad de Stock que se compro y Precios por unidad. A su vez, la el acceso a este sistema está limitado a un proceso de registración y loggeo.


FLUJO DEL PROGRAMA:
-------------------
En primera instancia el programa cuando el usuario esta "logeado" da una visualización principal de las noticias de la organización, en este caso son descuentos a afiliados/obras sociales. En el menú en el estado de "no logeado" podremos visualizar las solapas “Bienvenido” , “Login” y “Registrarse”. Una vez ingresado al sistema (mediante el LOGIN) este menú principal se desplegará y dejara ver lo siguiente: Base de Datos, Busqueda por Cliente, Busqueda por Producto, Busqueda por Cantidad y Busqueda por Precio. Cada una de estas secciones permitirá realizar las correspondientes consultas, que son: Filtrar por nombre de cliente, filtrar por nombre del producto, filtrar por precio o filtrar por cantidad de stock comprado.

ESTRUCTURA:
-----------
El programa consta de un archivo app.py el cual se encarga de importar modulos, definir rutas de flujo, vinculación con los templates y levantar el localhost. Posee, además, partes lógicas: de validación y procesos. 
Por otro lado tenemos el archivo formularios.py, este consta en su totalidad de clases que serán utilizadas para validar campos y obtener parámetros.
Para la base de datos y el registro de usuarios se utilizaron archivos csv. Estos son leídos mediante la utilización del lenguaje de programación Python3. Este lenguaje está presente en los dos archivos “.py”.
Otro elemento importante en el proceso de creación de este sistema de información, es la utilización de módulos y repositorios que ayudaron a la presentación visual de la información.
Siempre buscamos el checkeo del estado actual el usuario a la hora de movilizarse por el entorno. Esto de puede ver en cada uno de los @app.route con el **“username=session.get “**.
Siempre buscamos el encapsulamiento de errores para no tener altibajos en la utilización de la aplicación.

UTILIZACION EL PROGRAMA:
------------------------
El operador deberá validar la credencial de identidad para acceder a la informacion a la base de datos. Si el mismo no posee usuario de ingreso, podrá adquirir uno mediante el registro. Esto podrá realizarlo en el menu “Registrarse” que se encuentra en la parte superior del sistema. Una vez validado su ingreso (esto sera en el menu “Login”) podrá acceder a la Base de datos y a los sectores de consulta. Los sectores visibles a partir de su validacion de ingreso son:
+ **Base de Datos:** En donde se encuentra la información. Esta está representada mediante una tabla.
+ **Busqueda por Cliente:** Aca se podra hacer la filtracion de informacion en base al nombre del cliente.
+ **Busqueda por Producto:** La filtración se realizará en base al nombre del producto.
+ **Busqueda por Cantidad:** Se lista por la cantidad de productos comprados.
+ **Busqueda por Precio:** Se listará la información según el precio a buscar.
+ **Desloguear:** Este botón realizará del LogOut del usuario de forma inmediata.
Si los campos ingresados a la hora de realizar las filtraciones/consultas son inválidos, se mostrará un pequeño mensaje en rojo. Anunciando cuáles son los requerimientos mínimos para poder obtener un resultado efectivo.

CLASES UTILIZADAS:
------------------
Estos se encuentran en el archivo formularios.py, son utilizadas a la hora de requerir información al operador del programa. Del tipo formulario estas son manejadas gracias al FlaskForm.
Hemos diseñado las siguientes clases:
+SearchCliente 
+SearchProd 
Poseen validators como lo son el largo de caracteres requerido (minimo y maximo).
+SearchCant 
+SearchPrecio
Además de poseer validators decidimos poner la restricción de expresiones regulares __(Regexp)__.
Para la validación de usuarios con la clase **Checkeo_Log** y la creación de nuevos Usuarios como lo es la clase **CreaUsuario**. 
Todas poseen el DataRequired para solicitar si o si valores en esos campos y también destacamos el EqualTo a la hora de comparar contraseñas para la creación de nuevas credenciales de acesso. Todas estas propias de “wtforms.validators”.

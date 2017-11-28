#!/usr/bin/env python
import csv
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from formularios import SearchCliente,SearchProd,SearchCant,SearchPrecio, Checkeo_Log,CreaUsuario
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

#Se crea una lista donde se van a guardar los datos de loggeo del usuario.
#Se detectan los errores que pueden ocurrir si no se detectan los archivos csv.
users_check = []
try:
    with open('usuariosbase.csv') as archivo:
        leer_csv = csv.reader(archivo)
        for linea in leer_csv:
            users_check.append(linea[0])
except FileNotFoundError:
    print('Error de csv  de usuariosbase')

try:
    with open('basededatos.csv') as archivo:
        pass
except FileNotFoundError:
    print('Error al buscar el csv de base de datos')

#La pagina se pensó para que muestre el menú y el contenido del mismo cuando la persona se loggea
@app.route('/')
def index():
    if 'InicioSesion' in session:
        return render_template('index.html', username=session.get('InicioSesion'))
    return render_template('sign_off.html')

#Función de loggin
@app.route('/login', methods=['GET', 'POST'])
def login():
    fomu_log= Checkeo_Log()

    if fomu_log.validate_on_submit():
        try:
            with open('usuariosbase.csv') as archivo:
                #El try es para que  si se ingresa un unico campo lo capture en el IndexError
                try:
                    filecsv = csv.reader(archivo)
                    for linea in filecsv:
                        ubicacion = linea
                        nombre = ubicacion[0]
                        contrasenia = ubicacion[1]
                        if fomu_log.name.data == nombre and fomu_log.password.data == contrasenia:
                            session['InicioSesion'] = fomu_log.name.data
                            #El return renderiza en index.html con la sesion iniciada (poder ver el menu).
                            return render_template('index.html', username=session.get('InicioSesion'))
                except IndexError:
                    return 'usuario de usuariosbase.csv invalido'        
        except FileNotFoundError:
            return 'No se encuentra el archivo de usuariosbase'
    return render_template('login.html', form=fomu_log, username=session.get('InicioSesion'))

#Se crea la base de datos para que solo sea visible una vez que se loggea.
@app.route('/basededatos', methods=['GET', 'POST'])
def basededatos():
    if 'InicioSesion' in session:
        try:
            with open('basededatos.csv', 'r') as archivo:
                datalines = csv.reader(archivo)                
                titulos = next(datalines)                                
                return render_template('tabla.html', cabeza=titulos, cuerpo=datalines, username=session.get('InicioSesion'))
        except FileNotFoundError:
            return 'No se encuentra la base de datos de Farmacia Aleman'
    return render_template('sign_off.html')

#Acá empiezan las consultas.
#Estos menus aparecen solo cuando está loggeado.
#En todos ellos siempre se retorna el tabla.html para conformar la respuesta visual.
@app.route('/cliente', methods=['GET', 'POST'])
def consulcliente():
    if 'InicioSesion' in session:        
        form_nombre = SearchCliente()    
        try:
            with open('basededatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'cvs de base de datos inexistente'    
        if form_nombre.validate_on_submit():            
            with open('basededatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        cliente = ubicacion[1]
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las info que coincide el cliente
                        if form_nombre.parametro.data.lower() in cliente.lower():
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)
                    #Este if se puso para informar que no se encuentran resultados.
                    if len(infos) == 0 :
                        flash('El cliente que busca no se encuentra en nuestra Base de Datos.')
                        return render_template('cliente.html', form=form_nombre, username=session.get('InicioSesion'))
                    return render_template('tabla.html', form=form_nombre, cabeza=tupla, cuerpo=infos, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Numero invalido de datos a corroborar.'           
        return render_template('cliente.html', form=form_nombre, username=session.get('InicioSesion'))
    return render_template('sign_off.html')

#Consulta de producto.
@app.route('/producto', methods=['GET', 'POST'])
def consulproducto():
    if 'InicioSesion' in session:        
        form_producto = SearchProd()
        try:
            with open('basededatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'Error al buscar el csv de base de datos'
        if form_producto.validate_on_submit():
            with open('basededatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        producto = ubicacion[2]
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las infos que coincide el cliente
                        if form_producto.parametro.data.lower() in producto.lower():
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info) 
                    #Este if se adiciono para informar que no se encuentran resultados.
                    if len(infos) == 0 :
                        flash('El Producto que busca no se encuentra en nuestra Base de Datos.')
                        return render_template('producto.html', form=form_producto, username=session.get('InicioSesion'))
                    return render_template('tabla.html', form=form_producto, cabeza=tupla, cuerpo=infos, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Error al buscar informacion del producto'                           
        return render_template('producto.html', form=form_producto, username=session.get('InicioSesion'))
    return render_template('sign_off.html')


#Consulta de cantidad.
@app.route('/cantidad', methods=['GET', 'POST'])
def consulcantidad():
    if 'InicioSesion' in session:
        form_cantidad = SearchCant()
        try:
            with open('basededatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'Error al buscar el csv de base de datos'
        if form_cantidad.validate_on_submit():
            with open('basededatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        cantidad = ubicacion[3]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las infos que coincide el cliente
                        if form_cantidad.parametro.data == cantidad:
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)                            
                    #Este if se adiciono para informar que no se encuentran resultados.
                    if len(infos) == 0 :
                        flash('La cantidad ingresada  es inexistente en nuestra base de datos.')
                        return render_template('cantidad.html', form=form_cantidad, username=session.get('InicioSesion'))
                    return render_template('tabla.html', form=form_cantidad, cabeza=tupla, cuerpo=infos, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Error al encontrar los usuarios y cantidad'                           
        return render_template('cantidad.html', form=form_cantidad, username=session.get('InicioSesion'))
    return render_template('sign_off.html')


#Consulta de precios.
@app.route('/precio', methods=['GET', 'POST'])
def consulprecio():
    if 'InicioSesion' in session:
        form_precio = SearchPrecio()
        try:
            with open('basededatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de infos'
        if form_precio.validate_on_submit():
            with open('basededatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        precio = ubicacion[4]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las infos que coincide el cliente
                        if form_precio.parametro.data == precio:
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)                           
                    #Este if se adiciono para informar que no se encuentran resultados.
                    if len(infos) == 0 :
                        flash('El Precio que busca no se encuentra en nuestra Base de Datos.')
                        return render_template('precio.html', form=form_precio, username=session.get('InicioSesion'))
                    return render_template('tabla.html', form=form_precio, cabeza=tupla, cuerpo=infos, username=session.get('InicioSesion'))
                except IndexError:
                    return 'Error al buscar el usuario y su precio'                           
        return render_template('precio.html', form=form_precio, username=session.get('InicioSesion'))
    return render_template('sign_off.html')

#funcion de registro con if para validacion de contraseñas.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form_registro = CreaUsuario()
    if form_registro.validate_on_submit():
        if form_registro.pass1.data == form_registro.pass2.data:
            try:
                with open('usuariosbase.csv', 'a') as archivo:
                    escritor = csv.writer(archivo)
                    if form_registro.name.data in users_check:
                        return "El usuario ya existe, intente con otro usuario"
                    else:
                        escritor.writerow([form_registro.name.data, form_registro.pass1.data])
                        return redirect('login')
            except FileNotFoundError:
                return 'No se encuentra el CSV'
        return "Compruebe la contraseña"
    return render_template('register.html', form=form_registro)

@app.route('/signoff', methods=['GET', 'POST'])
def signoff():
    session.pop('InicioSesion', None)
    return redirect('/')

#Se agrego el , username=session.get('InicioSesion') para validar la navbar.
@app.errorhandler(404)
def paginanotf(e):
    return render_template('404.html', username=session.get('InicioSesion')), 404


#Se agrego el , username=session.get('InicioSesion') para validar la navbar.
@app.errorhandler(500)
def servererror(e):
    return render_template('500.html', username=session.get('InicioSesion')), 500

@app.route('/Ventas' , methods=['GET' , 'POST'])
def asd():
    with open ('venta.csv', 'r') as archivo:
        datalines = csv.reader(archivo)
        title = next(datalines)
        return render_template('Ventas.html', cabeza=title, cuerpo=datalines, username=session.get('InicioSesion'))




if __name__ == "__main__":
    manager.run()





# Librerias utilizadas para la funcionalidad de la aplicación
from threading import Thread
import sqlserverCon as sqlserverCon
import time
import datetime
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, flash, redirect, url_for
app = Flask(__name__)

# ____________________DB CONNECTION_________________________
sqlserverCon.init()
conn = sqlserverCon.conn
cursor = conn.cursor()
# _______________________CONFIGS____________________________
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://DESKTOP-F5IOQT8:1433/DBCcaphita?driver=ODBC+Driver+17+for+SQL+Server?TrustedConnection=yes"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisismysecretkey'
# _________________VARIABLES GLOBALES_______________________
global LoginInfo
LoginInfo = None
PedStatus = False
# ______________________FUNCION_____________________________


# metodo usado para mantener la sesión de un usuario, usa LoginInfo para mantenerlo activo.
def login_usuario(email, password):
    sqlString = f"select * from Usuarios where email='{email}' and pass='{password}';"
    cursor.execute(sqlString)
    data = cursor.fetchall()
    if data:
        global LoginInfo
        LoginInfo = data
        print(LoginInfo)
        return LoginInfo
    else:
        return None

# __________________FUNCIONABILIDAD_________________________


@app.route('/', methods=['GET'])
def home():  # --- Pagina principal del sistema
    global PedStatus
    PedStatus = False
    if not LoginInfo:
        return render_template('/product_bar.html')
    else:
        return render_template('/product_bar_logged.html')


@app.route('/login_register', methods=['GET', 'POST'])
def login_register():  # --- Pagina de inicio de sesión y registro de usuario nuevo
    # Dependiendo del tipo de request y el componente en la interfaz html, Logeará o procederá al resto de datos del cliente.
    if request.method == "POST":
        try:
            if request.form['emaillog']:
                email = request.form['emaillog']
                passw = request.form['passlog']

                usrid = login_usuario(email, passw)

                # Si los campos son correctos logra acceder, caso contrario, falla
                if usrid:
                    print("Login correcto de Usuario")
                    return redirect(url_for("user"))
                else:
                    return "<h1>Contraseña o correo incorrecto</h1>"
        except:
            pass
        try:
            if request.form['emailreg']:
                email = request.form['emailreg']
                passw = request.form['passreg']

                usrid = login_usuario(email, passw)

                return redirect(url_for('continuar_reg'))
        except:
            pass
    else:
        return render_template('/login_register.html')


@app.route('/registrarse')
def continuar_reg():

    return render_template('/register.html')


@app.route('/')
def user():  # pagina principal, con cambios al estar un usuario logeado
    return render_template('/product_bar_logged.html')


@app.route('/precios')
def prices():  # Pagina de precios de todos los productos, diferente si esta logeado el usuario, o no
    sqlString = "select * from producto;"
    cursor.execute(sqlString)
    data = cursor.fetchall()

    if not LoginInfo:
        return render_template('/precios.html', data=data)
    else:
        return render_template('/precios_logged.html', data=data)


@app.route('/product_id=<int:pid>')
def desc_product(pid):  # Pagina de un producto especifico
    sqlString = f"Select * from producto where idproducto={pid};"
    cursor.execute(sqlString)
    data = cursor.fetchone()

    if not LoginInfo:
        return render_template('/vistaproducto.html', data=data)
    else:
        return render_template('/vistaproducto_logged.html', data=data)


@app.route('/product_id=<int:pid>:add')
def agregar_carrito(pid):
    global LoginInfo
    if not LoginInfo:
        return redirect(url_for('desc_product', pid=pid))
    else:
        sqlString = f"Select * from producto where idproducto={pid};"
        cursor.execute(sqlString)
        data = cursor.fetchone()

        # Obteniendo data del carrito

        idcliente = LoginInfo[0][0]
        print(idcliente)
        sqlStringCar = f"select * from Carrito where personid = {idcliente};"
        cursor.execute(sqlStringCar)
        datacarrito = cursor.fetchall()
        print(datacarrito)

        if datacarrito[0][1] == None:
            prods = 1
            sqladd = f"update Carrito set numproductos={prods}, idproductos={pid} where personid = {idcliente}"
            cursor.execute(sqladd)
            conn.commit()
        else:

            breakf = False
            prods_carrito = datacarrito[0][2]
            prod_cods = prods_carrito.split()
            print(prod_cods)
            for cod in prod_cods:
                print(cod, pid)
                if pid == int(cod):
                    print("Producto ya existe en el carrito del usuario. . .")
                    breakf = True
                    break

            if breakf == True:
                return redirect(url_for('desc_product', pid=pid))
            else:
                prods_carrito = ' '.join([str(item) for item in prod_cods])
                prods_carrito_f = prods_carrito+f" {pid}"
                totprod = datacarrito[0][1]+1
                sqladd = f"update Carrito set numproductos={totprod}, idproductos='{prods_carrito_f}' where personid = {idcliente}"
                cursor.execute(sqladd)
                conn.commit()

        return render_template('/vistaproducto_logged.html', data=data)


@app.route('/carrito')
def carrito():  # Pagina de carrito
    global LoginInfo
    personid = LoginInfo[0][0]

    sql = f"insert into carrito(personid,numproductos, idproductos) values({personid}, 0, '')"
    cursor.execute(sql)
    conn.commit()

    sql = f"select * from carrito where personid={personid}"
    cursor.execute(sql)
    datac = cursor.fetchall()
    prods_carrito = datac[0][2]
    cant_prods = datac[0][1]
    prodids = prods_carrito.split()
    data = list()
    total_pago = 0
    for prodid in prodids:
        sql = f"select * from producto where idproducto = {prodid}"
        cursor.execute(sql)
        datac = cursor.fetchone()
        total_pago = total_pago + float(datac[5])
        data.append(datac)
    sql = "select count(*) as pedido from pedido"
    cursor.execute(sql)
    datac = cursor.fetchone()
    idped = datac[0]

    return render_template('/carrito.html', data=data, cprod=cant_prods, totp=total_pago, tidped=idped, ped_s=PedStatus)


@app.route('/quitar_prodid=<int:pid>')
def quitar_prod_carrito(pid):
    global LoginInfo
    idcliente = LoginInfo[0][0]
    sql = f"select * from carrito where personid = {idcliente}"
    cursor.execute(sql)
    datac = cursor.fetchone()
    print(datac)
    car_prod = datac[2]
    prod_cods = car_prod.split()
    print(prod_cods)

    for cod in prod_cods:
        if pid == int(cod):
            prod_cods.remove(cod)

    prods_carrito = ' '.join([str(item) for item in prod_cods])
    totprod = datac[1]-1
    sql = f"update carrito set numproductos={totprod}, idproductos='{prods_carrito}' where personid = {idcliente}"
    cursor.execute(sql)
    conn.commit()

    return redirect(url_for('carrito'))


@app.route('/realizarpago=<int:pid>', methods=['GET', 'POST'])
def realizarpedido(pid):
    if request.method == "POST":
        global PedStatus
        PedStatus = True

        global LoginInfo
        personid = LoginInfo[0][0]

        """
        1. obtengo el carrito
        2. obtengo la cantidad de productos
        3. inserto el registro de pedido (pedido), luego obtengo el idpedido usando el personid
        4. hago split a los idproductos del carrito
        5. con los idproducto hago detallepedido, cantidad siempre 1 ingresar registros a cantidadventas
        6. hago la tabla pago, con el idpedido generado. monto la suma de todos los productos.
        7. direccionfact la del form
        8. tipo pago siempre tarjeta
        9. fecha pago actual date
        10. hago la tabla boleta, con el id pago generado
        11. fecha boleta actual date
        12. ruc opcional, siempre null.
        13. limpio el carrito
        """

        # 1
        sql = f"select * from carrito where personid={personid}"
        cursor.execute(sql)
        datac = cursor.fetchone()
        print("Carrito obtenido. . .")
        # 2
        cp_carrito = datac[1]  # cantidad de productos del carrito
        print("Cantidad de productos obtenido. . .")
        # 3
        today = datetime.date.today()  # fecha actual

        sql = f"insert into pedido(personid,fechapedido,canttotalproductos) values('{personid}','{str(today)}','{cp_carrito}')"
        cursor.execute(sql)
        conn.commit()

        sql = f"select idpedido as idpedido from pedido where personid={personid}"
        cursor.execute(sql)
        idpedidoD = cursor.fetchone()  # data de pedido
        idpedido = idpedidoD[0]  # idpedido recien insertado
        print("pedido insertado. . .")
        # 4
        prodids_cart = datac[2]
        pid_c_split = prodids_cart.split()  # lista de ids de productos en el carrito
        print("obtenida lista de id productos. . .")
        # 5
        montot = 0
        for idp in pid_c_split:  # idp es el id individual de cada producto que estaba en el carrito
            sql = f"insert into detallepedido(idpedido,idproducto, cantidad) values({idpedido}, {idp}, 1)"
            cursor.execute(sql)
            conn.commit()
            print("insertando: ", idp, ". . .")

            sql = f"select precio, stock from producto where idproducto ={idp}"
            cursor.execute(sql)
            precioD = cursor.fetchone()
            montot = montot + float(precioD[0])

            sql = f"insert into cantidadventas(idproducto,cantidadcomprada,fechaultimacompra) values({idp},1,'{str(today)}')"
            cursor.execute(sql)
            conn.commit()
            #actualizando stock
            sql = f"update producto set stock={int(precioD[1])-1} where idproducto={idp}"
            cursor.execute(sql)
            conn.commit()


        # 6 7 8 9
        direcfact = request.form['direccionfact']
        sql = f"insert into pago(idpedido,monto,fechapago,direccionfact,tipopago) values({idpedido},{montot},'{str(today)}','{direcfact}','Tarjeta')"
        cursor.execute(sql)
        conn.commit()
        print("insertado a la tabla pago. . .")
        sql = f"select idpago as idpago from pago where idpedido={idpedido}"
        cursor.execute(sql)
        idpagoD = cursor.fetchone()
        idpago = idpagoD[0]
        print("obtenido el id pago. . .")
        # 10 11 12
        sql = f"insert into boleta(productos,fechaboleta,ruc,idpago) values({cp_carrito},'{str(today)}','',{idpago})"
        cursor.execute(sql)
        conn.commit()
        print("insertada la boleta. . .")
        # 13
        sql = f"update carrito set numproductos=0,idproductos='' where personid= {personid}"
        cursor.execute(sql)
        conn.commit()
        print("actualizando carrito. . .")

        time.sleep(3)

        print("PROCEDIMIENTO CONCLUIDO CON EXITO")

        return redirect(url_for('carrito'))

    return render_template('realizarpago.html')


@app.route('/pedidos')
def pedidos():  # Pagina de pedidos
    return render_template('/pedidos.html')


@app.route('/boletas')
def boletas():  # Pagina de boletas
    return render_template('/boletas.html')


@app.route('/#')
def logout():  # Metodo para cerrar sesión
    global LoginInfo
    LoginInfo = None

    print("Sesion Cerrada")
    return redirect(url_for("login_register"))


# Funcion principal que echa a correr la aplicación web.
if __name__ == '__main__':
    app.run(debug=True)

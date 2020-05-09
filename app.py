#render template para cargar plantillas, request para las peticiones
from flask import Flask, render_template, request, session, escape, jsonify, g, json, flash, redirect, url_for 
import psycopg2
from psycopg2 import pool
import os

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
#conexion a la base de datos, SimpleConnectionPool(1, 100 ,representa el numero de conexiones simulaneas que aceptara el sistema 
app.config['postgreSQL_pool'] = psycopg2.pool.SimpleConnectionPool(1, 100,
    user = "sky",
    password = "1234",
    host = "127.0.0.1",
    port = "5432",
    database = "mse")

def get_db():
    if 'db' not in g:
        g.db = app.config['postgreSQL_pool'].getconn()
    return g.db

@app.teardown_appcontext
def close_conn(e):
    db = g.pop('db', None)
    if db is not None:
        app.config['postgreSQL_pool'].putconn(db)
#cierre de la conexion

#Index
@app.route("/")
def index():
    return render_template("index.html")
   

@app.route("/estadisticas1",  methods=["GET", "POST"])
def estadisticas1():

    #Llenado de los select
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select nombreunidad from mse.unidad")
    unidad = cursor.fetchall()

    cursor.execute("select nombreárea from mse.áreaconocimiento")
    areainv = cursor.fetchall()

    cursor.execute("select departamento from mse.departamentos")
    departamento = cursor.fetchall()

    cursor.execute("select tiposector from mse.sector")
    sector = cursor.fetchall()
    
    cursor.execute("select distinct extract(year from fechatomagrado) from mse.egresados order by extract(year from fechatomagrado)")
    añoinicial = cursor.fetchall()

    cursor.execute("select distinct extract(year from fechatomagrado) from mse.egresados order by extract(year from fechatomagrado)")
    añofinal = cursor.fetchall()
    

    #if request.method=="POST":
       # unidad1 = request.args.get('unidad1')
        #sector1 = request.args.get('sector1')
        #departamento1 = request.args.get('departamento1')
        #areainv1 = request.args.get('areainv1')
        #grado1 = request.args.get('grado1')
        #añoinicial1 = request.args.get('añoinicial1')
        #añofinal1 = request.args.get('añofinal1')
        #print ("valor: ",unidad1,sector1, departamento1,areainv1, grado1,añoinicial1,añofinal1)
 
        #return render_template("estadisticas.html",unidad=unidad, areainv=areainv, departamento=departamento,sector=sector,añoinicial=añoinicial,añofinal=añofinal,
        #unidad1=unidad1, sector1=sector1, departamento1=departamento,areainv1=areainv1,grado1=grado1,añoinicial1=añoinicial1,añofinal1=añofinal1)
    return render_template("estadisticas.html", unidad=unidad, areainv=areainv, departamento=departamento,sector=sector,añoinicial=añoinicial,añofinal=añofinal)    


@app.route("/estadisticas", methods=["GET", "POST"])
def estadisticas():


        
        dato_json = '{"cols": [{"id":"","label":"Egresados","pattern":"","type":"string"},'
        
        dato_json= dato_json + '{"id":"","label":"valor","pattern":"","type":"number"}],"rows": [' 
    
        #Realizacion de la consulta para obtener los datos 
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select distinct cargoactual from mse.egresados")
        result = cursor.fetchall()
    
        #Contador de Registros
        contRow = 0

        #Ciclo para cada dato obtenido
        while contRow < len (result):

            #Obtiene el Registro
            registro = result[contRow]
            #print("Registro:",registro)

            #Obtiene la Columna
            columna = registro[0]
            #print("Columna:",columna)
        
            #Prepara una nueva Consulta
            cursor.execute("select count(*) from mse.egresados where cargoactual = '"+ columna +"'" )
            result2 = cursor.fetchall()
        
            #Obtiene el valor
            valor = str(result2[0][0])
            #print("Valor:",valor )

            #Obtener el año
            cursor.execute("select distinct extract(year from fechatomagrado) from mse.egresados where cargoactual = '"+ columna +"' order by extract(year from fechatomagrado)" )
            result3 = cursor.fetchall()
        
            #Obtiene el valor
            año = str(result3[0][0])
    
            #Agrega el row al dato_json con la columna y el valor
            dato_json = dato_json + '{"c":[{"v":"'+año+'","f":null},{"v":'+valor+',"f":null},{"v":'+valor+',"f":null}]}' 
        
            #Verifica si no es el ultimo renglon para agregar una coma
            if(contRow < len(result)-1):
                dato_json = dato_json + ","

        #Incrementa el Contador de Row
            contRow = contRow + 1

        #Coloca el cierre del dato_json
        dato_json = dato_json +  "]}"

        print("dato_json", dato_json)
        cursor.close()
        return dato_json
        

        
@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

@app.route("/area")
def area():

        dato_json = '{"cols": [{"id":"","label":"Egresados","pattern":"","type":"string"},'
        
        dato_json= dato_json + '{"id":"","label":"valor","pattern":"","type":"number"}],"rows": [' 
    
        #Realizacion de la consulta para obtener los datos 
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select departamento from mse.departamentos")
        result = cursor.fetchall()
    
        #Contador de Registros
        contRow = 0

        #Ciclo para cada dato obtenido
        while contRow < len (result):

            #Obtiene el Registro
            registro = result[contRow]

            #Obtiene la Columna
            columna = registro[0]
        
            #Prepara una nueva Consulta
            cursor.execute("Select count(e.idegresado) as count from mse.egresados e inner join mse.departamentos d on e.iddepartamento = d.iddepartamento where d.departamento = '"+columna+"'" )
            result2 = cursor.fetchall()
        
            #Obtiene el valor
            valor = str(result2[0][0])

            #Agrega el row al dato_json con la columna y el valor
            dato_json = dato_json + '{"c":[{"v":"'+columna+'","f":null},{"v":'+valor+',"f":null}]}' 
        
            #Verifica si no es el ultimo renglon para agregar una coma
            if(contRow < len(result)-1):
                dato_json = dato_json + ","

        #Incrementa el Contador de Row
            contRow = contRow + 1

        #Coloca el cierre del dato_json
        dato_json = dato_json +  "]}"

        cursor.close()
        return dato_json

@app.route("/departamento")
def departamento():
        dato_json = '{"cols": [{"id":"","label":"Egresados","pattern":"","type":"string"},'
        
        dato_json= dato_json + '{"id":"","label":"valor","pattern":"","type":"number"}],"rows": [' 
    
        #Realizacion de la consulta para obtener los datos 
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select departamento from mse.departamentos")
        result = cursor.fetchall()
    
        #Contador de Registros
        contRow = 0

        #Ciclo para cada dato obtenido
        while contRow < len (result):

            #Obtiene el Registro
            registro = result[contRow]

            #Obtiene la Columna
            columna = registro[0]
        
            #Prepara una nueva Consulta
            cursor.execute("Select count(e.idegresado) as count from mse.egresados e inner join mse.departamentos d on e.iddepartamento = d.iddepartamento where d.departamento = '"+columna+"'" )
            result2 = cursor.fetchall()
        
            #Obtiene el valor
            valor = str(result2[0][0])

            #Agrega el row al dato_json con la columna y el valor
            dato_json = dato_json + '{"c":[{"v":"'+columna+'","f":null},{"v":'+valor+',"f":null}]}' 
        
            #Verifica si no es el ultimo renglon para agregar una coma
            if(contRow < len(result)-1):
                dato_json = dato_json + ","

        #Incrementa el Contador de Row
            contRow = contRow + 1

        #Coloca el cierre del dato_json
        dato_json = dato_json +  "]}"

        cursor.close()
        return dato_json
        
@app.route("/prueba")
def prueba():
    return render_template("prueba.html")
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__=="__main__":
    app.run(debug=True)

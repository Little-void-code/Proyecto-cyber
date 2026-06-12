#importar las libreiras
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from datetime import datetime
from datetime import date

#conexion a la base de datos
URI = 'mongodb+srv://little_void:programando@cluster0.rn008dn.mongodb.net/?appName=Cluster0'
@st.cache_resource
def init_connection():
  return MongoClient(URI)
try:
  cliente = init_connection()
  #definimos los datos de la base
  db = cliente["cyber"]
  coleccion_b = db["EquiposBasicos"]
  coleccion_g = db["Gaming"]
  coleccion_z = db["ZonaInsonora"]
except Exception as e:
  st.error("Error al conectar la Base de Datos : ", e)

#Toca configurar la pagina y con ello la interfaz  🫡
st.set_page_config(page_title="Cyber - Vida social")
st.title("Cyber Vida Social")
st.header("Cyber especializado 😎")
st.write("Pues no se que poner y ya tengo sueño asi que queda esto 🙃")
st.write("JACKPOT 🎰🎰🎰😝")

import streamlit as st

def Equipo_Basico():
  #crear las pestañas del menu (tabs)
  tab_ver, tab_agregar, tab_editar = st.tabs([
    "🔍 Ver Equipos de la Zona 1",
    "➕ Agregar Equipo",
    "✏️ Editar Datos de los Equipos"
  ])
  ##creamos cada tab
  #leer y visualizar los datos
  with tab_ver:
    st.header("Listado de Equipos Actuales")
    # Obtener documentos actualizados
    documentos = list(coleccion_b.find())

    if documentos:
      # Convertimos temporalmente a DataFrame solo para calcular las métricas globales
      df_meta = pd.DataFrame(documentos)

      col_m1,col_m2,col_m3 = st.columns(3)
      #col_m1.metric("Total de Productos Únicos", len(df_meta))
      #col_m2.metric("Stock Total en Almacén", int(df_meta['stock']))
      #col_m3.metric("Precio Promedio", f"${df_meta['precio'].mean():.2f}")

      st.markdown("---")

      # --- DISEÑO DE LA TABLA CON ACCIONES ---
      # Definimos la proporción de ancho para cada columna (ajustable)
      # ID, Nombre, Precio, Stock, Categoría, Proveedor, Acción
      proporciones = [10, 10, 10, 10, 10, 10, 10, 10, 10]

      # Encabezados de la tabla
      cols_header = st.columns(proporciones)
      cols_header[0].markdown("**ID Equipo**")
      cols_header[1].markdown("**Datos Usuario**")
      cols_header[2].markdown("**Tiempo de uso**")
      cols_header[3].markdown("**Precio/h**")
      cols_header[4].markdown("**Monto Total**")
      cols_header[5].markdown("**Aplicaciones Usadas**")
      cols_header[6].markdown("**Informacion del Equipo**")
      cols_header[7].markdown("**Elementos Acompañantes**")
      cols_header[8].markdown("**Acción**")
      st.markdown("<hr style='margin-top:0px; margin-bottom:10px;'>", unsafe_allow_html=True)
      # Renderizar cada documento como una fila de la tabla
      for doc in documentos:
          cols_row = st.columns(proporciones)

          # Datos de las celdas
          cols_row[0].write(str(doc.get('id_equipo', '')))
          cols_row[1].write(str(doc.get('usuario', '')))
          cols_row[2].write(str(doc.get('tiempo_uso', 0)))
          cols_row[3].write(str(doc.get('precio_hora', 0)))
          cols_row[4].write(str(doc.get('monto_total', '')))
          cols_row[5].write(str(doc.get('aplicaciones_usadas', '')))
          cols_row[6].write(str(doc.get('informacion_extra', '')))
          cols_row[7].write(str(doc.get('elementos_acompanantes', '')))

          # Botón eliminar directo usando el _id único de MongoDB como Key
          # El parámetro 'type="primary"' resalta el botón en rojo/color de énfasis según el tema
          if cols_row[8].button("❌", key=f"del_{doc['_id']}", help=f"Eliminar permanentemente {doc.get('nombre')}"):
              coleccion_b.delete_one({"_id": doc["_id"]})
              st.toast(f"Producto '{doc.get('nombre')}' eliminado.", icon="❌")
              st.rerun()
    else:
      st.info("La colección está vacía. Agrega un producto en la siguiente pestaña.")

    with tab_agregar:
      st.header("Registrar Nuevo Equipo")

      with st.form("form_crear"):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_id = st.number_input("ID numérico aun no regitrado", min_value=1, step=1, value=73)
            nuevo_nombre = st.text_input("Nombre del Usuario que usara el equipo", placeholder="Ej. Raul Ramirez")
            nueva_edad = st.number_input("Edad del ", min_value=0, step=1, value=16)
            nuevo_tiempo = st.number_input("Tiempo de uso en minutos", min_value=0, step=1, value=120)
            nuevas_aplicaciones = st.text_input("Aplicaciones que se usaron", value="Chrome, WhatsApp")
            nuevos_elementos = st.text_input("Elementos que acompañan al equipo", value="Mouse, Teclado")
        with col2:
            nuevo_componente = st.text_input("Componentes que han sido combiados en el equipo", value="Memoria Ram, CPU")
            nueva_fecha = st.date_input("Fecha de Compra", value=datetime.now())
            nuevo_sistema = st.text_input("Sistema operativo del Equipo", placeholder="Ej. Linux")
            nuevo_procesador = st.text_input("Procesador que tiene el equipo", placeholder="Ej. Intel aceleron...")
            nuevo_almacenamiento = st.text_input("Espacio de almacenamiento", value="256GB")
            nueva_marca = st.text_input("Marca del equipo", placeholder="Ej. Hp")

        nuevo_usuario={
            "nombre":nuevo_nombre,
            "edad":int(nueva_edad)
        }
        fecha_datetime = datetime.combine(
              nueva_fecha,
              datetime.min.time()
        )
        nuevo_monto=10*(nuevo_tiempo/60)
        nueva_informacion={
            "fecha_compra":fecha_datetime,
            "componentes_cambiados":nuevo_componente,
            "sistema_operativo":nuevo_sistema,
            "procesador":nuevo_procesador,
            "almacenamiento":nuevo_almacenamiento,
            "marca_equipo":nueva_marca
        }
        boton_guardar = st.form_submit_button("Guardar Producto")
        if boton_guardar:
            if nuevo_nombre.strip() == "":
                st.error("El nombre no puede estar vacío.")
            else:
                nuevo_documento = {
                    "id_equipo": int(nuevo_id),
                    "usuario": nuevo_usuario,
                    "tiempo_uso": int(nuevo_tiempo),
                    "precio_hora": 10,
                    "monto_total": float(nuevo_monto),
                    "aplicaciones_usadas": nuevas_aplicaciones,
                    "informacion_extra": nueva_informacion,
                    "elementos_acompañantes": nuevos_elementos
                }
                coleccion_b.insert_one(nuevo_documento)
                st.success("Nuevo equipo agregado con exito 🥳")
                st.rerun()

    with tab_editar:
      st.header("Modificar un Equipo Existente")

      if documentos:
        opciones_equipos = {f"({doc['usuario']['nombre']} Tiempo de uso: {doc['tiempo_uso']} )": doc for doc in documentos}
        seleccion = st.selectbox("Selecciona el producto a editar:", opciones_equipos.keys())
        equipo_actual = opciones_equipos[seleccion]

        with st.form("form_actualizar"):
            col1, col2 = st.columns(2)
            with col1:
                edit_nombre = st.text_input("Nombre del Usuario que usara el equipo", value=equipo_actual.get('usuario').get('nombre'))
                edit_edad = st.number_input("Edad del ", min_value=0, step=1, value=int(equipo_actual.get('usuario').get('edad')))
                edit_tiempo = st.number_input("Tiempo de uso en minutos", min_value=0, step=1, value=int(equipo_actual.get('tiempo_uso')))
                edit_aplicaciones = st.text_input("Aplicaciones que se usaron", value=equipo_actual.get('aplicaciones_usadas'))
                edit_elementos = st.text_input("Elementos que acompañan al equipo", value=equipo_actual.get('elementos_acompanantes'))
            with col2:
                edit_componente = st.text_input("Componentes que quieras editar en el equipo", value=equipo_actual.get('informacion_extra').get('componentes_cambiados'))
                edit_sistema = st.text_input("Sistema operativo del Equipo",value=equipo_actual.get('informacion_extra').get('sistema_operativo'))
                edit_procesador = st.text_input("Procesador que tiene el equipo",value=equipo_actual.get('informacion_extra').get('procesador'))
                edit_almacenamiento = st.text_input("Espacio de almacenamiento", value=equipo_actual.get('informacion_extra').get('almacenamiento'))
                edit_marca = st.text_input("Marca del equipo", value=equipo_actual.get('informacion_extra').get('marca_equipo'))

                fecha_guardada = equipo_actual.get('informacion_extra').get('fecha_compra', datetime.now())
                if isinstance(fecha_guardada, str):
                    fecha_guardada = datetime.fromisoformat(fecha_guardada.replace("Z", ""))

                edit_fecha = st.date_input("Fecha de Compra", value=fecha_guardada)

            edit_usuario={
              "nombre":edit_nombre,
              "edad":int(edit_edad)
            }
            fecha_datetime = datetime.combine(
              edit_fecha,
              datetime.min.time()
            )
            informacion_editada={
              "fecha_compra":fecha_datetime,
              "componentes_cambiados":edit_componente,
              "sistema_operativo":edit_sistema,
              "procesador":edit_procesador,
              "almacenamiento":edit_almacenamiento,
              "marca_equipo":edit_marca
            }
            edit_monto=10*(edit_tiempo/60)
            boton_actualizar = st.form_submit_button("Actualizar Cambios")
            if boton_actualizar:
                coleccion_b.update_one(
                    {"_id": equipo_actual["_id"]},
                    {"$set": {
                        "usuario": edit_usuario,
                        "tiempo_uso": int(edit_tiempo),
                        "precio_hora": 10,
                        "monto_total": float(edit_monto),
                        "aplicaciones_usadas": edit_aplicaciones,
                        "informacion_extra": informacion_editada,
                        "elementos_acompanantes": edit_elementos
                    }}
                )
                st.success("Equipo actualizado!")
                st.rerun()
      else:
        st.info("No hay Equipos disponibles para editar.")


def Equipo_Gaming():
  #crear las pestañas del menu (tabs)
  tab_ver, tab_agregar, tab_editar= st.tabs([
    "🔍 Ver Equipos de la Zona 2",
    "➕ Agregar Equipo",
    "✏️ Editar Datos de los Equipos"
  ])
  ##creamos cada tab
  #leer y visualizar los datos
  with tab_ver:
    st.header("Listado de Equipos Actuales")
    # Obtener documentos actualizados
    documentos = list(coleccion_g.find())

    if documentos:
      # Convertimos temporalmente a DataFrame solo para calcular las métricas globales
      df_meta = pd.DataFrame(documentos)

      col_m1,col_m2,col_m3 = st.columns(3)
      #col_m1.metric("Total de Productos Únicos", len(df_meta))
      #col_m2.metric("Stock Total en Almacén", int(df_meta['stock']))
      #col_m3.metric("Precio Promedio", f"${df_meta['precio'].mean():.2f}")

      st.markdown("---")

      # --- DISEÑO DE LA TABLA CON ACCIONES ---
      # Definimos la proporción de ancho para cada columna (ajustable)
      # ID, Nombre, Precio, Stock, Categoría, Proveedor, Acción
      proporciones = [10, 10, 10, 10, 10, 10, 10, 10, 10]

      # Encabezados de la tabla
      cols_header = st.columns(proporciones)
      cols_header[0].markdown("**ID Equipo**")
      cols_header[1].markdown("**Datos Usuario**")
      cols_header[2].markdown("**Tiempo de uso**")
      cols_header[3].markdown("**Precio/h**")
      cols_header[4].markdown("**Monto Total**")
      cols_header[5].markdown("**Aplicaciones Usadas**")
      cols_header[6].markdown("**Informacion del Equipo**")
      cols_header[7].markdown("**Elementos Acompañantes**")
      cols_header[8].markdown("**Acción**")
      st.markdown("<hr style='margin-top:0px; margin-bottom:10px;'>", unsafe_allow_html=True)
      # Renderizar cada documento como una fila de la tabla
      for doc in documentos:
          cols_row = st.columns(proporciones)

          # Datos de las celdas
          cols_row[0].write(str(doc.get('id_equipo', '')))
          cols_row[1].write(str(doc.get('usuario', '')))
          cols_row[2].write(str(doc.get('tiempo_uso', 0)))
          cols_row[3].write(str(doc.get('precio_hora', 0)))
          cols_row[4].write(str(doc.get('monto_total', '')))
          cols_row[5].write(str(doc.get('aplicaciones_usadas', '')))
          cols_row[6].write(str(doc.get('informacion_extra', '')))
          cols_row[7].write(str(doc.get('elementos_acompanantes', '')))

          # Botón eliminar directo usando el _id único de MongoDB como Key
          # El parámetro 'type="primary"' resalta el botón en rojo/color de énfasis según el tema
          if cols_row[8].button("❌", key=f"del_{doc['_id']}", help=f"Eliminar permanentemente {doc.get('nombre')}"):
              coleccion_b.delete_one({"_id": doc["_id"]})
              st.toast(f"Producto '{doc.get('nombre')}' eliminado.", icon="❌")
              st.rerun()
    else:
      st.info("La colección está vacía. Agrega un producto en la siguiente pestaña.")

    with tab_agregar:
      st.header("Registrar Nuevo Equipo")

      with st.form("form_crear"):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_id = st.number_input("ID numérico aun no regitrado", min_value=1, step=1, value=73)
            nuevo_nombre = st.text_input("Nombre del Usuario que usara el equipo", placeholder="Ej. Raul Ramirez")
            nueva_edad = st.number_input("Edad del ", min_value=0, step=1, value=16)
            nuevo_tiempo = st.number_input("Tiempo de uso en minutos", min_value=0, step=1, value=120)
            nuevas_aplicaciones = st.text_input("Aplicaciones que se usaron", value="Chrome, WhatsApp")
            nuevos_elementos = st.text_input("Elementos que acompañan al equipo", value="Mouse, Teclado")
        with col2:
            nuevo_componente = st.text_input("Componentes que han sido combiados en el equipo", value="Memoria Ram, CPU")
            nueva_fecha = st.date_input("Fecha de Compra", value=datetime.now())
            nuevo_sistema = st.text_input("Sistema operativo del Equipo", placeholder="Ej. Linux")
            nuevo_procesador = st.text_input("Procesador que tiene el equipo", placeholder="Ej. Intel aceleron...")
            nuevo_almacenamiento = st.text_input("Espacio de almacenamiento", value="256GB")
            nueva_marca = st.text_input("Marca del equipo", placeholder="Ej. Hp")

        nuevo_usuario={
            "nombre":nuevo_nombre,
            "edad":int(nueva_edad)
        }
        fecha_datetime = datetime.combine(
          nueva_fecha,
          datetime.min.time()
        )
        nuevo_monto=10*(nuevo_tiempo/60)
        nueva_informacion={
            "fecha_compra":fecha_datetime,
            "componentes_cambiados":nuevo_componente,
            "sistema_operativo":nuevo_sistema,
            "procesador":nuevo_procesador,
            "almacenamiento":nuevo_almacenamiento,
            "marca_equipo":nueva_marca
        }
        boton_guardar = st.form_submit_button("Guardar Producto")
        if boton_guardar:
            if nuevo_nombre.strip() == "":
                st.error("El nombre no puede estar vacío.")
            else:
                nuevo_documento = {
                    "id_equipo": int(nuevo_id),
                    "usuario": nuevo_usuario,
                    "tiempo_uso": int(nuevo_tiempo),
                    "precio_hora": 10,
                    "monto_total": float(nuevo_monto),
                    "aplicaciones_usadas": nuevas_aplicaciones,
                    "informacion_extra": nueva_informacion,
                    "elementos_acompañantes": nuevos_elementos
                }
                coleccion_b.insert_one(nuevo_documento)
                st.success("Nuevo equipo agregado con exito 🥳")
                st.rerun()

    with tab_editar:
      st.header("Modificar un Producto Existente")

      if documentos:
        opciones_equipos = {f"(ID: {doc['id_equipo']} {doc['usuario']['nombre']})": doc for doc in documentos}
        seleccion = st.selectbox("Selecciona el producto a editar:", opciones_equipos.keys())
        equipo_actual = opciones_equipos[seleccion]

        with st.form("form_actualizar"):
            col1, col2 = st.columns(2)
            with col1:
                edit_nombre = st.text_input("Nombre del Usuario que usara el equipo", value=equipo_actual.get('usuario').get('nombre'))
                edit_edad = st.number_input("Edad del ", min_value=0, step=1, value=int(equipo_actual.get('usuario').get('edad')))
                edit_tiempo = st.number_input("Tiempo de uso en minutos", min_value=0, step=1, value=int(equipo_actual.get('tiempo_uso')))
                edit_aplicaciones = st.text_input("Aplicaciones que se usaron", value=equipo_actual.get('aplicaciones_usadas'))
                edit_elementos = st.text_input("Elementos que acompañan al equipo", value=equipo_actual.get('elementos_acompanantes'))
            with col2:
                edit_componente = st.text_input("Componentes que quieras editar en el equipo", value=equipo_actual.get('informacion_extra').get('componentes_cambiados'))
                edit_sistema = st.text_input("Sistema operativo del Equipo",value=equipo_actual.get('informacion_extra').get('sistema_operativo'))
                edit_procesador = st.text_input("Procesador que tiene el equipo",value=equipo_actual.get('informacion_extra').get('procesador'))
                edit_almacenamiento = st.text_input("Espacio de almacenamiento", value=equipo_actual.get('informacion_extra').get('almacenamiento'))
                edit_marca = st.text_input("Marca del equipo", value=equipo_actual.get('informacion_extra').get('marca_equipo'))

                fecha_guardada = equipo_actual.get('informacion_extra').get('fecha_compra', datetime.now())
                if isinstance(fecha_guardada, str):
                    fecha_guardada = datetime.fromisoformat(fecha_guardada.replace("Z", ""))

                edit_fecha = st.date_input("Fecha de Compra", value=fecha_guardada)

            edit_usuario={
              "nombre":edit_nombre,
              "edad":int(edit_edad)
            }
            informacion_editada={
              "fecha_compra":edit_fecha,
              "componentes_cambiados":edit_componente,
              "sistema_operativo":edit_sistema,
              "procesador":edit_procesador,
              "almacenamiento":edit_almacenamiento,
              "marca_equipo":edit_marca
            }
            edit_monto=10*(nuevo_tiempo/60)
            boton_actualizar = st.form_submit_button("Actualizar Cambios")
            if boton_actualizar:
                coleccion_b.update_one(
                    {"_id": equipo_actual["_id"]},
                    {"$set": {
                        "usuario": edit_usuario,
                        "tiempo_uso": int(edit_tiempo),
                        "precio_hora": 10,
                        "monto_total": float(edit_monto),
                        "aplicaciones_usadas": edit_aplicaciones,
                        "informacion_extra": informacion_editada,
                        "elementos_acompañantes": edit_elementos
                    }}
                )
                st.success("Equipo actualizado!")
                st.rerun()
      else:
        st.info("No hay Equipos disponibles para editar.")


def Equipo_Trabajo():
  #crear las pestañas del menu (tabs)
  tab_ver, tab_agregar, tab_editar = st.tabs([
    "🔍 Ver Equipos de la Zona 3",
    "➕ Agregar Equipo",
    "✏️ Editar Datos de los Equipos"
  ])
  ##creamos cada tab
  #leer y visualizar los datos
  with tab_ver:
    st.header("Listado de Equipos Actuales")
    # Obtener documentos actualizados
    documentos = list(coleccion_z.find())

    if documentos:
      # Convertimos temporalmente a DataFrame solo para calcular las métricas globales
      df_meta = pd.DataFrame(documentos)

      col_m1,col_m2,col_m3 = st.columns(3)
      #col_m1.metric("Total de Productos Únicos", len(df_meta))
      #col_m2.metric("Stock Total en Almacén", int(df_meta['stock']))
      #col_m3.metric("Precio Promedio", f"${df_meta['precio'].mean():.2f}")

      st.markdown("---")

      # --- DISEÑO DE LA TABLA CON ACCIONES ---
      # Definimos la proporción de ancho para cada columna (ajustable)
      # ID, Nombre, Precio, Stock, Categoría, Proveedor, Acción
      proporciones = [10, 10, 10, 10, 10, 10, 10, 10, 10]

      # Encabezados de la tabla
      cols_header = st.columns(proporciones)
      cols_header[0].markdown("**ID Equipo**")
      cols_header[1].markdown("**Datos Usuario**")
      cols_header[2].markdown("**Tiempo de uso**")
      cols_header[3].markdown("**Precio/h**")
      cols_header[4].markdown("**Monto Total**")
      cols_header[5].markdown("**Aplicaciones Usadas**")
      cols_header[6].markdown("**Informacion del Equipo**")
      cols_header[7].markdown("**Elementos Acompañantes**")
      cols_header[8].markdown("**Acción**")
      st.markdown("<hr style='margin-top:0px; margin-bottom:10px;'>", unsafe_allow_html=True)
      # Renderizar cada documento como una fila de la tabla
      for doc in documentos:
          cols_row = st.columns(proporciones)

          # Datos de las celdas
          cols_row[0].write(str(doc.get('id_equipo', '')))
          cols_row[1].write(str(doc.get('usuario', '')))
          cols_row[2].write(str(doc.get('tiempo_uso', 0)))
          cols_row[3].write(str(doc.get('precio_hora', 0)))
          cols_row[4].write(str(doc.get('monto_total', '')))
          cols_row[5].write(str(doc.get('aplicaciones_usadas', '')))
          cols_row[6].write(str(doc.get('informacion_extra', '')))
          cols_row[7].write(str(doc.get('elementos_acompanantes', '')))

          # Botón eliminar directo usando el _id único de MongoDB como Key
          # El parámetro 'type="primary"' resalta el botón en rojo/color de énfasis según el tema
          if cols_row[8].button("❌", key=f"del_{doc['_id']}", help=f"Eliminar permanentemente {doc.get('nombre')}"):
              coleccion_b.delete_one({"_id": doc["_id"]})
              st.toast(f"Producto '{doc.get('nombre')}' eliminado.", icon="❌")
              st.rerun()
    else:
      st.info("La colección está vacía. Agrega un producto en la siguiente pestaña.")

    with tab_agregar:
      st.header("Registrar Nuevo Equipo")

      with st.form("form_crear"):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_id = st.number_input("ID numérico aun no regitrado", min_value=1, step=1, value=73)
            nuevo_nombre = st.text_input("Nombre del Usuario que usara el equipo", placeholder="Ej. Raul Ramirez")
            nueva_edad = st.number_input("Edad del ", min_value=0, step=1, value=16)
            nuevo_tiempo = st.number_input("Tiempo de uso en minutos", min_value=0, step=1, value=120)
            nuevas_aplicaciones = st.text_input("Aplicaciones que se usaron", value="Chrome, WhatsApp")
            nuevos_elementos = st.text_input("Elementos que acompañan al equipo", value="Mouse, Teclado")
        with col2:
            nuevo_componente = st.text_input("Componentes que han sido combiados en el equipo", value="Memoria Ram, CPU")
            nueva_fecha = st.date_input("Fecha de Compra", value=datetime.now())
            nuevo_sistema = st.text_input("Sistema operativo del Equipo", placeholder="Ej. Linux")
            nuevo_procesador = st.text_input("Procesador que tiene el equipo", placeholder="Ej. Intel aceleron...")
            nuevo_almacenamiento = st.text_input("Espacio de almacenamiento", value="256GB")
            nueva_marca = st.text_input("Marca del equipo", placeholder="Ej. Hp")

        nuevo_usuario={
            "nombre":nuevo_nombre,
            "edad":int(nueva_edad)
        }
        fecha_datetime = datetime.combine(
          nueva_fecha,
          datetime.min.time()
        )
        nuevo_monto=10*(nuevo_tiempo/60)
        nueva_informacion={
            "fecha_compra":fecha_datetime,
            "componentes_cambiados":nuevo_componente,
            "sistema_operativo":nuevo_sistema,
            "procesador":nuevo_procesador,
            "almacenamiento":nuevo_almacenamiento,
            "marca_equipo":nueva_marca
        }
        boton_guardar = st.form_submit_button("Guardar Producto")
        if boton_guardar:
            if nuevo_nombre.strip() == "":
                st.error("El nombre no puede estar vacío.")
            else:
                nuevo_documento = {
                    "id_equipo": int(nuevo_id),
                    "usuario": nuevo_usuario,
                    "tiempo_uso": int(nuevo_tiempo),
                    "precio_hora": 10,
                    "monto_total": float(nuevo_monto),
                    "aplicaciones_usadas": nuevas_aplicaciones,
                    "informacion_extra": nueva_informacion,
                    "elementos_acompañantes": nuevos_elementos
                }
                coleccion_b.insert_one(nuevo_documento)
                st.success("Nuevo equipo agregado con exito 🥳")
                st.rerun()

    with tab_editar:
      st.header("Modificar un Producto Existente")

      if documentos:
        opciones_equipos ={f"(ID: {doc['id_equipo']} {doc['usuario']['nombre']})": doc for doc in documentos}
        seleccion = st.selectbox("Selecciona el producto a editar:", opciones_equipos.keys())
        equipo_actual = opciones_equipos[seleccion]

        with st.form("form_actualizar"):
            col1, col2 = st.columns(2)
            with col1:
                edit_nombre = st.text_input("Nombre del Usuario que usara el equipo", value=equipo_actual.get('usuario').get('nombre'))
                edit_edad = st.number_input("Edad del ", min_value=0, step=1, value=int(equipo_actual.get('usuario').get('edad')))
                edit_tiempo = st.number_input("Tiempo de uso en minutos", min_value=0, step=1, value=int(equipo_actual.get('tiempo_uso')))
                edit_aplicaciones = st.text_input("Aplicaciones que se usaron", value=equipo_actual.get('aplicaciones_usadas'))
                edit_elementos = st.text_input("Elementos que acompañan al equipo", value=equipo_actual.get('elementos_acompanantes'))
            with col2:
                edit_componente = st.text_input("Componentes que quieras editar en el equipo", value=equipo_actual.get('informacion_extra').get('componentes_cambiados'))
                edit_sistema = st.text_input("Sistema operativo del Equipo",value=equipo_actual.get('informacion_extra').get('sistema_operativo'))
                edit_procesador = st.text_input("Procesador que tiene el equipo",value=equipo_actual.get('informacion_extra').get('procesador'))
                edit_almacenamiento = st.text_input("Espacio de almacenamiento", value=equipo_actual.get('informacion_extra').get('almacenamiento'))
                edit_marca = st.text_input("Marca del equipo", value=equipo_actual.get('informacion_extra').get('marca_equipo'))

                fecha_guardada = equipo_actual.get('informacion_extra').get('fecha_compra', datetime.now())
                if isinstance(fecha_guardada, str):
                    fecha_guardada = datetime.fromisoformat(fecha_guardada.replace("Z", ""))

                edit_fecha = st.date_input("Fecha de Compra", value=fecha_guardada)

            edit_usuario={
              "nombre":edit_nombre,
              "edad":int(edit_edad)
            }
            informacion_editada={
              "fecha_compra":edit_fecha,
              "componentes_cambiados":edit_componente,
              "sistema_operativo":edit_sistema,
              "procesador":edit_procesador,
              "almacenamiento":edit_almacenamiento,
              "marca_equipo":edit_marca
            }
            edit_monto=10*(nuevo_tiempo/60)
            boton_actualizar = st.form_submit_button("Actualizar Cambios")
            if boton_actualizar:
                coleccion_b.update_one(
                    {"_id": equipo_actual["_id"]},
                    {"$set": {
                        "usuario": edit_usuario,
                        "tiempo_uso": int(edit_tiempo),
                        "precio_hora": 10,
                        "monto_total": float(edit_monto),
                        "aplicaciones_usadas": edit_aplicaciones,
                        "informacion_extra": informacion_editada,
                        "elementos_acompañantes": edit_elementos
                    }}
                )
                st.success("Equipo actualizado!")
                st.rerun()
      else:
        st.info("No hay Equipos disponibles para editar.")



# 2. Definir las opciones del menú
menu = ["Zona 1", "Zona 2", "Zona 3"]

# 3. Crear el menú desplegable (selectbox)
elección = st.selectbox("Selecciona una opción:", menu)

# 4. Mostrar contenido según la selección
if elección == "Zona 1":
    st.subheader("Primera zona: Equipos Basicos")
    st.write("Aqui se encuentran registrados los equipos de la primer zona.")
    Equipo_Basico()

elif elección == "Zona 2":
    st.subheader("Segunda Zona: Gaming")
    st.write("Aquí se encuentran los equipo de la segunda zona.")
    Equipo_Gaming()


elif elección == "Zona 3":
    st.subheader("Tercera Zona: Trabajo(Zona Insonora)")
    st.write("Aqui se encuentran los equipos de la tercer zona")
    Equipo_Trabajo()

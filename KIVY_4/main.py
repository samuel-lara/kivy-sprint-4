from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
from kivymd.uix.list import ThreeLineIconListItem, IconLeftWidget #import para crear listas (cambia dependiendo de los campos que queremos que tenga la lista), le pasamos diferentes imports de la misma biblioteca
import json #importamos la libreria de python que nos permite trabajar con json
from pathlib import Path #cargar ruta del script


class ContentNavigationDrawer(MDBoxLayout):
    manager = ObjectProperty()
    nav_drawer = ObjectProperty()  

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        
class SearchE4(MDTextField): 
    def calc(self, item):
        print(item)
        app = MDApp.get_running_app()
        script_location = Path(__file__).absolute().parent #indicamos donde se encuentra el archivo actual
        with open(script_location / "tareas.json","rt") as json_file: #abre el archivo en modo texto, en este caso el json de donde sacamos los datos
            data3 = json.load(json_file) #guardamos en una variable los datos del json cargados
            
        # Filtramos los datos según el texto de búsqueda
        search_results = [search_text for search_text in data3 if item.lower() in search_text['name'].lower()]
        print(search_results)

        # Actualizamos la lista de resultados de búsqueda en la interfaz de usuario
        search_results_list = app.root()
        print(search_results_list)
        search_results_list.clear_widgets()

        for result in search_results:
            search_results_list.add_widget(
                OneLineIconListItem( #método que nos deja trabajar con 3 lineas que previamente lo hemos importado en la parte superior
                    IconLeftWidget( #método que nos permite agregar un icono
                        icon="table"
                    ),
                    
                    id = f"Tarea {result['id']}",
                    text = f"Tarea {result['name']}",
                    secondary_text=f"Descripcion {result['descripcion']}", #línea 2
                )
            )
            
            # self.clear_widgets() #borramos todos los widgets del widget de texto
            
            # self.add_widget( #añade widgets, despues de ids. va el id con el que podremos trabajar en el documento .kv
            #     OneLineIconListItem( #método que nos deja trabajar con 3 lineas que previamente lo hemos importado en la parte superior
            #         IconLeftWidget( #método que nos permite agregar un icono
            #             icon="table"
            #         ),
                    
            #         id = f"Tarea {i['id']}",
            #         text = f"Tarea {i['name']}",
            #         secondary_text=f"Descripcion {i['descripcion']}", #línea 2
            #     )
            # )## Lista que muestra los cuestionarios
            
            # if name == item: #comprovamos si id es igual a id_tasca
            #     break   #si los valores son iguales generamos un break en la ejecución del código


class MyApp (MDApp):    
    def build(self):
        self.title = "PymeShield"
        if platform in ['win', 'linux', 'macosx']:
            Window.size = (400, 600)
        else:
            Window.size = (400, 600)
        
        return Builder.load_file("main2.kv")
    def root(self):
        self.sm = self.root.ids.tareas
        
    id_tasca = "" #creamos una variable vacia
    def detalles(self,row): #inicializamos una función con el parametro row
        id_tasca = row.id #le damos un valor a id_tasca que recuperamos del parametro de la función
        print(f"Pressed {row.id}") #imprimimos el valor
        self.root.ids['screen_manager'].current = "DetallesTarea" #instruccion donde ruteamos con la pantalla que ha de verse
        script_location = Path(__file__).absolute().parent #indicamos donde se encuentra el archivo actual
        with open(script_location / "tareas.json","rt") as json_file: #abre el archivo en modo texto, en este caso el json de donde sacamos los datos
            data2 = json.load(json_file) #guardamos en una variable los datos del json cargados
        id_tasca = row.id[5:] #asignamos un valor a id_tasca accediendo con el parametro row y con id que es un campo del json
        print(id_tasca) #imprimos el valor de id_tasca

        for i in data2: #recorremos los valores de la variable data2 que guarda los datos del json
            id = i['id'] #asignamos el nuevo valos a la variable id
            text= f"{i['name']} - {i['descripcion']}" #asignamos un nuevo valor a la variable text recuperando datos del archivo json

            self.root.ids.desc.text = text #damos valor a la variable

            if id == id_tasca: #comprovamos si id es igual a id_tasca
                break   #si los valores son iguales generamos un break en la ejecución del código

    id_presupost = ""
    def detallesPre(self,row):
        id_presupost = row.id
        print(f"Pressed {row.id}")
        self.root.ids['screen_manager'].current = "DetallesPresupuesto"
        script_location = Path(__file__).absolute().parent 
        with open(script_location / "data.json","rt") as json_file:
            data = json.load(json_file)
        id_presupost = row.id[10:]
        print(id_presupost)

        for i in data:
            id = i['id']
            text= f"{i['name']} - {i['preu']} - {i['data']}"

            self.root.ids.preudata.text = text

            if id == id_presupost:
                break

   
        def calc(self, instance, text):
                print(text)

    

    def on_start(self): #creamos la clase on_start
        #sirve para que cargue bien el json desde cualquier directorio
        script_location = Path(__file__).absolute().parent 
        # Cargamos los datos desde el archivo data.json
        with open(script_location / "data.json","rt") as json_file:
            data = json.load(json_file)

        with open(script_location / "tareas.json","rt") as json_file:
            data2 = json.load(json_file)

        #print(data)
                
        for i in data: #bucle que recorre el rango que le pasemos como parametro
            self.root.ids.presupuesto.add_widget( #añade widgets, despues de ids. va el id con el que podremos trabajar en el documento .kv
                ThreeLineIconListItem( #método que nos deja trabajar con 3 lineas que previamente lo hemos importado en la parte superior
                    IconLeftWidget( #método que nos permite agregar un icono
                        icon="account-cash"
                    ),
                    
                    text = f"Presupuesto {i['id']}",
                    secondary_text=f"Nombre {i['name']}", #línea 2
                    tertiary_text=f"Precio {i['preu']}", #línea 3
                    # quartiary_text=f"Fecha {i['data']}", #línea 4
                    on_press = self.detallesPre


                )
            )## Lista que muestra los cuestionarios

    
        #print(data)
                
        for i in data2: #bucle que recorre el rango que le pasemos como parametro
            self.root.ids.tareas.add_widget( #añade widgets, despues de ids. va el id con el que podremos trabajar en el documento .kv
                ThreeLineIconListItem( #método que nos deja trabajar con 3 lineas que previamente lo hemos importado en la parte superior
                    IconLeftWidget( #método que nos permite agregar un icono
                        icon="table"
                    ),
                    
                    id = f"Tarea {i['id']}",
                    text = f"Tarea {i['name']}",
                    secondary_text=f"Descripcion {i['descripcion']}", #línea 2
                    on_press = self.detalles
                )
            )## Lista que muestra los cuestionarios
            
MyApp().run()

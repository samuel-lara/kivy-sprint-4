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

# Esta clase es la clase que se encarga de las acciones que va a realizar el buscador.
class SearchE4(MDTextField): 
    # Variable que utilizaremos para acceder a la applicacion que esta ejecutada.
    app = MDApp.get_running_app()
    def calc(self, item):
        
        #variable que guarda el resultado el método getTareasData()
        dataTareas = app.getTareasData()
            
        # Filtramos los datos según el texto de búsqueda
        search_results = [search_text for search_text in dataTareas if item.lower() in search_text['name'].lower()]

        # Actualizamos la lista de resultados de búsqueda en la interfaz de usuario
        search_results_list = app.getTaresScreen()
        # Borramos todos los elementos de la lista
        search_results_list.clear_widgets()

        for result in search_results:
            search_results_list.add_widget(
                OneLineIconListItem( #método que nos deja trabajar con 1 linea que previamente lo hemos importado en la parte superior
                    IconLeftWidget( #método que nos permite agregar un icono
                        icon="clipboard-list"
                    ),
                    
                    id = f"Tarea {result['id']}",
                    text = f"Tarea {result['name']}",
                    secondary_text=f"Descripcion {result['descripcion']}",
                )
            )


    def filterBudget(self, item):
        
        #variable que guarda el resultado el método getPresuData()
        dataPresu = app.getPresuData()
            
        # Filtramos los datos según el texto de búsqueda
        search_results = [search_text for search_text in dataPresu if item.lower() in search_text['name'].lower()]

        # Actualizamos la lista de resultados de búsqueda en la interfaz de usuario
        search_results_list = app.getBudgetsScreen()
        # Borramos todos los elementos de la lista
        search_results_list.clear_widgets()

        for result in search_results:
            search_results_list.add_widget(
                OneLineIconListItem( #método que nos deja trabajar con 1 linea que previamente lo hemos importado en la parte superior
                    IconLeftWidget( #método que nos permite agregar un icono
                        icon="account-cash"
                    ),
                    
                    text = f"Presupuesto {result['id']}",
                    secondary_text=f"Nombre {result['name']}", 
                    tertiary_text=f"Precio {result['preu']}", 
                )
            )

class MainApp (MDApp):  
    
    # Variable global que contendrá self.root
    sm = None
    # Variable global que contendrá les dades del JSON de presupostos
    dataJsonPresu = None
    # Variable global que contendrá les dades del JSON de tasques
    dataJsonTask = None
    #indicamos donde se encuentra el archivo actual
    rutaPath = None
      
    def build(self):
        
        self.title = "PymeShield"
        if platform in ['win', 'linux', 'macosx']:
            Window.size = (400, 600)
        else:
            Window.size = (400, 600)
        
        #variables globales utilatarias
        self.sm = self.root
        self.rutaPath = script_location = Path(__file__).absolute().parent
        
       
    # Método que utilizaremos para situarnos en la screen de tareas mediante id.
    def getTaresScreen(self):
        return self.sm.ids.tareas
    
    # Método que utilizaremos para situarnos en la screen de presupuesto mediante id.
    def getBudgetsScreen(self):
        return self.sm.ids.presupuesto
    
    #Método que utilizaremos para recoger los datos del Json de Tareas y guardarlos 
    def getTareasData(self):
        self.dataJsonTask = None
        with open(self.rutaPath / "tareas.json","rt") as json_file: #abre el archivo en modo texto, en este caso el json de donde sacamos los datos
            self.dataJsonTask = json.load(json_file) #guardamos en una variable los datos del json cargados
        return self.dataJsonTask
    
    #Método que utilizaremos para recoger los datos del Json de Presupuestos y guardarlos 
    def getPresuData(self):
        self.dataJsonPresu = None
        with open(self.rutaPath / "data.json","rt") as json_file: #abre el archivo en modo texto, en este caso el json de donde sacamos los datos
            self.dataJsonPresu = json.load(json_file) #guardamos en una variable los datos del json cargados
        return self.dataJsonPresu
        
    id_tasca = "" #creamos una variable vacia
    def detalles(self,row): #inicializamos una función con el parametro row
        id_tasca = row.id #le damos un valor a id_tasca que recuperamos del parametro de la función
        print(f"Pressed {row.id}") #imprimimos el valor
        self.root.ids['screen_manager'].current = "DetallesTarea" #instruccion donde ruteamos con la pantalla que ha de verse
        dataTareas = self.getTareasData()
        id_tasca = row.id[5:] #asignamos un valor a id_tasca accediendo con el parametro row y con id que es un campo del json
        print(id_tasca) #imprimos el valor de id_tasca

        for i in dataTareas: #recorremos los valores de la variable data2 que guarda los datos del json
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
        dataPresu = self.getPresuData()
        id_presupost = row.id[10:]
        print(id_presupost)

        for i in dataPresu:
            id = i['id']
            text= f"{i['name']} - {i['preu']} - {i['data']}"

            self.root.ids.preudata.text = text

            if id == id_presupost:
                break

   
        def calc(self, instance, text):
                print(text)

    

    def on_start(self): #creamos la clase on_start
        #sirve para que cargue bien el json desde cualquier directorio
        dataTareas = self.getTareasData()

        dataPresu = self.getPresuData()

        #print(data)
                
        for i in dataPresu: #bucle que recorre el rango que le pasemos como parametro
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
                
        for i in dataTareas: #bucle que recorre el rango que le pasemos como parametro
            self.root.ids.tareas.add_widget( #añade widgets, despues de ids. va el id con el que podremos trabajar en el documento .kv
                ThreeLineIconListItem( #método que nos deja trabajar con 3 lineas que previamente lo hemos importado en la parte superior
                    IconLeftWidget( #método que nos permite agregar un icono
                        icon="clipboard-list"
                    ),
                    
                    id = f"Tarea {i['id']}",
                    text = f"Tarea {i['name']}",
                    secondary_text=f"Descripcion {i['descripcion']}", #línea 2
                    on_press = self.detalles
                )
            )## Lista que muestra los cuestionarios
            
if __name__ == '__main__':
    app = MainApp()
    app.run()

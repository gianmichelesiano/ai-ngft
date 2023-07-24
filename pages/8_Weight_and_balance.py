import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from matplotlib.patches import Polygon
from pages.api.client import create_supabase_client
from pages.api.shap import get_result
import json
import ast

def crea_poligono(coordinate):
    poligono = Polygon(coordinate)
    return poligono

def punto_in_poligono(x_in, y_in, coordinate_poligono):
    poligono = crea_poligono(coordinate_poligono)
    punto = Point(x_in, y_in)
    if poligono.contains(punto):
        return True
    else:
        return False


def disegna_poligono_e_punto( x_in, y_in, poligono):
    punto = (x_in, y_in)
    # Creazione del grafico
    fig, ax = plt.subplots()

    # Disegno del poligono
    poligono_patch = Polygon(poligono, closed=True, alpha=0.3)
    ax.add_patch(poligono_patch)
    
    # Disegno del punto
    x, y = punto
    ax.plot(x, y, 'ro')

    # Impostazioni degli assi
    ax.set_xlabel('LOADED HELICOPTER MOMENT')
    ax.set_ylabel('LOADED HELICOPTER WEIGHT')
    ax.set_xlim([min(x for x, y in poligono) - 10, max(x for x, y in poligono) + 10])
    ax.set_ylim([min(y for x, y in poligono) - 100, max(y for x, y in poligono) + 100])

    ax.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    
    # Visualizzazione del grafico
    plt.grid(True)
    st.pyplot(fig)
    

def back_to_enter_point():
    st.session_state.new_poligon = False
    st.session_state.enter_point = True

def new_polygon():
    st.session_state.new_poligon = True
    st.session_state.enter_point = False
    
    
def initialize_session_state():
    if "new_poligon" not in st.session_state:
        st.session_state.new_poligon = False
    if "enter_point" not in st.session_state:
        st.session_state.enter_point = True

def insert_polygon():
    try:
        supabase = create_supabase_client()
        response = supabase.table('polygon').insert({"name": name_polygon, "coordinate": str(coordinate_poligono)}).execute()
        st.success("Inserted polygon")
    except Exception as e:
        print(e)
        st.warning("Error in insert polygon")
    
# Parse the string into a list of tuples
def convert_to_list(string_data):
    list_data = ast.literal_eval(string_data)
    # Convert the elements of each tuple to floats
    list_of_tuples_of_floats = [tuple(float(val) for val in tpl) for tpl in list_data]
    return list_of_tuples_of_floats

def get_polygon():
    supabase = create_supabase_client()
    response = supabase.table('polygon').select('name','coordinate').execute()
    return response.data


def get_coordinate_polygon(polygons, name_polygon):
    for d in polygons:
        if d['name'] == name_polygon:
            selected_dict = d
            break
    return selected_dict['coordinate']


# Disegno del poligono e del punto
def execute_design(x, y, coordinate_poligono):
    risultato = get_result(x, y, coordinate_poligono)
    if (risultato):
        st.success("The point is inside the polygon")
    else:
        st.warning("The point is outside the polygon")
    disegna_poligono_e_punto( x, y, coordinate_poligono)



initialize_session_state()
# Funzione principale dell'applicazione Streamlit
st.title("Application for viewing a polygon and a point")

if st.session_state.new_poligon:
    # Input dei dati
    st.header("Enter the new polygon")
    st.button("Back to enter point", on_click=back_to_enter_point)
    coordinate_poligono = []
    name_polygon = st.text_input("Name", key="name_polygon")
    num_coordinate = st.number_input("Number of polygon coordinates", min_value=3, step=1, key="num_coordinate")
    for i in range(num_coordinate):
        col1, col2 = st.columns(2)
        x = col1.number_input(f"x coordinate of the point {i+1}", key=f"x_{i}")
        y = col2.number_input(f"y coordinate of the point {i+1}", key=f"y_{i}")
        coordinate_poligono.append((x, y))
    st.button("Insert polygon", key="insert_polygon", on_click=insert_polygon)
    
if st.session_state.enter_point:
    polygons = get_polygon()
    st.button("Add a new polygon", on_click=new_polygon)
    if len(polygons) > 0:
        names_polygon = [i['name'] for i in polygons]
        
        name_polygon = st.selectbox(
            'Select Polygon',
            (names_polygon))
        coordinate_poligono = get_coordinate_polygon(polygons, name_polygon)
        st.write('Coordinate polygon:', coordinate_poligono)
        
        st.header("Enter the point")
        col1, col2 = st.columns(2)
        x = col1.number_input("x coordinate of the point", key="x")
        y = col2.number_input("y coordinate of the point", key="y")
        punto = (x, y)

        
        if st.button("Calculate and draw", key="calculate"):
            execute_design(x,y,convert_to_list(coordinate_poligono))






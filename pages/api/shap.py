from shapely.geometry import Point, Polygon

# Definisci le coordinate del poligono

def get_result(x_in, y_in, c_pol):
    c_pt = (x_in, y_in)

    poly = Polygon(c_pol)
    # Crea un oggetto Point utilizzando le coordinate del punto
    pt = Point(c_pt)
    # Verifica se il punto è all'interno del poligono utilizzando il metodo contains()
    if poly.contains(pt):
        val = True
    else:
        val = False
    return val
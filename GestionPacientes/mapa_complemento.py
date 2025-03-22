import os
from graphviz import Digraph

def generar_mapa():
    dot = Digraph(format="png")

    # Definir nodos principales
    dot.node("VC", "Vía Clásica", shape="box", style="filled", fillcolor="lightblue")
    dot.node("VL", "Vía de las Lectinas", shape="box", style="filled", fillcolor="lightblue")
    dot.node("VA", "Vía Alternativa", shape="box", style="filled", fillcolor="lightblue")

    # Convertasas y C5a
    dot.node("C3", "C3 Convertasa", style="filled", fillcolor="red")
    dot.node("C5", "C5a", style="filled", fillcolor="green")

    # Conexiones entre vías y convertasas
    dot.edge("VC", "C3")
    dot.edge("VL", "C3")
    dot.edge("VA", "C3")
    dot.edge("C3", "C5")

    # Guardar en la carpeta 'static'
    ruta_imagen = os.path.join("static", "mapa_complemento")
    dot.render(ruta_imagen)

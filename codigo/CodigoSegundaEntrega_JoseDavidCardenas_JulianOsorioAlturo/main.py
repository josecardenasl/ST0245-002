import pandas as pd
import folium

dato = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')
Principal = dato['harassmentRisk'].mean()
dato['ha|moñrassmentRisk'].fillna(Principal, inplace=True)

def CrearGrafico():
    grafico = {}
    for i in dato.index:
        ListaOriginal = list(dato['origin'][i][1:-1].split(','))
        ListaOriginal[0], ListaOriginal[1] = float(ListaOriginal[1]), float(ListaOriginal[0])
        TuplaOriginal = tuple(ListaOriginal)

        destino = list(dato['destination'][i][1:-1].split(','))
        destino[0], destino[1] = float(destino[1]), float(destino[0])
        TuplaDestino  = tuple(destino)

        try:
            if dato['oneway'][i]:
                grafico[TuplaOriginal].update({TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])})
                grafico[TuplaDestino].update({TuplaOriginal: (dato['length'][i], dato['harassmentRisk'][i])})
            else:
                grafico[TuplaOriginal].update({TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])})
        except KeyError:
            if dato['oneway'][i]:
                if TuplaOriginal not in grafico and TuplaDestino not in grafico:
                    grafico[TuplaOriginal] = {TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])}
                    grafico[TuplaDestino] = {TuplaOriginal: (dato['length'][i], dato['harassmentRisk'][i])}
                elif TuplaDestino not in grafico:
                    grafico[TuplaOriginal].update({TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])})
                    grafico[TuplaDestino] = {TuplaOriginal: (dato['length'][i], dato['harassmentRisk'][i])}
                else:
                    grafico[TuplaDestino].update({TuplaOriginal: (dato['length'][i], dato['harassmentRisk'][i])})
                    grafico[TuplaOriginal] = {TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])}
            else:
                if TuplaOriginal not in grafico:
                    grafico[TuplaOriginal] = {TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])}
                else:
                    grafico[TuplaOriginal].update({TuplaDestino: (dato['length'][i], dato['harassmentRisk'][i])})

    return grafico

grafico = CrearGrafico()


def bellman(grafico,Ini,Meta):
    DistanciaCorta = {}
    Anterior = {}
    NodosInvi = grafico
    Limite = 9999999
    Camino = []
    for Nodo in NodosInvi:
        DistanciaCorta[Nodo] = Limite
    DistanciaCorta[Ini] = 0

    while NodosInvi:
        MiNodo = None
        for Nodo in NodosInvi:
            if MiNodo is None:
                MiNodo = Nodo
            elif DistanciaCorta[Nodo] < DistanciaCorta[MiNodo]:
                MiNodo = Nodo

        for NodoHijo, weight in grafico[MiNodo].items():
            if weight[0] + DistanciaCorta[MiNodo] < DistanciaCorta[NodoHijo]:
                DistanciaCorta[NodoHijo] = weight[0] + DistanciaCorta[MiNodo]
                Anterior[NodoHijo] = MiNodo
        NodosInvi.pop(MiNodo)

    currentnode = Meta
    while currentnode != Ini:
        try:
            Camino.insert(0,currentnode)
            currentnode = Anterior[currentnode]
        except KeyError:
            return 'No Se Puede Acceder Al Camino'
    Camino.insert(0,Ini)
    if DistanciaCorta[Meta] != Limite:
        return Camino

Camino = bellman(grafico,(6.2734442, -75.5443961),(6.2094357, -75.5674348))

def CrearMapa(Camino):
    Mapa = folium.Map(location=[Camino[0][0], Camino[0][1]], zoom_start=14)
    folium.PolyLine(Camino, color='green', weigth=14, opacity=0.9).add_to(Mapa)
    Mapa.save('index.html')

CrearMapa(Camino)


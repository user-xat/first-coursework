import owlready2 as owl
import igraph as ig
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px


class OwlRead:
    __PROP = ['hasBirthDay', 'hasDate', 'hasDomain', 'hasFirstName', 'hasLastName', 'hasGender', 'hasName', 'hasPhoto',
              'hasTag', 'isAds']
    __CONNECT = ['friendsWith', 'hasActivity', 'hasSubscriber', 'isRepostOf', 'liked', 'likedBy', 'posted', 'postedBy',
                 'subscribedTo', 'viewed', 'viewedBy']

    @staticmethod
    def __read_owl_file(path) -> list:
        data = list()
        onto = owl.get_ontology("file://" + path).load()
        for oclass in onto.classes():
            instances = list()
            for instance in oclass.instances():
                properties = dict()
                connections = dict()
                for prop in instance.get_properties():
                    if prop.name in OwlRead.__PROP:
                        properties[prop.name] = prop[instance][0]
                    elif prop.name in OwlRead.__CONNECT:
                        connections[prop.name] = prop[instance]
                properties["class"] = oclass.name
                instances.append((instance.name, properties, connections))
            data += instances
        return data

    @staticmethod
    def __create_graph(data: list) -> ig.Graph:
        g = ig.Graph(directed=True)
        for node, prop, _ in data:
            g.add_vertices([node], prop)

        for node, _, typesConn in data:
            for type, conns in typesConn.items():
                for conn in conns:
                    g.add_edge(node, conn.name, name=type)
        return g

    @staticmethod
    def create_graph_from_onto(path: str) -> ig.Graph:
        data = OwlRead.__read_owl_file(path)
        graph = OwlRead.__create_graph(data)
        return graph


class Charts:
    __LABELS = {
        'Class': 'Класс',
        'Degree': 'Степени вершин',
        'PageRank':'PageRank',
        'Betweenness': 'Степень посредничества',
        'Closeness': 'Степень близости',
        'Eigenvector_centrality': 'Степень влиятельности'
    }

    def __init__(self, path: str):
        self.__graph = OwlRead.create_graph_from_onto(path)
        self.__df = pd.DataFrame({
            'Name': self.__graph.vs['name'],
            'Class': self.__graph.vs['class'],
            'Degree': self.__graph.degree(),
            'PageRank': self.__graph.pagerank(),
            'Betweenness': self.__graph.betweenness(),
            'Closeness': self.__graph.closeness(),
            'Eigenvector_centrality': self.__graph.eigenvector_centrality()
        })

    def scatter_plots(self, values: list):
        if len(values) == 2:
            fig = px.scatter(self.__df, x=values[0], y=values[1], color='Class', hover_name='Name', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 3:
            fig = px.scatter(self.__df, x=values[0], y=values[1], size=values[2], log_x=True, size_max=60,
                             labels=Charts.__LABELS, color='Class', hover_name='Name')
            fig.show()
        elif len(values) == 4:
            fig = px.scatter(self.__df, x=values[0], y=values[1], size=values[2], color=values[3],
                             log_x=True, size_max=60, hover_name='Name', symbol='Class', labels=Charts.__LABELS)
            fig.show()

    def scatter_matrix(self, values: list):
        if len(values) > 1:
            fig = px.scatter_matrix(self.__df, dimensions=values, color="Class", labels=Charts.__LABELS)
            fig.show()

    def scatter_3d(self, values: list):
        if len(values) == 3:
            fig = px.scatter_3d(self.__df, x=values[0], y=values[1], z=values[2], color="Class",
                                hover_name='Name', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 4:
            fig = px.scatter_3d(self.__df, x=values[0], y=values[1], z=values[2], size=values[3],
                                size_max=50, color='Class', hover_name='Name', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 5:
            fig = px.scatter_3d(self.__df, x=values[0], y=values[1], z=values[2], size=values[3], color=values[4],
                                size_max=50, symbol='Class', hover_name='Name', labels=Charts.__LABELS)
            fig.show()

    def histogram(self, values: list):
        if len(values) == 1:
            fig = px.histogram(self.__df, x=values[0], hover_name='Name', color='Class', labels=Charts.__LABELS)
            fig.show()

    def bar(self, values: list):
        if len(values) == 1:
            fig = px.bar(self.__df, y=values[0], hover_name='Name', color='Class', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 2:
            fig = px.bar(self.__df, x=values[0], y=values[1], hover_name='Name', color='Class', labels=Charts.__LABELS)
            fig.show()

    def line(self, values: list):
        if len(values) == 1:
            fig = px.line(self.__df.sort_values(by=values[0]), x=values[0], color='Class',
                          symbol="Class", hover_name='Name', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 2:
            fig = px.line(self.__df.sort_values(by=values[0]), x=values[0], y=values[1], color='Class',
                          symbol="Class", hover_name='Name', labels=Charts.__LABELS)
            fig.show()

    def line_3d(self, values: list):
        if len(values) == 3:
            fig = px.line_3d(self.__df.sort_values(by=values[0]), x=values[0], y=values[1], z=values[2],
                             color='Class', hover_name='Name', symbol='Class', labels=Charts.__LABELS)
            fig.show()
        # elif len(values) == 4:
        #     fig = px.line_3d(self.df.sort_values(by=values[0]), x=values[0], y=values[1], z=values[2], color=values[3],
        #                      hover_name='Name', symbol='Class', labels=Charts.labels)
        #     fig.show()

    def ternary(self, values: list):
        if len(values) == 3:
            fig = px.scatter_ternary(self.__df, a=values[0], b=values[1], c=values[2],
                                     hover_name='Name', color='Class', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 4:
            fig = px.scatter_ternary(self.__df, a=values[0], b=values[1], c=values[2], size=values[3],
                                     size_max=40, hover_name='Name', color='Class', labels=Charts.__LABELS)
            fig.show()
        elif len(values) == 5:
            fig = px.scatter_ternary(self.__df, a=values[0], b=values[1], c=values[2], size=values[3], color=values[4],
                                     size_max=40, hover_name='Name', symbol='Class', labels=Charts.__LABELS)
            fig.show()
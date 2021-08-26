import owlready2 as owl
import igraph as ig
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px


class OwlRead:
    PROP = ['hasBirthDay', 'hasDate', 'hasDomain', 'hasFirstName', 'hasLastName', 'hasGender', 'hasName', 'hasPhoto',
            'hasTag', 'isAds']
    CONNECT = ['friendsWith', 'hasActivity', 'hasSubscriber', 'isRepostOf', 'liked', 'likedBy', 'posted', 'postedBy',
               'subscribedTo', 'viewed', 'viewedBy']

    @staticmethod
    def read_owl_file(path):
        data = list()
        onto = owl.get_ontology("file://" + path).load()
        for oclass in onto.classes():
            instances = list()
            for instance in oclass.instances():
                properties = dict()
                connections = dict()
                for prop in instance.get_properties():
                    if prop.name in OwlRead.PROP:
                        properties[prop.name] = prop[instance][0]
                    elif prop.name in OwlRead.CONNECT:
                        connections[prop.name] = prop[instance]
                properties["class"] = oclass.name
                instances.append((instance.name, properties, connections))
            data += instances
        return data


class Graph:
    @staticmethod
    def create_graph_from_onto(data):
        g = ig.Graph(directed=True)
        for node, prop, _ in data:
            g.add_vertices([node], prop)

        for node, _, typesConn in data:
            for type, conns in typesConn.items():
                for conn in conns:
                    g.add_edge(node, conn.name, name=type)
        return g


class Charts:
    labels = {
        'Class': 'Класс',
        'Degree': 'Степени вершин',
        'PageRank':'PageRank',
        'Betweenness': 'Степень посредничества',
        'Closeness': 'Степень близости',
        'Eigenvector_centrality': 'Степень влиятельности'
    }
    def __init__(self, path):
        data = OwlRead.read_owl_file(path)
        self.graph = Graph.create_graph_from_onto(data)
        self.df = pd.DataFrame({
            'Name': self.graph.vs['name'],
            'Class': self.graph.vs['class'],
            'Degree': self.graph.degree(),
            'PageRank': self.graph.pagerank(),
            'Betweenness': self.graph.betweenness(),
            'Closeness': self.graph.closeness(),
            'Eigenvector_centrality': self.graph.eigenvector_centrality()
        })

    def scatter_plots(self, values: list):
        if len(values) == 2:
            fig = px.scatter(self.df, x=values[0], y=values[1], color='Class', hover_name='Name', labels=Charts.labels)
            fig.show()
        elif len(values) == 3:
            fig = px.scatter(self.df, x=values[0], y=values[1], size=values[2], log_x=True, size_max=60,
                             labels=Charts.labels, color='Class', hover_name='Name')
            fig.show()
        elif len(values) == 4:
            fig = px.scatter(self.df, x=values[0], y=values[1], size=values[2], color=values[3],
                             log_x=True, size_max=60, hover_name='Name', symbol='Class', labels=Charts.labels)
            fig.show()

    def scatter_matrix(self, values: list):
        if len(values) > 1:
            fig = px.scatter_matrix(self.df, dimensions=values, color="Class", labels=Charts.labels)
            fig.show()

    def scatter_3d(self, values: list):
        if len(values) == 3:
            fig = px.scatter_3d(self.df, x=values[0], y=values[1], z=values[2], color="Class",
                                hover_name='Name', labels=Charts.labels)
            fig.show()
        elif len(values) == 4:
            fig = px.scatter_3d(self.df, x=values[0], y=values[1], z=values[2], size=values[3],
                                size_max=50, color='Class', hover_name='Name', labels=Charts.labels)
            fig.show()
        elif len(values) == 5:
            fig = px.scatter_3d(self.df, x=values[0], y=values[1], z=values[2], size=values[3], color=values[4],
                                size_max=50, symbol='Class', hover_name='Name', labels=Charts.labels)
            fig.show()

    def histogram(self, values: list):
        if len(values) == 1:
            fig = px.histogram(self.df, x=values[0], hover_name='Name', color='Class', labels=Charts.labels)
            fig.show()

    def bar(self, values: list):
        if len(values) == 1:
            fig = px.bar(self.df, y=values[0], hover_name='Name', color='Class', labels=Charts.labels)
            fig.show()
        elif len(values) == 2:
            fig = px.bar(self.df, x=values[0], y=values[1], hover_name='Name', color='Class', labels=Charts.labels)
            fig.show()

    def line(self, values: list):
        if len(values) == 1:
            fig = px.line(self.df.sort_values(by=values[0]), x=values[0], color='Class',
                          symbol="Class", hover_name='Name', labels=Charts.labels)
            fig.show()
        elif len(values) == 2:
            fig = px.line(self.df.sort_values(by=values[0]), x=values[0], y=values[1], color='Class',
                          symbol="Class", hover_name='Name', labels=Charts.labels)
            fig.show()

    def line_3d(self, values: list):
        if len(values) == 3:
            fig = px.line_3d(self.df.sort_values(by=values[0]), x=values[0], y=values[1], z=values[2],
                             color='Class', hover_name='Name', labels=Charts.labels)
            fig.show()
        # elif len(values) == 4:
        #     fig = px.line_3d(self.df.sort_values(by=values[0]), x=values[0], y=values[1], z=values[2], color=values[3],
        #                      hover_name='Name', symbol='Class', labels=Charts.labels)
        #     fig.show()

    def ternary(self, values: list):
        if len(values) == 3:
            fig = px.scatter_ternary(self.df, a=values[0], b=values[1], c=values[2],
                                     hover_name='Name', color='Class', labels=Charts.labels)
            fig.show()
        elif len(values) == 4:
            fig = px.scatter_ternary(self.df, a=values[0], b=values[1], c=values[2], size=values[3],
                                     size_max=40, hover_name='Name', color='Class', labels=Charts.labels)
            fig.show()
        elif len(values) == 5:
            fig = px.scatter_ternary(self.df, a=values[0], b=values[1], c=values[2], size=values[3], color=values[4],
                                     size_max=40, hover_name='Name', symbol='Class', labels=Charts.labels)
            fig.show()
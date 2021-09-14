import owlready2 as owl
import igraph as ig


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

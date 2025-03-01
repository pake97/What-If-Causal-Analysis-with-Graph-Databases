import networkx as nx


def neo4j_to_nx(neo4jConnector):
    """
    Convert a neo4j graph to a networkx graph
    :param neo4jConnector: the neo4j connector
    :return: a networkx graph
    
    1) use apoc to export the entire graph to a csv file
    2) read the csv file and create a df to save instances of nodes and edges
    3) create a networkx graph and add nodes and edges, but using only nodes of type CausalVariable and edges of type CAUSALLY_LINKED
    """
    
    # 1) use apoc to export the entire graph to a csv file
    query = """
    CALL apoc.export.csv.all("graph.csv", {})
    """
    neo4jConnector.merge_query(query)
    
    # 2) read the csv file and create a df to save instances of nodes and edges
    import pandas as pd
    df = pd.read_csv('/Users/amedeo/Downloads/neo4j-community-5.12.0/import/graph.csv')
    
    
    # 3) create a networkx graph and add nodes and edges, but using only nodes of type CausalVariable and edges of type CAUSALLY_LINKED
    
    id_to_name = {}
    
    G = nx.DiGraph()
    for index, row in df.iterrows():
        if row['_labels'] == 'CausalVariable':
            G.add_node(row['name'], type='CausalVariable')
            id_to_name[row['_id']] = row['name']
        elif row['_type'] == 'CAUSALLY_LINKED':
            print(id_to_name)
            start = id_to_name[row['_start']]
            end = id_to_name[row['_end']]
            G.add_edge(start, end, type='CAUSALLY_LINKED', weight=int(row['weight']))
        print(id_to_name)
    return df,G     
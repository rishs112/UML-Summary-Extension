import xml.etree.ElementTree as ET

from uml_geom import parse_classes  

RELATION_MAP = {
    "lt=-": "an association",
    "lt=<-": "a directed association",
    "lt=->": "a directed association",
    "lt=<<-": "an inheritance relationship",
    "lt=->>": "an inheritance relationship",
    "lt=<<<<-": "an aggregation relationship",
    "lt=->>>>": "an aggregation relationship",
    "lt=<<<<<-": "a composition relationship",
    "lt=->>>>>": "a composition relationship",
    "lt=<.": "a dependency",
    "lt=.>": "a dependency"
}

def is_point_in_box(x, y, box, padding=15):
    """
    Checks if an (x, y) coordinate falls within a bounding box.
    Adding 'padding' creates a margin of error for hand-drawn, snapped lines.
    """
    return (box["x_min"] - padding <= x <= box["x_max"] + padding) and \
           (box["y_min"] - padding <= y <= box["y_max"] + padding)

def build_class_graph(classes, relations):
    """
    Compares line endpoints against class boundaries to build a 
    logical list of connections (Edges).
    """
    graph_edges = []
    
    for rel in relations:
        start_x, start_y = rel["start"]
        end_x, end_y = rel["end"]
        
        source_class = None
        target_class = None
        
        for cls in classes:
            if is_point_in_box(start_x, start_y, cls):
                source_class = cls["name"]
            
            if is_point_in_box(end_x, end_y, cls):
                target_class = cls["name"]
                
        # When a valid connection is found
        if source_class and target_class:
            english_meaning = RELATION_MAP.get(rel["style"].strip(), "a relationship")
            
            graph_edges.append({
                "source": source_class,
                "target": target_class,
                "relationship": english_meaning,
                "source_multi": rel["m1"], 
                "target_multi": rel["m2"]  
            })
            
    return graph_edges


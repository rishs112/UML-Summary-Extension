import xml.etree.ElementTree as ET

# Import the specific functions from your custom modules
from text_parser import generate_frequency_map, identify_diagram
from uml_geom import parse_classes, parse_relations
from uml_graph import build_class_graph
from uml_summary import generate_summary

def process_uml_file(filepath):
    
    freq_map = generate_frequency_map(filepath)
    prediction, scores = identify_diagram(freq_map)
        
    # If it's not a class diagram, we stop here.
    if prediction != "Class Diagram":
        print("Note: Summarization is currently only supported for Class Diagrams.")
        return
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return

    classes = parse_classes(root)
    relations = parse_relations(root)
     
    # Connect the dots
    graph_edges = build_class_graph(classes, relations)

    print("\n=======================================================")
    print("                 UML DIAGRAM SUMMARY                   ")
    print("=======================================================")
    
    # Print Level 1 
    print(generate_summary(classes, graph_edges, level=1))
    
    # Prompt for Level 2
    print("-" * 55)
    choice = input("Would you like to see the Structural Outline (Class names and relationships)? (y/n): ").strip().lower()
    
    if choice == 'y':
        print("\n" + generate_summary(classes, graph_edges, level=2))
        
        # Prompt for Level 3
        print("-" * 55)
        choice = input("Would you like a Deep Dive into all internal attributes and methods? (y/n): ").strip().lower()
        
        if choice == 'y':
            print("\n" + generate_summary(classes, graph_edges, level=3))
            
    print("\n=======================================================")
    print("                END OF SUMMARY                         ")
    print("=======================================================\n")
if __name__ == "__main__":
    TARGET_FILE = "test4_class.uxf" 
    
    process_uml_file(TARGET_FILE)
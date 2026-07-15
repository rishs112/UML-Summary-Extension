def parse_classes(root):
    classes = []
    for element in root.findall(".//element"):
        id_node = element.find("id")
        if id_node is not None and id_node.text.strip() == "UMLClass":
            panel_node = element.find("panel_attributes")
            class_name = "UnknownClass"
            is_abstract = False
            
            attributes = [] 
            methods = []

            if panel_node is not None and panel_node.text:
                lines = [l.strip() for l in panel_node.text.split('\n') if l.strip()]
                if lines:
                    raw_name = lines[0]
                    start_idx = 1
                    if raw_name.startswith("/") and raw_name.endswith("/"):
                        is_abstract = True
                        class_name = raw_name[1:-1]
                    elif "<<abstract>>" in raw_name.lower():
                        is_abstract = True
                        if len(lines) > 1:
                            class_name = lines[1]
                            start_idx = 2
                        else:
                            class_name = raw_name.replace("<<abstract>>", "").strip()
                    else:
                        class_name = raw_name

                    for line in lines[start_idx:]:
                        if line == "--": 
                            continue # Skip compartment dividers
                        
                        modifier = "default/package" # fallback
                        if line.startswith("+"): modifier = "public"
                        elif line.startswith("-"): modifier = "private"
                        elif line.startswith("#"): modifier = "protected"
                        elif line.startswith("~"): modifier = "package"

                        # Categorize based on parentheses
                        item_data = {"modifier": modifier, "raw_text": line}
                        if "(" in line and ")" in line:
                            methods.append(item_data)
                        else:
                            attributes.append(item_data)

            # Extract coordinates
            coord_node = element.find("coordinates")
            if coord_node is not None:
                x = int(coord_node.find("x").text)
                y = int(coord_node.find("y").text)
                w = int(coord_node.find("w").text)
                h = int(coord_node.find("h").text)
                
                classes.append({
                    "name": class_name,
                    "is_abstract": is_abstract,
                    "attributes": attributes, 
                    "methods": methods,       
                    "x_min": x, "x_max": x + w,
                    "y_min": y, "y_max": y + h
                })
    return classes

def parse_relations(root):
    relations = []
    for element in root.findall(".//element"):
        id_node = element.find("id")
        if id_node is not None and id_node.text.strip() == "Relation":
            panel_node = element.find("panel_attributes")
            lt_style = ""
            m1 = "" 
            m2 = "" 
            
            if panel_node is not None and panel_node.text:
                for line in panel_node.text.split('\n'):
                    line = line.strip()
                    if line.startswith("lt="): lt_style = line
                    elif line.startswith("m1="): m1 = line.replace("m1=", "").strip()
                    elif line.startswith("m2="): m2 = line.replace("m2=", "").strip()
            
            coord_node = element.find("coordinates")
            attr_node = element.find("additional_attributes")
            
            if coord_node is not None and attr_node is not None and attr_node.text:
                box_x, box_y = int(coord_node.find("x").text), int(coord_node.find("y").text)
                waypoints = [int(val) for val in attr_node.text.split(';') if val.strip()]
                
                if len(waypoints) >= 4:
                    relations.append({
                        "style": lt_style,
                        "m1": m1, # Pass start multiplicity
                        "m2": m2, # Pass end multiplicity
                        "start": (box_x + waypoints[0], box_y + waypoints[1]),
                        "end": (box_x + waypoints[-2], box_y + waypoints[-1])
                    })
    return relations

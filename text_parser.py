import xml.etree.ElementTree as ET
from collections import Counter

def generate_frequency_map(xml_filepath):
    """
    Parses a .uxf file and returns a Counter object detailing the frequency 
    of specific UML elements, sub-types, and key relation styles.
    """
    counts = Counter()
    
    try:
        tree = ET.parse(xml_filepath)
        root = tree.getroot()
    except ET.ParseError:
        return counts # Return empty counter on failure

    for element in root.findall(".//element"):
        # Track that we found a valid Umletino element
        counts["_TOTAL_ELEMENTS_"] += 1 
        
        id_node = element.find("id")
        panel_node = element.find("panel_attributes")
        
        # 1. Count the primary Object IDs
        if id_node is not None and id_node.text:
            uml_id = id_node.text.strip()
            counts[uml_id] += 1
            
        # 2. Dig into panel attributes for sub-types and specific relations
        if panel_node is not None and panel_node.text:
            panel_text = panel_node.text
            
            # Check for special state sub-types
            if "type=decision" in panel_text: counts["type=decision"] += 1
            if "type=initial" in panel_text: counts["type=initial"] += 1
            if "type=final" in panel_text: counts["type=final"] += 1
            if "type=termination" in panel_text: counts["type=termination"] += 1
            
            # Check for diagram-specific relationship arrows
            if "lt=<<<<-" in panel_text or "lt=<<<<<-" in panel_text: 
                counts["class_relation"] += 1
            if "lt=<<<-" in panel_text: 
                counts["sync_message"] += 1

    return counts

def identify_diagram(counts):
    """
    Takes a frequency map and scores it against 5 UML diagram signatures.
    """
    scores = {
        "Use Case Diagram": 0,
        "Class Diagram": 0,
        "Sequence Diagram": 0,
        "Activity Diagram": 0,
        "State Machine Diagram": 0
    }
    
    # --- USE CASE SIGNATURE ---
    scores["Use Case Diagram"] += counts.get("UMLActor", 0) * 50
    scores["Use Case Diagram"] += counts.get("UMLUseCase", 0) * 50
    
    # --- CLASS SIGNATURE ---
    scores["Class Diagram"] += counts.get("UMLClass", 0) * 50
    scores["Class Diagram"] += counts.get("UMLPackage", 0) * 30
    scores["Class Diagram"] += counts.get("class_relation", 0) * 40
    
    # --- SEQUENCE SIGNATURE ---
    scores["Sequence Diagram"] += counts.get("UMLGeneric", 0) * 30
    scores["Sequence Diagram"] += counts.get("sync_message", 0) * 30
    scores["Sequence Diagram"] += counts.get("type=termination", 0) * 40
    
    # --- ACTIVITY VS STATE MACHINE ---
    base_state_score = counts.get("UMLState", 0) * 20
    scores["Activity Diagram"] += base_state_score
    scores["State Machine Diagram"] += base_state_score
    
    sync_bars = counts.get("UMLSyncBarHorizontal", 0) + counts.get("UMLSyncBarVertical", 0)
    decisions = counts.get("type=decision", 0)
    
    scores["Activity Diagram"] += sync_bars * 50
    scores["Activity Diagram"] += decisions * 30
    
    if base_state_score > 0 and sync_bars == 0:
        scores["State Machine Diagram"] += 40 
        
    best_match = max(scores, key=scores.get)
    
    # --- VALID DIAGRAM BUT NOT A PART OF THE 5 ---
    if scores[best_match] == 0: 
        if counts.get("_TOTAL_ELEMENTS_", 0) > 0:
            return "Valid UML Diagram (Type not within the targeted 5 core diagrams)", scores
        else:
            return "Invalid or Empty .uxf File", scores
        
    return best_match, scores

if __name__ == "__main__":
    filepath = "test1_statemachine.uxf" 
    
    freq_map = generate_frequency_map(filepath)
    print("--- Frequency Map ---")
    for key, value in freq_map.items():
        if key != "_TOTAL_ELEMENTS_":
            print(f"{key}: {value}")
        
    prediction, raw_scores = identify_diagram(freq_map)
    print("\n--- Scoring Results ---")
    for category, score in raw_scores.items():
        print(f"{category}: {score}")
        1
    print(f"\n>> FINAL PREDICTION: {prediction} <<")
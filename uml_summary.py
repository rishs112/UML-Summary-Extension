def generate_summary(classes, graph_edges, level):
    """
    Returns only the specific tier of information requested.
    """
    if not classes:
        return "This diagram does not appear to contain any valid classes."
        
    summary_lines = []

    if level == 1:
        summary_lines.append("=== LEVEL 1: OVERVIEW ===")
        summary_lines.append(f"This diagram contains {len(classes)} classes and {len(graph_edges)} defined relationships.")
        return "\n".join(summary_lines)

 
    if level == 2:
        summary_lines.append("=== LEVEL 2: STRUCTURAL OUTLINE ===")
        summary_lines.append("Classes Outline:")
        for c in classes:
            identity = c['name']
            if c.get("is_abstract"): identity += " (Abstract)"
            if c.get("stereotype"): identity += f" <<{c['stereotype']}>>"
            
            attr_count, meth_count = len(c["attributes"]), len(c["methods"])
            summary_lines.append(f"  * {identity} [{attr_count} attributes, {meth_count} methods]")
            
        summary_lines.append("\nRelationships:")
        if not graph_edges:
            summary_lines.append("  * No relationships found.")
        else:
            for edge in graph_edges:
                multi = ""
                if edge.get("source_multi") or edge.get("target_multi"):
                    m1 = edge.get("source_multi") or "unspecified"
                    m2 = edge.get("target_multi") or "unspecified"
                    multi = f" ({m1} to {m2})"
                summary_lines.append(f"  * {edge['source']} has {edge['relationship']}{multi} with {edge['target']}.")
        
        return "\n".join(summary_lines)

   
    if level == 3:
        summary_lines.append("=== LEVEL 3: INTERNAL DETAILS ===")
        for c in classes:
            summary_lines.append(f"Class: {c['name']}")
            if not c["attributes"] and not c["methods"]:
                summary_lines.append("  (No internal attributes or methods defined)\n")
                continue
                
            if c["attributes"]:
                summary_lines.append("  Attributes:")
                for attr in c["attributes"]:
                    summary_lines.append(f"    - [{attr['modifier']}] {attr['raw_text'].replace('+', '').replace('-', '').strip()}")
            if c["methods"]:
                summary_lines.append("  Methods:")
                for meth in c["methods"]:
                    summary_lines.append(f"    - [{meth['modifier']}] {meth['raw_text'].replace('+', '').replace('-', '').strip()}")
            summary_lines.append("") 
            
        return "\n".join(summary_lines)
import re

def extract_facts(text):
    facts = re.findall(
        r'\b(\d+(?:\.\d+)?)\s*(years?|months?|hours?|minutes?|seconds?|days?|rs\.?|inr|mbps|gb|tb|devices?)\b',
        text.lower()
    )
    return [(v, u) for v, u in facts]

def chunks_are_related(chunk_a, chunk_c, threshold=3):
    STOP_WORDS = {
        "the","is","are","was","a","an","and","or","but","in",
        "on","at","to","for","of","with","by","from","this",
        "that","it","its","be","been","have","has","do","does",
        "will","can","if","as","not","no","also","just","all",
        "any","each","more","most","other","some","only","same"
    }

    #Get all set of words in lower case related to chunk a
    words_a = set(w.lower().strip(".,:-") for w in chunk_a.split()
                  if w.lower().strip(".,:-") not in STOP_WORDS
                  and len(w) > 3)
    
    #Get all set of words in lower case related to chunk c
    words_c = set(w.lower().strip(".,:-") for w in chunk_c.split()
                  if w.lower().strip(".,:-") not in STOP_WORDS
                  and len(w) > 3)
    common = words_a & words_c
    return len(common) >= threshold

def detect_conflict(ranked_chunks):

    #Only keeps pdf chunks
    source_a  = [(s,c,m) for s,c,m in ranked_chunks if m["source"]=="A"]

    #Only keeps wiki chunks
    source_c  = [(s,c,m) for s,c,m in ranked_chunks if m["source"]=="C"]
    conflicts = []



    for _, chunk_a, _ in source_a:
        for _, chunk_c, _ in source_c:

            # Only compare chunks that talk about the same thing
            if not chunks_are_related(chunk_a, chunk_c):
                continue

            diffs = []
            facts_a = extract_facts(chunk_a)

            
            facts_c = extract_facts(chunk_c)

            for val_a, unit_a in facts_a:
                for val_c, unit_c in facts_c:
                    if unit_a == unit_c and val_a != val_c:
                        already = any(
                            d["unit"] == unit_a and
                            d["manual_value"] == val_a and
                            d["wiki_value"] == val_c
                            for d in diffs
                        )
                        if not already:
                            diffs.append({
                                "unit":         unit_a,
                                "manual_value": val_a,
                                "wiki_value":   val_c
                            })

            if diffs:
                conflicts.append({
                    "manual_chunk":   chunk_a[:200],
                    "wiki_chunk":     chunk_c[:200],
                    "differences":    diffs,
                    "trusted_chunk":  chunk_a,
                    "trusted_source": "Technical Manual"
                })

    return conflicts

def prioritize_sources(ranked_chunks):
    return sorted(ranked_chunks, key=lambda x: x[2]["priority"])




def format_conflict_message(conflicts):
    if not conflicts:
        return None
    lines = ["\n⚠️  CONFLICT DETECTED between sources!\n"]
    for i, conflict in enumerate(conflicts, 1):
        lines.append(f"Conflict #{i}:")
        for d in conflict["differences"]:
            lines.append(
                f"  • {d['unit'].upper()}: "
                f"✅ Technical Manual says {d['manual_value']} | "
                f"❌ Legacy Wiki says {d['wiki_value']}"
            )
        lines.append("  → Using Technical Manual (highest priority)\n")
    return "\n".join(lines)
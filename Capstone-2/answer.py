import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

_client = genai.Client(api_key=api_key)

def build_answer(query, ranked_chunks, conflicts, conflict_msg):
    if not ranked_chunks:
        return "❌ No information found. Please check your uploaded files."

    top_score  = float(ranked_chunks[0][0])
    confidence = round(min(100, max(0, (top_score + 10) / 20 * 100)), 1)

    if confidence < 25:
        return (
            "❌ I don't have enough reliable information to answer this.\n"
            f"📊 Confidence: {confidence}%"
        )

    # ── Step 1: Find what each source says ────────────────
    source_texts = {"A": None, "B": None, "C": None}
    source_names = {
        "A": "Source A (Technical Manual)",
        "B": "Source B (Support Logs)",
        "C": "Source C (Legacy Wiki)"
    }

    for _, chunk, meta in ranked_chunks[:6]:
        src = meta["source"]
        if source_texts[src] is None:
            source_texts[src] = chunk[:200]

    # ── Step 2: Ask Gemini what each source says ──────────
    context = "\n\n".join(
        f"[{meta['source_name']}]: {chunk}"
        for _, chunk, meta in ranked_chunks[:4]
    )

    prompt = f"""You are a precise technical assistant.
Given the context below, answer the question in this EXACT format:

Source A (Technical Manual): [what source A says, or "No information found"]
Source B (Support Logs): [what source B says, or "No information found"]  
Source C (Legacy Wiki): [what source C says, or "No information found"]

Use ONLY information from the context.
Keep each source answer to ONE short sentence.
Do not add anything else.

--- CONTEXT ---
{context}
--- END ---

Question: {query}"""

    try:
        response = _client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        source_summary = response.text.strip()
    except Exception as e:
        if "429" in str(e):
            # Fallback if quota exceeded
            lines = []
            for src, name in source_names.items():
                if source_texts[src]:
                    lines.append(f"{name}: {source_texts[src][:150]}...")
                else:
                    lines.append(f"{name}: No information found")
            source_summary = "\n".join(lines)
        else:
            source_summary = f"Error: {e}"

    # ── Step 3: Build conflict section ────────────────────
    conflict_section = ""
    if conflicts:
        conflict_section = "\n⚠️  CONFLICT DETECTED!\n"
        for i, conflict in enumerate(conflicts, 1):
            for d in conflict["differences"]:
                conflict_section += (
                    f"  Reason: {d['unit'].upper()} is different — "
                    f"Manual says {d['manual_value']}, "
                    f"Wiki says {d['wiki_value']}\n"
                )
        conflict_section += (
            "\n✅ Preferred Answer: From Technical Manual (Source A)"
            "\n   Why: Technical Manual is the most recent "
            "and officially verified source.\n"
        )
    else:
        conflict_section = "\n✅ All sources agree — no conflict found.\n"

    # ── Step 4: Combine everything ─────────────────────────
    final = (
        f"{source_summary}\n"
        f"{conflict_section}"
        f"\n📊 Confidence: {confidence}%"
    )
    return final

"""
```

---

Now run and ask:
```
What is the price of MacBook Air M2?
```

Output will look like:
```
Source A (Technical Manual): MacBook Air M2 costs Rs 114990 with 18 hour battery
Source B (Support Logs):     MacBook Air M2 is priced at Rs 114990
Source C (Legacy Wiki):      MacBook Air M2 costs Rs 99990 with 12 hour battery

⚠️ CONFLICT DETECTED!
  Reason: RS is different — Manual says 114990, Wiki says 99990
  Reason: HOURS is different — Manual says 18, Wiki says 12

✅ Preferred Answer: From Technical Manual (Source A)
   Why: Technical Manual is the most recent and officially verified source.

📊 Confidence: 92.5%

"""
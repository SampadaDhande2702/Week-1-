import os
import time
import chromadb
from ingest import ingest_pdf, ingest_json, ingest_markdown, embedder, _client, get_collection
from retriever import hybrid_search
from resolver import detect_conflict, prioritize_sources, format_conflict_message
from answer import build_answer

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")

def get_file_paths():
    print("\n" + "="*60)
    print("         TRUTH ENGINE — File Setup")
    print("="*60)
    print("Enter full path or just filename if file is in data/")
    print("Example: data/laptop_manual.pdf\n")

    def ask(label, default):
        val = input(f"Source A — {label} (default: {default}): ").strip()
        return val if val else default

    a = ask("PDF  (Technical Manual)", "data/laptop_manual.pdf")
    b = ask("JSON (Support Logs)",     "data/laptop_sales_logs.json")
    c = ask("MD   (Legacy Wiki)",      "data/laptop_wiki.md")
    return a, b, c

def validate(a, b, c):
    errors = []
    for f in [a, b, c]:
        if not os.path.exists(f):
            errors.append(f"  ❌ Not found: {f}")
    return errors

def load_database(pdf, json_file, md):
    print("\nClearing old data and loading new files...")
    try:
        _client.delete_collection("truth_engine")
    except:
        pass
    _client.get_or_create_collection("truth_engine")


   #Calling Ingest functions
    ingest_pdf(pdf)
    ingest_json(json_file)
    ingest_markdown(md)

    col   = get_collection()
    total = col.count()
    print(f"\n✅ Ready! {total} chunks loaded into database.\n")
    return col

def print_banner(pdf, json_file, md):
    print("\n" + "="*60)
    print("         TRUTH ENGINE — Ask Anything!")
    print("="*60)
    print(f"  [A] {os.path.basename(pdf):<38} Priority 1 ✅")
    print(f"  [B] {os.path.basename(json_file):<38} Priority 2")
    print(f"  [C] {os.path.basename(md):<38} Priority 3")
    print("-"*60)
    print("  Commands:")
    print("  'reload' — reload files if you changed them")
    print("  'files'  — switch to different files")
    print("  'quit'   — exit")
    print("="*60 + "\n")


def ask_question(query, collection):
    ranked       = hybrid_search(query, collection, embedder)
    prioritized  = prioritize_sources(ranked)
    conflicts    = detect_conflict(prioritized)
    conflict_msg = format_conflict_message(conflicts)
    answer       = build_answer(query, prioritized, conflicts, conflict_msg)
    return answer

def chat(collection, pdf, json_file, md):
    print_banner(pdf, json_file, md)
    file_times = {f: os.path.getmtime(f) for f in [pdf, json_file, md] if os.path.exists(f)}

    while True:
        try:
            query = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return "quit", collection

        if not query:
            continue

        if query.lower() in ["quit", "exit"]:
            print("Goodbye!")
            return "quit", collection

        if query.lower() == "files":
            return "files", collection

        if query.lower() == "reload":
            collection = load_database(pdf, json_file, md)
            file_times = {f: os.path.getmtime(f) for f in [pdf, json_file, md] if os.path.exists(f)}
            print_banner(pdf, json_file, md)
            continue

        # Auto detect file changes
        for f in [pdf, json_file, md]:
            if os.path.exists(f):
                new_time = os.path.getmtime(f)
                if new_time != file_times.get(f, 0):
                    print(f"\n📂 Change detected in {os.path.basename(f)} — reloading...\n")
                    collection = load_database(pdf, json_file, md)
                    file_times = {f: os.path.getmtime(f) for f in [pdf, json_file, md] if os.path.exists(f)}
                    print_banner(pdf, json_file, md)
                    break

        print("\n🔍 Searching sources...\n")
        try:
            answer = ask_question(query, collection)
            print("-"*60)
            print(f"Bot: {answer}")
            print("-"*60 + "\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

def main():
    print("\n🚀 Welcome to Truth Engine!")

    pdf = json_file = md = None

    while True:
        if pdf is None:
            pdf, json_file, md = get_file_paths()
            errors = validate(pdf, json_file, md)
            if errors:
                print("\nErrors:")
                for e in errors:
                    print(e)
                print("Please try again.\n")
                pdf = None
                continue
            collection = load_database(pdf, json_file, md)

        action, collection = chat(collection, pdf, json_file, md)

        if action == "quit":
            break
        elif action == "files":
            pdf = None

if __name__ == "__main__":
    main()
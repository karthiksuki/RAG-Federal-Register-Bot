import json

INPUT_FILE = "raw_documents.json"
OUTPUT_FILE = "processed_documents.json"


def process_documents():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    processed = []
    for doc in data['results']:
        processed.append({
            "title": doc.get("title"),
            "date": doc.get("publication_date"),
            "agency": doc['agencies'][0]['name'] if doc.get('agencies') else "Unknown",
            "url": doc.get("html_url"),
            "pdf": doc.get("pdf_url")
        })

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(processed, f, indent=4)
    print(f"Processed {len(processed)} json fields")


if __name__ == "__main__":
    process_documents()

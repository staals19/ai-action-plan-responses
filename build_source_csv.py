import csv, glob, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from attachment_utils import extract_text_from_file  # PyMuPDF + OCR + gibberish check

PDF_DIR = "nitrd_responses"
OUT_CSV = "regulations/ai-action-plan/source.csv"

fieldnames = ["Document ID", "Comment", "First Name", "Last Name",
              "Organization Name", "Posted Date", "Received Date",
              "Attachment Files"]

rows, empty = [], 0
paths = sorted(glob.glob(os.path.join(PDF_DIR, "**", "*.pdf"), recursive=True))

for i, path in enumerate(paths, 1):
    doc_id = os.path.splitext(os.path.basename(path))[0]
    text = extract_text_from_file(path).strip()
    if not text:
        empty += 1
    rows.append({
        "Document ID": doc_id,
        "Comment": text,
        "First Name": "", "Last Name": "", "Organization Name": "",
        "Posted Date": "", "Received Date": "",
        "Attachment Files": "",
    })
    if i % 500 == 0:
        print(f"  {i}/{len(paths)} extracted...")

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUT_CSV} ({empty} came back empty)")
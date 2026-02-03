import csv
import re

INPUT_FILE = "dataset/unsorted_dataset4.csv"
OUTPUT_FILE = "dataset/sorted_dataset4.csv"

rows_out = []

with open(INPUT_FILE, newline="", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    data = list(reader)

technology_types = data[0][1:]  # skip first column

current_trl = None

for row in data[1:]:
    if not row:
        continue

    # Check if row starts with TRL label (e.g. "TRL 1")
    trl_match = re.match(r"TRL\s*(\d+)", row[0].strip())
    if trl_match:
        current_trl = int(trl_match.group(1))
        # **Process this row’s question texts too!**
        for i, cell in enumerate(row[1:]):
            if cell.strip():
                rows_out.append({
                    "questionText": cell.strip(),
                    "trlLevel": current_trl,
                    "technologyType": technology_types[i].strip(),
                    "category": ""  # no inference
                })
        continue

    # For rows without TRL label, treat them as additional questions under current TRL
    if current_trl is None:
        continue

    for i, cell in enumerate(row[1:]):
        if cell.strip():
            rows_out.append({
                "questionText": cell.strip(),
                "trlLevel": current_trl,
                "technologyType": technology_types[i].strip(),
                "category": ""
            })

# Sort by Technology Type, then TRL
rows_out.sort(key=lambda r: (r["technologyType"].lower(), r["trlLevel"]))

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["questionText", "trlLevel", "technologyType", "category"])
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Fixed: included TRL row questions. Output: {OUTPUT_FILE}")

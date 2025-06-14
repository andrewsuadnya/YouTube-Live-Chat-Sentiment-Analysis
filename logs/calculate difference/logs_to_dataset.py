import re
import json
import csv
import os

# Regex untuk deteksi log baris
pattern_chat = re.compile(r"Sent to Kafka: ({.*})")
pattern_video_id = re.compile(r"Fetching live chat ID for video ID: (\w+)")

# Loop semua file .log di direktori kerja
for file_name in os.listdir():
    if file_name.endswith(".log"):
        messages = []
        video_id = ""

        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                # Ambil video_id satu kali di awal log
                if not video_id:
                    match_vid = pattern_video_id.search(line)
                    if match_vid:
                        video_id = match_vid.group(1)

                # Tangkap pesan chat biasa
                match = pattern_chat.search(line)
                if match:
                    raw_data = match.group(1)
                    try:
                        data = json.loads(raw_data.replace("'", '"'))
                    except Exception:
                        try:
                            data = eval(raw_data)
                        except Exception:
                            data = {}

                    messages.append({
                        "video_id": video_id,
                        "author": data.get("author", ""),
                        "message": data.get("message", ""),
                        "published_at": data.get("published_at", "")
                    })

        # Simpan hasil ke CSV dan JSON
        base_name = file_name.replace(".log", "")
        csv_name = f"{base_name}_full.csv"
        json_name = f"{base_name}_full.json"

        with open(csv_name, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["video_id", "author", "message", "published_at"])
            writer.writeheader()
            writer.writerows(messages)

        with open(json_name, "w", encoding='utf-8') as jsonfile:
            json.dump(messages, jsonfile, indent=2, ensure_ascii=False)

        print(f"[✓] {file_name} → {csv_name} & {json_name} | Total: {len(messages)} pesan")

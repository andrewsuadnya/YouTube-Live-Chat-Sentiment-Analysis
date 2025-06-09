import re
import pandas as pd

# Filepath ke file log
input_file = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\spark\spark.log"
output_file = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\final_log\hitung akurasi\spark.csv"

# Membaca file log
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Regex untuk menangkap baris data
data_pattern = re.compile(r"\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|")

# Menyimpan data yang diproses
data = []

# Memproses setiap baris
for line in lines:
    match = data_pattern.search(line)
    if match:
        # Menambahkan data yang cocok ke dalam list
        data.append([col.strip() for col in match.groups()])

# Membuat DataFrame dari data yang diproses
df = pd.DataFrame(data, columns=["message", "vader_sentiment", "textblob_sentiment", "final_sentiment"])

# Menghapus baris yang berisi header berulang
df = df[df['message'] != 'message']

# Menyimpan ke file CSV
df.to_csv(output_file, index=False)
print(f"File CSV berhasil disimpan ke: {output_file}")
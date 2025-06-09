input_file = 'd:\\Dokumen\\(SKRIPSI)\\..PEMBUATAN SISTEM\\LIVE CHAT SENTIMENT ANALYSIS\\SKRIPSI (SPARK)\\logs\\final_log\\spark.log'
output_dir = 'd:\\Dokumen\\(SKRIPSI)\\..PEMBUATAN SISTEM\\LIVE CHAT SENTIMENT ANALYSIS\\SKRIPSI (SPARK)\\logs\\final_log\\batches'

import os

# Pastikan direktori output ada
os.makedirs(output_dir, exist_ok=True)

try:
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Variabel untuk menyimpan batch
    batch = []
    batch_count = 0
    message_count = 0

    for line in lines:
        # Tambahkan baris ke batch
        batch.append(line)

        # Jika baris mengandung "INFO:__main__", anggap sebagai akhir pesan
        if "INFO:__main__" in line:
            message_count += 1

        # Jika sudah mencapai 1000 pesan, simpan batch ke file baru
        if message_count == 1000:
            batch_count += 1
            output_file = os.path.join(output_dir, f"batch_{batch_count}.log")
            with open(output_file, "w", encoding="utf-8") as batch_file:
                batch_file.writelines(batch)
            # Reset batch dan hitungan pesan
            batch = []
            message_count = 0

    # Simpan sisa batch jika ada
    if batch:
        batch_count += 1
        output_file = os.path.join(output_dir, f"batch_{batch_count}.log")
        with open(output_file, "w", encoding="utf-8") as batch_file:
            batch_file.writelines(batch)

    print(f"Berhasil membagi log menjadi {batch_count} batch di folder '{output_dir}'.")

except FileNotFoundError:
    print(f"File '{input_file}' tidak ditemukan. Pastikan file tersebut ada di path yang benar.")
except UnicodeDecodeError as e:
    print(f"Terjadi kesalahan decoding: {e}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
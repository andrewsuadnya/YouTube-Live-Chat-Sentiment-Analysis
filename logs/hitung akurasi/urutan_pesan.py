import pandas as pd

# File paths
manual_labelling_path = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\final_log\hitung akurasi\manual labelling.csv"
spark_path = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\final_log\hitung akurasi\spark.csv"
output_path = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\final_log\hitung akurasi\spark_sorted.csv"

# Load both CSV files
manual_labelling_df = pd.read_csv(manual_labelling_path)
spark_df = pd.read_csv(spark_path)

# Merge spark.csv with manual_labelling.csv based on the 'message' column
sorted_spark_df = pd.merge(
    manual_labelling_df[['message']],  # Use only the 'message' column for ordering
    spark_df,
    on='message',
    how='left'  # Keep the order of manual_labelling.csv
)

# Save the sorted spark.csv
sorted_spark_df.to_csv(output_path, index=False)

print(f"File spark.csv telah diurutkan dan disimpan ke: {output_path}")
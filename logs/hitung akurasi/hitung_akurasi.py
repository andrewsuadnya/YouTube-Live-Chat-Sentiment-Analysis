import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns; import matplotlib.pyplot as plt

# Filepath ke file CSV
predicted_file = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\final_log\hitung akurasi\hasil sentiment.csv"
manual_file = r"d:\Dokumen\(SKRIPSI)\..PEMBUATAN SISTEM\LIVE CHAT SENTIMENT ANALYSIS\SKRIPSI (SPARK)\logs\final_log\hitung akurasi\manual labelling.csv"

# Membaca file CSV
predicted_data = pd.read_csv(predicted_file)
manual_data = pd.read_csv(manual_file)

# Pastikan kedua file memiliki jumlah baris yang sama
if len(predicted_data) != len(manual_data):
    raise ValueError(f"Jumlah baris pada hasil sentiment ({len(predicted_data)}) dan manual labelling ({len(manual_data)}) tidak sama!")

# Membandingkan kolom 'final_sentiment'
predicted_sentiments = predicted_data['final_sentiment']
manual_sentiments = manual_data['true_sentiment']

# Menghasilkan classification report
report = classification_report(manual_sentiments, predicted_sentiments, target_names=['negative', 'neutral', 'positive'])
print(report)

# Membuat dan menampilkan confusion matrix
cm = confusion_matrix(manual_sentiments, predicted_sentiments)

# Visualisasi confusion matrix
classes = ['negative', 'neutral', 'positive']
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes) 
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

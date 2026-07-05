import os
import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import joblib

factory = StemmerFactory()
stemmer = factory.create_stemmer()

STOPWORDS = set(['yang', 'untuk', 'di', 'dari', 'ke', 'ini', 'itu', 'dan', 'atau', 'dengan'])

def preprocessing_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS]
    tokens = [stemmer.render(word) if hasattr(stemmer, 'render') else stemmer.stem(word) for word in tokens]
    return " ".join(tokens)

if __name__ == "__main__":
    print("--- Memulai Proses Membaca Dataset ---")
    
    # Buat dataset darurat jika file csv belum ada
    os.makedirs('dataset', exist_ok=True)
    csv_path = 'dataset/dataset_sms_spam.csv'
    if not os.path.exists(csv_path):
        data = {
            'teks': ["Promo hadiah mobil klik bit.ly/win", "Pinjaman online cepat cair hubungi WA", "Besok ada kuliah jam berapa?", "Tugas kuliah dikumpulkan nanti malam"],
            'label': ["spam", "spam", "ham", "ham"]
        }
        pd.DataFrame(data).to_csv(csv_path, index=False)
        
    df = pd.read_csv(csv_path)
    df['clean_teks'] = df['teks'].apply(preprocessing_text)
    
    X_train, X_test, y_train, y_test = train_test_split(df['clean_teks'], df['label'], test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)
    
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/model_naive_bayes.pkl')
    joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')
    print("--- Model Berhasil Dibuat dan Disimpan! ---")
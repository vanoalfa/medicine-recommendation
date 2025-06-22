import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# Download resource NLTK
nltk.download('punkt')
nltk.download('stopwords')

document_df = pd.read_csv("/content/products.csv")

# Cek duplikasi
print('Cek Duplikasi...')
print(document_df.isnull().sum())
print("\n")
print(document_df.duplicated().sum())
print("=============================================================================")

document_df['product_title+description'] = document_df['title'] + ' : ' + document_df['description']
print('Cek duplikasi selesai...')

# Cleaning data
print('Cleaning karakter...')
def cleanResume(txt):
    cleantxt = re.sub(r'http\S+\s', ' ', txt)
    cleantxt = re.sub(r'RT|cc', ' ', cleantxt)
    cleantxt = re.sub(r'@\S+', ' ', cleantxt)
    cleantxt = re.sub(r'#\S+', ' ', cleantxt)
    cleantxt = re.sub(r'[%s]' % re.escape("!\"#$%&'()*+,-./:;<=>?@[\\]^_{|}~ "), ' ', cleantxt)
    cleantxt = re.sub(r'[^\x00-\x7f]', ' ', cleantxt)
    cleantxt = re.sub(r'\s+', ' ', cleantxt)
    return cleantxt

document_df['product_title+description'] = document_df['product_title+description'].apply(lambda x: cleanResume(x))
print('Cleaning karakter selesai')

# Case folding
print('Proses casefolding dimulai...')
document_df['product_preprocessed'] = document_df['product_title+description'].str.lower()
print('Proses casefolding selesai...')

# Tokenisasi
print('Tokenisasi dimulai...')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

document_df['product_preprocessed'] = document_df['product_preprocessed'].apply(word_tokenize)
print('Tokenisasi selesai...')

# Stopwords dan Stemming
print('Proses Stopwords dan Stemming dimulai...')
stopwords = stopwords.words('indonesian')
factory = StemmerFactory()
stemmer = factory.create_stemmer()

document_df['product_preprocessed'] = document_df['product_preprocessed'].apply(
    lambda tokens: [word for word in tokens if word.isalpha() and word not in stopwords]
)
print('Proses Stopwords dan Stemming selesai...')
print("="*100)
print("Preprocessing selesai, fungsi VSMModel dapat digunakan")
print("-"*100)

# Simpan ke file
print("Simpan ke file product_preprocessed.csv")
document_df.to_csv("/content/product_preprocessed.csv", index=False)

# 🧬 DNA Sequence & Pattern Recognition for Disease Classification

## 📌 Overview

This project is a **machine learning-based DNA analysis system** that predicts possible diseases from DNA sequences using pattern recognition techniques.

It combines:

* 🧪 Bioinformatics (DNA sequence analysis)
* 🤖 Machine Learning (Random Forest Classifier)
* 🌐 Interactive Web App using Streamlit

---

## 🚀 Features

* Analyze DNA sequences (A, T, C, G)
* Pattern detection using **KMP algorithm**
* Feature extraction (GC content, sequence length, motifs)
* Disease prediction with confidence score
* Interactive UI with manual input or file upload

---

## 🏗️ Project Structure

```id="d41zsb"
DNA-Sequence-and-Pattern-Recognition-Disease-Classification/
│
├── dna_hybrid_model.py          # Main file (UI + ML model + logic)
│
├── data/
│   └── raw/
│       └── dna_disease_dataset.csv
│
├── models/
│   └── disease_classifier.joblib
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash id="hy4px1"
git clone https://github.com/SakshiAher-Codes/DNA-Sequence-and-Pattern-Recognition-Disease-Classification.git
cd DNA-Sequence-and-Pattern-Recognition-Disease-Classification
```

### 2. Install dependencies

```bash id="0r7dyw"
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash id="k6f6w4"
streamlit run dna_hybrid_model.py
```

---

## 🧠 Model Details

* Algorithm: **Random Forest Classifier**
* Features used:

  * DNA sequence length
  * GC content
  * Motif (pattern) frequency using KMP
* Model stored using `joblib`

---

## 📊 Dataset

* `dna_disease_dataset.csv` (located in `data/raw/`)
* Contains DNA sequences and corresponding disease labels

---

## 📸 Screenshots

*Add screenshots of your Streamlit app here (recommended)*

---

## 🌐 Deployment

You can deploy this project using:

* Streamlit Community Cloud

---

## 💡 Future Improvements

* Improve model accuracy using deep learning
* Add real-world genomic datasets
* Enhance UI/UX
* Separate backend and frontend for scalability

---

## 👩‍💻 Author

**Sakshi Aher**
GitHub: https://github.com/SakshiAher-Codes

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!

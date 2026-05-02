import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# ------------------ KMP Algorithm ------------------
def kmp_build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_count(text, pattern):
    if not pattern:
        return 0
    lps = kmp_build_lps(pattern)
    i = j = 0
    count = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                count += 1
                j = lps[j-1]
        else:
            j = lps[j-1] if j else 0
            if j == 0: i += 1
    return count

# ------------------ Feature Engineering ------------------
def extract_features(seq, motifs):
    gc = (seq.count('G') + seq.count('C')) / len(seq)
    feats = [len(seq), gc]
    for m in motifs:
        feats.append(kmp_count(seq, m))
    return np.array(feats)

def build_feature_matrix(df, motifs):
    X = np.array([extract_features(s, motifs) for s in df["dna_sequence"]])
    return X

# ------------------ Model Training ------------------
def train_model(csv_path, model_path="disease_classifier.joblib"):
    df = pd.read_csv("./dna_disease_dataset.csv")
    df["dna_sequence"] = df["dna_sequence"].str.upper().str.replace(" ", "")
    motifs = ["ATG", "CGT", "AAA", "TGC", "GGA"]  # Common 3-mer patterns
    X = build_feature_matrix(df, motifs)
    le = LabelEncoder()
    y = le.fit_transform(df["label"])
    model = RandomForestClassifier(n_estimators=300, random_state=42)
    model.fit(X, y)
    joblib.dump({"model": model, "encoder": le, "motifs": motifs}, model_path)
    print(f"✅ Model trained and saved to {model_path}")

# ------------------ Load or Train Once ------------------
MODEL_PATH = "disease_classifier.joblib"
if not os.path.exists(MODEL_PATH):
    st.info("Training model from provided dataset...")
    # ⚠️ Update this path to your CSV file
    train_model("dna_disease_dataset.csv")

saved = joblib.load(MODEL_PATH)
model = saved["model"]
encoder = saved["encoder"]
motifs = saved["motifs"]

# ------------------ Streamlit Doctor UI ------------------
st.set_page_config(page_title="DNA Disease Classifier", layout="centered")
st.title("🧬 DNA Disease Classifier")
st.write("This tool analyzes DNA sequences to predict the likely disease category based on trained genomic patterns.")

seq_input = st.text_area("Enter DNA Sequence", height=120, placeholder="Paste DNA sequence here...")
uploaded = st.file_uploader("Or upload a text file containing DNA sequence", type=["txt"])

if uploaded is not None:
    seq_input = uploaded.read().decode().strip().upper()

if st.button("🔍 Analyze DNA Sequence"):
    if not seq_input:
        st.error("Please enter or upload a DNA sequence.")
    else:
        seq = seq_input.upper().replace(" ", "").replace("\n", "")
        if any(ch not in "ATCG" for ch in seq):
            st.error("Invalid DNA sequence. Use only A, T, C, G characters.")
        else:
            feats = extract_features(seq, motifs).reshape(1, -1)
            probs = model.predict_proba(feats)[0]
            pred_class = encoder.inverse_transform([np.argmax(probs)])[0]
            confidence = np.max(probs)

            st.markdown(f"### 🧫 Predicted Disease: **{pred_class}**")
            st.progress(confidence)
            st.write(f"**Confidence:** {confidence*100:.2f}%")

            st.subheader("Sequence Summary")
            st.write(f"🧬 Length: {len(seq)} bases")
            st.write(f"💠 GC Content: {(seq.count('G') + seq.count('C'))/len(seq):.3f}")
            motif_counts = {m: kmp_count(seq, m) for m in motifs}
            st.write("Pattern Occurrences:")
            st.table(pd.DataFrame.from_dict(motif_counts, orient="index", columns=["Count"]))

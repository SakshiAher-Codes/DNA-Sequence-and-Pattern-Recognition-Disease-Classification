import streamlit as st
import joblib
import numpy as np
from itertools import groupby


model = joblib.load("models/disease_classifier.joblib")


# KMP algorithm for pattern searching (same as backend)
def kmp_search(text, pattern):
    def compute_lps(pattern):
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
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps(pattern)
    i = 0
    j = 0
    count = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            count += 1
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return count


# Streamlit app
st.title("DNA Sequence Disease Classifier")
st.write("Enter a DNA sequence (ATCG only) to classify for disease based on pattern recognition.")

# Input for DNA sequence
dna_sequence = st.text_input("DNA Sequence:",
                             value="GCTCGTAACACTAGGACAGATAAAAAAATGACCCTCGTTATGAAAATTGGCTAGACGGCGTCCCTGATTGATGAGACCAATTAACACAACTGTGATGAGG")

if st.button("Classify"):
    if dna_sequence:
        # Validate sequence (only ATCG)
        if all(base in 'ATCG' for base in dna_sequence.upper()):
            seq = dna_sequence.upper()
            # Extract features (matching backend)
            disease_pattern = "ATCG"
            pattern_count = kmp_search(seq, disease_pattern)
            gc_content = (seq.count('G') + seq.count('C')) / len(seq)
            max_homopolymer = max(len(list(g)) for k, g in groupby(seq)) if seq else 0

            features = np.array([[pattern_count, gc_content, max_homopolymer]])

            # Predict
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]

            if prediction == 1:
                st.error(f"Disease Detected! Probability: {probability:.2f}")
            else:
                st.success(f"No Disease Detected. Probability: {probability:.2f}")

            st.write(
                f"Features extracted: Pattern Count ({disease_pattern}): {pattern_count}, GC Content: {gc_content:.2f}, Max Homopolymer: {max_homopolymer}")
        else:
            st.error("Invalid DNA sequence. Only A, T, C, G allowed.")
    else:
        st.warning("Please enter a DNA sequence.")

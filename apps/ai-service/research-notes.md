# AI Service - Research Notes

## Keputusan: Rule-Based vs Machine Learning untuk Klasifikasi Transaksi

### Untuk MVP (8 minggu)
**Pilih: Rule-Based (Berbasis Aturan)**

**Alasan:**
1. Cepat implementasi (bisa selesai 1-2 hari)
2. Tidak butuh dataset besar untuk training
3. Akurasi cukup (80-90% untuk kasus umum)
4. Mudah di-debug dan diperbaiki
5. Cocok untuk MVP karena kita ingin buktikan produknya dulu

**Contoh implementasi:**
if "Starbucks" in description → "Food & Dining"
if "Grab" in description → "Transportation"
if "Netflix" in description → "Entertainment"


### Rencana Post-MVP (Fast-Follow)
**Migrasi ke Machine Learning**

**Target:**
- Akurasi > 95%
- Menggunakan data transaksi nyata dari pengguna
- Model: TF-IDF + Logistic Regression atau SVM

### Dataset Publik yang Potensial
| Nama | Jumlah Data | Link |
|------|-------------|------|
| mitulshah/transaction-categorization | 4.5 juta | huggingface.co/datasets/mitulshah/transaction-categorization |
| alokkulkarni/financial_Transactions | 378 | huggingface.co/datasets/alokkulkarni/financial_Transactions |
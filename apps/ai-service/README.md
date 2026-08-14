# FinSight AI Service

AI Service untuk FinSight yang digunakan untuk memprediksi kategori transaksi berdasarkan deskripsi transaksi.

## Overview

Service ini menggunakan Machine Learning untuk mengklasifikasikan teks transaksi ke dalam kategori keuangan.

Contoh prediksi:

```text
Beli kipas angin → shopping
Beli nasi goreng → food
Bayar uang kuliah → education
Top up GoPay → topup
Payroll → income
Potongan admin payroll → fees
```

## Technology

* Python
* Flask
* scikit-learn
* Pandas
* Joblib
* TF-IDF Vectorizer
* Support Vector Machine (SVM)

## Model

Model klasifikasi menggunakan:

1. TF-IDF untuk mengubah teks transaksi menjadi fitur numerik.
2. Support Vector Machine (SVM) untuk melakukan klasifikasi.
3. Label Encoder untuk mengubah hasil prediksi menjadi nama kategori.

Model dan komponen pendukung disimpan di:

```text
models/
├── model.pkl
├── vectorizer.pkl
└── label_encoder.pkl
```

## Categories

Model saat ini mendukung 15 kategori:

* bills
* donation
* education
* entertainment
* fees
* food
* healthcare
* income
* investment
* loan
* shopping
* topup
* transfer
* transport
* travel

## API Endpoints

### Health Check

```http
GET /api/v1/health
```

### Predict Transaction

```http
POST /api/v1/predict
Content-Type: application/json
```

Request body:

```json
{
  "text": "Beli kipas angin"
}
```

Example response:

```json
{
  "text": "Beli kipas angin",
  "predicted_label": "shopping"
}
```

### Submit Feedback

```http
POST /api/v1/feedback
Content-Type: application/json
```

Request body:

```json
{
  "text": "Beli kipas angin",
  "predicted_label": "shopping",
  "corrected_label": "shopping"
}
```

Feedback dapat berupa konfirmasi bahwa prediksi benar atau koreksi kategori apabila prediksi salah.

## Feedback and Retraining

AI Service mendukung proses feedback dan retraining.

Alur sistem:

```text
Transaction Text
       ↓
Prediction
       ↓
User Feedback
       ↓
Feedback Dataset
       ↓
Retraining
       ↓
Model Evaluation
       ↓
Compare Old and New Model
       ↓
Keep Better Model
```

Model baru tidak langsung menggantikan model lama.

Setelah retraining, model baru dievaluasi dan dibandingkan dengan model lama. Model hanya diperbarui apabila performanya lebih baik sesuai kriteria evaluasi. Jika tidak, model lama tetap digunakan.

## Model Evaluation

Hasil evaluasi terakhir:

```text
Accuracy: 96.59%
```

Beberapa hasil pengujian prediksi langsung:

```text
Beli kipas angin          → shopping
beli kado ultah           → shopping
Beli nasi goreng          → food
Bayar uang kuliah         → education
Top up GoPay              → topup
Payroll                   → income
Payroll July Rp8200000    → income
Potongan admin payroll    → fees
```

## Project Structure

```text
apps/ai-service/
├── app/
│   ├── main.py
│   ├── ml/
│   │   ├── dataset_updater.py
│   │   ├── evaluator.py
│   │   ├── model_manager.py
│   │   ├── predictor.py
│   │   ├── retrainer.py
│   │   └── trainer.py
│   └── routes/
│       ├── feedback.py
│       ├── health.py
│       └── predict.py
├── data/
│   ├── final/
│   ├── processed/
│   └── raw/
├── models/
│   ├── model.pkl
│   ├── vectorizer.pkl
│   └── label_encoder.pkl
├── notebook/
├── test/
├── requirements.txt
└── README.md
```

## Running Locally

### 1. Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run AI Service

```powershell
python -m app.main
```

Service berjalan di:

```text
http://127.0.0.1:5000
```

## Testing

Jalankan evaluasi model:

```powershell
python test_final_evaluation.py
```

Jalankan pengujian prediksi langsung:

```powershell
python test_direct.py
```

Jalankan pengujian retraining:

```powershell
python test_retrain.py
```

## Integration

AI Service diintegrasikan dengan NestJS API.

Alurnya:

```text
Next.js Frontend
       ↓
NestJS API
       ↓
Flask AI Service
       ↓
Machine Learning Model
       ↓
Prediction Result
```

NestJS API meneruskan request prediksi ke AI Service, kemudian hasil prediksi dikembalikan ke frontend.

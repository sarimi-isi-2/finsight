"use client";

import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showCorrection, setShowCorrection] = useState(false);
  const [correctedLabel, setCorrectedLabel] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [feedbackSent, setFeedbackSent] = useState(false);

  const categories = [
  "shopping",
  "investment",
  "food",
  "travel",
  "loan",
  "transfer",
  "healthcare",
  "education",
  "bills",
  "entertainment",
  "topup",
  "donation",
  "transport",
  "income",
  "fees"
];

  const handlePredict = async () => {
    if (!text.trim()) {
      setError("Masukkan deskripsi transaksi terlebih dahulu.");
      return;
    }

      setLoading(true);
      setError("");
      setResult("");
      setFeedbackMessage("");
      setShowCorrection(false);
      setCorrectedLabel("");
      setFeedbackSent(false);

    try {
      const response = await fetch(
        "http://127.0.0.1:3001/ai/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Gagal mendapatkan prediksi dari AI Service.");
      }

      const data = await response.json();

      setResult(data.predicted_label);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Terjadi kesalahan."
      );
    } finally {
      setLoading(false);
    }
  };

  const sendFeedback = async (label: string) => {
  if (!text.trim() || !result || !label) {
    setFeedbackMessage("Data feedback belum lengkap.");
    return;
  }

  if (feedbackSent) {
    return;
  }

  setFeedbackLoading(true);
  setFeedbackMessage("");

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/v1/feedback",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          predicted_label: result,
          corrected_label: label,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Feedback gagal dikirim."
      );
    }

    setFeedbackMessage(
      label === result
        ? "✓ Feedback berhasil disimpan."
        : "✓ Koreksi berhasil disimpan."
    );

    setFeedbackSent(true);
    setShowCorrection(false);
    setCorrectedLabel("");

  } catch (error) {
    console.error("Feedback error:", error);

    setFeedbackMessage(
      error instanceof Error
        ? error.message
        : "Feedback gagal dikirim."
    );

  } finally {
    setFeedbackLoading(false);
  }
};

  return (
    <main
      style={{
        maxWidth: "600px",
        margin: "80px auto",
        padding: "24px",
      }}
    >
      <h1>FinSight AI Transaction Predictor</h1>

      <p style={{ marginTop: "10px", marginBottom: "20px" }}>
        Masukkan deskripsi transaksi untuk diprediksi kategorinya.
      </p>

      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Contoh: Bayar uang sekolah adik"
        rows={5}
        style={{
          width: "100%",
          padding: "12px",
          fontSize: "16px",
        }}
      />

      <button
        onClick={handlePredict}
        disabled={loading}
        style={{
          marginTop: "16px",
          padding: "12px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        {loading ? "Predicting..." : "Predict Category"}
      </button>

      {result && (
  <div>
    <p>Predicted Category: {result}</p>

    <button
  onClick={() => sendFeedback(result)}
  disabled={feedbackLoading || feedbackSent}
>
  {feedbackLoading ? "Mengirim..." : "✓ Benar"}
</button>

<button
  onClick={() => setShowCorrection(true)}
  disabled={feedbackLoading || feedbackSent}
>
  ✕ Salah
</button>

    {showCorrection && (
      <div>
        <p>Pilih kategori yang benar:</p>

        <select
          value={correctedLabel}
          onChange={(e) => setCorrectedLabel(e.target.value)}
        >
          <option value="">Pilih kategori</option>

          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>

        <button
  onClick={() => sendFeedback(correctedLabel)}
  disabled={!correctedLabel || feedbackLoading || feedbackSent}
>
  {feedbackLoading
    ? "Mengirim..."
    : "Submit Correction"}
</button>
      </div>
    )}

    {feedbackMessage && (
      <p>{feedbackMessage}</p>
    )}
  </div>
)}
      {error && (
        <div
          style={{
            marginTop: "24px",
            padding: "16px",
            border: "1px solid red",
          }}
        >
          {error}
        </div>
      )}
    </main>
  );
}
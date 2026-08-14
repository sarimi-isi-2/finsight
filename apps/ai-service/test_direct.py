from app.ml.predictor import predict_transaction


texts = [
    "Beli kipas angin",
    "beli kado ultah",
    "Beli nasi goreng",
    "Bayar uang kuliah",
    "Top up GoPay",
    "Payroll",
    "Payroll July Rp8200000",
    "Potongan admin payroll",
    "beli permen",
    "beli es krim",
    "beli coklat",
    "beli snack",
    "beli makanan ringan",
    "beli wafer",
    "beli jajanan"
]


print("=== DIRECT PREDICTION ===")

for text in texts:
    label = predict_transaction(text)
    print(f"{text} => {label}")
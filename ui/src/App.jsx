import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [apiOk, setApiOk] = useState(false);
  const [loading, setLoading] = useState(false);
  const [payloadText, setPayloadText] = useState(`{
  "features": {
    "Gender": "Female",
    "Age": 29,
    "Under 30": "No",
    "Senior Citizen": "No",
    "Married": "Yes",
    "Dependents": "No",
    "Number of Dependents": 0,
    "Referred a Friend": "No",
    "Number of Referrals": 0,
    "Tenure in Months": 3,
    "Offer": null,
    "Phone Service": "Yes",
    "Avg Monthly Long Distance Charges": 10.0,
    "Multiple Lines": "No",
    "Internet Service": "Yes",
    "Internet Type": "Fiber Optic",
    "Avg Monthly GB Download": 25,
    "Online Security": "No",
    "Online Backup": "Yes",
    "Device Protection Plan": "No",
    "Premium Tech Support": "No",
    "Streaming TV": "Yes",
    "Streaming Movies": "Yes",
    "Streaming Music": "No",
    "Unlimited Data": "Yes",
    "Contract": "Month-to-Month",
    "Paperless Billing": "Yes",
    "Payment Method": "Bank Withdrawal",
    "Monthly Charge": 95.0,
    "Total Charges": 280.0,
    "Total Refunds": 0.0,
    "Total Extra Data Charges": 0.0,
    "Total Long Distance Charges": 30.0,
    "Total Revenue": 310.0,
    "CLTV": 4000
  }
}`);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    fetch(`${API}/health`)
      .then((r) => r.ok ? r.json() : Promise.reject(r))
      .then(() => setApiOk(true))
      .catch(() => setApiOk(false));
  }, []);

  async function onPredict() {
    setErr("");
    setResult(null);
    setLoading(true);
    try {
      // JSON parse kontrolü
      let body;
      try {
        body = JSON.parse(payloadText);
      } catch (parseError) {
        setErr(`JSON Parse Hatası: ${parseError.message}`);
        setLoading(false);
        return;
      }

      // API'ye istek gönder
      const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      // Response kontrolü
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ error: `HTTP ${res.status}: ${res.statusText}` }));
        setErr(JSON.stringify(errorData, null, 2));
        setLoading(false);
        return;
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error("Predict error:", e);
      setErr(`Hata: ${e.message || String(e)}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 980, margin: "40px auto", fontFamily: "system-ui", padding: 16 }}>
      <h1 style={{ marginBottom: 6 }}>Churn Predictor UI</h1>
      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 18 }}>
        <span style={{
          display: "inline-block",
          padding: "6px 10px",
          borderRadius: 999,
          background: apiOk ? "#e8fff0" : "#fff3f3",
          border: "1px solid #eee"
        }}>
          API: {apiOk ? "Connected" : "Not reachable"}
        </span>
        <span style={{ color: "#666", fontSize: 13 }}>React → FastAPI → Model Artifact</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 16 }}>
        <div style={{ border: "1px solid #eee", borderRadius: 14, padding: 14, background: "white" }}>
          <div style={{ fontWeight: 600, marginBottom: 8 }}>Request Body (JSON)</div>
          <textarea
            value={payloadText}
            onChange={(e) => setPayloadText(e.target.value)}
            rows={22}
            style={{ width: "100%", fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace", fontSize: 12, padding: 12, borderRadius: 12, border: "1px solid #ddd" }}
          />
          <button
            onClick={onPredict}
            disabled={loading}
            style={{ marginTop: 12, padding: "10px 14px", borderRadius: 12, border: "none", background: "#111827", color: "white", fontWeight: 600, cursor: "pointer" }}
          >
            {loading ? "Predicting..." : "Predict"}
          </button>
        </div>

        <div style={{ border: "1px solid #eee", borderRadius: 14, padding: 14, background: "white" }}>
          <div style={{ fontWeight: 600, marginBottom: 8 }}>Result</div>

          {!result && !err && !loading && (
            <div style={{ color: "#666", padding: 16, textAlign: "center" }}>
              "Predict" butonuna tıklayın, sonuç burada görünecek.
            </div>
          )}
          {loading && (
            <div style={{ color: "#666", padding: 16, textAlign: "center" }}>
              Tahmin yapılıyor...
            </div>
          )}

          {err && (
            <pre style={{ whiteSpace: "pre-wrap", background: "#fff3f3", border: "1px solid #ffd1d1", padding: 12, borderRadius: 12, fontSize: 12 }}>
              {err}
            </pre>
          )}

          {result && (
            <div style={{ display: "grid", gap: 12, padding: 8 }}>
              <div style={{ padding: 12, background: "#f0f9ff", borderRadius: 8, border: "1px solid #bae6fd" }}>
                <div style={{ fontSize: 12, color: "#666", marginBottom: 4 }}>Tahmin Sonucu</div>
                <div style={{ fontSize: 18, fontWeight: 600, color: result.pred_label === "Yes" ? "#dc2626" : "#16a34a" }}>
                  {result.pred_label === "Yes" ? "Müşteri Kaybedecek ⚠️" : "Müşteri Kalacak ✅"}
                </div>
              </div>
              <div style={{ padding: 12, background: "#f8fafc", borderRadius: 8 }}>
                <div><b>Olasılık (Yes):</b> {(Number(result.pred_proba_yes) * 100).toFixed(2)}%</div>
                <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
                  <b>Ham Değer:</b> {Number(result.pred_proba_yes).toFixed(4)}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

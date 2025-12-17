import { useEffect, useMemo, useState } from "react";

const API = "http://127.0.0.1:8000";

function Badge({ children }) {
  return (
    <span className="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-slate-100 text-slate-700">
      {children}
    </span>
  );
}

function Card({ title, children, right }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
        <div className="text-sm font-semibold text-slate-800">{title}</div>
        {right}
      </div>
      <div className="p-5">{children}</div>
    </div>
  );
}

function Progress({ value }) {
  const pct = Math.max(0, Math.min(1, value || 0));
  return (
    <div className="w-full">
      <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
        <div className="h-2 bg-slate-900" style={{ width: `${pct * 100}%` }} />
      </div>
      <div className="mt-2 text-xs text-slate-600">{(pct * 100).toFixed(1)}%</div>
    </div>
  );
}

// basit gruplama (istersen sonra daha “akıllı” hale getiririz)
function groupField(name) {
  const n = name.toLowerCase();
  if (["age", "gender", "married", "dependents", "senior", "under 30", "referr"].some(k => n.includes(k))) return "Demographics";
  if (["internet", "stream", "security", "backup", "device", "support", "unlimited", "phone", "lines"].some(k => n.includes(k))) return "Services";
  if (["contract", "payment", "paperless", "offer"].some(k => n.includes(k))) return "Billing";
  if (["gb", "download", "tenure", "long distance"].some(k => n.includes(k))) return "Usage";
  if (["charge", "revenue", "refund", "cltv"].some(k => n.includes(k))) return "Charges";
  return "Other";
}

export default function App() {
  const [meta, setMeta] = useState(null);
  const [features, setFeatures] = useState({});
  const [result, setResult] = useState(null);
  const [activeGroup, setActiveGroup] = useState("Demographics");
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      const m = await fetch(`${API}/meta`).then(r => r.json());
      setMeta(m);
      const s = await fetch(`${API}/sample`).then(r => r.json());
      setFeatures(s.features);
    })().catch(e => setErr(String(e)));
  }, []);

  const groups = useMemo(() => {
    if (!meta) return {};
    const g = {};
    for (const col of meta.expected_cols) {
      const grp = groupField(col);
      g[grp] = g[grp] || [];
      g[grp].push(col);
    }
    return g;
  }, [meta]);

  const visibleCols = useMemo(() => {
    const cols = (groups[activeGroup] || []);
    const qq = q.trim().toLowerCase();
    if (!qq) return cols;
    return cols.filter(c => c.toLowerCase().includes(qq));
  }, [groups, activeGroup, q]);

  function setField(col, value) {
    setFeatures(prev => ({ ...prev, [col]: value }));
  }

  async function predict() {
    setErr("");
    setResult(null);
    setLoading(true);
    try {
      const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features }),
      });
      const data = await res.json();
      if (!res.ok) setErr(JSON.stringify(data, null, 2));
      else setResult(data);
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  }

  if (err && !meta) {
    return <div className="p-8 text-red-600">{err}</div>;
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="flex items-start justify-between gap-6">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-semibold text-slate-900">Churn Predictor</h1>
              <Badge>React UI</Badge>
              <Badge>FastAPI</Badge>
              <Badge>Artifact Model</Badge>
            </div>
            <p className="mt-2 text-sm text-slate-600">
              Profesyonel demo: UI → API → Pipeline → Prediction
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={async () => {
                const s = await fetch(`${API}/sample`).then(r => r.json());
                setFeatures(s.features);
                setResult(null);
              }}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Load sample
            </button>

            <button
              disabled={loading || !meta}
              onClick={predict}
              className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-60"
            >
              {loading ? "Predicting..." : "Predict"}
            </button>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-12 gap-6">
          {/* Sidebar */}
          <div className="col-span-12 md:col-span-3">
            <Card title="Sections" right={<Badge>{meta ? meta.expected_cols.length : 0} fields</Badge>}>
              <div className="space-y-2">
                {Object.keys(groups).map(g => (
                  <button
                    key={g}
                    onClick={() => setActiveGroup(g)}
                    className={`w-full rounded-xl px-3 py-2 text-left text-sm font-medium ${
                      activeGroup === g ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                  >
                    {g} <span className="ml-2 text-xs opacity-70">({groups[g].length})</span>
                  </button>
                ))}
              </div>

              <div className="mt-4">
                <div className="text-xs font-medium text-slate-600 mb-2">Search field</div>
                <input
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  placeholder="e.g. Contract, Charges..."
                  className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-slate-300"
                />
              </div>
            </Card>

            <div className="mt-6">
              <Card title="Result">
                {!result && <div className="text-sm text-slate-600">Run prediction to see results.</div>}
                {result && (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-semibold text-slate-900">Label</div>
                      <Badge>{result.pred_label}</Badge>
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-slate-900 mb-2">Churn probability</div>
                      <Progress value={result.pred_proba_yes} />
                    </div>
                  </div>
                )}
                {err && (
                  <pre className="mt-4 text-xs bg-red-50 border border-red-100 text-red-700 rounded-xl p-3 overflow-x-auto">
                    {err}
                  </pre>
                )}
              </Card>
            </div>
          </div>

          {/* Form */}
          <div className="col-span-12 md:col-span-9">
            <Card title={`Inputs — ${activeGroup}`} right={<Badge>Auto-filled defaults</Badge>}>
              {!meta ? (
                <div className="text-sm text-slate-600">Loading meta…</div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {visibleCols.map((col) => {
                    const opts = meta.categorical_options?.[col];
                    const isCategorical = Array.isArray(opts);
                    const val = features[col] ?? "";

                    return (
                      <label key={col} className="space-y-1">
                        <div className="text-xs font-semibold text-slate-700">{col}</div>

                        {isCategorical ? (
                          <select
                            value={val}
                            onChange={(e) => setField(col, e.target.value)}
                            className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-slate-300"
                          >
                            {opts.map((o) => (
                              <option key={o} value={o}>{o}</option>
                            ))}
                          </select>
                        ) : (
                          <input
                            value={val}
                            onChange={(e) => setField(col, e.target.value)}
                            className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-slate-300"
                            placeholder={String(meta.defaults?.[col] ?? "")}
                          />
                        )}
                      </label>
                    );
                  })}
                </div>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

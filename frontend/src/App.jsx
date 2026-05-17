import React, {
  useEffect,
  useState,
  useRef,
} from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const API = "http://localhost:8000";

const S = {
  page: {
    background: "#f3f7fc",
    minHeight: "100vh",
    padding: 24,
    fontFamily: "Inter, sans-serif",
  },

  hero: {
    background:
      "linear-gradient(135deg,#2563eb,#1e40af)",
    borderRadius: 20,
    padding: 28,
    color: "white",
    marginBottom: 24,
    boxShadow: "0 10px 30px rgba(37,99,235,0.25)",
  },

  heroTitle: {
    fontSize: 34,
    fontWeight: 700,
    marginBottom: 10,
  },

  heroSub: {
    opacity: 0.9,
    fontSize: 16,
  },

  select: {
    padding: 14,
    borderRadius: 14,
    border: "1px solid #dbe4f0",
    marginBottom: 20,
    width: 320,
    fontSize: 16,
    background: "white",
  },

  alert: {
    background: "#fff1f2",
    border: "1px solid #fecdd3",
    color: "#be123c",
    padding: 14,
    borderRadius: 14,
    marginBottom: 12,
    fontWeight: 600,
  },

  grid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit,minmax(240px,1fr))",
    gap: 18,
    marginBottom: 24,
  },

  card: {
    background: "white",
    borderRadius: 20,
    padding: 22,
    boxShadow: "0 4px 18px rgba(0,0,0,0.06)",
  },

  label: {
    color: "#64748b",
    fontSize: 14,
    marginBottom: 10,
  },

  value: {
    fontSize: 34,
    fontWeight: 700,
    color: "#0f172a",
  },

  patientName: {
    fontSize: 24,
    fontWeight: 700,
    marginBottom: 8,
  },

  chartCard: {
    background: "white",
    borderRadius: 20,
    padding: 20,
    boxShadow: "0 4px 18px rgba(0,0,0,0.06)",
  },

  chatbotButton: {
    position: "fixed",
    bottom: 24,
    right: 24,
    width: 72,
    height: 72,
    borderRadius: "50%",
    background:
      "linear-gradient(135deg,#2563eb,#1d4ed8)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "white",
    fontSize: 34,
    cursor: "pointer",
    boxShadow: "0 12px 30px rgba(37,99,235,0.35)",
    zIndex: 999,
  },

  chatbotWindow: {
    position: "fixed",
    bottom: 110,
    right: 24,
    width: 380,
    height: 600,
    background: "white",
    borderRadius: 24,
    boxShadow: "0 20px 60px rgba(0,0,0,0.18)",
    overflow: "hidden",
    display: "flex",
    flexDirection: "column",
    zIndex: 999,
  },

  chatbotHeader: {
    background:
      "linear-gradient(135deg,#2563eb,#1d4ed8)",
    color: "white",
    padding: 18,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  },

  botTitle: {
    fontSize: 18,
    fontWeight: 700,
  },

  botSub: {
    fontSize: 13,
    opacity: 0.85,
  },

  closeBtn: {
    cursor: "pointer",
    fontSize: 22,
    fontWeight: 700,
  },

  messages: {
    flex: 1,
    overflowY: "auto",
    padding: 16,
    background: "#f8fafc",
  },

  userWrap: {
    textAlign: "right",
    marginBottom: 14,
  },

  botWrap: {
    textAlign: "left",
    marginBottom: 14,
  },

  userBubble: {
    display: "inline-block",
    background: "#2563eb",
    color: "white",
    padding: "12px 16px",
    borderRadius: 18,
    maxWidth: "78%",
    lineHeight: 1.5,
  },

  botBubble: {
    display: "inline-block",
    background: "white",
    color: "#111827",
    padding: "12px 16px",
    borderRadius: 18,
    maxWidth: "78%",
    lineHeight: 1.6,
    border: "1px solid #e2e8f0",
    whiteSpace: "pre-wrap",
  },

  inputArea: {
    padding: 16,
    borderTop: "1px solid #e5e7eb",
    display: "flex",
    gap: 10,
    background: "white",
  },

  input: {
    flex: 1,
    padding: 14,
    borderRadius: 14,
    border: "1px solid #dbe4f0",
    outline: "none",
  },

  sendBtn: {
    background: "#2563eb",
    color: "white",
    border: "none",
    padding: "14px 18px",
    borderRadius: 14,
    cursor: "pointer",
    fontWeight: 600,
  },
};

export default function App() {
  const [patients, setPatients] = useState([]);
  const [selected, setSelected] = useState("P0001");
  const [dashboard, setDashboard] = useState(null);

  const [chatOpen, setChatOpen] = useState(false);

  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text:
        "Hello 👋\nI am your AI healthcare monitoring assistant. Ask me anything about patient vitals, alerts, risks, or sensor data.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const messageEndRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/patients`)
      .then((r) => r.json())
      .then(setPatients)
      .catch(console.error);
  }, []);

  useEffect(() => {
    fetch(`${API}/patient/${selected}`)
      .then((r) => r.json())
      .then(setDashboard)
      .catch(console.error);
  }, [selected]);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMessage = {
      role: "user",
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
        }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.answer,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Backend connection failed.",
        },
      ]);
    }

    setLoading(false);
    setQuery("");
  };

  if (!dashboard) {
    return <div style={{ padding: 20 }}>Loading...</div>;
  }

  const p = dashboard.patient;
  const s = dashboard.summary;

  return (
    <div style={S.page}>

      <div style={S.hero}>
        <div style={S.heroTitle}>
          🏥 IoT Patient Monitoring Dashboard
        </div>

        <div style={S.heroSub}>
          Real-time wearable healthcare analytics powered by AI + RAG + GPT-4o
        </div>
      </div>

      <select
        style={S.select}
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
      >
        {patients.map((p) => (
          <option
            key={p.patient_id}
            value={p.patient_id}
          >
            {p.patient_id} - {p.name}
          </option>
        ))}
      </select>

      {s.alerts.map((a, i) => (
        <div key={i} style={S.alert}>
          🚨 {a}
        </div>
      ))}

      <div style={S.grid}>

        <div style={S.card}>
          <div style={S.patientName}>{p.name}</div>
          <div>{p.patient_id}</div>
          <div>{p.age} years</div>
          <div>{p.known_condition}</div>
        </div>

        <div style={S.card}>
          <div style={S.label}>Heart Rate</div>
          <div style={S.value}>
            {s.heart_rate.bpm}
          </div>
          <div>BPM</div>
        </div>

        <div style={S.card}>
          <div style={S.label}>Blood Oxygen</div>
          <div style={S.value}>
            {s.spo2.spo2_pct}%
          </div>
          <div>SpO2</div>
        </div>

        <div style={S.card}>
          <div style={S.label}>Temperature</div>
          <div style={S.value}>
            {s.temperature.temp_celsius}°C
          </div>
        </div>

      </div>

      <div style={S.grid}>

        <div style={S.chartCard}>
          <h3>Heart Rate Trend</h3>

          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={dashboard.charts.heart_rate}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" hide />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="bpm"
                stroke="#2563eb"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={S.chartCard}>
          <h3>SpO2 Trend</h3>

          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={dashboard.charts.spo2}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" hide />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="spo2_pct"
                stroke="#16a34a"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={S.chartCard}>
          <h3>Temperature Trend</h3>

          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={dashboard.charts.temperature}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" hide />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="temp_celsius"
                stroke="#dc2626"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

      </div>

      {!chatOpen && (
        <div
          style={S.chatbotButton}
          onClick={() => setChatOpen(true)}
        >
          🤖
        </div>
      )}

      {chatOpen && (
        <div style={S.chatbotWindow}>

          <div style={S.chatbotHeader}>

            <div>
              <div style={S.botTitle}>
                🤖 AI Health Assistant
              </div>

              <div style={S.botSub}>
                GPT-4o + RAG Monitoring
              </div>
            </div>

            <div
              style={S.closeBtn}
              onClick={() => setChatOpen(false)}
            >
              ×
            </div>

          </div>

          <div style={S.messages}>

            {messages.map((m, i) => (
              <div
                key={i}
                style={
                  m.role === "user"
                    ? S.userWrap
                    : S.botWrap
                }
              >

                <div
                  style={
                    m.role === "user"
                      ? S.userBubble
                      : S.botBubble
                  }
                >
                  {m.text}
                </div>

              </div>
            ))}

            {loading && (
              <div style={S.botWrap}>
                <div style={S.botBubble}>
                  Thinking...
                </div>
              </div>
            )}

            <div ref={messageEndRef} />

          </div>

          <div style={S.inputArea}>

            <input
              style={S.input}
              placeholder="Ask about patient vitals..."
              value={query}
              onChange={(e) =>
                setQuery(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button
              style={S.sendBtn}
              onClick={sendMessage}
            >
              Send
            </button>

          </div>

        </div>
      )}

    </div>
  );
}
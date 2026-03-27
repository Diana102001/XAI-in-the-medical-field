import "./App.css";
import PageShell from "./components/PageShell";
import AIModelForm from "./components/AIModelForm";
import ModelChat from "./components/ModelChat";
import { useState } from "react";

export default function App() {
  const [tab, setTab] = useState("registry");

  return (
    <PageShell
      title="Model Registry"
      subtitle="Create, describe, and ship explainable AI models with confidence."
    >
      <div className="tabs">
        <button onClick={() => setTab("registry")} className={tab === "registry" ? "active" : ""}>
          Create model
        </button>
        <button onClick={() => setTab("query")} className={tab === "query" ? "active" : ""}>
          Query model
        </button>
      </div>

      {tab === "registry" ? <AIModelForm /> : <ModelChat />}
    </PageShell>
  );
}

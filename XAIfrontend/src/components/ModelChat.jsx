import { useState, useEffect } from "react";

export default function ModelChat() {
  const [models, setModels] = useState([]);
  const [selectedModelId, setSelectedModelId] = useState(null);
  const [fields, setFields] = useState([]);
  const [inputs, setInputs] = useState({});
  const [messages, setMessages] = useState([]);
  const [working, setWorking] = useState(false);

  useEffect(() => {
    async function loadModels() {
      try {
        const response = await fetch("/api/ai/models/");
        const data = await response.json();
        setModels(data);
      } catch (error) {
        console.error("Unable to load models", error);
      }
    }
    loadModels();
  }, []);

  useEffect(() => {
    if (!selectedModelId) return;

    async function loadDynamicForm() {
      try {
        const response = await fetch(`/api/ai/models/${selectedModelId}/dynamic-form/`);
        const data = await response.json();
        const fieldEntries = [];
        if (data.form) {
          for (const key in data.form) {
            if (!Object.hasOwn(data.form, key)) continue;
            const field = data.form[key];
            fieldEntries.push({
              name: field.name || key,
              label: field.label || key,
              type: field.type || "text",
              required: field.required,
              attrs: field.attrs || {},
            });
          }
        }
        setFields(fieldEntries);
        setInputs(fieldEntries.reduce((acc, f) => ({ ...acc, [f.name]: "" }), {}));
        setMessages((prev) => [
          ...prev,
          { from: "system", text: `Form for model ${selectedModelId} loaded.` },
        ]);
      } catch (error) {
        console.error("Unable to load form", error);
      }
    }

    loadDynamicForm();
  }, [selectedModelId]);

  const handleModelChange = (event) => {
    setSelectedModelId(event.target.value);
    setFields([]);
    setInputs({});
    setMessages((prev) => [
      ...prev,
      { from: "system", text: `Model ${event.target.value} selected.` },
    ]);
  };

  const handleInputChange = (name, value) => {
    setInputs((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedModelId) return;

    setWorking(true);

    setMessages((prev) => [...prev, { from: "user", text: JSON.stringify(inputs) }]);

    try {
      const response = await fetch(`/api/ai/models/${selectedModelId}/dynamic-form/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs),
      });
      const data = await response.json();

      if (response.ok) {
        setMessages((prev) => [...prev, { from: "model", text: JSON.stringify(data.result) }]);
      } else {
        setMessages((prev) => [...prev, { from: "error", text: JSON.stringify(data.errors || data) }]);
      }
    } catch (error) {
      console.error("Query failed", error);
      setMessages((prev) => [...prev, { from: "error", text: String(error) }]);
    }

    setWorking(false);
  };

  return (
    <div className="chat-page">
      <h3>Query a registered model</h3>

      <div className="field">
        <label htmlFor="model-select">Choose model:</label>
        <select id="model-select" value={selectedModelId || ""} onChange={handleModelChange}>
          <option value="" disabled>Select a model</option>
          {models.map((model) => (
            <option key={model.id} value={model.id}>{model.name || model.modelURI || `#${model.id}`}</option>
          ))}
        </select>
      </div>

      {selectedModelId && (
        <form onSubmit={handleSubmit} className="query-form">
          {fields.map((field) => (
            <div className="field" key={field.name}>
              <label htmlFor={`field-${field.name}`}>{field.label}</label>
              <input
                id={`field-${field.name}`}
                type={field.type === "integer" ? "number" : field.type}
                required={field.required}
                value={inputs[field.name] || ""}
                onChange={(event) => handleInputChange(field.name, event.target.value)}
              />
            </div>
          ))}

          <button type="submit" disabled={working}>
            {working ? "Running..." : "Query model"}
          </button>
        </form>
      )}

      <div className="chat-window">
        {messages.map((message, idx) => (
          <div key={idx} className={`chat-message ${message.from}`}>
            <strong>{message.from}:</strong> {message.text}
          </div>
        ))}
      </div>
    </div>
  );
}

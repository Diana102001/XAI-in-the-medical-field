import { useState } from "react";

export default function TagInput({ label, placeholder, value, onChange, maxTags }) {
  const [draft, setDraft] = useState("");

  const addTag = () => {
    const trimmed = draft.trim();
    if (!trimmed) return;
    if (value.includes(trimmed)) {
      setDraft("");
      return;
    }
    if (maxTags && value.length >= maxTags) return;
    onChange([...value, trimmed]);
    setDraft("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addTag();
    }
  };

  const removeTag = (tag) => {
    onChange(value.filter((item) => item !== tag));
  };

  const canAdd = !maxTags || value.length < maxTags;

  return (
    <div className="tag-input">
      <div className="label-row">
        <span className="label">{label}</span>
        <span className="tag-count">{value.length} labels</span>
      </div>
      <div className="tag-list">
        {value.map((tag) => (
          <button
            key={tag}
            type="button"
            className="tag"
            onClick={() => removeTag(tag)}
          >
            {tag}
            <span className="tag-x">×</span>
          </button>
        ))}
      </div>
      <div className="tag-form">
        <input
          className="input"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={!canAdd}
        />
        <button className="btn ghost" type="button" onClick={addTag} disabled={!canAdd}>
          Add
        </button>
      </div>
      <p className="hint">Tap a label to remove it.</p>
    </div>
  );
}

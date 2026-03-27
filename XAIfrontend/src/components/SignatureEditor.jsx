export default function SignatureEditor({ label, value, onChange, hint }) {
  return (
    <label className="field">
      <span className="label">{label}</span>
      <textarea
        className="textarea monospace"
        rows={6}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
      {hint ? <span className="hint">{hint}</span> : null}
    </label>
  );
}

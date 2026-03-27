export default function PageShell({ title, subtitle, children }) {
  return (
    <div className="page">
      <header className="hero">
        <p className="eyebrow">XAI Studio</p>
        <h1>{title}</h1>
        <p className="subtitle">{subtitle}</p>
      </header>
      <main className="content">{children}</main>
    </div>
  );
}

import React, { useState } from "react";

export default function App() {
  const [brief, setBrief] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [projectData, setProjectData] = useState<any>(null);

  const generateProject = async () => {
    if (!brief.trim()) {
      alert("Please enter a project brief!");
      return;
    }

    setLoading(true);
    setMessage("");
    setProjectData(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/brief", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ brief }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Unknown error");

      setProjectData(data);
      setMessage("✅ Project generated successfully!");
    } catch (err: any) {
      console.error(err);
      setMessage("❌ Error generating project: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadZip = async () => {
    if (!projectData?.project_dir) return;

    const folderName = projectData.project_dir.split("\\").pop();
    window.open(`http://127.0.0.1:8000/api/brief/download/${folderName}`, "_blank");
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "Inter, sans-serif",
        color: "#fff",
        padding: "2rem",
      }}
    >
      <div
        style={{
          background: "rgba(255, 255, 255, 0.1)",
          backdropFilter: "blur(8px)",
          borderRadius: "16px",
          padding: "2rem",
          width: "100%",
          maxWidth: "600px",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.3)",
        }}
      >
        <h1 style={{ textAlign: "center", marginBottom: "1rem", fontSize: "1.8rem" }}>
          🧠 AI Project Builder
        </h1>
        <p style={{ textAlign: "center", marginBottom: "1rem", opacity: 0.8 }}>
          Describe your project idea — I’ll generate the backend, frontend, and tasks for you.
        </p>

        <textarea
          value={brief}
          onChange={(e) => setBrief(e.target.value)}
          placeholder="e.g., Build a movie review app using FastAPI and React"
          style={{
            width: "100%",
            height: "120px",
            padding: "1rem",
            borderRadius: "8px",
            border: "none",
            outline: "none",
            resize: "none",
            background: "rgba(255,255,255,0.15)",
            color: "#fff",
            marginBottom: "1rem",
          }}
        />

        <button
          onClick={generateProject}
          disabled={loading}
          style={{
            width: "100%",
            padding: "0.8rem",
            background: loading
              ? "linear-gradient(90deg, #777, #555)"
              : "linear-gradient(90deg, #00c6ff, #0072ff)",
            border: "none",
            color: "#fff",
            fontSize: "1rem",
            fontWeight: 600,
            borderRadius: "8px",
            cursor: loading ? "wait" : "pointer",
            transition: "0.3s ease",
          }}
        >
          {loading ? "⏳ Generating..." : "🚀 Generate Project"}
        </button>

        {message && (
          <p
            style={{
              marginTop: "1.5rem",
              textAlign: "center",
              fontWeight: 500,
              color: message.startsWith("✅") ? "#90ee90" : "#ff7f7f",
            }}
          >
            {message}
          </p>
        )}

        {projectData && (
          <div
            style={{
              marginTop: "1.5rem",
              background: "rgba(255,255,255,0.1)",
              padding: "1rem",
              borderRadius: "8px",
            }}
          >
            <h3 style={{ marginBottom: "0.5rem" }}>📁 Project Folder:</h3>
            <code
              style={{
                display: "block",
                marginBottom: "1rem",
                color: "#aee",
                wordWrap: "break-word",
              }}
            >
              {projectData.project_dir}
            </code>

            <button
              onClick={downloadZip}
              style={{
                background: "linear-gradient(90deg, #43e97b, #38f9d7)",
                border: "none",
                padding: "0.6rem 1rem",
                borderRadius: "8px",
                cursor: "pointer",
                color: "#000",
                fontWeight: 600,
                display: "block",
                margin: "0 auto",
              }}
            >
              💾 Download ZIP
            </button>

            <h3 style={{ marginTop: "1.5rem" }}>🧩 Tasks:</h3>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {projectData.tasks?.map((task: any, i: number) => (
                <li
                  key={i}
                  style={{
                    background: "rgba(255,255,255,0.1)",
                    padding: "0.5rem 1rem",
                    borderRadius: "6px",
                    marginBottom: "0.5rem",
                  }}
                >
                  <strong>{task.name}</strong> — {task.description} ({task.assigned_to})
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

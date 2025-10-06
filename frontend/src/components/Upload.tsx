import { useState } from "react";

export default function ProjectBrief() {
  const [brief, setBrief] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/brief/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ brief }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Failed to process brief");
      }

      const data = await response.json();
      setResult(data.result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-12 p-6 bg-white shadow-md rounded-2xl">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">AI Project Brief</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="w-full p-3 border rounded-lg text-gray-700 focus:ring-2 focus:ring-indigo-500"
          rows={4}
          placeholder="Describe your project idea..."
          value={brief}
          onChange={(e) => setBrief(e.target.value)}
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-4 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700"
        >
          {loading ? "Processing..." : "Submit Brief"}
        </button>
      </form>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {result && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Project Summary</h2>
          <p className="text-gray-700 mb-4">{result.summary}</p>
          <h3 className="font-semibold">Initial Tasks:</h3>
          <ul className="list-disc ml-6 text-gray-700">
            {result.tasks.map((task: string, idx: number) => (
              <li key={idx}>{task}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

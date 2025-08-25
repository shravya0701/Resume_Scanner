import React, { useState } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from "recharts";
import "../styles/App.css"; // import your CSS file

interface ScoreResult {
  score: number;
  coverage_percentage: number;
  matched_keywords: string[];
  missing_keywords: string[];
  suggestions: string[];
}

const COLORS = ["#4caf50", "#f44336"]; // green = matched, red = missing

const UploadForm: React.FC = () => {
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [positionTitle, setPositionTitle] = useState("");
  const [result, setResult] = useState<ScoreResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resume || !jobDescription) return;

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);
    formData.append("position_title", positionTitle);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/score",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  // Prepare pie chart data
  const pieData = result
    ? [
        { name: "Matched", value: result.matched_keywords.length },
        { name: "Missing", value: result.missing_keywords.length },
      ]
    : [];

  return (
    <div className="container mt-5">
      {/* Page Title */}
      <h2 className="page-title">
        <i className="bi bi-file-earmark-text"></i> Resume–Job Match Scorer
      </h2>

      {/* Upload Form */}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Position Title (optional)</label>
          <input
            type="text"
            className="form-control"
            value={positionTitle}
            onChange={(e) => setPositionTitle(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Job Description</label>
          <textarea
            className="form-control"
            rows={6}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            required
          ></textarea>
        </div>

        <div className="mb-3">
          <label className="form-label">Upload Resume (.pdf only)</label>
          <input
            type="file"
            className="form-control"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setResume(e.target.files?.[0] || null)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Scoring..." : "Submit"}
        </button>
      </form>

      {/* Error Message */}
      {error && <div className="alert alert-danger mt-3">{error}</div>}

      {/* Results Section */}
      {result && (
        <div className="mt-4">
          {/* Score Card */}
          <div className="score-card">
            <h5>Score: {result.score}/10</h5>
            <div className="mb-2">
              <div className="progress">
                <div
                  className="progress-bar"
                  role="progressbar"
                  style={{ width: `${result.coverage_percentage}%` }}
                  aria-valuenow={result.coverage_percentage}
                  aria-valuemin={0}
                  aria-valuemax={100}
                >
                  {result.coverage_percentage}%
                </div>
              </div>
            </div>
          </div>

          {/* Matched / Missing Keywords */}
          <div className="row">
            <div className="col-md-6 mb-3">
              <div className="card h-100 p-3">
                <h6>Matched Keywords</h6>
                <p>{result.matched_keywords.join(", ") || "None"}</p>
              </div>
            </div>

            <div className="col-md-6 mb-3">
              <div className="card h-100 p-3">
                <h6>Missing Keywords (top 10)</h6>
                <p>
                  {result.missing_keywords.slice(0, 10).join(", ")}
                  {result.missing_keywords.length > 10 ? "..." : ""}
                </p>
              </div>
            </div>
          </div>

          {/* Suggestions */}
          <div className="card mb-3 p-3">
            <h6>Suggestions</h6>
            <ul>
              {result.suggestions.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          {/* Pie Chart */}
          {pieData.length > 0 && (
            <div className="card pie-card">
              <h6>Keyword Match Pie Chart</h6>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    label
                  >
                    {pieData.map((_entry, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Legend verticalAlign="bottom" />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadForm;

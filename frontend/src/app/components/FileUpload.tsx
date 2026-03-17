"use client";

import { useState } from "react";

type AnalyzeResponse = {
  parsed: string;
  context: string[];
  recommendation: string;
};

type FileUploadProps = {
  onAnalyzeSuccess: (result: AnalyzeResponse) => void;
  onAnalyzeStateChange: (isAnalyzing: boolean) => void;
};

const API_BASE = "/backend";

export default function FileUpload({ onAnalyzeSuccess, onAnalyzeStateChange }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyzeClick = async () => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError(null);
      onAnalyzeStateChange(true);

      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
        cache: "no-store"
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}.`);
      }

      const data: AnalyzeResponse = await response.json();
      onAnalyzeSuccess(data);
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Upload failed.");
    } finally {
      setLoading(false);
      onAnalyzeStateChange(false);
    }
  };
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Upload PDF Report</h2>
      <p className="mt-2 text-sm text-slate-600">
        Select a maintenance report PDF and analyze it with the backend.
      </p>

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          type="file"
          accept="application/pdf"
          onChange={(event) => {
            setFile(event.target.files?.[0] ?? null);
            setError(null);
          }}
          className="block w-full flex-1 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 file:mr-4 file:rounded-md file:border-0 file:bg-slate-100 file:px-3 file:py-2 file:text-sm file:font-medium"
        />

        <button
          type="button"
          onClick={handleAnalyzeClick}
          disabled={loading}
          className="w-full shrink-0 rounded-md border border-blue-700 bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:border-slate-300 disabled:bg-slate-300 sm:w-auto"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {file ? <p className="mt-2 text-xs text-slate-500">Selected: {file.name}</p> : null}

      {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
    </section>
  );
}

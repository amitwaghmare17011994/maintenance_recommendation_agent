"use client";

type AnalyzeResult = {
  parsed: string;
  context: string[];
  recommendation: string;
};

type ResultViewProps = {
  result: AnalyzeResult | null;
};

function formatParsed(parsed: string): string {
  try {
    const parsedJson = JSON.parse(parsed);
    return JSON.stringify(parsedJson, null, 2);
  } catch {
    return parsed;
  }
}

export default function ResultView({ result }: ResultViewProps) {
  if (!result) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Analysis Result</h2>
        <p className="mt-2 text-sm text-slate-600">
          Upload a PDF to see parsed data and recommendation.
        </p>
      </section>
    );
  }

  return (
    <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Analysis Result</h2>

      <div>
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Parsed Data</h3>
        <pre className="mt-2 overflow-auto rounded-md bg-slate-900 p-4 text-xs text-slate-100">
          {formatParsed(result.parsed)}
        </pre>
      </div>

      <div>
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Recommendation
        </h3>
        <p className="mt-2 whitespace-pre-wrap rounded-md bg-slate-50 p-4 text-sm text-slate-800">
          {result.recommendation}
        </p>
      </div>
    </section>
  );
}

"use client";

type AnalyzeResult = {
  parsed: string;
  context: string[];
  recommendation: string;
};

type ResultViewProps = {
  result: AnalyzeResult | null;
  isLoading: boolean;
};

function formatParsed(parsed: string): string {
  try {
    const parsedJson = JSON.parse(parsed);
    return JSON.stringify(parsedJson, null, 2);
  } catch {
    return parsed;
  }
}

export default function ResultView({ result, isLoading }: ResultViewProps) {
  if (!isLoading && !result) {
    return null;
  }

  if (isLoading) {
    return (
      <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-900">Analysis Result</h2>
        <div className="animate-pulse space-y-4">
          <div>
            <div className="h-4 w-28 rounded bg-slate-200" />
            <div className="mt-2 h-44 w-full rounded-md bg-slate-200" />
          </div>
          <div>
            <div className="h-4 w-36 rounded bg-slate-200" />
            <div className="mt-2 h-32 w-full rounded-md bg-slate-200" />
          </div>
        </div>
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

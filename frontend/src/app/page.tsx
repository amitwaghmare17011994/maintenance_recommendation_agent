"use client";

import { useState } from "react";

import ChatBox from "./components/ChatBox";
import FileUpload from "./components/FileUpload";
import FloatingChat from "./components/FloatingChat";
import ResultView from "./components/ResultView";

type AnalyzeResult = {
  parsed: string;
  context: string[];
  recommendation: string;
};

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

const API_BASE = "/backend";

export default function HomePage() {
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const handleAnalyzeSuccess = (data: AnalyzeResult) => {
    setResult(data);
  };

  const handleSendMessage = async (query: string) => {
    setMessages((previous) => [...previous, { role: "user", content: query }]);
    setChatLoading(true);

    try {
      const response = await fetch(`${API_BASE}/agent?query=${encodeURIComponent(query)}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
      });

      if (!response.ok) {
        throw new Error(`Agent request failed with status ${response.status}.`);
      }

      const data: { answer?: string } = await response.json();
      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.answer ?? "No response from agent." }
      ]);
    } catch (requestError) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            requestError instanceof Error ? requestError.message : "Failed to contact backend."
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 p-6 text-slate-900 sm:p-8">
      <div className="mx-auto max-w-4xl space-y-6">
        <section className="space-y-2">
          <h1 className="text-3xl font-bold">Maintenance Agent UI</h1>
          <p className="text-sm text-slate-600">
            Upload a report, review analysis output, then chat with the agent.
          </p>
        </section>

        <FileUpload
          onAnalyzeSuccess={handleAnalyzeSuccess}
          onAnalyzeStateChange={(loading) => {
            setIsAnalyzing(loading);
            if (loading) {
              setResult(null);
              setChatOpen(false);
            }
          }}
        />
        <ResultView result={result} isLoading={isAnalyzing} />
      </div>

      <FloatingChat visible={Boolean(result) && !chatOpen} onOpen={() => setChatOpen(true)} />
      {result ? (
        <ChatBox
          open={chatOpen}
          messages={messages}
          loading={chatLoading}
          onSendMessage={handleSendMessage}
          onClose={() => setChatOpen(false)}
        />
      ) : null}
    </main>
  );
}

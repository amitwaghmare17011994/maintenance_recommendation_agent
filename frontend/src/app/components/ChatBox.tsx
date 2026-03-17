"use client";

import { FormEvent, useState } from "react";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

type ChatBoxProps = {
  open: boolean;
  messages: ChatMessage[];
  loading: boolean;
  onSendMessage: (query: string) => Promise<void>;
  onClose: () => void;
};

export default function ChatBox({ open, messages, loading, onSendMessage, onClose }: ChatBoxProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmed = query.trim();
    if (!trimmed || loading) {
      return;
    }

    setQuery("");
    await onSendMessage(trimmed);
  };

  return (
    <aside
      className={`fixed right-0 top-0 z-30 flex h-screen w-full max-w-md transform flex-col border-l border-slate-200 bg-white shadow-xl transition-transform duration-200 ${
        open ? "translate-x-0" : "translate-x-full"
      }`}
    >
      <div className="border-b border-slate-200 p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Maintenance Agent Chat</h2>
            <p className="text-sm text-slate-500">Ask questions about your uploaded report.</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close chat panel"
            className="rounded-md border border-slate-300 px-2 py-1 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
          >
            X
          </button>
        </div>
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <p className="rounded-md bg-slate-50 p-3 text-sm text-slate-600">
            Your chat history will appear here.
          </p>
        ) : null}

        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`max-w-[90%] rounded-lg px-3 py-2 text-sm ${
              message.role === "user"
                ? "ml-auto bg-slate-900 text-white"
                : "bg-slate-100 text-slate-800"
            }`}
          >
            {message.content}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="border-t border-slate-200 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Ask the agent..."
            className="flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </form>
    </aside>
  );
}

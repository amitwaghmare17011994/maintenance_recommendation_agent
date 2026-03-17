"use client";

type FloatingChatProps = {
  visible: boolean;
  onOpen: () => void;
};

export default function FloatingChat({ visible, onOpen }: FloatingChatProps) {
  if (!visible) {
    return null;
  }

  return (
    <button
      type="button"
      onClick={onOpen}
      className="fixed bottom-6 right-6 z-40 rounded-full bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-slate-700"
    >
      Open Chat
    </button>
  );
}

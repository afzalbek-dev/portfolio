import React from 'react';
import { Send, MessageSquare } from 'lucide-react';

interface FloatingCTAProps {
  adminTelegramLink?: string;
  whatsappNumber?: string;
}

export const FloatingCTA: React.FC<FloatingCTAProps> = ({
  adminTelegramLink = "https://t.me/developer_username",
  whatsappNumber = "+998901234567"
}) => {
  const waClean = whatsappNumber.replace(/[^0-9]/g, "");

  return (
    <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-3">
      {/* WhatsApp Floating Button */}
      <a
        href={`https://wa.me/${waClean}`}
        target="_blank"
        rel="noreferrer"
        className="w-13 h-13 p-3.5 rounded-full bg-emerald-500 hover:bg-emerald-600 text-white shadow-xl shadow-emerald-500/30 hover:scale-110 active:scale-95 transition-all flex items-center justify-center group"
        title="Chat on WhatsApp"
      >
        <MessageSquare className="w-6 h-6" />
      </a>

      {/* Telegram Floating Button (Direct Personal Link) */}
      <a
        href={adminTelegramLink}
        target="_blank"
        rel="noreferrer"
        className="w-13 h-13 p-3.5 rounded-full bg-brand-blue hover:bg-blue-600 text-white shadow-xl shadow-blue-500/30 hover:scale-110 active:scale-95 transition-all flex items-center justify-center group"
        title="Chat on Telegram"
      >
        <Send className="w-6 h-6" />
      </a>
    </div>
  );
};

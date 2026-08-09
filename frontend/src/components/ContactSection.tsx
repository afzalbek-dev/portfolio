import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Send, MessageSquare, Instagram, Mail } from 'lucide-react';

interface ContactSectionProps {
  adminTelegramLink?: string;
  whatsappNumber?: string;
  instagramUser?: string;
  emailAddr?: string;
}

export const ContactSection: React.FC<ContactSectionProps> = ({
  adminTelegramLink = "https://t.me/developer_username",
  whatsappNumber = "+998901234567",
  instagramUser = "@developer_username",
  emailAddr = "dev@example.com"
}) => {
  const { t } = useTranslation();

  const waClean = whatsappNumber.replace(/[^0-9]/g, "");
  const instaClean = instagramUser.replace("@", "").trim();

  const contacts = [
    {
      name: "Telegram (Admin)",
      icon: <Send className="w-6 h-6 text-brand-blue" />,
      action: t('contact.admin_btn'),
      link: adminTelegramLink,
      badge: "Direct Telegram"
    },
    {
      name: "WhatsApp",
      icon: <MessageSquare className="w-6 h-6 text-emerald-400" />,
      action: t('contact.msg_wa'),
      link: `https://wa.me/${waClean}`,
      badge: whatsappNumber
    },
    {
      name: "Instagram",
      icon: <Instagram className="w-6 h-6 text-rose-400" />,
      action: "Instagram",
      link: `https://instagram.com/${instaClean}`,
      badge: instagramUser
    },
    {
      name: "Email",
      icon: <Mail className="w-6 h-6 text-purple-400" />,
      action: t('contact.msg_email'),
      link: `mailto:${emailAddr}`,
      badge: emailAddr
    }
  ];

  return (
    <section id="contact" className="py-20 relative bg-slate-900/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-purple bg-brand-purple/10 px-3 py-1 rounded-full">
            {t('contact.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('contact.subtitle')}
          </h2>
        </div>

        {/* Contacts Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {contacts.map((c, idx) => (
            <motion.a
              key={idx}
              href={c.link}
              target="_blank"
              rel="noreferrer"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: idx * 0.1 }}
              className="glass-card rounded-2xl p-6 text-center space-y-4 hover:border-brand-blue/50 hover:scale-105 transition-all group flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                  {c.icon}
                </div>
                <h3 className="text-lg font-bold text-white">{c.name}</h3>
                <p className="text-xs text-slate-400 font-mono truncate">{c.badge}</p>
              </div>

              <span className="w-full py-2.5 rounded-xl bg-white/5 group-hover:bg-brand-blue group-hover:text-white text-xs font-bold text-slate-300 transition-colors block">
                {c.action}
              </span>
            </motion.a>
          ))}
        </div>

      </div>
    </section>
  );
};

import React from 'react';
import { useTranslation } from 'react-i18next';
import { Terminal, Github, Send, Instagram, Mail } from 'lucide-react';

export const Footer: React.FC = () => {
  const { t } = useTranslation();

  return (
    <footer className="glass-panel border-t border-white/10 pt-16 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-white/10">
          
          {/* Brand Col */}
          <div className="space-y-4 md:col-span-2">
            <a href="#" className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-blue to-brand-purple flex items-center justify-center text-white">
                <Terminal className="w-6 h-6" />
              </div>
              <span className="font-extrabold text-xl tracking-tight text-white">
                Dev<span className="text-brand-blue">Portfolio</span>
              </span>
            </a>
            <p className="text-xs text-slate-400 max-w-sm leading-relaxed">
              Professional Telegram Bot, Web & AI Engineering Solutions. High quality scalable applications for businesses, startups, and private projects.
            </p>
          </div>

          {/* Nav Quick Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Navigation</h4>
            <div className="flex flex-col gap-2 text-xs text-slate-400 font-medium">
              <a href="#home" className="hover:text-brand-blue transition-colors">{t('nav.home')}</a>
              <a href="#about" className="hover:text-brand-blue transition-colors">{t('nav.about')}</a>
              <a href="#services" className="hover:text-brand-blue transition-colors">{t('nav.services')}</a>
              <a href="#portfolio" className="hover:text-brand-blue transition-colors">{t('nav.portfolio')}</a>
              <a href="#order" className="hover:text-brand-blue transition-colors">{t('nav.order')}</a>
            </div>
          </div>

          {/* Social Media Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Social Media</h4>
            <div className="flex items-center gap-3">
              <a href="https://t.me/developer_username" target="_blank" rel="noreferrer" className="p-2 rounded-lg bg-white/5 hover:bg-brand-blue/20 text-slate-300 hover:text-brand-blue transition-colors">
                <Send className="w-4 h-4" />
              </a>
              <a href="https://github.com" target="_blank" rel="noreferrer" className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white transition-colors">
                <Github className="w-4 h-4" />
              </a>
              <a href="https://instagram.com" target="_blank" rel="noreferrer" className="p-2 rounded-lg bg-white/5 hover:bg-rose-500/20 text-slate-300 hover:text-rose-400 transition-colors">
                <Instagram className="w-4 h-4" />
              </a>
            </div>
          </div>

        </div>

        {/* Bottom Copyright */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>© 2026 Developer Portfolio. {t('footer.rights')}</p>
          <p className="font-mono">Built with React, FastAPI & Aiogram 3.x</p>
        </div>

      </div>
    </footer>
  );
};

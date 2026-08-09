import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Bot, Globe, Sparkles, Terminal, CheckCircle2 } from 'lucide-react';

interface AboutProps {
  aboutText?: string;
}

export const About: React.FC<AboutProps> = ({ aboutText }) => {
  const { t, i18n } = useTranslation();

  return (
    <section id="about" className="py-20 relative bg-slate-900/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-blue bg-brand-blue/10 px-3 py-1 rounded-full">
            {t('about.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('about.subtitle')}
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Text Overview */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-7 space-y-6"
          >
            <h3 className="text-2xl font-bold text-white leading-snug">
              Specialized in high-load Telegram Bots, Web Applications & Generative AI Systems.
            </h3>
            
            <p className="text-slate-300 text-base leading-relaxed">
              {aboutText || t('hero.subtitle')}
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                <span className="text-sm font-medium text-slate-200">Aiogram 3.x Async Bot Architecture</span>
              </div>
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                <span className="text-sm font-medium text-slate-200">FastAPI REST APIs & PostgreSQL</span>
              </div>
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                <span className="text-sm font-medium text-slate-200">Telegram Mini Apps (Web Apps)</span>
              </div>
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                <span className="text-sm font-medium text-slate-200">OpenAI & Gemini API Integrations</span>
              </div>
            </div>
          </motion.div>

          {/* Right Stats Grid */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-5 grid grid-cols-2 gap-4"
          >
            <div className="glass-card p-6 rounded-2xl border border-white/10 hover:border-brand-blue/40 transition-all text-center space-y-3">
              <div className="w-12 h-12 rounded-xl bg-brand-blue/10 text-brand-blue flex items-center justify-center mx-auto">
                <Bot className="w-6 h-6" />
              </div>
              <h4 className="text-3xl font-extrabold text-white">25+</h4>
              <p className="text-xs font-semibold text-slate-400">{t('about.stat_bots')}</p>
            </div>

            <div className="glass-card p-6 rounded-2xl border border-white/10 hover:border-brand-purple/40 transition-all text-center space-y-3">
              <div className="w-12 h-12 rounded-xl bg-brand-purple/10 text-brand-purple flex items-center justify-center mx-auto">
                <Globe className="w-6 h-6" />
              </div>
              <h4 className="text-3xl font-extrabold text-white">15+</h4>
              <p className="text-xs font-semibold text-slate-400">{t('about.stat_sites')}</p>
            </div>

            <div className="glass-card p-6 rounded-2xl border border-white/10 hover:border-cyan-400/40 transition-all text-center space-y-3">
              <div className="w-12 h-12 rounded-xl bg-cyan-400/10 text-cyan-400 flex items-center justify-center mx-auto">
                <Sparkles className="w-6 h-6" />
              </div>
              <h4 className="text-3xl font-extrabold text-white">10+</h4>
              <p className="text-xs font-semibold text-slate-400">{t('about.stat_ai')}</p>
            </div>

            <div className="glass-card p-6 rounded-2xl border border-white/10 hover:border-amber-400/40 transition-all text-center space-y-3">
              <div className="w-12 h-12 rounded-xl bg-amber-400/10 text-amber-400 flex items-center justify-center mx-auto">
                <Terminal className="w-6 h-6" />
              </div>
              <h4 className="text-3xl font-extrabold text-white">100%</h4>
              <p className="text-xs font-semibold text-slate-400">Clean Code & Docs</p>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};

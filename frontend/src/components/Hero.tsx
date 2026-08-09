import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

export const Hero: React.FC = () => {
  const { t } = useTranslation();

  return (
    <section id="home" className="relative pt-16 pb-24 lg:pt-24 lg:pb-32 overflow-hidden">
      
      {/* Background Glowing Gradients */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-brand-blue/15 rounded-full blur-[140px] pointer-events-none -z-10" />
      <div className="absolute top-1/3 right-10 w-[400px] h-[400px] bg-brand-purple/15 rounded-full blur-[120px] pointer-events-none -z-10" />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-8 flex flex-col items-center"
        >
          {/* Status Pill */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card border border-brand-blue/30 text-xs font-semibold text-brand-blue">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Available for New Orders & Projects 2026</span>
          </div>

          {/* Main Title */}
          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
            {t('hero.title').split(',')[0]}, <br />
            <span className="text-gradient">
              {t('hero.title').split(',').slice(1).join(',') || 'Web & AI Developer'}
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl text-slate-300 max-w-2xl font-normal leading-relaxed">
            {t('hero.subtitle')}
          </p>

          {/* Call to Actions */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <a 
              href="#order"
              className="px-8 py-4 rounded-xl font-bold text-white bg-gradient-to-r from-brand-blue via-brand-accent to-brand-purple shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-105 transition-all flex items-center gap-3 group"
            >
              <span>{t('hero.cta_start')}</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>

            <a 
              href="#portfolio"
              className="px-8 py-4 rounded-xl font-bold text-slate-200 glass-card border border-white/10 hover:border-brand-blue/50 hover:bg-white/5 transition-all flex items-center gap-3"
            >
              <span>{t('hero.cta_portfolio')}</span>
            </a>
          </div>

          {/* Live Stats */}
          <div className="pt-8 border-t border-white/10 grid grid-cols-3 gap-8 w-full max-w-lg">
            <div>
              <h4 className="text-3xl font-extrabold text-white">50+</h4>
              <p className="text-xs text-slate-400 font-medium mt-1">{t('hero.completed_projects')}</p>
            </div>
            <div>
              <h4 className="text-3xl font-extrabold text-brand-blue">4+</h4>
              <p className="text-xs text-slate-400 font-medium mt-1">{t('hero.years')} {t('hero.experience')}</p>
            </div>
            <div>
              <h4 className="text-3xl font-extrabold text-brand-purple">99%</h4>
              <p className="text-xs text-slate-400 font-medium mt-1">Client Satisfaction</p>
            </div>
          </div>

        </motion.div>
      </div>
    </section>
  );
};

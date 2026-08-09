import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Bot, Smartphone, Globe, Server, Sparkles, Zap, ArrowRight, CheckCircle } from 'lucide-react';
import { ServiceItem } from '../types';

interface ServicesProps {
  services: ServiceItem[];
  onSelectService: (serviceSlug: string, serviceTitle: string) => void;
}

const iconMap: { [key: string]: React.ReactNode } = {
  Bot: <Bot className="w-8 h-8 text-brand-blue" />,
  Smartphone: <Smartphone className="w-8 h-8 text-brand-purple" />,
  Globe: <Globe className="w-8 h-8 text-cyan-400" />,
  Server: <Server className="w-8 h-8 text-emerald-400" />,
  Sparkles: <Sparkles className="w-8 h-8 text-amber-400" />,
  Zap: <Zap className="w-8 h-8 text-rose-400" />,
};

export const Services: React.FC<ServicesProps> = ({ services, onSelectService }) => {
  const { t, i18n } = useTranslation();
  const currentLang = i18n.language.slice(0, 2);

  const getTitle = (item: ServiceItem) => {
    if (currentLang === 'ru') return item.title_ru;
    if (currentLang === 'en') return item.title_en;
    return item.title_uz;
  };

  const getDesc = (item: ServiceItem) => {
    if (currentLang === 'ru') return item.desc_ru;
    if (currentLang === 'en') return item.desc_en;
    return item.desc_uz;
  };

  const getFeatures = (item: ServiceItem) => {
    if (currentLang === 'ru') return item.features_ru || [];
    if (currentLang === 'en') return item.features_en || [];
    return item.features_uz || [];
  };

  return (
    <section id="services" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-purple bg-brand-purple/10 px-3 py-1 rounded-full">
            {t('services.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('services.subtitle')}
          </h2>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, idx) => (
            <motion.div
              key={service.id || idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="glass-card rounded-2xl p-8 flex flex-col justify-between hover:border-brand-blue/50 transition-all group"
            >
              <div className="space-y-6">
                
                {/* Icon & Title */}
                <div className="flex items-center justify-between">
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10 group-hover:scale-110 transition-transform">
                    {iconMap[service.icon] || <Bot className="w-8 h-8 text-brand-blue" />}
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-white/5 text-slate-400">
                    0{idx + 1}
                  </span>
                </div>

                <div>
                  <h3 className="text-xl font-bold text-white group-hover:text-brand-blue transition-colors">
                    {getTitle(service)}
                  </h3>
                  <p className="text-sm text-slate-300 mt-2 leading-relaxed">
                    {getDesc(service)}
                  </p>
                </div>

                {/* Feature bullets */}
                <div className="space-y-2 pt-2 border-t border-white/10">
                  {getFeatures(service).map((feat, fIdx) => (
                    <div key={fIdx} className="flex items-center gap-2 text-xs text-slate-300">
                      <CheckCircle className="w-3.5 h-3.5 text-brand-blue shrink-0" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>

              </div>

              {/* Order Button */}
              <div className="pt-8">
                <button
                  onClick={() => onSelectService(service.slug, getTitle(service))}
                  className="w-full py-3 rounded-xl font-bold text-sm text-white bg-white/5 hover:bg-gradient-to-r hover:from-brand-blue hover:to-brand-purple border border-white/10 hover:border-transparent transition-all flex items-center justify-center gap-2 group/btn"
                >
                  <span>{t('services.btn_order')}</span>
                  <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
                </button>
              </div>

            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
};

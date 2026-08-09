import React from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Cpu, Server, Database, Wrench, Sparkles } from 'lucide-react';

export const TechStack: React.FC = () => {
  const { t } = useTranslation();

  const categories = [
    {
      title: "Frontend",
      icon: <Cpu className="w-5 h-5 text-brand-blue" />,
      items: ["React", "TypeScript", "Tailwind CSS", "Vite", "Framer Motion", "HTML5/CSS3"]
    },
    {
      title: "Backend",
      icon: <Server className="w-5 h-5 text-brand-purple" />,
      items: ["Python", "FastAPI", "Aiogram 3.x", "Django", "SQLAlchemy", "Asyncio"]
    },
    {
      title: "Database & Storage",
      icon: <Database className="w-5 h-5 text-emerald-400" />,
      items: ["PostgreSQL", "SQLite", "Redis", "Alembic Migrations"]
    },
    {
      title: "Tools & Infra",
      icon: <Wrench className="w-5 h-5 text-cyan-400" />,
      items: ["Docker", "Git / GitHub", "Linux CLI", "Nginx", "RESTful APIs", "JWT Auth"]
    },
    {
      title: "AI Ecosystem",
      icon: <Sparkles className="w-5 h-5 text-amber-400" />,
      items: ["Google Gemini API", "OpenAI GPT-4", "Midjourney v6", "Runway Gen-2", "ElevenLabs"]
    }
  ];

  return (
    <section id="tech" className="py-20 relative bg-slate-900/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-blue bg-brand-blue/10 px-3 py-1 rounded-full">
            {t('tech.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('tech.subtitle')}
          </h2>
        </div>

        {/* Tech Stack Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {categories.map((cat, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="glass-card rounded-2xl p-6 space-y-4 hover:border-brand-blue/40 transition-all"
            >
              <div className="flex items-center gap-3 border-b border-white/10 pb-4">
                <div className="p-2.5 rounded-xl bg-white/5 border border-white/10">
                  {cat.icon}
                </div>
                <h3 className="text-lg font-bold text-white">{cat.title}</h3>
              </div>

              <div className="flex flex-wrap gap-2 pt-2">
                {cat.items.map((item, iIdx) => (
                  <span
                    key={iIdx}
                    className="px-3 py-1.5 rounded-xl text-xs font-mono font-medium bg-white/5 border border-white/10 text-slate-200 hover:bg-brand-blue/20 hover:border-brand-blue/40 transition-colors"
                  >
                    {item}
                  </span>
                ))}
              </div>

            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
};

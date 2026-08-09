import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import { ExternalLink, Bot, Github, Play, X, Eye } from 'lucide-react';
import { ProjectItem } from '../types';

interface PortfolioProps {
  projects: ProjectItem[];
}

export const Portfolio: React.FC<PortfolioProps> = ({ projects }) => {
  const { t, i18n } = useTranslation();
  const currentLang = i18n.language.slice(0, 2);
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [selectedProject, setSelectedProject] = useState<ProjectItem | null>(null);

  const categories = [
    { id: 'all', label: t('portfolio.all') },
    { id: 'bot', label: t('portfolio.bots') },
    { id: 'web', label: t('portfolio.web') },
    { id: 'miniapp', label: t('portfolio.miniapps') },
    { id: 'ai_video', label: t('portfolio.ai_video') },
    { id: 'ai_image', label: t('portfolio.ai_image') },
    { id: 'automation', label: t('portfolio.automation') },
  ];

  const filteredProjects = activeCategory === 'all'
    ? projects
    : projects.filter(p => p.category === activeCategory);

  const getTitle = (p: ProjectItem) => {
    if (currentLang === 'ru') return p.title_ru;
    if (currentLang === 'en') return p.title_en;
    return p.title_uz;
  };

  const getDesc = (p: ProjectItem) => {
    if (currentLang === 'ru') return p.desc_ru;
    if (currentLang === 'en') return p.desc_en;
    return p.desc_uz;
  };

  const getImageUrl = (url?: string) => {
    if (!url) return 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&q=80';
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    return url.startsWith('/') ? url : `/${url}`;
  };

  return (
    <section id="portfolio" className="py-20 relative bg-slate-900/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-blue bg-brand-blue/10 px-3 py-1 rounded-full">
            {t('portfolio.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('portfolio.subtitle')}
          </h2>
        </div>

        {/* Category Filter Tabs */}
        <div className="flex items-center justify-start sm:justify-center gap-2 overflow-x-auto pb-4 mb-12 no-scrollbar">
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-5 py-2.5 rounded-xl font-medium text-xs sm:text-sm whitespace-nowrap transition-all ${
                activeCategory === cat.id
                  ? 'bg-brand-blue text-white shadow-lg shadow-blue-500/25 font-bold'
                  : 'glass-card text-slate-300 hover:bg-white/10 hover:text-white'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Projects Grid */}
        <motion.div layout className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <AnimatePresence>
            {filteredProjects.map(project => (
              <motion.div
                key={project.id}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3 }}
                className="glass-card rounded-2xl overflow-hidden border border-white/10 hover:border-brand-blue/40 transition-all flex flex-col group"
              >
                
                {/* Media Cover Container */}
                <div className="relative aspect-video overflow-hidden bg-slate-800">
                  <img
                    src={getImageUrl(project.cover_image)}
                    alt={getTitle(project)}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-dark-bg via-dark-bg/40 to-transparent opacity-80" />

                  {/* Category Pill */}
                  <span className="absolute top-3 left-3 px-3 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider bg-dark-bg/80 text-brand-blue border border-brand-blue/30 backdrop-blur-md">
                    {project.category}
                  </span>

                  {/* Eye quick view trigger */}
                  <button
                    onClick={() => setSelectedProject(project)}
                    className="absolute inset-0 m-auto w-12 h-12 rounded-full bg-brand-blue/90 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 scale-75 group-hover:scale-100 transition-all shadow-xl"
                  >
                    <Eye className="w-6 h-6" />
                  </button>
                </div>

                {/* Project Details */}
                <div className="p-6 flex-1 flex flex-col justify-between space-y-4">
                  <div className="space-y-2">
                    <h3 
                      onClick={() => setSelectedProject(project)}
                      className="text-lg font-bold text-white group-hover:text-brand-blue transition-colors cursor-pointer"
                    >
                      {getTitle(project)}
                    </h3>
                    <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">
                      {getDesc(project)}
                    </p>
                  </div>

                  {/* Tech stack tags */}
                  <div className="flex flex-wrap gap-1.5 pt-2">
                    {project.tech_stack?.map((tech, tIdx) => (
                      <span key={tIdx} className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-white/5 border border-white/10 text-slate-300">
                        {tech}
                      </span>
                    ))}
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center gap-3 pt-3 border-t border-white/10">
                    {project.demo_url && (
                      <a
                        href={project.demo_url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 py-2 rounded-lg bg-brand-blue/10 hover:bg-brand-blue text-brand-blue hover:text-white text-xs font-semibold text-center transition-colors flex items-center justify-center gap-1.5"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>{t('portfolio.btn_demo')}</span>
                      </a>
                    )}

                    {project.bot_url && (
                      <a
                        href={project.bot_url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 py-2 rounded-lg bg-emerald-500/10 hover:bg-emerald-500 text-emerald-400 hover:text-white text-xs font-semibold text-center transition-colors flex items-center justify-center gap-1.5"
                      >
                        <Bot className="w-3.5 h-3.5" />
                        <span>{t('portfolio.btn_bot')}</span>
                      </a>
                    )}

                    {project.github_url && (
                      <a
                        href={project.github_url}
                        target="_blank"
                        rel="noreferrer"
                        className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white transition-colors"
                        title="GitHub"
                      >
                        <Github className="w-4 h-4" />
                      </a>
                    )}
                  </div>

                </div>

              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>

        {/* Detailed Modal View */}
        {selectedProject && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
            <div className="relative w-full max-w-3xl max-h-[90vh] overflow-y-auto glass-panel rounded-3xl p-6 sm:p-8 space-y-6 border border-white/20">
              
              <button
                onClick={() => setSelectedProject(null)}
                className="absolute top-6 right-6 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="relative aspect-video rounded-2xl overflow-hidden">
                <img
                  src={getImageUrl(selectedProject.cover_image)}
                  alt={getTitle(selectedProject)}
                  className="w-full h-full object-cover"
                />
              </div>

              <div>
                <span className="text-xs font-bold uppercase text-brand-blue bg-brand-blue/10 px-3 py-1 rounded-full">
                  {selectedProject.category}
                </span>
                <h3 className="text-2xl font-bold text-white mt-3">{getTitle(selectedProject)}</h3>
                <p className="text-slate-300 text-sm mt-3 leading-relaxed">{getDesc(selectedProject)}</p>
              </div>

              {/* Tech Stack */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Technologies Used:</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedProject.tech_stack?.map((t, idx) => (
                    <span key={idx} className="px-3 py-1 rounded-lg bg-white/10 text-xs font-mono text-white">
                      {t}
                    </span>
                  ))}
                </div>
              </div>

              {/* Links */}
              <div className="flex items-center gap-4 pt-4 border-t border-white/10">
                {selectedProject.demo_url && (
                  <a
                    href={selectedProject.demo_url}
                    target="_blank"
                    rel="noreferrer"
                    className="px-6 py-3 rounded-xl bg-brand-blue text-white font-bold text-sm flex items-center gap-2"
                  >
                    <ExternalLink className="w-4 h-4" /> Live Demo
                  </a>
                )}
                {selectedProject.bot_url && (
                  <a
                    href={selectedProject.bot_url}
                    target="_blank"
                    rel="noreferrer"
                    className="px-6 py-3 rounded-xl bg-emerald-500 text-white font-bold text-sm flex items-center gap-2"
                  >
                    <Bot className="w-4 h-4" /> Open Telegram Bot
                  </a>
                )}
              </div>

            </div>
          </div>
        )}

      </div>
    </section>
  );
};

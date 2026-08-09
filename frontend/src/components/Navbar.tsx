import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Menu, X, Sun, Moon, Globe, Terminal } from 'lucide-react';

interface NavbarProps {
  darkMode: boolean;
  setDarkMode: (val: boolean) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ darkMode, setDarkMode }) => {
  const { t, i18n } = useTranslation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [langDropdown, setLangDropdown] = useState(false);

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('i18nextLng', lang);
    setLangDropdown(false);
  };

  const currentLangLabel = {
    uz: '🇺🇿 UZ',
    ru: '🇷🇺 RU',
    en: '🇬🇧 EN'
  }[i18n.language.slice(0, 2)] || '🇺🇿 UZ';

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-white/10 backdrop-blur-md transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo / Developer Name */}
          <a href="#" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-blue to-brand-purple flex items-center justify-center text-white shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <Terminal className="w-6 h-6" />
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold text-xl tracking-tight text-white group-hover:text-brand-blue transition-colors">
                Dev<span className="text-brand-blue">Portfolio</span>
              </span>
              <span className="text-xs text-slate-400 font-medium">Telegram & Web AI Solutions</span>
            </div>
          </a>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-8 font-medium text-sm text-slate-300">
            <a href="#home" className="hover:text-brand-blue transition-colors">{t('nav.home')}</a>
            <a href="#about" className="hover:text-brand-blue transition-colors">{t('nav.about')}</a>
            <a href="#services" className="hover:text-brand-blue transition-colors">{t('nav.services')}</a>
            <a href="#portfolio" className="hover:text-brand-blue transition-colors">{t('nav.portfolio')}</a>
            <a href="#videos" className="hover:text-brand-blue transition-colors">{t('nav.videos')}</a>
            <a href="#tech" className="hover:text-brand-blue transition-colors">{t('nav.tech')}</a>
            <a href="#contact" className="hover:text-brand-blue transition-colors">{t('nav.contact')}</a>
          </nav>

          {/* Right Action Controls */}
          <div className="hidden sm:flex items-center gap-4">
            
            {/* Language Switcher Dropdown */}
            <div className="relative">
              <button 
                onClick={() => setLangDropdown(!langDropdown)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm font-semibold hover:bg-white/10 transition-colors"
              >
                <Globe className="w-4 h-4 text-brand-blue" />
                <span>{currentLangLabel}</span>
              </button>

              {langDropdown && (
                <div className="absolute right-0 mt-2 w-32 glass-panel rounded-xl py-2 shadow-xl border border-white/10 z-50 animate-fadeIn">
                  <button 
                    onClick={() => changeLanguage('uz')} 
                    className="w-full text-left px-4 py-2 text-sm hover:bg-brand-blue/20 transition-colors flex items-center gap-2"
                  >
                    🇺🇿 O'zbek
                  </button>
                  <button 
                    onClick={() => changeLanguage('ru')} 
                    className="w-full text-left px-4 py-2 text-sm hover:bg-brand-blue/20 transition-colors flex items-center gap-2"
                  >
                    🇷🇺 Русский
                  </button>
                  <button 
                    onClick={() => changeLanguage('en')} 
                    className="w-full text-left px-4 py-2 text-sm hover:bg-brand-blue/20 transition-colors flex items-center gap-2"
                  >
                    🇬🇧 English
                  </button>
                </div>
              )}
            </div>

            {/* Dark / Light Toggle */}
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 text-slate-300 hover:text-white transition-colors"
              title="Toggle Theme"
            >
              {darkMode ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-indigo-400" />}
            </button>

            {/* Order Now CTA */}
            <a 
              href="#order" 
              className="px-5 py-2.5 rounded-xl font-semibold text-sm text-white bg-gradient-to-r from-brand-blue via-brand-accent to-brand-purple shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-105 transition-all"
            >
              {t('nav.order')}
            </a>
          </div>

          {/* Mobile Hamburger Toggle */}
          <div className="flex sm:hidden items-center gap-3">
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg bg-white/5 border border-white/10"
            >
              {darkMode ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-indigo-400" />}
            </button>

            <button 
              onClick={() => setMobileOpen(!mobileOpen)}
              className="p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            >
              {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileOpen && (
        <div className="sm:hidden glass-panel border-t border-white/10 px-4 py-6 space-y-4 animate-slideDown">
          <nav className="flex flex-col gap-4 font-medium text-base">
            <a href="#home" onClick={() => setMobileOpen(false)}>{t('nav.home')}</a>
            <a href="#about" onClick={() => setMobileOpen(false)}>{t('nav.about')}</a>
            <a href="#services" onClick={() => setMobileOpen(false)}>{t('nav.services')}</a>
            <a href="#portfolio" onClick={() => setMobileOpen(false)}>{t('nav.portfolio')}</a>
            <a href="#videos" onClick={() => setMobileOpen(false)}>{t('nav.videos')}</a>
            <a href="#tech" onClick={() => setMobileOpen(false)}>{t('nav.tech')}</a>
            <a href="#contact" onClick={() => setMobileOpen(false)}>{t('nav.contact')}</a>
          </nav>

          <div className="pt-4 border-t border-white/10 flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-400">Language:</span>
              <button onClick={() => changeLanguage('uz')} className={`px-2 py-1 text-xs rounded ${i18n.language.startsWith('uz') ? 'bg-brand-blue text-white' : 'bg-white/5'}`}>UZ</button>
              <button onClick={() => changeLanguage('ru')} className={`px-2 py-1 text-xs rounded ${i18n.language.startsWith('ru') ? 'bg-brand-blue text-white' : 'bg-white/5'}`}>RU</button>
              <button onClick={() => changeLanguage('en')} className={`px-2 py-1 text-xs rounded ${i18n.language.startsWith('en') ? 'bg-brand-blue text-white' : 'bg-white/5'}`}>EN</button>
            </div>

            <a 
              href="#order" 
              onClick={() => setMobileOpen(false)}
              className="w-full text-center py-3 rounded-xl font-bold text-white bg-gradient-to-r from-brand-blue to-brand-purple shadow-lg"
            >
              {t('nav.order')}
            </a>
          </div>
        </div>
      )}
    </header>
  );
};

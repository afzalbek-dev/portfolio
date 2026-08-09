import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Send, Phone, MessageSquare, Mail, ShieldAlert, ExternalLink } from 'lucide-react';
import { submitContactRequest } from '../services/api';
import { ServiceItem } from '../types';

interface OrderFormProps {
  services: ServiceItem[];
  selectedServiceSlug?: string;
  selectedServiceTitle?: string;
  adminTelegramLink?: string;
  onOrderSubmitted: () => void;
}

export const OrderForm: React.FC<OrderFormProps> = ({
  services,
  selectedServiceSlug,
  selectedServiceTitle,
  adminTelegramLink = "https://t.me/developer_username",
  onOrderSubmitted,
}) => {
  const { t, i18n } = useTranslation();
  
  const [name, setName] = useState('');
  const [serviceId, setServiceId] = useState('');
  const [serviceName, setServiceName] = useState('');
  const [description, setDescription] = useState('');
  
  // Option A Contact Method selector (Default 'telegram')
  const [contactMethod, setContactMethod] = useState<'telegram' | 'whatsapp' | 'email'>('telegram');
  const [contactValue, setContactValue] = useState('');
  const [honeypot, setHoneypot] = useState('');

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (selectedServiceSlug || selectedServiceTitle) {
      setServiceId(selectedServiceSlug || '');
      setServiceName(selectedServiceTitle || '');
    }
  }, [selectedServiceSlug, selectedServiceTitle]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    if (!contactValue || contactValue.trim().length === 0) {
      setErrorMsg(t('order.error_contact'));
      return;
    }

    setLoading(true);

    try {
      await submitContactRequest({
        name,
        service_id: serviceId,
        service_name: serviceName,
        description,
        contact_method: contactMethod,
        contact_value: contactValue,
        language: i18n.language.slice(0, 2),
        honeypot,
      });

      // Reset form
      setName('');
      setDescription('');
      setContactValue('');
      onOrderSubmitted();
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.response?.data?.detail || t('order.error_general'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="order" className="py-20 relative">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center space-y-3 mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-blue bg-brand-blue/10 px-3 py-1 rounded-full">
            {t('order.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('order.subtitle')}
          </h2>
        </div>

        {/* Outer Form Card */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="glass-panel rounded-3xl p-6 sm:p-10 border border-white/10 shadow-2xl space-y-8"
        >
          {/* OPTION A: FORM SUBMISSION */}
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Anti-spam honeypot hidden field */}
            <input
              type="text"
              name="honeypot"
              value={honeypot}
              onChange={(e) => setHoneypot(e.target.value)}
              className="hidden"
              tabIndex={-1}
              autoComplete="off"
            />

            {/* Error banner if any */}
            {errorMsg && (
              <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm flex items-center gap-3">
                <ShieldAlert className="w-5 h-5 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              
              {/* Name Field */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  {t('order.name_label')}
                </label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder={t('order.name_placeholder')}
                  className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-brand-blue transition-colors text-sm"
                />
              </div>

              {/* Service Dropdown */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  {t('order.service_label')}
                </label>
                <select
                  value={serviceId}
                  onChange={(e) => {
                    setServiceId(e.target.value);
                    const sel = services.find(s => s.slug === e.target.value);
                    setServiceName(sel ? sel.title_uz : e.target.value);
                  }}
                  className="w-full px-4 py-3 rounded-xl bg-dark-bg border border-white/10 text-white focus:outline-none focus:border-brand-blue transition-colors text-sm"
                >
                  <option value="">{t('order.service_select')}</option>
                  <option value="telegram_bot">Telegram Bot Development</option>
                  <option value="website">Website Development</option>
                  <option value="mini_app">Telegram Mini App</option>
                  <option value="backend_api">Backend & REST API</option>
                  <option value="ai_solutions">AI Solutions</option>
                  <option value="automation">Automation System</option>
                </select>
              </div>

            </div>

            {/* Project Description Textarea */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                {t('order.desc_label')}
              </label>
              <textarea
                required
                rows={3}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder={t('order.desc_placeholder')}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-brand-blue transition-colors text-sm resize-none"
              />
            </div>

            {/* SINGLE CONTACT METHOD SELECTOR */}
            <div className="pt-4 border-t border-white/10 space-y-4">
              <p className="text-xs font-bold text-brand-blue uppercase tracking-wider">
                {t('order.contact_method_title')}
              </p>

              {/* Method Selector Buttons */}
              <div className="grid grid-cols-3 gap-3">
                <button
                  type="button"
                  onClick={() => { setContactMethod('telegram'); setContactValue(''); }}
                  className={`py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 border transition-all ${
                    contactMethod === 'telegram'
                      ? 'bg-brand-blue text-white border-brand-blue shadow-lg shadow-blue-500/20'
                      : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10'
                  }`}
                >
                  <Send className="w-4 h-4" /> Telegram
                </button>

                <button
                  type="button"
                  onClick={() => { setContactMethod('whatsapp'); setContactValue(''); }}
                  className={`py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 border transition-all ${
                    contactMethod === 'whatsapp'
                      ? 'bg-emerald-500 text-white border-emerald-500 shadow-lg shadow-emerald-500/20'
                      : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10'
                  }`}
                >
                  <MessageSquare className="w-4 h-4" /> WhatsApp
                </button>

                <button
                  type="button"
                  onClick={() => { setContactMethod('email'); setContactValue(''); }}
                  className={`py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 border transition-all ${
                    contactMethod === 'email'
                      ? 'bg-purple-500 text-white border-purple-500 shadow-lg shadow-purple-500/20'
                      : 'bg-white/5 text-slate-300 border-white/10 hover:bg-white/10'
                  }`}
                >
                  <Mail className="w-4 h-4" /> Email
                </button>
              </div>

              {/* SHOW ONLY ONE INPUT FIELD BASED ON SELECTED METHOD */}
              <div className="pt-2">
                {contactMethod === 'telegram' && (
                  <div className="relative">
                    <Send className="w-4 h-4 text-brand-blue absolute left-4 top-3.5" />
                    <input
                      type="text"
                      required
                      value={contactValue}
                      onChange={(e) => setContactValue(e.target.value)}
                      placeholder={t('order.contact_val_tg') + " (@username)"}
                      className="w-full pl-11 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-brand-blue text-sm"
                    />
                  </div>
                )}

                {contactMethod === 'whatsapp' && (
                  <div className="relative">
                    <Phone className="w-4 h-4 text-emerald-400 absolute left-4 top-3.5" />
                    <input
                      type="tel"
                      required
                      value={contactValue}
                      onChange={(e) => setContactValue(e.target.value)}
                      placeholder={t('order.contact_val_wa') + " (+998...)"}
                      className="w-full pl-11 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 text-sm"
                    />
                  </div>
                )}

                {contactMethod === 'email' && (
                  <div className="relative">
                    <Mail className="w-4 h-4 text-purple-400 absolute left-4 top-3.5" />
                    <input
                      type="email"
                      required
                      value={contactValue}
                      onChange={(e) => setContactValue(e.target.value)}
                      placeholder={t('order.contact_val_email') + " (example@gmail.com)"}
                      className="w-full pl-11 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 text-sm"
                    />
                  </div>
                )}
              </div>

            </div>

            {/* Submit Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 rounded-xl font-extrabold text-white bg-gradient-to-r from-brand-blue via-brand-accent to-brand-purple shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-[1.01] transition-all flex items-center justify-center gap-3 disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
                <span>{loading ? t('order.submitting') : t('order.submit_btn')}</span>
              </button>
            </div>

          </form>

          {/* OPTION B: DIRECT CONTACT LINK TO PERSONAL TELEGRAM ACCOUNT */}
          <div className="pt-6 border-t border-white/10 text-center space-y-3">
            <p className="text-xs font-semibold text-slate-400">
              {t('order.direct_title')}
            </p>

            <a
              href={adminTelegramLink}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-white/5 hover:bg-brand-blue text-slate-200 hover:text-white border border-white/10 hover:border-transparent font-bold text-sm transition-all shadow-lg group"
            >
              <Send className="w-4 h-4 text-brand-blue group-hover:text-white transition-colors" />
              <span>{t('order.direct_btn')}</span>
              <ExternalLink className="w-3.5 h-3.5 ml-1" />
            </a>
          </div>

        </motion.div>

      </div>
    </section>
  );
};

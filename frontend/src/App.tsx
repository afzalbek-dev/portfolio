import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { About } from './components/About';
import { Services } from './components/Services';
import { Portfolio } from './components/Portfolio';
import { VideoShowcase } from './components/VideoShowcase';
import { TechStack } from './components/TechStack';
import { OrderForm } from './components/OrderForm';
import { SuccessModal } from './components/SuccessModal';
import { ContactSection } from './components/ContactSection';
import { FloatingCTA } from './components/FloatingCTA';
import { Footer } from './components/Footer';
import { fetchServices, fetchProjects, fetchSettings } from './services/api';
import { ServiceItem, ProjectItem } from './types';
import './i18n';

export const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [aboutText, setAboutText] = useState<string>('');

  const [adminTelegramLink, setAdminTelegramLink] = useState<string>('https://t.me/Obunachi786');
  const [whatsappNumber, setWhatsappNumber] = useState<string>('+998908734005');
  const [instagramUser, setInstagramUser] = useState<string>('@developer_username');
  const [emailAddr, setEmailAddr] = useState<string>('dev@example.com');

  const [selectedServiceSlug, setSelectedServiceSlug] = useState<string>('');
  const [selectedServiceTitle, setSelectedServiceTitle] = useState<string>('');

  const [successModalOpen, setSuccessModalOpen] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    }
  }, [darkMode]);

  const loadData = async () => {
    try {
      const [sData, pData, setRes] = await Promise.all([
        fetchServices(),
        fetchProjects(),
        fetchSettings(),
      ]);
      setServices(sData);
      setProjects(pData);

      if (setRes) {
        if (setRes.admin_telegram_link) {
          setAdminTelegramLink(setRes.admin_telegram_link);
        }
        if (setRes.contacts) {
          if (setRes.contacts.whatsapp_number) setWhatsappNumber(setRes.contacts.whatsapp_number);
          if (setRes.contacts.instagram) setInstagramUser(setRes.contacts.instagram);
          if (setRes.contacts.email) setEmailAddr(setRes.contacts.email);
        }
        if (setRes.site_settings && setRes.site_settings.about_text) {
          setAboutText(setRes.site_settings.about_text.uz);
        }
      }
    } catch (err) {
      console.warn("API loading initial data:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSelectService = (slug: string, title: string) => {
    setSelectedServiceSlug(slug);
    setSelectedServiceTitle(title);
    const orderSection = document.getElementById('order');
    if (orderSection) {
      orderSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-dark-bg text-slate-100 selection:bg-brand-blue selection:text-white">
      
      {/* Navigation Header */}
      <Navbar 
        darkMode={darkMode} 
        setDarkMode={setDarkMode}
      />

      {/* Main Content Sections */}
      <main className="flex-1">
        <Hero />
        <About aboutText={aboutText} />
        <Services services={services} onSelectService={handleSelectService} />
        <Portfolio projects={projects} />
        <VideoShowcase />
        <TechStack />
        <OrderForm 
          services={services}
          selectedServiceSlug={selectedServiceSlug}
          selectedServiceTitle={selectedServiceTitle}
          adminTelegramLink={adminTelegramLink}
          onOrderSubmitted={() => setSuccessModalOpen(true)}
        />
        <ContactSection 
          adminTelegramLink={adminTelegramLink}
          whatsappNumber={whatsappNumber}
          instagramUser={instagramUser}
          emailAddr={emailAddr}
        />
      </main>

      {/* Floating CTA Quick Buttons */}
      <FloatingCTA 
        adminTelegramLink={adminTelegramLink}
        whatsappNumber={whatsappNumber}
      />

      {/* Footer */}
      <Footer />

      {/* Order Success Modal */}
      {successModalOpen && (
        <SuccessModal onClose={() => setSuccessModalOpen(false)} />
      )}

    </div>
  );
};

export default App;

/**
 * Main Application Component for Krishi Mitra Agricultural Advisory System.
 * Theme: White, Dark Blue, and Royal Gold.
 * Compliance: Arm Bharat AI-SoC Challenge & Multilingual Offline Accessibility.
 * Zero Unicode emojis, strictly uses react-icons. Zero technical jargon.
 */
import { useState, useEffect } from 'react';
import { FiWifiOff, FiPhoneCall } from 'react-icons/fi';
import { Navigation } from './components/Navigation.tsx';
import type { TabId } from './components/Navigation.tsx';
import { CropDoctor } from './components/CropDoctor.tsx';
import { Chat } from './components/Chat.tsx';
import { SoilCard } from './components/SoilCard.tsx';
import { Schemes } from './components/Schemes.tsx';
import { Status } from './components/Status.tsx';
import { checkHealth } from './services/api.ts';
import type { LanguageCode } from './i18n/translations.ts';
import { getTranslation } from './i18n/translations.ts';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabId>('crop_doctor');
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [language, setLanguage] = useState<LanguageCode>('en');
  const [consultCrop, setConsultCrop] = useState<string | undefined>(undefined);
  const [consultCondition, setConsultCondition] = useState<string | undefined>(undefined);

  const t = (key: string) => getTranslation(language, key);

  // Periodic heartbeat verifying station connectivity
  useEffect(() => {
    let isMounted = true;

    const verifyStation = async () => {
      try {
        const health = await checkHealth();
        if (isMounted) {
          setIsOnline(health?.status === 'ready');
        }
      } catch {
        if (isMounted) {
          setIsOnline(false);
        }
      }
    };

    verifyStation();
    const interval = setInterval(verifyStation, 15000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  // Handler for cascading diagnosis directly to advisory chat
  const handleConsultAdvisor = (cropName: string, condition: string) => {
    setConsultCrop(cropName);
    setConsultCondition(condition);
    setActiveTab('chat');
  };

  return (
    <div className="app-layout">
      {/* Network Reconnect Alert Banner if station drops */}
      {!isOnline && (
        <div className="reconnect-banner" role="alert">
          <div className="container reconnect-container">
            <FiWifiOff className="reconnect-icon" aria-hidden="true" />
            <span className="reconnect-message">
              {t('reconnectNotice')}
            </span>
            <a href="tel:18001801551" className="reconnect-helpline">
              <FiPhoneCall aria-hidden="true" />
              <span>{t('callHelpline')}</span>
            </a>
          </div>
        </div>
      )}

      {/* Top Header & Navigation Bar in Dark Blue & Gold */}
      <Navigation
        activeTab={activeTab}
        onTabChange={setActiveTab}
        isOnline={isOnline}
        language={language}
        onLanguageChange={setLanguage}
      />

      {/* Main Content Area */}
      <main className="main-content container" id="main-content">
        {activeTab === 'crop_doctor' && (
          <CropDoctor onConsultAdvisor={handleConsultAdvisor} language={language} />
        )}

        {activeTab === 'chat' && (
          <Chat
            key={consultCrop ? `${consultCrop}-${consultCondition}` : 'chat-session'}
            initialCropContext={consultCrop}
            initialConditionContext={consultCondition}
            language={language}
          />
        )}

        {activeTab === 'soil_card' && <SoilCard language={language} />}

        {activeTab === 'schemes' && <Schemes language={language} />}

        {activeTab === 'status' && <Status language={language} />}
      </main>

      {/* Footer in Deep Dark Blue with Royal Gold Accents */}
      <footer className="footer-bar" style={{ backgroundColor: '#06101E', borderTop: '2px solid #D4AF37', padding: '16px 0', marginTop: 'auto' }}>
        <div className="container footer-container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <p className="footer-text" style={{ fontSize: '13px', color: '#CBD5E1' }}>
            {t('footerNotice')}
          </p>
          <div className="footer-links">
            <a href="tel:18001801551" className="footer-helpline-link" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: '#FFD700', fontWeight: 600, fontSize: '13px' }}>
              <FiPhoneCall className="footer-icon" aria-hidden="true" />
              <span>{t('tollFreeKisan')}</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

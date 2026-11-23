/**
 * Navigation Header and Tab Bar for Krishi Mitra Agricultural Advisory System.
 * Theme: White, Dark Blue, and Royal Gold.
 * Compliance: Arm Bharat AI-SoC Challenge & Multilingual Offline Accessibility.
 * Zero emojis, uses react-icons exclusively.
 */
import type { ChangeEvent } from 'react';
import {
  FiPhoneCall,
  FiMessageSquare,
  FiActivity,
  FiGlobe,
} from 'react-icons/fi';
import {
  FaLeaf,
  FaFlask,
  FaLandmark,
} from 'react-icons/fa6';
import logoEmblem from '../assets/logo_emblem.jpg';
import type { LanguageCode } from '../i18n/translations.ts';
import { SUPPORTED_LANGUAGES, getTranslation } from '../i18n/translations.ts';

export type TabId = 'crop_doctor' | 'chat' | 'soil_card' | 'schemes' | 'status';

interface NavigationProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
  isOnline?: boolean;
  language: LanguageCode;
  onLanguageChange: (lang: LanguageCode) => void;
}

export function Navigation({
  activeTab,
  onTabChange,
  language,
  onLanguageChange,
}: NavigationProps) {
  const t = (key: string) => getTranslation(language, key);

  const navTabs: Array<{ id: TabId; label: string; icon: React.ReactElement }> = [
    { id: 'crop_doctor', label: t('tabCropScanner'), icon: <FaLeaf aria-hidden="true" /> },
    { id: 'chat', label: t('tabAdvisoryChat'), icon: <FiMessageSquare aria-hidden="true" /> },
    { id: 'soil_card', label: t('tabSoilHealth'), icon: <FaFlask aria-hidden="true" /> },
    { id: 'schemes', label: t('tabSchemes'), icon: <FaLandmark aria-hidden="true" /> },
    { id: 'status', label: t('tabStationStatus'), icon: <FiActivity aria-hidden="true" /> },
  ];

  const handleLangChange = (e: ChangeEvent<HTMLSelectElement>) => {
    onLanguageChange(e.target.value as LanguageCode);
  };

  return (
    <header className="header-nav" role="banner">
      <div className="container header-container">
        {/* Brand Crest with Generated Logo Emblem */}
        <div className="brand-group">
          <img
            src={logoEmblem}
            alt="Krishi Mitra Emblem"
            className="brand-logo-img"
          />
          <div>
            <h1 className="brand-title">
              Krishi <span className="brand-title-gold">Mitra</span>
            </h1>
            <p className="brand-subtitle">{t('appSubtitle')}</p>
          </div>
        </div>

        {/* Right Header Actions: Language Dropdown, Station Pill, Helpline */}
        <div className="header-actions">
          {/* Multilingual Selector */}
          <div className="lang-selector-wrapper" title="Select Advisory Language">
            <FiGlobe className="lang-icon" aria-hidden="true" />
            <select
              className="lang-select"
              value={language}
              onChange={handleLangChange}
              aria-label="Select Application Language"
            >
              {SUPPORTED_LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.nativeLabel} ({lang.label})
                </option>
              ))}
            </select>
          </div>

          {/* Kisan Call Centre Toll-Free Helpline in Royal Gold */}
          <a
            href="tel:18001801551"
            className="helpline-btn"
            title={t('kisanCallCentre')}
            aria-label="Call Kisan Call Centre Toll-Free Helpline"
          >
            <FiPhoneCall className="helpline-icon" aria-hidden="true" />
            <span className="helpline-text">{t('helplineText')}</span>
          </a>
        </div>
      </div>

      {/* Main Navigation Tabs */}
      <nav className="tab-navigation" aria-label="Main Navigation">
        <div className="container nav-tabs-container">
          {navTabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                className={`nav-tab ${isActive ? 'nav-tab--active' : ''}`}
                onClick={() => onTabChange(tab.id)}
                aria-selected={isActive}
                role="tab"
              >
                <span className="nav-tab-icon">{tab.icon}</span>
                <span className="nav-tab-label">{tab.label}</span>
              </button>
            );
          })}
        </div>
      </nav>
    </header>
  );
}

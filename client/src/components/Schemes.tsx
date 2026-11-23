/**
 * Schemes Component for Krishi Mitra Agricultural Advisory System.
 * Directory of key Government of India agricultural schemes and helplines.
 * Zero Unicode emojis, strictly uses react-icons. Zero technical jargon.
 * Full multilingual support for all 22 Scheduled Indian Languages + English.
 * Core Schemes: PM-KISAN, PMFBY (mandatory 72-hour calamity notice, helpline 14447), KCC, KCC helpline 1800-180-1551.
 */
import { useState } from 'react';
import {
  FiShield,
  FiPhoneCall,
  FiSearch,
  FiCheckCircle,
  FiClock,
  FiExternalLink,
} from 'react-icons/fi';
import {
  FaLandmark,
  FaCreditCard,
  FaFlask,
} from 'react-icons/fa6';
import type { LanguageCode } from '../i18n/translations.ts';
import { getTranslation } from '../i18n/translations.ts';
import { getLocalizedSchemes } from '../i18n/schemesData.ts';

export interface SchemesProps {
  language?: LanguageCode;
}

const CATEGORY_TABS = [
  { key: 'filterAll' },
  { key: 'filterFinancial' },
  { key: 'filterInsurance' },
  { key: 'filterCredit' },
  { key: 'filterSoil' },
];

const SCHEME_CATEGORY_MAP: Record<string, string> = {
  'pm-kisan': 'filterFinancial',
  'pmfby': 'filterInsurance',
  'kcc': 'filterCredit',
  'enam': 'filterCredit',
  'soil-health-card': 'filterSoil',
  'kisan-call-centre': 'filterSoil',
};

export function Schemes({ language = 'en' }: SchemesProps) {
  const [selectedCategoryKey, setSelectedCategoryKey] = useState<string>('filterAll');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const t = (key: string) => getTranslation(language, key);
  const schemesData = getLocalizedSchemes(language);

  const filteredSchemes = schemesData.filter((scheme) => {
    const schemeCatKey = SCHEME_CATEGORY_MAP[scheme.id] || 'filterAll';
    const matchesCategory = selectedCategoryKey === 'filterAll' || schemeCatKey === selectedCategoryKey;
    const q = searchQuery.toLowerCase().trim();
    const matchesSearch =
      !q ||
      scheme.title.toLowerCase().includes(q) ||
      scheme.benefit.toLowerCase().includes(q) ||
      scheme.eligibility.toLowerCase().includes(q);
    return matchesCategory && matchesSearch;
  });

  const getCategoryIcon = (schemeId: string) => {
    const catKey = SCHEME_CATEGORY_MAP[schemeId];
    switch (catKey) {
      case 'filterFinancial':
        return <FaLandmark className="category-icon" aria-hidden="true" />;
      case 'filterInsurance':
        return <FiShield className="category-icon" aria-hidden="true" />;
      case 'filterCredit':
        return <FaCreditCard className="category-icon" aria-hidden="true" />;
      case 'filterSoil':
        return <FaFlask className="category-icon" aria-hidden="true" />;
      default:
        return <FaLandmark className="category-icon" aria-hidden="true" />;
    }
  };

  return (
    <section className="schemes-section" aria-labelledby="schemes-heading">
      <div className="section-header">
        <h2 id="schemes-heading" className="section-title">
          {t('schemesHeading')}
        </h2>
        <p className="section-description">
          {t('schemesDesc')}
        </p>
      </div>

      {/* Emergency Helpline Banner */}
      <div className="emergency-helpline-card glass-card">
        <div className="emergency-content">
          <div className="emergency-icon-wrapper" aria-hidden="true">
            <FiPhoneCall className="emergency-icon" />
          </div>
          <div>
            <h3 className="emergency-title">{t('kisanCallCentre')}</h3>
            <p className="emergency-text">
              {t('nationalSupport')}
            </p>
          </div>
        </div>
        <div className="emergency-numbers-row">
          <a href="tel:18001801551" className="helpline-pill">
            <FiPhoneCall className="pill-phone-icon" aria-hidden="true" />
            <span>1800-180-1551 ({t('tabAdvisoryChat')})</span>
          </a>
          <a href="tel:14447" className="helpline-pill helpline-pill--insurance">
            <FiShield className="pill-phone-icon" aria-hidden="true" />
            <span>14447 ({t('filterInsurance')})</span>
          </a>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="schemes-controls-bar">
        <div className="search-box">
          <FiSearch className="search-icon" aria-hidden="true" />
          <input
            type="text"
            className="search-input"
            placeholder={t('searchSchemesPlaceholder')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Search government schemes"
          />
        </div>

        <div className="category-filters-scroll" role="tablist" aria-label="Scheme Categories">
          {CATEGORY_TABS.map((cat) => (
            <button
              key={cat.key}
              type="button"
              className={`category-filter-btn ${selectedCategoryKey === cat.key ? 'category-filter-btn--active' : ''}`}
              onClick={() => setSelectedCategoryKey(cat.key)}
            >
              {t(cat.key)}
            </button>
          ))}
        </div>
      </div>

      {/* Schemes Grid */}
      <div className="schemes-grid">
        {filteredSchemes.length === 0 ? (
          <div className="glass-card" style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--color-slate-300)', fontSize: '15px' }}>{t('noSchemesFound')}</p>
          </div>
        ) : (
          filteredSchemes.map((scheme) => (
            <article key={scheme.id} className="scheme-card glass-card">
              <div className="scheme-card-header">
                <div className="scheme-title-group">
                  <span className="scheme-cat-icon-wrapper" aria-hidden="true">
                    {getCategoryIcon(scheme.id)}
                  </span>
                  <div>
                    <span className="scheme-category-badge">
                      {t(SCHEME_CATEGORY_MAP[scheme.id] || 'filterAll')}
                    </span>
                    <h3 className="scheme-title">{scheme.title}</h3>
                  </div>
                </div>
              </div>

              {/* Mandatory notice callout for PMFBY */}
              {scheme.notice_period && (
                <div className="scheme-notice-alert">
                  <FiClock className="notice-icon" aria-hidden="true" />
                  <span>{scheme.notice_period}</span>
                </div>
              )}

              <div className="scheme-section-block">
                <h4 className="scheme-subhead">{t('benefitHeading')}:</h4>
                <p className="scheme-body-text">{scheme.benefit}</p>
              </div>

              <div className="scheme-section-block">
                <h4 className="scheme-subhead">{t('eligibilityHeading')}:</h4>
                <p className="scheme-body-text">{scheme.eligibility}</p>
              </div>

              <div className="scheme-section-block">
                <h4 className="scheme-subhead">{t('keyActionsHeading')}:</h4>
                <ul className="scheme-actions-list">
                  {scheme.key_actions.map((act, idx) => (
                    <li key={idx} className="scheme-action-item">
                      <FiCheckCircle className="scheme-check-icon" aria-hidden="true" />
                      <span>{act}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="scheme-card-footer">
                <div className="scheme-helpline">
                  <FiPhoneCall className="helpline-footer-icon" aria-hidden="true" />
                  <span>{t('officialHelpline')}: <strong>{scheme.helpline}</strong></span>
                </div>

                {scheme.portal_url && (
                  <a
                    href={scheme.portal_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="portal-link-btn"
                    title={t('officialPortal')}
                  >
                    <span>{t('visitPortal')}</span>
                    <FiExternalLink className="link-icon" aria-hidden="true" />
                  </a>
                )}
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  );
}

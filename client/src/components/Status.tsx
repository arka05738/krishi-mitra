/**
 * Status Component for Krishi Mitra Agricultural Advisory System.
 * Theme: White, Dark Blue, and Royal Gold.
 * Diagnostics panel displaying local station readiness and Arm reference architecture.
 * Zero Unicode emojis, strictly uses react-icons. Zero technical jargon.
 */
import { useState, useEffect } from 'react';
import {
  FiCheckCircle,
  FiAlertTriangle,
  FiRefreshCw,
  FiWifi,
  FiWifiOff,
  FiPhoneCall,
  FiShield,
  FiLoader,
  FiCpu,
} from 'react-icons/fi';
import { FaLeaf } from 'react-icons/fa6';
import type { SystemHealthResponse } from '../types/index.ts';
import { checkHealth } from '../services/api.ts';
import type { LanguageCode } from '../i18n/translations.ts';
import { getTranslation } from '../i18n/translations.ts';

export interface StatusProps {
  language?: LanguageCode;
}

export function Status({ language = 'en' }: StatusProps) {
  const [health, setHealth] = useState<SystemHealthResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastChecked, setLastChecked] = useState<string>('');

  const t = (key: string) => getTranslation(language, key);

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await checkHealth();
      setHealth(res);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to reach local station.');
      setLastChecked(new Date().toLocaleTimeString());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let isMounted = true;
    checkHealth()
      .then((res) => {
        if (isMounted) {
          setHealth(res);
          setLastChecked(new Date().toLocaleTimeString());
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Unable to reach local station.');
          setLastChecked(new Date().toLocaleTimeString());
        }
      })
      .finally(() => {
        if (isMounted) {
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const isStationReady = health?.status === 'ready';

  return (
    <section className="status-section" aria-labelledby="status-heading">
      <div className="section-header">
        <h2 id="status-heading" className="section-title">
          {t('statusHeading')}
        </h2>
        <p className="section-description">
          {t('statusDesc')}
        </p>
      </div>

      <div className="status-card glass-card">
        {/* Top Header Card */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', paddingBottom: '20px', borderBottom: '1px solid rgba(212,175,55,0.25)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <span
              style={{
                width: '44px',
                height: '44px',
                borderRadius: '50%',
                backgroundColor: '#0B192C',
                border: `2px solid ${isStationReady ? '#10B981' : '#EF4444'}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: isStationReady ? '#10B981' : '#EF4444',
                fontSize: '20px'
              }}
            >
              {isStationReady ? <FiWifi /> : <FiWifiOff />}
            </span>
            <div>
              <h3 style={{ fontSize: '20px', fontWeight: 800, color: '#FFFFFF' }}>
                {isStationReady ? t('stationOnlineTitle') : t('stationOfflineTitle')}
              </h3>
              <p style={{ fontSize: '13px', color: 'var(--color-slate-300)', marginTop: '2px' }}>
                {lastChecked ? `${t('lastVerifiedAt')}: ${lastChecked}` : t('checkingStatus')}
              </p>
            </div>
          </div>

          <button
            type="button"
            className="btn btn-secondary"
            onClick={fetchHealth}
            disabled={loading}
          >
            {loading ? (
              <FiLoader className="btn-icon spin" aria-hidden="true" />
            ) : (
              <FiRefreshCw className="btn-icon" aria-hidden="true" />
            )}
            <span>{t('refreshDiagnostics')}</span>
          </button>
        </div>

        {error && (
          <div className="alert-banner alert-banner--warning" role="alert" style={{ marginTop: '16px' }}>
            <FiAlertTriangle className="alert-icon" aria-hidden="true" />
            <div className="alert-content">
              <strong>{t('stationOfflineTitle')}</strong>
              <p>{t('reconnectNotice')}</p>
            </div>
          </div>
        )}

        {/* Diagnostic Metrics Grid */}
        <div className="status-grid" style={{ marginTop: '24px' }}>
          {/* Diagnostic 1: Offline Security */}
          <div className="status-metric-card">
            <div className="status-metric-header">
              <span className="status-metric-label">{t('operatingSecurity')}</span>
              <FiShield style={{ color: 'var(--color-gold-bright)', fontSize: '20px' }} />
            </div>
            <div className="status-metric-value">{t('offlinePercent')}</div>
            <p className="status-metric-subtext">
              {t('offlineSecurityDesc')}
            </p>
          </div>

          {/* Diagnostic 2: Arm Challenge Reference Runtime */}
          <div className="status-metric-card" style={{ border: '2px solid var(--color-gold)' }}>
            <div className="status-metric-header">
              <span className="status-metric-label" style={{ color: 'var(--color-gold-bright)' }}>{t('armReferenceRuntime')}</span>
              <FiCpu style={{ color: 'var(--color-gold-bright)', fontSize: '20px' }} />
            </div>
            <div className="status-metric-value" style={{ fontSize: '20px' }}>ExecuTorch + Llama 3.2</div>
            <p className="status-metric-subtext">
              {t('armRuntimeDesc')}
            </p>
          </div>

          {/* Diagnostic 3: Plant Health Scanner */}
          <div className="status-metric-card">
            <div className="status-metric-header">
              <span className="status-metric-label">{t('plantScannerDiagnostic')}</span>
              <FaLeaf style={{ color: 'var(--color-gold-bright)', fontSize: '20px' }} />
            </div>
            <div className="status-metric-value">
              {health?.vision_model_status === 'ready' ? t('activeAndReady') : t('initializingText')}
            </div>
            <p className="status-metric-subtext">
              {t('scannerDiagnosticDesc')}
            </p>
          </div>

          {/* Diagnostic 4: Field Knowledge Base */}
          <div className="status-metric-card">
            <div className="status-metric-header">
              <span className="status-metric-label">{t('icarKbDiagnostic')}</span>
              <FiCheckCircle style={{ color: 'var(--color-gold-bright)', fontSize: '20px' }} />
            </div>
            <div className="status-metric-value">
              {health?.total_documents ? `${health.total_documents} ${t('guidelinesSuffix')}` : t('guidelinesIndexed')}
            </div>
            <p className="status-metric-subtext">
              {t('icarKbDiagnosticDesc')}
            </p>
          </div>
        </div>

        {/* Edge Station Access Box */}
        <div style={{ marginTop: '24px', padding: '16px 20px', backgroundColor: '#0B192C', border: '1.5px solid var(--color-border-gold)', borderRadius: 'var(--radius-md)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-gold-bright)', textTransform: 'uppercase' }}>
              {t('hotspotAddressLabel')}
            </span>
            <code style={{ background: '#102A43', padding: '4px 10px', borderRadius: '6px', color: '#FFFFFF', fontWeight: 700 }}>
              {health?.edge_access || 'http://192.168.31.235:8000'}
            </code>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--color-slate-300)', marginTop: '8px' }}>
            {t('hotspotAddressDesc')}
          </p>
        </div>

        {/* Support Footer */}
        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid rgba(212,175,55,0.2)', display: 'flex', alignItems: 'center', gap: '10px', color: '#CBD5E1', fontSize: '14px' }}>
          <FiPhoneCall style={{ color: 'var(--color-gold-bright)', fontSize: '16px' }} />
          <span>
            {t('nationalSupport')}
          </span>
        </div>
      </div>
    </section>
  );
}

/**
 * SoilCard Component for Krishi Mitra Agricultural Advisory System.
 * 12-Parameter Soil Health Card diagnostic calculator and split fertilizer schedules.
 * Zero Unicode emojis, strictly uses react-icons. Zero technical jargon.
 */
import { useState, useEffect } from 'react';
import type { FormEvent, ChangeEvent } from 'react';
import {
  FiAlertTriangle,
  FiLoader,
  FiChevronDown,
  FiChevronUp,
  FiCheckCircle,
  FiMapPin,
  FiDroplet,
  FiPackage,
  FiPrinter,
  FiClipboard,
} from 'react-icons/fi';
import { FaFlask } from 'react-icons/fa6';
import type { SoilReportInput, SoilReportOutput } from '../types/index.ts';
import { calculateSoilReport } from '../services/api.ts';
import type { LanguageCode } from '../i18n/translations.ts';
import { getTranslation } from '../i18n/translations.ts';


interface RegionalGuideData {
  regions: Array<{
    id: string;
    name: string;
    states: string;
    soil_types: string;
    cropping_systems: string;
    recommended_varieties: string;
    early_warning_focus: string;
    weather_contingency: string;
  }>;
  selected_region: {
    id: string;
    name: string;
    states: string;
    soil_types: string;
    cropping_systems: string;
    recommended_varieties: string;
    early_warning_focus: string;
    weather_contingency: string;
  };
  selected_crop_guide: {
    crop_name: string;
    seed_rate_acre: string;
    seed_rate_bigha: string;
    spacing: string;
    seed_treatment_fir: string;
    critical_irrigation_stages: string[];
    post_harvest_protocol: {
      maturity_indice: string;
      safe_moisture_pct: string;
      storage_loss_prevention: string;
      market_grading: string;
    };
    early_warning_signs: string;
  };
}

interface ExtensionLogItem {
  id: string;
  farmerName: string;
  village: string;
  region: string;
  season: string;
  crop: string;
  acres: number;
  summary: string;
  timestamp: string;
}

export interface SoilCardProps {
  language?: LanguageCode;
}

interface SoilPreset {
  name: string;
  key: string;
  data: SoilReportInput;
}

const PRESETS: SoilPreset[] = [
  {
    name: 'Typical Alluvial Paddy Soil',
    key: 'presetAlluvial',
    data: {
      crop: 'Rice',
      nitrogen: 210,
      phosphorus: 35,
      potassium: 190,
      ph: 5.8,
      electrical_conductivity: 0.6,
      organic_carbon: 0.45,
      area_acres: 2.5,
      zinc: 0.6,
      sulphur: 10.0,
      boron: 0.4,
    },
  },
  {
    name: 'Acidic Hill Soil',
    key: 'presetAcidic',
    data: {
      crop: 'Wheat',
      nitrogen: 160,
      phosphorus: 20,
      potassium: 140,
      ph: 4.8,
      electrical_conductivity: 0.3,
      organic_carbon: 0.8,
      area_acres: 1.0,
      zinc: 0.5,
      sulphur: 8.0,
    },
  },
  {
    name: 'Alkaline Black Soil',
    key: 'presetAlkaline',
    data: {
      crop: 'Cotton',
      nitrogen: 180,
      phosphorus: 28,
      potassium: 240,
      ph: 8.4,
      electrical_conductivity: 1.2,
      organic_carbon: 0.5,
      area_acres: 2.0,
      zinc: 0.7,
      iron: 4.5,
    },
  },
];

export function SoilCard({ language = 'en' }: SoilCardProps) {
  const t = (key: string) => getTranslation(language, key);
  const [formData, setFormData] = useState<SoilReportInput>({
    crop: 'Rice',
    nitrogen: 210,
    phosphorus: 35,
    potassium: 190,
    ph: 5.8,
    electrical_conductivity: 0.6,
    organic_carbon: 0.45,
    area_acres: 1.0,
    zinc: 0.6,
    sulphur: 10.0,
    boron: 0.4,
    iron: 4.0,
    manganese: 3.0,
    copper: 1.0,
  });

  const [showMicronutrients, setShowMicronutrients] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [output, setOutput] = useState<SoilReportOutput | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activePreset, setActivePreset] = useState<string | null>(null);
  const [selectedRegionId, setSelectedRegionId] = useState<string>('zone_3_lower_gangetic');
  const [selectedSeason, setSelectedSeason] = useState<string>('Kharif (Monsoon)');
  const [regionalGuide, setRegionalGuide] = useState<RegionalGuideData | null>(null);
  const [farmerName, setFarmerName] = useState<string>('');
  const [villageName, setVillageName] = useState<string>('');
  const [extensionLogs, setExtensionLogs] = useState<ExtensionLogItem[]>([]);

  useEffect(() => {
    fetch(`/api/advisory/regional-guide?region_id=${encodeURIComponent(selectedRegionId)}&crop=${encodeURIComponent(formData.crop)}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setRegionalGuide(data);
      })
      .catch(() => {});
  }, [selectedRegionId, formData.crop]);

  const handleSaveExtensionLog = () => {
    const name = farmerName.trim() || 'Walk-in Kisan Bhai';
    const vil = villageName.trim() || 'Local Gram Panchayat';
    const regName = regionalGuide?.selected_region?.name || 'Lower Gangetic Plains (West Bengal)';
    const fertSummary = output
      ? `pH: ${output.ph_status} | Urea: ${output.urea_kg.toFixed(1)}kg, DAP: ${output.dap_kg.toFixed(1)}kg, MOP: ${output.mop_kg.toFixed(1)}kg`
      : `Seed Rate: ${regionalGuide?.selected_crop_guide?.seed_rate_acre || 'Standard ICAR'}`;
    const newEntry: ExtensionLogItem = {
      id: String(Date.now()),
      farmerName: name,
      village: vil,
      region: regName,
      season: selectedSeason,
      crop: formData.crop,
      acres: formData.area_acres,
      summary: fertSummary,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setExtensionLogs((prev) => [newEntry, ...prev.slice(0, 9)]);
    setFarmerName('');
    setVillageName('');
  };


  const handleInputChange = (field: keyof SoilReportInput, value: string) => {
    setActivePreset(null);
    if (field === 'crop') {
      setFormData((prev) => ({ ...prev, [field]: value }));
    } else {
      const num = parseFloat(value);
      setFormData((prev) => ({
        ...prev,
        [field]: isNaN(num) ? 0 : num,
      }));
    }
  };

  const handleApplyPreset = (preset: SoilPreset) => {
    setActivePreset(preset.name);
    setFormData(preset.data);
    setError(null);
    setOutput(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Form boundary validation
    if (formData.ph < 0 || formData.ph > 14) {
      setError('Soil pH must be between 0.0 and 14.0');
      setLoading(false);
      return;
    }
    if (formData.area_acres <= 0) {
      setError('Farm area must be greater than zero acres');
      setLoading(false);
      return;
    }

    try {
      const res = await calculateSoilReport(formData);
      setOutput(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Soil calculation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="soil-card-section" aria-labelledby="soil-card-heading">
      <div className="section-header">
        <h2 id="soil-card-heading" className="section-title">
          {t("soilHeading")}
        </h2>
        <p className="section-description">
          {t("soilDesc")}
        </p>
      </div>

      {/* Preset Quick Fill */}
      <div className="presets-bar">
        <span className="presets-label">{t("quickPresets")}:</span>
        <div className="presets-buttons">
          {PRESETS.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              className={`preset-btn ${activePreset === preset.name ? 'preset-btn--active' : ''}`}
              onClick={() => handleApplyPreset(preset)}
              disabled={loading}
            >
              {t(preset.key) || preset.name}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="alert-banner alert-banner--error" role="alert">
          <FiAlertTriangle className="alert-icon" aria-hidden="true" />
          <span className="alert-message">{error}</span>
        </div>
      )}

      <div className="soil-layout">
        {/* Input Form Card */}
        <div className="soil-form-card glass-card">
          <form onSubmit={handleSubmit} className="soil-form">
            <h3 className="card-subheading">{t("tabSoilHealth")}</h3>

            {/* Crop and Field Area */}
            <div className="form-row-2">
              <div className="form-group">
                <label htmlFor="soil-crop" className="input-label">
                  {t("cropType")}:
                </label>
                <select
                  id="soil-crop"
                  className="select-input"
                  value={formData.crop}
                  onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                    handleInputChange('crop', e.target.value)
                  }
                  disabled={loading}
                >
                  <option value="Rice">{t("cropRice")}</option>
                  <option value="Wheat">{t("cropWheat")}</option>
                  <option value="Tomato">{t("cropTomato")}</option>
                  <option value="Potato">{t("cropPotato")}</option>
                  <option value="Sunflower">{t("cropSunflower")}</option>
                  <option value="Maize">{t("cropMaize")}</option>
                  <option value="Cotton">{t("cropCotton")}</option>
                  <option value="Mustard">{t("cropMustard")}</option>
                  <option value="Soybean">{t("cropSoybean")}</option>
                  <option value="Chilli">{t("cropChilli")}</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="soil-acres" className="input-label">
                  {t("farmArea")}:
                </label>
                <input
                  id="soil-acres"
                  type="number"
                  step="0.1"
                  min="0.1"
                  className="text-input"
                  value={formData.area_acres}
                  onChange={(e) => handleInputChange('area_acres', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            {/* Primary Chemical Parameters (pH, EC, OC) */}
            <h4 className="group-label">{t("primaryNutrients")}</h4>
            <div className="form-row-3">
              <div className="form-group">
                <label htmlFor="soil-ph" className="input-label">
                  {t("soilPh")}:
                </label>
                <input
                  id="soil-ph"
                  type="number"
                  step="0.1"
                  min="0"
                  max="14"
                  className="text-input"
                  value={formData.ph}
                  onChange={(e) => handleInputChange('ph', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="soil-ec" className="input-label">
                  {t("electricalConductivity")}:
                </label>
                <input
                  id="soil-ec"
                  type="number"
                  step="0.05"
                  min="0"
                  className="text-input"
                  value={formData.electrical_conductivity}
                  onChange={(e) => handleInputChange('electrical_conductivity', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="soil-oc" className="input-label">
                  {t("organicCarbon")}:
                </label>
                <input
                  id="soil-oc"
                  type="number"
                  step="0.05"
                  min="0"
                  className="text-input"
                  value={formData.organic_carbon}
                  onChange={(e) => handleInputChange('organic_carbon', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            {/* Primary Macronutrients (N, P, K) in kg/ha */}
            <h4 className="group-label">{t("primaryNutrients")} (kg/ha)</h4>
            <div className="form-row-3">
              <div className="form-group">
                <label htmlFor="soil-n" className="input-label">
                  {t("nitrogen")}:
                </label>
                <input
                  id="soil-n"
                  type="number"
                  step="1"
                  min="0"
                  className="text-input"
                  value={formData.nitrogen}
                  onChange={(e) => handleInputChange('nitrogen', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="soil-p" className="input-label">
                  {t("phosphorus")}:
                </label>
                <input
                  id="soil-p"
                  type="number"
                  step="1"
                  min="0"
                  className="text-input"
                  value={formData.phosphorus}
                  onChange={(e) => handleInputChange('phosphorus', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="soil-k" className="input-label">
                  {t("potassium")}:
                </label>
                <input
                  id="soil-k"
                  type="number"
                  step="1"
                  min="0"
                  className="text-input"
                  value={formData.potassium}
                  onChange={(e) => handleInputChange('potassium', e.target.value)}
                  disabled={loading}
                  required
                />
              </div>
            </div>

            {/* Micronutrients Toggle */}
            <div className="micronutrients-toggle-row">
              <button
                type="button"
                className="toggle-expand-btn"
                onClick={() => setShowMicronutrients(!showMicronutrients)}
              >
                <span>{showMicronutrients ? t("hideMicronutrients") : t("showMicronutrients")}</span>
                {showMicronutrients ? <FiChevronUp /> : <FiChevronDown />}
              </button>
            </div>

            {showMicronutrients && (
              <div className="micronutrients-panel">
                <div className="form-row-3">
                  <div className="form-group">
                    <label htmlFor="soil-s" className="input-label">
                      {t("sulphur")} (ppm):
                    </label>
                    <input
                      id="soil-s"
                      type="number"
                      step="0.5"
                      min="0"
                      className="text-input"
                      value={formData.sulphur ?? 0}
                      onChange={(e) => handleInputChange('sulphur', e.target.value)}
                      disabled={loading}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="soil-zn" className="input-label">
                      {t("zinc")} (ppm):
                    </label>
                    <input
                      id="soil-zn"
                      type="number"
                      step="0.1"
                      min="0"
                      className="text-input"
                      value={formData.zinc ?? 0}
                      onChange={(e) => handleInputChange('zinc', e.target.value)}
                      disabled={loading}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="soil-b" className="input-label">
                      {t("boron")} (ppm):
                    </label>
                    <input
                      id="soil-b"
                      type="number"
                      step="0.1"
                      min="0"
                      className="text-input"
                      value={formData.boron ?? 0}
                      onChange={(e) => handleInputChange('boron', e.target.value)}
                      disabled={loading}
                    />
                  </div>
                </div>

                <div className="form-row-3">
                  <div className="form-group">
                    <label htmlFor="soil-fe" className="input-label">
                      {t("iron")} (ppm):
                    </label>
                    <input
                      id="soil-fe"
                      type="number"
                      step="0.5"
                      min="0"
                      className="text-input"
                      value={formData.iron ?? 0}
                      onChange={(e) => handleInputChange('iron', e.target.value)}
                      disabled={loading}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="soil-mn" className="input-label">
                      {t("manganese")} (ppm):
                    </label>
                    <input
                      id="soil-mn"
                      type="number"
                      step="0.5"
                      min="0"
                      className="text-input"
                      value={formData.manganese ?? 0}
                      onChange={(e) => handleInputChange('manganese', e.target.value)}
                      disabled={loading}
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="soil-cu" className="input-label">
                      {t("copper")} (ppm):
                    </label>
                    <input
                      id="soil-cu"
                      type="number"
                      step="0.1"
                      min="0"
                      className="text-input"
                      value={formData.copper ?? 0}
                      onChange={(e) => handleInputChange('copper', e.target.value)}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>
            )}

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary btn-large btn-full"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <FiLoader className="btn-icon spin" aria-hidden="true" />
                    <span>{t("calculatingDosagesText")}</span>
                  </>
                ) : (
                  <>
                    <FaFlask className="btn-icon" aria-hidden="true" />
                    <span>{t("calculateDose")}</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Output Recommendation Card */}
        <div className="soil-result-column">
          {loading && (
            <div className="loading-card glass-card">
              <FiLoader className="loading-spinner spin" aria-hidden="true" />
              <h3 className="loading-title">{t("calculatingNutrientTitle")}</h3>
              <p className="loading-subtitle">
                {t("calculatingNutrientSubtitle")}
              </p>
            </div>
          )}

          {output && !loading && (
            <div className="soil-output-card glass-card" tabIndex={0} aria-label="Fertilizer Recommendations">
              <div className="output-header">
                <div>
                  <span className="badge-tag">{formData.crop} {t("recommendationSummary")}</span>
                  <h3 className="output-title">{t("fertilizerDosageTitle")}</h3>
                </div>
                <span className="acres-badge">{t("farmArea")}: {formData.area_acres}</span>
              </div>

              {/* Soil Status & Amendment */}
              <div className="ph-diagnostic-banner">
                <div className="ph-status-row">
                  <span className="ph-label">{t("soilDiagnosticLabel")}</span>
                  <strong className="ph-value">{output.ph_status}</strong>
                </div>
                {output.amendment_needed && (
                  <div className="amendment-callout">
                    <FiAlertTriangle className="callout-icon" aria-hidden="true" />
                    <span>{t("amendmentPrescribedLabel")} {output.amendment_needed}</span>
                  </div>
                )}
              </div>

              {/* Commercial Fertilizer Dosages Grid */}
              <h4 className="block-subheading">{t("fertilizerDosageTitle")}</h4>
              <div className="fertilizer-grid">
                <div className="fert-card fert-card--urea">
                  <span className="fert-title">{t("ureaLabel")}</span>
                  <span className="fert-kg">{output.urea_kg.toFixed(1)} kg</span>
                  <span className="fert-bags">
                    ({(output.urea_kg / 45).toFixed(1)} {t("bagsOf45kg")})
                  </span>
                </div>

                <div className="fert-card fert-card--dap">
                  <span className="fert-title">{t("dapLabel")}</span>
                  <span className="fert-kg">{output.dap_kg.toFixed(1)} kg</span>
                  <span className="fert-bags">
                    ({(output.dap_kg / 50).toFixed(1)} {t("bagsOf50kg")})
                  </span>
                </div>

                <div className="fert-card fert-card--mop">
                  <span className="fert-title">{t("mopLabel")}</span>
                  <span className="fert-kg">{output.mop_kg.toFixed(1)} kg</span>
                  <span className="fert-bags">
                    ({(output.mop_kg / 50).toFixed(1)} {t("bagsOf50kg")})
                  </span>
                </div>

                {output.zinc_sulphate_kg !== undefined && output.zinc_sulphate_kg > 0 && (
                  <div className="fert-card fert-card--zinc">
                    <span className="fert-title">{t("zincSulphateLabel")}</span>
                    <span className="fert-kg">{output.zinc_sulphate_kg.toFixed(1)} kg</span>
                    <span className="fert-bags">{t("secondaryMicronutrients")}</span>
                  </div>
                )}
              </div>

              {/* MANDATORY MIXING SAFETY WARNING: Do NOT mix Zinc Sulphate directly with DAP */}
              <div className="mixing-warning-banner" role="alert">
                <FiAlertTriangle className="warning-icon" aria-hidden="true" />
                <div className="warning-content">
                  <strong className="warning-title">{t("safetyWarningTitle")}</strong>
                  <p className="warning-text">
                    {t("safetyWarningDesc") || "Do NOT mix Zinc Sulphate directly with DAP. Applying them together causes chemical lock-up forming insoluble zinc phosphate, making both nutrients unavailable to plant roots. Keep a minimum 3-day gap or apply separately."}
                  </p>
                </div>
              </div>

              {/* Phenological Split-Application Schedule */}
              {output.application_schedule && output.application_schedule.length > 0 && (
                <div className="schedule-block">
                  <h4 className="block-subheading">{t("splitScheduleTitle")}</h4>
                  <ol className="schedule-list">
                    {output.application_schedule.map((step, idx) => (
                      <li key={idx} className="schedule-item">
                        <span className="schedule-step-number">{idx + 1}</span>
                        <span className="schedule-step-text">{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </div>
          )}

          {!output && !loading && (
            <div className="soil-placeholder-card glass-card">
              <FaFlask className="placeholder-flask-icon" aria-hidden="true" />
              <h3 className="placeholder-title">{t("tabSoilHealth")}</h3>
              <p className="placeholder-text">{t("soilDesc")}</p>
            </div>
          )}
        </div>
      </div>
{/* =====================================================================
          REGION-SPECIFIC, IRRIGATION, POST-HARVEST & EXTENSION WORKER SUITE
          ===================================================================== */}
      {regionalGuide && (
        <div style={{ marginTop: '32px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* 1. Region-Specific Agro-Climatic & Season Selector Bar */}
          <div className="glass-card" style={{ padding: '22px', border: '1.5px solid var(--color-gold)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <FiMapPin style={{ color: 'var(--color-gold-bright)', fontSize: '22px' }} />
                <div>
                  <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-gold-bright)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    {t("agroClimaticHeading")}
                  </span>
                  <h3 style={{ fontSize: '20px', fontWeight: 800, color: '#FFFFFF', margin: 0 }}>
                    {regionalGuide.selected_region.name}
                  </h3>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                <div>
                  <label htmlFor="region-select" className="input-label" style={{ fontSize: '12px', marginBottom: '4px', display: 'block' }}>
                    {t("selectAgroRegion")}
                  </label>
                  <select
                    id="region-select"
                    className="select-input"
                    value={selectedRegionId}
                    onChange={(e) => setSelectedRegionId(e.target.value)}
                  >
                    {regionalGuide.regions.map((reg) => (
                      <option key={reg.id} value={reg.id}>
                        {reg.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="season-select" className="input-label" style={{ fontSize: '12px', marginBottom: '4px', display: 'block' }}>
                    {t("selectCroppingSeason")}
                  </label>
                  <select
                    id="season-select"
                    className="select-input"
                    value={selectedSeason}
                    onChange={(e) => setSelectedSeason(e.target.value)}
                  >
                    <option value="Kharif (Monsoon)">{t("seasonKharif")}</option>
                    <option value="Rabi (Winter)">{t("seasonRabi")}</option>
                    <option value="Zaid / Pre-Kharif (Summer)">{t("seasonZaid")}</option>
                  </select>
                </div>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '14px' }}>
              <div style={{ background: 'rgba(11, 25, 44, 0.75)', padding: '14px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <strong style={{ color: 'var(--color-gold-bright)', fontSize: '13px', display: 'block', marginBottom: '4px' }}>
                  {t("districtsAndSoils")}
                </strong>
                <p style={{ fontSize: '13px', color: '#E2E8F0', margin: 0 }}>
                  {regionalGuide.selected_region.states} &bull; <em>{regionalGuide.selected_region.soil_types}</em>
                </p>
              </div>

              <div style={{ background: 'rgba(11, 25, 44, 0.75)', padding: '14px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <strong style={{ color: 'var(--color-gold-bright)', fontSize: '13px', display: 'block', marginBottom: '4px' }}>
                  {t("regionalVarieties")}
                </strong>
                <p style={{ fontSize: '13px', color: '#E2E8F0', margin: 0 }}>
                  {regionalGuide.selected_region.recommended_varieties}
                </p>
              </div>

              <div style={{ background: 'rgba(217, 119, 6, 0.14)', padding: '14px', borderRadius: '8px', border: '1px solid rgba(217, 119, 6, 0.35)' }}>
                <strong style={{ color: '#FCD34D', fontSize: '13px', display: 'block', marginBottom: '4px' }}>
                  {t("earlyWarningContingency")}
                </strong>
                <p style={{ fontSize: '13px', color: '#FEF3C7', margin: 0 }}>
                  {regionalGuide.selected_region.early_warning_focus} {regionalGuide.selected_region.weather_contingency}
                </p>
              </div>
            </div>
          </div>

          {/* 2. Three-Column Operational Suite: Irrigation Advisory | Post-Harvest Loss Reduction | Smallholder Decision Support */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(310px, 1fr))', gap: '20px' }}>
            {/* Card A: Critical Irrigation & Water Management Advisory */}
            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <FiDroplet style={{ color: '#38BDF8', fontSize: '22px' }} />
                <div>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#38BDF8', textTransform: 'uppercase' }}>
                    {t("waterManagement")}
                  </span>
                  <h4 style={{ fontSize: '17px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>
                    {t("criticalIrrigationTitle")} ({regionalGuide.selected_crop_guide.crop_name})
                  </h4>
                </div>
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {regionalGuide.selected_crop_guide.critical_irrigation_stages.map((st, i) => (
                  <li key={i} style={{ display: 'flex', gap: '8px', fontSize: '13px', color: '#E2E8F0', background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                    <FiCheckCircle style={{ color: 'var(--color-gold-bright)', flexShrink: 0, marginTop: '3px' }} />
                    <span>{st}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Card B: Post-Harvest Loss Reduction & Safe Storage */}
            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <FiPackage style={{ color: 'var(--color-gold-bright)', fontSize: '22px' }} />
                <div>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--color-gold-bright)', textTransform: 'uppercase' }}>
                    {t("postHarvestLossTitle")}
                  </span>
                  <h4 style={{ fontSize: '17px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>
                    {t("safeStorageProtocol")}
                  </h4>
                </div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px', color: '#E2E8F0' }}>
                <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: 'var(--color-gold-bright)', display: 'block' }}>{t("harvestMaturity")}</strong>
                  <span>{regionalGuide.selected_crop_guide.post_harvest_protocol.maturity_indice}</span>
                </div>
                <div style={{ background: 'rgba(16, 185, 129, 0.12)', border: '1px solid rgba(16, 185, 129, 0.35)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: '#34D399', display: 'block' }}>{t("safeStorageMoisture")}</strong>
                  <span>{regionalGuide.selected_crop_guide.post_harvest_protocol.safe_moisture_pct}</span>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: 'var(--color-gold-bright)', display: 'block' }}>{t("storagePestControl")}</strong>
                  <span>{regionalGuide.selected_crop_guide.post_harvest_protocol.storage_loss_prevention}</span>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: 'var(--color-gold-bright)', display: 'block' }}>{t("mandiLotGrading")}</strong>
                  <span>{regionalGuide.selected_crop_guide.post_harvest_protocol.market_grading}</span>
                </div>
              </div>
            </div>

            {/* Card C: Smallholder Farmer Decision Support & Seed Treatment */}
            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <FiClipboard style={{ color: '#34D399', fontSize: '22px' }} />
                <div>
                  <span style={{ fontSize: '11px', fontWeight: 700, color: '#34D399', textTransform: 'uppercase' }}>
                    {t("decisionSupportHeader")}
                  </span>
                  <h4 style={{ fontSize: '17px', fontWeight: 700, color: '#FFFFFF', margin: 0 }}>
                    {t("plotCalculator")} ({formData.area_acres} {formData.area_acres === 1 ? 'Acre' : 'Acres'} = {(formData.area_acres * 3.0).toFixed(1)} {t("acreEqualsBigha")})
                  </h4>
                </div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px', color: '#E2E8F0' }}>
                <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: 'var(--color-gold-bright)', display: 'block' }}>{t("seedRateLabel")}</strong>
                  <span>{regionalGuide.selected_crop_guide.seed_rate_acre} &bull; ({regionalGuide.selected_crop_guide.seed_rate_bigha})</span>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: 'var(--color-gold-bright)', display: 'block' }}>{t("plantingGeometry")}</strong>
                  <span>{regionalGuide.selected_crop_guide.spacing}</span>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: 'var(--color-gold-bright)', display: 'block' }}>{t("firSeedTreatment")}</strong>
                  <span>{regionalGuide.selected_crop_guide.seed_treatment_fir}</span>
                </div>
                <div style={{ background: 'rgba(217, 119, 6, 0.14)', border: '1px solid rgba(217, 119, 6, 0.35)', padding: '10px', borderRadius: '6px' }}>
                  <strong style={{ color: '#FCD34D', display: 'block' }}>{t("fieldScouting")}</strong>
                  <span>{regionalGuide.selected_crop_guide.early_warning_signs}</span>
                </div>
              </div>
            </div>
          </div>

          {/* 3. Agri-Extension Worker Field Prescription & Village Camp Log Tool */}
          <div className="glass-card" style={{ padding: '22px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '14px' }}>
              <div>
                <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-gold-bright)', textTransform: 'uppercase' }}>
                  {t("extensionToolkit")}
                </span>
                <h3 style={{ fontSize: '19px', fontWeight: 800, color: '#FFFFFF', margin: 0 }}>
                  {t("villageClinicTitle")}
                </h3>
              </div>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => window.print()}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}
              >
                <FiPrinter aria-hidden="true" />
                <span>{t("printPrescriptionBtn")}</span>
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', alignItems: 'end', marginBottom: '16px' }}>
              <div>
                <label htmlFor="ext-farmer-name" className="input-label" style={{ fontSize: '12px' }}>{t("farmerNameLabel")}</label>
                <input
                  id="ext-farmer-name"
                  type="text"
                  className="text-input"
                  placeholder="e.g., Ramesh Mondal"
                  value={farmerName}
                  onChange={(e) => setFarmerName(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="ext-village" className="input-label" style={{ fontSize: '12px' }}>{t("villageLabel")}</label>
                <input
                  id="ext-village"
                  type="text"
                  className="text-input"
                  placeholder="e.g., Singur GP, Hooghly"
                  value={villageName}
                  onChange={(e) => setVillageName(e.target.value)}
                />
              </div>
              <div>
                <button
                  type="button"
                  className="btn btn-accent btn-full"
                  onClick={handleSaveExtensionLog}
                >
                  <span>{t("logConsultationBtn")}</span>
                </button>
              </div>
            </div>

            {extensionLogs.length > 0 && (
              <div style={{ background: 'rgba(11, 25, 44, 0.8)', borderRadius: '8px', padding: '14px', border: '1px solid rgba(212, 175, 55, 0.3)' }}>
                <strong style={{ color: 'var(--color-gold-bright)', fontSize: '13px', display: 'block', marginBottom: '8px' }}>
                  {t("consultationLogHeader")} ({extensionLogs.length}):
                </strong>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {extensionLogs.map((log) => (
                    <div key={log.id} style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px', fontSize: '13px', padding: '8px 10px', background: 'rgba(30, 62, 98, 0.35)', borderRadius: '6px', color: '#F8FAFC' }}>
                      <span>
                        <strong>{log.farmerName}</strong> ({log.village}) &bull; {log.crop} ({log.acres} Acre / {(log.acres * 3).toFixed(1)} Bigha) &bull; {log.season}
                      </span>
                      <span style={{ color: '#FCD34D' }}>{log.summary} [{log.timestamp}]</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );
}

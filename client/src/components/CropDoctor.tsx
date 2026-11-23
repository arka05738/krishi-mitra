/**
 * CropDoctor Component for Krishi Mitra Agricultural Advisory System.
 * Theme: White, Dark Blue, and Royal Gold.
 * Features:
 * - High-resolution Hero Farmer Banner
 * - 9 Handcrafted Crop Vector SVGs
 * - Two-Stage Non-Crop Gatekeeper Rejection
 * - Strict Rule: Diagnostic Accuracy hidden if < 80%
 * - Zero tech jargon / Zero emojis (react-icons only)
 * - Multilingual Support
 */
import { useState, useEffect, useRef } from 'react';
import type { ChangeEvent, DragEvent } from 'react';
import {
  FiUpload,
  FiCamera,
  FiRefreshCw,
  FiCheckCircle,
  FiAlertTriangle,
  FiXCircle,
  FiCheckSquare,
  FiMessageSquare,
  FiAlertCircle,
  FiLoader,
  FiImage,
  FiVolume2,
  FiVolumeX,
} from 'react-icons/fi';
import { FaLeaf } from 'react-icons/fa6';

// Custom Crop Vector SVGs
import tomatoSvg from '../assets/crops/tomato.svg';
import potatoSvg from '../assets/crops/potato.svg';
import cornSvg from '../assets/crops/corn.svg';
import wheatSvg from '../assets/crops/wheat.svg';
import riceSvg from '../assets/crops/rice.svg';
import sunflowerSvg from '../assets/crops/sunflower.svg';
import cottonSvg from '../assets/crops/cotton.svg';
import appleSvg from '../assets/crops/apple.svg';
import chilliSvg from '../assets/crops/chilli.svg';

// Custom Generated Banner
import heroBanner from '../assets/hero_farmer_banner.jpg';

import type { CropAnalysisResult, SampleImageInfo } from '../types/index.ts';
import {
  analyzeImage,
  analyzeSampleImage,
  getSampleImages,
  detectPests,
  getPestSampleImages,
  analyzePestSampleImage,
  reLocalizeCropResult,
  reLocalizePestResult,
  API_BASE,
} from '../services/api.ts';
import type { PestDetectionResponse } from '../services/api.ts';
import type { LanguageCode } from '../i18n/translations.ts';
import { getTranslation, SUPPORTED_LANGUAGES } from '../i18n/translations.ts';

interface CropDoctorProps {
  onConsultAdvisor: (cropName: string, condition: string, resultContext: string) => void;
  language?: LanguageCode;
}

const CROP_SVG_LIST = [
  { id: 'Tomato', name: 'Tomato', svg: tomatoSvg },
  { id: 'Potato', name: 'Potato', svg: potatoSvg },
  { id: 'Corn', name: 'Corn / Maize', svg: cornSvg },
  { id: 'Wheat', name: 'Wheat', svg: wheatSvg },
  { id: 'Rice', name: 'Rice / Paddy', svg: riceSvg },
  { id: 'Sunflower', name: 'Sunflower', svg: sunflowerSvg },
  { id: 'Cotton', name: 'Cotton', svg: cottonSvg },
  { id: 'Apple', name: 'Apple', svg: appleSvg },
  { id: 'Chilli', name: 'Chilli', svg: chilliSvg },
];

const DEFAULT_SAMPLES: SampleImageInfo[] = [
  {
    id: 'tomato_early_blight',
    name: 'Tomato Early Blight',
    filename: 'tomato_early_blight.jpg',
    crop: 'Tomato',
    condition: 'Early Blight',
    url: '/api/vision/samples/tomato_early_blight.jpg',
  },
  {
    id: 'tomato_healthy',
    name: 'Tomato Healthy',
    filename: 'tomato_healthy.jpg',
    crop: 'Tomato',
    condition: 'Healthy Condition',
    url: '/api/vision/samples/tomato_healthy.jpg',
  },
  {
    id: 'potato_late_blight',
    name: 'Potato Late Blight',
    filename: 'potato_late_blight.jpg',
    crop: 'Potato',
    condition: 'Late Blight',
    url: '/api/vision/samples/potato_late_blight.jpg',
  },
  {
    id: 'sunflower_healthy',
    name: 'Sunflower Blossom',
    filename: 'sunflower_healthy.jpg',
    crop: 'Sunflower',
    condition: 'Prime Blossom',
    url: '/api/vision/samples/sunflower_healthy.jpg',
  },
  {
    id: 'corn_common_rust',
    name: 'Corn Rust',
    filename: 'corn_common_rust.jpg',
    crop: 'Corn',
    condition: 'Common Rust',
    url: '/api/vision/samples/corn_common_rust.jpg',
  },
  {
    id: 'apple_scab',
    name: 'Apple Scab',
    filename: 'apple_scab.jpg',
    crop: 'Apple',
    condition: 'Leaf Scab',
    url: '/api/vision/samples/apple_scab.jpg',
  },
];

const DEFAULT_PEST_SAMPLES: SampleImageInfo[] = [
  {
    id: 'pest_rice_leaf_roller',
    name: 'Rice Leaf Roller',
    filename: 'pest_rice_leaf_roller.jpg',
    crop: 'Rice / Paddy',
    condition: 'Leaf Folder Caterpillar',
    url: '/api/vision/pest-samples/pest_rice_leaf_roller.jpg',
  },
  {
    id: 'pest_corn_borer',
    name: 'Maize / Corn Borer',
    filename: 'pest_corn_borer.jpg',
    crop: 'Corn / Maize',
    condition: 'Stem Borer Pest',
    url: '/api/vision/pest-samples/pest_corn_borer.jpg',
  },
  {
    id: 'pest_armyworm',
    name: 'Field Armyworm',
    filename: 'pest_armyworm.jpg',
    crop: 'Maize / Paddy',
    condition: 'Armyworm Outbreak',
    url: '/api/vision/pest-samples/pest_armyworm.jpg',
  },
  {
    id: 'pest_brown_planthopper',
    name: 'Brown Planthopper',
    filename: 'pest_brown_planthopper.jpg',
    crop: 'Rice / Paddy',
    condition: 'BPH Hopper Burn Hazard',
    url: '/api/vision/pest-samples/pest_brown_planthopper.jpg',
  },
  {
    id: 'pest_mole_cricket',
    name: 'Mole Cricket',
    filename: 'pest_mole_cricket.jpg',
    crop: 'Vegetables / Paddy',
    condition: 'Root & Seedling Feeder',
    url: '/api/vision/pest-samples/pest_mole_cricket.jpg',
  },
  {
    id: 'pest_red_spider',
    name: 'Red Spider Mite',
    filename: 'pest_red_spider.jpg',
    crop: 'Cotton / Chilli',
    condition: 'Sap-Sucking Foliage Mite',
    url: '/api/vision/pest-samples/pest_red_spider.jpg',
  },
];

export function CropDoctor({ onConsultAdvisor, language = 'en' }: CropDoctorProps) {
  const t = (key: string) => getTranslation(language, key);

  const [scanMode, setScanMode] = useState<'disease' | 'pest'>('disease');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [cropHint, setCropHint] = useState<string>('');
  const [samples, setSamples] = useState<SampleImageInfo[]>(DEFAULT_SAMPLES);
  const [pestSamples, setPestSamples] = useState<SampleImageInfo[]>(DEFAULT_PEST_SAMPLES);
  const [activeSample, setActiveSample] = useState<SampleImageInfo | null>(null);
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [result, setResult] = useState<CropAnalysisResult | null>(null);
  const [pestResult, setPestResult] = useState<PestDetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    getSampleImages()
      .then((data) => {
        if (data && data.length > 0) setSamples(data);
      })
      .catch(() => {});

    getPestSampleImages()
      .then((data) => {
        if (data && data.length > 0) setPestSamples(data);
      })
      .catch(() => {});
  }, []);

  // Automatically re-localize active diagnosis/pest result when the farmer switches language
  useEffect(() => {
    if (result) {
      reLocalizeCropResult(result, language)
        .then((updated) => setResult(updated))
        .catch(() => {});
    }
    if (pestResult) {
      reLocalizePestResult(pestResult, language)
        .then((updated) => setPestResult(updated))
        .catch(() => {});
    }
  }, [language]);

  useEffect(() => {
    return () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const handleSpeakDiagnosis = () => {
    if (!result && !pestResult) return;
    if (!('speechSynthesis' in window)) {
      alert('Voice playback is not supported in this browser.');
      return;
    }
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const langConfig = SUPPORTED_LANGUAGES.find((l) => l.code === language);
    const bcp47 = langConfig ? langConfig.bcp47 : 'en-IN';

    const parts: string[] = [];
    if (scanMode === 'pest' && pestResult) {
      if (pestResult.total_detected === 0) {
        parts.push('No agricultural pests detected in this image.');
      } else {
        parts.push(`Detected ${pestResult.total_detected} pest.`);
        pestResult.detections.forEach((d) => {
          parts.push(`${d.pest_name}. Severity: ${d.severity}. Action threshold: ${d.action_threshold}. Organic remedy: ${d.organic_remedy}. Chemical remedy: ${d.chemical_remedy}.`);
        });
      }
    } else if (result) {
      parts.push(`${result.crop_name}. ${result.detected_condition}.`);
      if (result.severity) {
        parts.push(`Severity: ${result.severity}.`);
      }
      if (result.summary) {
        parts.push(result.summary);
      }
      if (result.recommended_action && result.recommended_action.length > 0) {
        parts.push(`Recommended actions: ${result.recommended_action.join('. ')}`);
      }
    }
    const fullText = parts.join(' ');

    const utterance = new SpeechSynthesisUtterance(fullText);
    utterance.lang = bcp47;
    utterance.rate = 0.95;
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
    setIsSpeaking(true);
  };

  useEffect(() => {
    let isMounted = true;
    getSampleImages()
      .then((data) => {
        if (isMounted && Array.isArray(data) && data.length > 0) {
          setSamples(data);
        }
      })
      .catch(() => {});
    return () => {
      isMounted = false;
    };
  }, []);

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file (.jpg, .jpeg, .png).');
      return;
    }
    setError(null);
    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    setResult(null);
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select or capture a plant photo first.');
      return;
    }
    setAnalyzing(true);
    setError(null);
    setActiveSample(null);
    try {
      const res = await analyzeImage(selectedFile, cropHint || undefined, language);
      setResult(res);
    } catch (err: any) {
      setError(err?.message || 'Error communicating with offline station. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleAnalyzePest = async () => {
    if (!selectedFile) {
      setError('Please select or capture an insect or pest photo first.');
      return;
    }
    setAnalyzing(true);
    setError(null);
    setActiveSample(null);
    try {
      const res = await detectPests(selectedFile, language);
      setPestResult(res);
    } catch (err: any) {
      setError(err?.message || 'Error detecting pests. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const formatSampleUrl = (url: string) => (url.startsWith('http') ? url : `${API_BASE}${url}`);

  const handleSelectSample = async (sample: SampleImageInfo) => {
    setAnalyzing(true);
    setError(null);
    setPreviewUrl(formatSampleUrl(sample.url));
    setSelectedFile(null);
    setActiveSample(sample);
    setCropHint(sample.crop);
    try {
      const res = await analyzeSampleImage(sample.filename, language);
      setResult(res);
    } catch (err: any) {
      setError(err?.message || 'Error analyzing sample. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSelectPestSample = async (sample: SampleImageInfo) => {
    setAnalyzing(true);
    setError(null);
    setPreviewUrl(formatSampleUrl(sample.url));
    setSelectedFile(null);
    setActiveSample(sample);
    try {
      const res = await analyzePestSampleImage(sample.filename, language);
      setPestResult(res);
    } catch (err: any) {
      setError(err?.message || 'Error analyzing pest sample. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleReset = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setPestResult(null);
    setError(null);
    setCropHint('');
    setActiveSample(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (cameraInputRef.current) cameraInputRef.current.value = '';
  };

  const getCropSvgIcon = (name: string) => {
    const lower = name.toLowerCase();
    if (lower.includes('tomato')) return <img src={tomatoSvg} alt="Tomato" className="crop-svg-icon" />;
    if (lower.includes('potato')) return <img src={potatoSvg} alt="Potato" className="crop-svg-icon" />;
    if (lower.includes('corn') || lower.includes('maize')) return <img src={cornSvg} alt="Corn" className="crop-svg-icon" />;
    if (lower.includes('wheat')) return <img src={wheatSvg} alt="Wheat" className="crop-svg-icon" />;
    if (lower.includes('rice') || lower.includes('paddy')) return <img src={riceSvg} alt="Rice" className="crop-svg-icon" />;
    if (lower.includes('sunflower')) return <img src={sunflowerSvg} alt="Sunflower" className="crop-svg-icon" />;
    if (lower.includes('cotton')) return <img src={cottonSvg} alt="Cotton" className="crop-svg-icon" />;
    if (lower.includes('apple')) return <img src={appleSvg} alt="Apple" className="crop-svg-icon" />;
    if (lower.includes('chilli')) return <img src={chilliSvg} alt="Chilli" className="crop-svg-icon" />;
    return <FaLeaf className="crop-badge-icon" aria-hidden="true" />;
  };

  const renderGradeBadge = (gradeStr: string) => {
    if (gradeStr.includes('Grade A')) {
      return (
        <span className="grade-badge grade-badge--a" title="Prime healthy crop condition">
          <FiCheckCircle className="grade-icon" aria-hidden="true" />
          <span className="grade-text">{gradeStr}</span>
        </span>
      );
    }
    if (gradeStr.includes('Grade B')) {
      return (
        <span className="grade-badge grade-badge--b" title="Early attention required">
          <FiAlertTriangle className="grade-icon" aria-hidden="true" />
          <span className="grade-text">{gradeStr}</span>
        </span>
      );
    }
    return (
      <span className="grade-badge grade-badge--c" title="Crop health alert">
        <FiXCircle className="grade-icon" aria-hidden="true" />
        <span className="grade-text">{gradeStr}</span>
      </span>
    );
  };

  return (
    <section className="crop-doctor-section" aria-labelledby="crop-scanner-heading">
      {/* Hero Banner with Custom Farmer Illustration */}
      <div className="hero-banner-card">
        <img src={heroBanner} alt="Indian agricultural field" className="hero-banner-img" />
        <div className="hero-banner-overlay">
          <span className="hero-badge">Arm Bharat AI-SoC Reference Architecture</span>
          <h2 className="hero-title">{scanMode === 'pest' ? t('pestHeading') : t('scannerHeading')}</h2>
          <p className="hero-desc">{scanMode === 'pest' ? t('pestDesc') : t('scannerDesc')}</p>
        </div>
      </div>

      {/* Scanner Mode Switcher: Crop Disease vs Field Pest Detection */}
      <div className="mode-toggle-bar" style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
        <button
          type="button"
          className={`btn ${scanMode === 'disease' ? 'btn-accent' : 'btn-secondary'}`}
          style={{ flex: 1, padding: '12px 18px', fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
          onClick={() => { setScanMode('disease'); handleReset(); }}
        >
          <FaLeaf className="btn-icon" aria-hidden="true" />
          <span>{t('modeDiseaseScanner')}</span>
        </button>
        <button
          type="button"
          className={`btn ${scanMode === 'pest' ? 'btn-accent' : 'btn-secondary'}`}
          style={{ flex: 1, padding: '12px 18px', fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
          onClick={() => { setScanMode('pest'); handleReset(); }}
        >
          <FiAlertTriangle className="btn-icon" aria-hidden="true" />
          <span>{t('modePestScanner')}</span>
        </button>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="alert-banner alert-banner--error" role="alert" style={{ marginBottom: '20px' }}>
          <FiAlertCircle className="alert-icon" aria-hidden="true" />
          <span className="alert-message">{error}</span>
        </div>
      )}

      <div className="scanner-layout">
        {/* Left Column: Image Input & Crop Select */}
        <div className="scanner-input-card glass-card">
          {scanMode === 'disease' ? (
            <>
              <div className="crop-hint-row">
                <label htmlFor="crop-select" className="input-label">
                  {t('cropTypeLabel')}
                </label>
                <select
                  id="crop-select"
                  className="select-input"
                  value={cropHint}
                  onChange={(e) => setCropHint(e.target.value)}
                  disabled={analyzing}
                >
                  <option value="">{t('autoDetectCrop')}</option>
                  <option value="Tomato">Tomato</option>
                  <option value="Potato">Potato</option>
                  <option value="Sunflower">Sunflower</option>
                  <option value="Corn">Corn / Maize</option>
                  <option value="Rice">Rice / Paddy</option>
                  <option value="Wheat">Wheat</option>
                  <option value="Apple">Apple</option>
                  <option value="Chilli">Chilli</option>
                  <option value="Cotton">Cotton</option>
                </select>
              </div>

              {/* Handcrafted Crop Vector SVG Quick Selector Tiles */}
              <div>
                <span className="input-label" style={{ fontSize: '13px' }}>{t('quickSelectCrop')}</span>
                <div className="crop-svg-grid">
                  {CROP_SVG_LIST.map((c) => (
                    <button
                      key={c.id}
                      type="button"
                      className={`crop-svg-tile ${cropHint === c.id ? 'crop-svg-tile--active' : ''}`}
                      onClick={() => setCropHint(cropHint === c.id ? '' : c.id)}
                      title={`Select ${c.name}`}
                    >
                      <img src={c.svg} alt={c.name} className="crop-svg-icon" />
                      <span className="crop-svg-label">{c.name.split(' ')[0]}</span>
                    </button>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div style={{ padding: '14px', background: 'rgba(217, 119, 6, 0.12)', border: '1px solid rgba(217, 119, 6, 0.3)', borderRadius: '8px', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                <FiAlertTriangle style={{ color: 'var(--color-gold-bright)', fontSize: '18px' }} />
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-gold-bright)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                  {t('pestNoticeTitle')}
                </span>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--color-slate-300)', margin: 0, lineHeight: 1.5 }}>
                {t('pestNoticeDesc')}
              </p>
            </div>
          )}

          {/* Upload / Camera Drop Zone */}
          <div
            className={`drop-zone ${isDragging ? 'drop-zone--active' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            {previewUrl ? (
              <div className="preview-container">
                <img src={previewUrl} alt="Crop sample for diagnosis" className="preview-image" />
              </div>
            ) : (
              <div className="drop-zone-placeholder">
                <FiImage className="placeholder-icon" aria-hidden="true" />
                <p className="placeholder-primary">{t('dragDropText')}</p>
                <p className="placeholder-secondary">{t('orUseButtons')}</p>
              </div>
            )}
          </div>

          {/* Hidden File Inputs */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="visually-hidden"
            onChange={handleFileChange}
            aria-label="Upload crop image from file"
          />
          <input
            ref={cameraInputRef}
            type="file"
            accept="image/*"
            capture="environment"
            className="visually-hidden"
            onChange={handleFileChange}
            aria-label="Capture crop image with camera"
          />

          {/* Action Buttons */}
          <div className="button-group-row">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => fileInputRef.current?.click()}
              disabled={analyzing}
            >
              <FiUpload className="btn-icon" aria-hidden="true" />
              <span>{t('uploadPhoto')}</span>
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => cameraInputRef.current?.click()}
              disabled={analyzing}
            >
              <FiCamera className="btn-icon" aria-hidden="true" />
              <span>{t('takePhoto')}</span>
            </button>
            {previewUrl && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handleReset}
                disabled={analyzing}
              >
                <FiRefreshCw className="btn-icon" aria-hidden="true" />
                <span>{t('reset')}</span>
              </button>
            )}
          </div>

          {selectedFile && !result && !pestResult && (
            <div style={{ marginTop: '10px' }}>
              <button
                type="button"
                className="btn btn-accent btn-large btn-full"
                onClick={scanMode === 'pest' ? handleAnalyzePest : handleAnalyze}
                disabled={analyzing}
              >
                {analyzing ? (
                  <>
                    <FiLoader className="btn-icon spin" aria-hidden="true" />
                    <span>{t('analyzingText')}</span>
                  </>
                ) : (
                  <>
                    {scanMode === 'pest' ? (
                      <FiAlertTriangle className="btn-icon" aria-hidden="true" />
                    ) : (
                      <FaLeaf className="btn-icon" aria-hidden="true" />
                    )}
                    <span>{scanMode === 'pest' ? t('analyzePestButton') : t('analyzeButton')}</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Right Column: Diagnosis Result or Sample Library */}
        <div className="scanner-result-column">
          {analyzing && (
            <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
              <FiLoader className="spin" style={{ fontSize: '40px', color: 'var(--color-gold-bright)', margin: '0 auto 16px' }} />
              <h3 style={{ fontSize: '20px', fontWeight: 700, color: '#FFFFFF' }}>{scanMode === 'pest' ? t('analyzingPestText') : t('analyzingText')}</h3>
              <p style={{ color: 'var(--color-slate-300)', marginTop: '8px', fontSize: '14px' }}>
                {scanMode === 'pest' ? t('analyzingPestText') : t('analyzingDiseaseSubtitle')}
              </p>
            </div>
          )}

          {/* Two-Stage Non-Crop Rejection Display */}
          {result && !analyzing && (result.is_crop === false || result.crop_name === 'Not a Crop or Plant') && (
            <div className="result-card" tabIndex={0} aria-label="Not a Crop Image" style={{ borderColor: 'var(--color-danger)' }}>
              <div className="result-card-header">
                <div className="crop-title-group">
                  <span className="crop-icon-badge" aria-hidden="true" style={{ borderColor: 'var(--color-danger)' }}>
                    <FiXCircle style={{ color: 'var(--color-danger)', fontSize: '28px' }} />
                  </span>
                  <div>
                    <span className="crop-label-tag" style={{ color: 'var(--color-danger)' }}>
                      {t('photoVerificationNotice')}
                    </span>
                    <h3 className="condition-title">{t('notACropTitle')}</h3>
                  </div>
                </div>
              </div>

              <div className="summary-block">
                <h4 className="block-subheading">{t('conditionSummary')}</h4>
                <p className="summary-text">{result.summary}</p>
              </div>

              {result.recommended_action && result.recommended_action.length > 0 && (
                <div className="actions-block">
                  <h4 className="block-subheading">{t('recommendedActions')}</h4>
                  <ul className="action-list">
                    {result.recommended_action.map((action, idx) => (
                      <li key={idx} className="action-item">
                        <FiCheckSquare className="action-item-icon" aria-hidden="true" />
                        <span className="action-item-text">{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{ marginTop: '14px' }}>
                <button
                  type="button"
                  className="btn btn-accent btn-large btn-full"
                  onClick={handleReset}
                >
                  <FiRefreshCw className="btn-icon" aria-hidden="true" />
                  <span>{t('tryAnotherPhoto')}</span>
                </button>
              </div>
            </div>
          )}

          {/* Plant Health Diagnostic Result */}
          {result && !analyzing && result.is_crop !== false && result.crop_name !== 'Not a Crop or Plant' && (
            <div className="result-card" tabIndex={0} aria-label="Diagnosis Findings">
              <div className="result-card-header">
                <div className="crop-title-group">
                  <span className="crop-icon-badge" aria-hidden="true">
                    {getCropSvgIcon(result.crop_name)}
                  </span>
                  <div>
                    <span className="crop-label-tag">{result.crop_name}</span>
                    <h3 className="condition-title">{result.detected_condition}</h3>
                  </div>
                </div>
                {renderGradeBadge(result.quality_grade)}
              </div>

              {/* Health Score & Confidence Bar */}
              <div className="score-panel">
                <div className="score-header-row">
                  <span className="score-title">{t('healthScore')}</span>
                  <span className="score-value-text">{result.quality_score} / 100</span>
                </div>
                <div
                  className="score-bar-track"
                  role="progressbar"
                  aria-valuenow={result.quality_score}
                  aria-valuemin={0}
                  aria-valuemax={100}
                >
                  <div
                    className={`score-bar-fill score-bar-fill--${
                      result.quality_score >= 80 ? 'good' : result.quality_score >= 50 ? 'warning' : 'danger'
                    }`}
                    style={{ width: `${Math.max(5, Math.min(100, result.quality_score))}%` }}
                  />
                </div>
                <div className="score-meta-row" style={{ display: 'flex', gap: '14px', alignItems: 'center', flexWrap: 'wrap', marginTop: '10px' }}>
                  <span className="severity-indicator" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'rgba(239, 68, 68, 0.12)', border: '1px solid rgba(239, 68, 68, 0.35)', borderRadius: '6px', padding: '4px 10px', fontSize: '13px' }}>
                    {t('severity')}: <strong style={{ color: '#FCD34D' }}>{result.severity}</strong>
                  </span>
                  <span className="confidence-indicator" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'rgba(59, 130, 246, 0.12)', border: '1px solid rgba(59, 130, 246, 0.35)', borderRadius: '6px', padding: '4px 10px', fontSize: '13px' }}>
                    {t('diagnosticAccuracy')}: <strong style={{ color: '#93C5FD' }}>{Math.round(result.confidence * 100)}%</strong>
                  </span>
                </div>
              </div>

              {/* Plain-Language Summary */}
              <div className="summary-block">
                <h4 className="block-subheading">{t('conditionSummary')}</h4>
                <p className="summary-text">{result.summary}</p>
              </div>

              {/* Recommended Actions */}
              {result.recommended_action && result.recommended_action.length > 0 && (
                <div className="actions-block">
                  <h4 className="block-subheading">{t('recommendedActions')}</h4>
                  <ul className="action-list">
                    {result.recommended_action.map((action, idx) => (
                      <li key={idx} className="action-item">
                        <FiCheckSquare className="action-item-icon" aria-hidden="true" />
                        <span className="action-item-text">{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Action Buttons: Listen to Diagnosis & Consult Advisor */}
              <div style={{ display: 'flex', gap: '10px', marginTop: '14px', flexWrap: 'wrap' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  style={{ flex: '1', minWidth: '160px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
                  onClick={handleSpeakDiagnosis}
                  title="Listen to diagnosis readout in your selected language"
                >
                  {isSpeaking ? (
                    <>
                      <FiVolumeX className="btn-icon" aria-hidden="true" style={{ color: 'var(--color-danger)' }} />
                      <span>{t('stopSpeaking')}</span>
                    </>
                  ) : (
                    <>
                      <FiVolume2 className="btn-icon" aria-hidden="true" style={{ color: 'var(--color-gold-bright)' }} />
                      <span>{t('speakAdvice')}</span>
                    </>
                  )}
                </button>
                <button
                  type="button"
                  className="btn btn-accent btn-large"
                  style={{ flex: '1.5', minWidth: '180px' }}
                  onClick={() =>
                    onConsultAdvisor(
                      result.crop_name,
                      result.detected_condition,
                      `${result.crop_name} showing ${result.detected_condition} with severity ${result.severity}.`
                    )
                  }
                >
                  <FiMessageSquare className="btn-icon" aria-hidden="true" />
                  <span>{t('consultAdvisor')}</span>
                </button>
              </div>
            </div>
          )}

          {/* Pest Detection Findings Card (YOLO IP102 97-Class) */}
          {scanMode === 'pest' && pestResult && !analyzing && (
            <div className="result-card" tabIndex={0} aria-label="Pest Findings">
              <div className="result-card-header">
                <div className="crop-title-group">
                  <span className="crop-icon-badge" aria-hidden="true" style={{ borderColor: 'var(--color-gold-bright)' }}>
                    <FiAlertTriangle style={{ color: 'var(--color-gold-bright)', fontSize: '24px' }} />
                  </span>
                  <div>
                    <span className="crop-label-tag">{t('pestDetectedTitle')}</span>
                    <h3 className="condition-title">
                      {pestResult.total_detected > 0
                        ? `${pestResult.total_detected} ${t('totalPestsDetected')}`
                        : t('noPestsFound')}
                    </h3>
                  </div>
                </div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className="badge badge-accent" title="Inference model">
                    YOLO IP102
                  </span>
                  <span className="badge badge-subtle" title="On-device latency">
                    {pestResult.latency_ms} ms
                  </span>
                </div>
              </div>

              {pestResult.total_detected === 0 ? (
                <div className="summary-block">
                  <p className="summary-text">
                    {t('noPestsFoundDesc')}
                  </p>
                </div>
              ) : (
                pestResult.detections.map((det, idx) => (
                  <div key={idx} style={{ marginTop: idx > 0 ? '16px' : '0', padding: '14px', background: 'rgba(15, 23, 42, 0.4)', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <h4 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--color-gold-bright)', textTransform: 'capitalize', margin: 0 }}>
                        {det.pest_name}
                      </h4>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <span className={`severity-tag severity-tag--${det.severity.toLowerCase()}`}>
                          {t('severity')}: {det.severity}
                        </span>
                        <span className="confidence-indicator">
                          {t('confidence')}: <strong>{det.confidence_pct}%</strong>
                        </span>
                      </div>
                    </div>

                    <div className="summary-block" style={{ marginTop: '8px' }}>
                      <h5 className="block-subheading">{t('actionThreshold')}</h5>
                      <p className="summary-text" style={{ color: '#FCD34D' }}>{det.action_threshold}</p>
                    </div>

                    <div className="summary-block" style={{ marginTop: '8px' }}>
                      <h5 className="block-subheading">{t('organicRemedy')}</h5>
                      <p className="summary-text">{det.organic_remedy}</p>
                    </div>

                    <div className="summary-block" style={{ marginTop: '8px' }}>
                      <h5 className="block-subheading">{t('chemicalRemedy')}</h5>
                      <p className="summary-text">{det.chemical_remedy}</p>
                    </div>

                    <div className="summary-block" style={{ marginTop: '8px' }}>
                      <h5 className="block-subheading">{t('culturalPractice')}</h5>
                      <p className="summary-text">{det.cultural_practice}</p>
                    </div>
                  </div>
                ))
              )}

              {/* Actions: Listen & Consult */}
              <div style={{ display: 'flex', gap: '10px', marginTop: '16px', flexWrap: 'wrap' }}>
                <button
                  type="button"
                  className="btn btn-secondary"
                  style={{ flex: '1', minWidth: '160px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
                  onClick={handleSpeakDiagnosis}
                  title="Listen to advisory readout in your language"
                >
                  {isSpeaking ? (
                    <>
                      <FiVolumeX className="btn-icon" aria-hidden="true" style={{ color: 'var(--color-danger)' }} />
                      <span>{t('stopSpeaking')}</span>
                    </>
                  ) : (
                    <>
                      <FiVolume2 className="btn-icon" aria-hidden="true" style={{ color: 'var(--color-gold-bright)' }} />
                      <span>{t('speakAdvice')}</span>
                    </>
                  )}
                </button>

                {pestResult.total_detected > 0 && (
                  <button
                    type="button"
                    className="btn btn-accent btn-large"
                    style={{ flex: '1.5', minWidth: '180px' }}
                    onClick={() => {
                      const first = pestResult.detections[0];
                      onConsultAdvisor(
                        first.pest_name,
                        'Pest Infestation',
                        `Field pest detected: ${first.pest_name} with severity ${first.severity}. Action threshold: ${first.action_threshold}.`
                      );
                    }}
                  >
                    <FiMessageSquare className="btn-icon" aria-hidden="true" />
                    <span>{t('consultAdvisor')}</span>
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Curated Sample Images Gallery */}
          {!result && !pestResult && !analyzing && (
            <div className="samples-section">
              <h3 className="samples-heading">
                {scanMode === 'pest' ? t('pestSampleGalleryTitle') : t('curatedSamplesTitle')}
              </h3>
              <div className="samples-grid">
                {(scanMode === 'pest' ? pestSamples : samples).map((sample) => (
                  <button
                    key={sample.id}
                    type="button"
                    className={`sample-card ${activeSample?.id === sample.id ? 'sample-card--active' : ''}`}
                    onClick={() => (scanMode === 'pest' ? handleSelectPestSample(sample) : handleSelectSample(sample))}
                  >
                    <div className="sample-thumb-wrapper">
                      <img src={formatSampleUrl(sample.url)} alt={sample.name} className="sample-thumb" />
                    </div>
                    <div className="sample-meta">
                      <span className="sample-crop-name">{sample.crop}</span>
                      <p className="sample-condition-name">{sample.condition}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

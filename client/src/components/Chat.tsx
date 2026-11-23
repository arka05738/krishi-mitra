/**
 * Chat Component for Krishi Mitra Agricultural Advisory System.
 * Theme: White, Dark Blue, and Royal Gold.
 * Conversational agricultural advisory grounded in ICAR guidelines.
 * Supports 22 Scheduled Indian Languages + English and Integrated Voice Assistant.
 * Zero Unicode emojis, strictly uses react-icons. Zero technical jargon.
 */
import { useState, useEffect, useRef } from 'react';
import type { FormEvent, KeyboardEvent } from 'react';
import {
  FiSend,
  FiUser,
  FiBookOpen,
  FiLoader,
  FiMic,
  FiMicOff,
  FiVolume2,
  FiVolumeX,
} from 'react-icons/fi';
import { FaLeaf } from 'react-icons/fa6';
import type { ChatMessage } from '../types/index.ts';
import { sendChatMessage, transcribeAudio, reLocalizeChatMessages } from '../services/api.ts';
import type { LanguageCode } from '../i18n/translations.ts';
import { getTranslation, getLanguageOption } from '../i18n/translations.ts';

interface ChatProps {
  initialCropContext?: string;
  initialConditionContext?: string;
  language?: LanguageCode;
}

const QUICK_TOPICS_BY_LANG: Record<string, string[]> = {
  en: [
    'Tomato Early Blight spray dose',
    'Yellow stem borer in paddy',
    'Sunflower seed harvest timing',
    'PM-KISAN status & e-KYC',
    'Hailstorm PMFBY claim 72h rule',
    'Can I mix Zinc Sulphate with DAP?',
  ],
  hi: [
    'टमाटर के अगेती झुलसा का उपचार',
    'धान में तना छेदक कीट की रोकथाम',
    'सूरजमुखी बीज कटाई का सही समय',
    'पीएम-किसान ई-केवाईसी प्रक्रिया',
    'ओलावृष्टि पर फसल बीमा का 72 घंटे का नियम',
    'क्या जिंक सल्फेट को डीएपी के साथ मिला सकते हैं?',
  ],
  bn: [
    'টমেটোর আর্লি ব্লাইট স্প্রে মাত্রা',
    'ধানে মাজরা পোকা দমন ব্যবস্থা',
    'সূর্যমুখী বীজ কাটার সঠিক সময়',
    'প্রধানমন্ত্রী কিষাণ ই-কেওয়াইসি নিয়ম',
    'শিলাবৃষ্টিতে ফসল বীমা দাবির নিয়ম',
    'জিঙ্ক সালফেট কি ডিএপির সাথে মেশানো যায়?',
  ],
  te: [
    'టమాటా ముందస్తు తెగులు నివారణ',
    'వరిలో కాండం తొలిచే పురుగు నివారణ',
    'పొద్దుతిరుగుడు కోత సమయం',
    'పీఎం-కిసాన్ ఈ-కేవైసీ వివరాలు',
    'వడగండ్ల పంట నష్టపరిహారం 72 గంటల నియమం',
    'జింక్ సల్ఫేట్ మరియు డీఏపీ కలపవచ్చా?',
  ],
  ta: [
    'தக்காளி இலை கருகல் நோய் தடுப்பு',
    'நெல் தண்டு துளைப்பான் கட்டுப்பாடு',
    'சூரியகாந்தி அறுவடை காலம்',
    'பிஎம்-கிசான் இ-கேஒய்சி முறை',
    'பயிர் காப்பீடு 72 மணி நேர விதி',
    'ஜிங்க் சல்பேட்டை டிஏபியுடன் கலக்கலாமா?',
  ],
  mr: [
    'टोमॅटोवरील करपा रोगाचे नियंत्रण',
    'भातातील खोडकिडीचा बंदोबस्त',
    'सूर्यफूल काढणीची योग्य वेळ',
    'पीएम-किसान ई-केवायसी प्रक्रिया',
    'गारपीट पीक विमा ७२ तास नियम',
    'झिंक सल्फेट डीएपीमध्ये मिसळावे का?',
  ],
  gu: [
    'ટમેટામાં સુકારો રોગ નિયંત્રણ',
    'ડાંગરમાં ગાભમારાની ઇયળ નિયંત્રણ',
    'સૂર્યમુખી લણણીનો યોગ્ય સમય',
    'પીએમ-કિસાન ઇ-કેવાયસી',
    'પાક વીમા ક્લેઇમ ૭૨ કલાક નિયમ',
    'શું ઝિંક સલ્ફેટ ડીએપી સાથે મિશ્ર કરી શકાય?',
  ],
  kn: [
    'ಟೊಮೆಟೊ ಬೆಳೆ ರೋಗ ನಿವಾರಣೆ',
    'ಭತ್ತದ ಬೆಳೆ ಕೀಟ ನಿರ್ವಹಣೆ',
    'ಸೂರ್ಯಕಾಂತಿ ಕಟಾವಿನ ಸಮಯ',
    'ಪಿಎಂ-ಕಿಸಾನ್ ಇ-ಕೆವೈಸಿ',
    'ಬೆಳೆ ವಿಮೆ 72 ಗಂಟೆಗಳ ನಿಯಮ',
  ],
  ml: [
    'തക്കാളിയിലെ രോഗ നിയന്ത്രണം',
    'നെല്ലിലെ തണ്ടുതുരപ്പൻ പുഴു',
    'സൂര്യകാന്തി വിളവെടുപ്പ് സമയം',
    'പിഎം-കിസാൻ ഇ-കെവൈസി',
  ],
  pa: [
    'ਟਮਾਟਰ ਦੇ ਝੁਲਸਾ ਰੋਗ ਦਾ ਇਲਾਜ',
    'ਝੋਨੇ ਵਿੱਚ ਤਣਾ ਛੇਦਕ ਕੀੜੇ ਦੀ ਰੋਕਥਾਮ',
    'ਸੂਰਜਮੁਖੀ ਬੀਜ ਕਟਾਈ ਦਾ ਸਮਾਂ',
    'ਪੀਐਮ-ਕਿਸਾਨ ਈ-ਕੇਵਾਈਸੀ',
    'ਗੜੇਮਾਰੀ ਤੇ ਫਸਲ ਬੀਮਾ ਨਿਯਮ',
  ],
  or: [
    'ଟମାଟୋ ରୋଗ ନିୟନ୍ତ୍ରଣ ଉପାୟ',
    'ଧାନରେ କାଣ୍ଡବିନ୍ଧା ପୋକ ଦମନ',
    'ସୂର୍ଯ୍ୟମୁଖୀ ଅମଳ ସମୟ',
    'ପିଏମ-କିଷାନ ଇ-କେୱାଇସି',
  ],
};

export function Chat({
  initialCropContext,
  initialConditionContext,
  language = 'en',
}: ChatProps) {
  const t = (key: string) => getTranslation(language, key);
  const langOpt = getLanguageOption(language);

  const getInitialGreeting = (lang: LanguageCode): string => {
    switch (lang) {
      case 'hi':
        return 'नमस्ते किसान भाई। मैं आपका कृषि मित्र सलाहकार हूँ। अपनी भाषा में बोलकर या लिखकर फसल रोग, खाद या योजनाओं के बारे में पूछें।';
      case 'bn':
        return 'নমস্কার কৃষক ভাই। আমি আপনার কৃষি মিত্র উপদেষ্টা। মুখে বলে বা লিখে ফসলের রোগ, সার বা সরকারি প্রকল্প সম্পর্কে প্রশ্ন করুন।';
      case 'te':
        return 'నమస్కారం రైతు సోదరా. నేను మీ కృషి మిత్ర సలహాదారుని. మాట్లాడి లేదా టైప్ చేసి మీ వ్యవసాయ ప్రశ్నలను అడగండి.';
      case 'ta':
        return 'வணக்கம் விவசாய தோழரே. நான் உங்கள் கிருஷி மித்ரா ஆலோசகர். குரல் வழியாகவோ அல்லது தட்டச்சு செய்தோ விவசாய கேள்விகளைக் கேளுங்கள்.';
      case 'mr':
        return 'नमस्कार शेतकरी बांधवांनो. मी आपला कृषी मित्र सल्लागार आहे. बोलून किंवा लिहून शेतीविषयक कोणतेही प्रश्न विचारा.';
      case 'gu':
        return 'નમસ્તે ખેડૂત મિત્ર. હું તમારો કૃષિ મિત્ર સલાહકાર છું. બોલીને કે લખીને ખેતીના પ્રશ્નો પૂછો.';
      case 'pa':
        return 'ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਕਿਸਾਨ ਵੀਰੋ। ਮੈਂ ਤੁਹਾਡਾ ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਸਲਾਹਕਾਰ ਹਾਂ। ਬੋਲ ਕੇ ਜਾਂ ਲਿਖ ਕੇ ਖੇਤੀਬਾੜੀ ਬਾਰੇ ਕੋਈ ਵੀ ਸਵਾਲ ਪੁੱਛੋ।';
      case 'kn':
        return 'ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ. ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಮಿತ್ರ ಸಲಹೆಗಾರ. ಧ್ವನಿಯ ಮೂಲಕ ಅಥವಾ ಬರೆದು ಕೃಷಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ.';
      case 'ml':
        return 'നമസ്കാരം കർഷക സുഹൃത്തേ. ഞാൻ നിങ്ങളുടെ കൃഷി മിത്ര ഉപദേശകനാണ്. സംസാരിച്ചോ എഴുതിയോ കൃഷി ചോദ്യങ്ങൾ ചോദിക്കാം.';
      case 'or':
        return 'ନମସ୍କାର ଚାଷୀ ଭାଇ। ମୁଁ ଆପଣଙ୍କ କୃଷି ମିତ୍ର ପରାମର୍ଶଦାତା। କହି କିମ୍ବା ଲେଖି ଚାଷ ସମ୍ପର୍କିତ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ।';
      case 'as':
        return 'নমস্কাৰ কৃষক ভাই। মই আপোনাৰ কৃষি মিত্ৰ সহায়ক। কথা কৈ বা লিখি খেতিৰ বিষয়ে সুধিব পাৰে।';
      case 'ur':
        return 'آداب کسان بھائی۔ میں آپ کا زرعی مشیر ہوں۔ بول کر یا لکھ کر زراعت اور فصلوں کے بارے میں سوال پوچھیں۔';
      default:
        return 'Namaste Kisan Bhai. I am your Krishi Mitra Advisory Assistant. Tap the microphone to speak your question, or type below.';
    }
  };

  const getConsultQuestion = (crop: string, condition: string, lang: LanguageCode): string => {
    switch (lang) {
      case 'bn':
        return `${crop}-এ ${condition} কীভাবে চিকিৎসা ও প্রতিকার করবেন?`;
      case 'hi':
        return `${crop} में ${condition} का उपचार एवं रोकथाम कैसे करें?`;
      case 'te':
        return `${crop} లో ${condition} నివారణ మరియు చిকিత్స ఎలా చేయాలి?`;
      case 'ta':
        return `${crop} பயிரில் ${condition} எவ்வாறு கட்டுப்படுத்துவது?`;
      case 'mr':
        return `${crop} मध्ये ${condition} चा उपचार कसा करावा?`;
      case 'gu':
        return `${crop} માં ${condition} નો ઉપચાર કેવી રીતે કરવો?`;
      case 'pa':
        return `${crop} ਵਿੱਚ ${condition} ਦਾ ਇਲਾਜ ਕਿਵੇਂ ਕਰੀਏ?`;
      case 'kn':
        return `${crop} ನಲ್ಲಿ ${condition} ಚಿಕಿತ್ಸೆ ಹೇಗೆ ಮಾಡುವುದು?`;
      case 'ml':
        return `${crop} വിളയിൽ ${condition} എങ്ങനെ നിയന്ത്രിക്കാം?`;
      case 'or':
        return `${crop} ରେ ${condition} ର ଚିକିତ୍ସା କିପରି କରିବେ?`;
      case 'as':
        return `${crop}ত ${condition}ৰ চিকিৎসা কেনেকৈ কৰিব?`;
      case 'ur':
        return `${crop} میں ${condition} کا علاج کیسے کریں؟`;
      default:
        return `How to treat and control ${condition} in ${crop}?`;
    }
  };

  const [messages, setMessages] = useState<ChatMessage[]>(() => [
    {
      role: 'assistant',
      content: getInitialGreeting(language),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sources: ['ICAR Package of Practices'],
      helpline: 'Kisan Call Centre: 1800-180-1551',
    },
  ]);

  const [inputText, setInputText] = useState<string>(() => {
    if (initialCropContext && initialConditionContext) {
      return getConsultQuestion(initialCropContext, initialConditionContext, language);
    }
    return '';
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [, setError] = useState<string | null>(null);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [speakingIndex, setSpeakingIndex] = useState<number | null>(null);

  const lastSubmitRef = useRef<number>(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Dynamically re-localize entire conversation and greeting when farmer switches language
  useEffect(() => {
    if (messages.length === 1 && messages[0].role === 'assistant') {
      setMessages([{
        ...messages[0],
        content: getInitialGreeting(language),
        sources: language === 'bn'
          ? ['ভারতীয় কৃষি গবেষণা পরিষদ নির্দেশিকা']
          : language === 'hi'
          ? ['भारतीय कृषि अनुसंधान परिषद संदर्शिका']
          : ['ICAR Package of Practices'],
        helpline: language === 'bn'
          ? 'টোল-ফ্রি কিষাণ কল সেন্টার: ১৮০০-১৮০-১৫৫১ (২৪x৭)'
          : language === 'hi'
          ? 'टोल-फ्री किसान कॉल सेंटर: 1800-180-1551 (24x7)'
          : 'Toll-Free Kisan Call Centre: 1800-180-1551 (24x7)',
      }]);
    } else if (messages.length > 1) {
      reLocalizeChatMessages(messages, language)
        .then((updated) => {
          if (updated && updated.length > 0) {
            setMessages(updated);
          }
        })
        .catch(() => {});
    }

    if (initialCropContext && initialConditionContext) {
      setInputText(getConsultQuestion(initialCropContext, initialConditionContext, language));
    }
  }, [language]);

  // Clean up any ongoing TTS on unmount or language switch
  useEffect(() => {
    return () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, [language]);

  // 1. Text-To-Speech (Voice Output)
  const handleToggleSpeak = (text: string, index: number) => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported on this browser.');
      return;
    }

    if (speakingIndex === index) {
      window.speechSynthesis.cancel();
      setSpeakingIndex(null);
      return;
    }

    window.speechSynthesis.cancel();

    // Clean markdown symbols for natural reading
    const cleanSpeech = text
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/\*([^*]+)\*/g, '$1')
      .replace(/[#\*\-•]+/g, '')
      .replace(/@/g, ' at ')
      .replace(/\\%/g, ' percent')
      .replace(/%/g, ' percent')
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.lang = langOpt.bcp47;
    utterance.rate = 0.95; // Slightly slower for rural farmer clarity
    utterance.pitch = 1.0;

    utterance.onend = () => setSpeakingIndex(null);
    utterance.onerror = () => setSpeakingIndex(null);

    setSpeakingIndex(index);
    window.speechSynthesis.speak(utterance);
  };

  // 2. Speech-To-Text (Voice Input via Web Speech API or MediaRecorder fallback)
  const handleToggleVoiceInput = async () => {
    if (isListening) {
      // Stop listening
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop();
      }
      setIsListening(false);
      return;
    }

    // Try Web Speech Recognition
    const SpeechRecognition =
      (window as unknown as { SpeechRecognition?: any }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: any }).webkitSpeechRecognition;

    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = langOpt.bcp47;
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
          setIsListening(true);
        };

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          if (transcript) {
            setInputText(transcript);
            handleSend(transcript);
          }
          setIsListening(false);
        };

        recognition.onerror = () => {
          setIsListening(false);
          // Try fallback recording
          startMediaRecorderFallback();
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognition.start();
        return;
      } catch {
        // Fallback to MediaRecorder
      }
    }

    // Fallback: Record microphone audio and send to offline Whisper backend
    startMediaRecorderFallback();
  };

  const startMediaRecorderFallback = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        if (audioBlob.size > 1000) {
          try {
            setLoading(true);
            const res = await transcribeAudio(audioBlob, language);
            if (res.text) {
              setInputText(res.text);
              handleSend(res.text);
            }
          } catch {
            setError('Voice recognition service could not process audio.');
          } finally {
            setLoading(false);
          }
        }
      };

      recorder.start();
      setIsListening(true);
    } catch {
      alert('Microphone access denied or not supported on this device.');
      setIsListening(false);
    }
  };

  const handleSend = async (textToSend?: string) => {
    const raw = textToSend !== undefined ? textToSend : inputText;
    const query = raw.trim();

    if (!query || loading) return;

    const now = Date.now();
    if (now - lastSubmitRef.current < 800) return;
    lastSubmitRef.current = now;

    const userTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMessage: ChatMessage = {
      role: 'user',
      content: query,
      timestamp: userTimestamp,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setLoading(true);
    setError(null);

    const historyPayload = messages.slice(-6).map((m) => ({
      role: m.role,
      content: m.content,
    }));

    try {
      const response = await sendChatMessage(query, initialCropContext, historyPayload, language);

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.reply || response.response || '',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: response.sources,
        urgency_level: response.urgency_level,
        helpline: response.helpline || 'Kisan Call Centre 24x7 Helpline: 1800-180-1551',
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err?.message || 'Unable to connect to local offline advisory station.');
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();
    handleSend();
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const currentTopics = QUICK_TOPICS_BY_LANG[language] || QUICK_TOPICS_BY_LANG.hi || QUICK_TOPICS_BY_LANG.en;

  return (
    <section className="chat-section container" aria-label="Agricultural Advisory Chat">
      <div className="card chat-card">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="chat-header-title-row">
            <h2 className="chat-title">{t('chatHeading')}</h2>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <span className="badge badge-subtle" title="Active Language">
                {langOpt.nativeLabel} ({langOpt.label})
              </span>
              <span className="badge badge-accent" title="Zero internet needed">
                {t('offlineBadge')}
              </span>
            </div>
          </div>
          <p className="chat-subtitle">{t('chatDesc')}</p>
        </div>

        {/* Suggested Quick Questions */}
        <div className="quick-topics-row">
          <span className="quick-topics-label">{t('suggestedQuestions')}:</span>
          {currentTopics.slice(0, 5).map((topic, idx) => (
            <button
              key={idx}
              type="button"
              className="quick-topic-chip"
              onClick={() => handleSend(topic)}
              disabled={loading}
            >
              {topic}
            </button>
          ))}
        </div>

        {/* Messages Body */}
        <div className="chat-messages-container" role="log" aria-live="polite">
          {messages.map((msg, index) => {
            const isUser = msg.role === 'user';
            const isSpeaking = speakingIndex === index;
            return (
              <div
                key={index}
                className={`chat-msg ${isUser ? 'chat-msg--farmer' : 'chat-msg--advisor'}`}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                  {isUser ? (
                    <FiUser style={{ fontSize: '14px', color: 'var(--color-gold-bright)' }} />
                  ) : (
                    <FaLeaf style={{ fontSize: '14px', color: 'var(--color-gold-bright)' }} />
                  )}
                  <strong style={{ fontSize: '13px', color: isUser ? '#FFFFFF' : 'var(--color-gold-bright)' }}>
                    {isUser ? 'Kisan Bhai' : 'Krishi Mitra Advisor'}
                  </strong>
                  <span style={{ fontSize: '11px', color: 'var(--color-slate-400)', marginLeft: 'auto' }}>
                    {msg.timestamp}
                  </span>

                  {/* Text-to-Speech Button for Advisor Replies */}
                  {!isUser && (
                    <button
                      type="button"
                      onClick={() => handleToggleSpeak(msg.content, index)}
                      className={`btn-tts ${isSpeaking ? 'btn-tts--active' : ''}`}
                      title={isSpeaking ? t('stopSpeaking') : t('speakAdvice')}
                      aria-label={isSpeaking ? 'Stop speaking' : 'Read advice aloud'}
                      style={{
                        background: isSpeaking ? 'var(--color-gold-bright)' : 'rgba(212, 175, 55, 0.15)',
                        border: '1px solid var(--color-gold)',
                        color: isSpeaking ? '#0B192C' : 'var(--color-gold-bright)',
                        borderRadius: '6px',
                        padding: '4px 8px',
                        cursor: 'pointer',
                        fontSize: '11px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        marginLeft: '8px',
                      }}
                    >
                      {isSpeaking ? <FiVolumeX aria-hidden="true" /> : <FiVolume2 aria-hidden="true" />}
                      <span>{isSpeaking ? t('stopSpeaking') : t('speakAdvice')}</span>
                    </button>
                  )}
                </div>

                <div style={{ whiteSpace: 'pre-line', marginTop: '6px' }}>{msg.content}</div>

                {!isUser && msg.sources && msg.sources.length > 0 && (
                  <div style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid rgba(212,175,55,0.2)', fontSize: '12px', color: 'var(--color-slate-300)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <FiBookOpen style={{ color: 'var(--color-gold-bright)' }} />
                      <span>{msg.sources.join(' • ')}</span>
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div className="chat-msg chat-msg--advisor" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
              <FiLoader className="spin" style={{ color: 'var(--color-gold-bright)' }} />
              <span>{t('thinking')}</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Listening Status Bar with Animated Audio Waveform */}
        {isListening && (
          <div className="voice-listening-bar" role="status" aria-live="assertive">
            <span className="voice-record-dot" aria-hidden="true" />
            <div className="voice-wave-container" aria-hidden="true">
              <span className="voice-wave-bar" style={{ animationDelay: '0.0s' }} />
              <span className="voice-wave-bar" style={{ animationDelay: '0.2s' }} />
              <span className="voice-wave-bar" style={{ animationDelay: '0.4s' }} />
              <span className="voice-wave-bar" style={{ animationDelay: '0.15s' }} />
              <span className="voice-wave-bar" style={{ animationDelay: '0.35s' }} />
            </div>
            <strong>{t('listening')}</strong>
            <span className="voice-lang-tag">({langOpt.nativeLabel} / {langOpt.bcp47})</span>
          </div>
        )}

        {/* Chat Input Bar with Microphone Voice Assistant */}
        <form className="chat-input-row" onSubmit={handleFormSubmit}>
          {/* Voice Input Button */}
          <button
            type="button"
            className={`btn ${isListening ? 'btn-danger' : 'btn-secondary'}`}
            onClick={handleToggleVoiceInput}
            title={isListening ? t('listening') : t('voicePrompt')}
            aria-label={isListening ? 'Stop voice listening' : 'Start voice input'}
            style={{
              padding: '0 16px',
              background: isListening ? '#DC2626' : 'rgba(212, 175, 55, 0.15)',
              borderColor: isListening ? '#EF4444' : 'var(--color-gold)',
              color: isListening ? '#FFFFFF' : 'var(--color-gold-bright)',
            }}
          >
            {isListening ? (
              <FiMicOff className="btn-icon" aria-hidden="true" />
            ) : (
              <FiMic className="btn-icon" aria-hidden="true" />
            )}
            <span className="hide-on-mobile">{isListening ? t('listening') : t('voiceInput')}</span>
          </button>

          <input
            type="text"
            className="chat-text-input"
            placeholder={isListening ? t('listening') : t('askPlaceholder')}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            aria-label="Ask agricultural advisory question"
          />

          <button
            type="submit"
            className="btn btn-accent"
            disabled={loading || !inputText.trim()}
          >
            <FiSend className="btn-icon" aria-hidden="true" />
            <span>{t('send')}</span>
          </button>
        </form>
      </div>
    </section>
  );
}

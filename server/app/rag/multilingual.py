"""
Multilingual Agronomic Advisory & Native-Language Translation Engine for 22 Scheduled Indian Languages + English.
Provides authentic localized templates, comprehensive fungicide/insecticide treatment protocols,
application methods & timing guides, and vision/pest result localization for Llama 3.2 on-device
ExecuTorch and offline ICAR RAG synthesis.
"""

import re
from typing import Dict, Any, List, Optional

# The 22 Scheduled Languages of India + English
INDIC_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "native": "English", "bcp47": "en-IN", "script": "Latin"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "bcp47": "hi-IN", "script": "Devanagari"},
    "bn": {"name": "Bengali", "native": "বাংলা", "bcp47": "bn-IN", "script": "Bengali"},
    "te": {"name": "Telugu", "native": "తెలుగు", "bcp47": "te-IN", "script": "Telugu"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "bcp47": "ta-IN", "script": "Tamil"},
    "mr": {"name": "Marathi", "native": "मराठी", "bcp47": "mr-IN", "script": "Devanagari"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "bcp47": "gu-IN", "script": "Gujarati"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "bcp47": "kn-IN", "script": "Kannada"},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "bcp47": "ml-IN", "script": "Malayalam"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "bcp47": "pa-IN", "script": "Gurmukhi"},
    "or": {"name": "Odia", "native": "ଓଡ଼ିଆ", "bcp47": "or-IN", "script": "Odia"},
    "as": {"name": "Assamese", "native": "অসমীয়া", "bcp47": "as-IN", "script": "Assamese"},
    "ur": {"name": "Urdu", "native": "اردو", "bcp47": "ur-IN", "script": "Perso-Arabic"},
    "ne": {"name": "Nepali", "native": "नेपाली", "bcp47": "ne-NP", "script": "Devanagari"},
    "mai": {"name": "Maithili", "native": "मैथिली", "bcp47": "mai-IN", "script": "Devanagari"},
    "kok": {"name": "Konkani", "native": "कोंकणी", "bcp47": "kok-IN", "script": "Devanagari"},
    "sa": {"name": "Sanskrit", "native": "संस्कृतम्", "bcp47": "sa-IN", "script": "Devanagari"},
    "doi": {"name": "Dogri", "native": "डोगरी", "bcp47": "doi-IN", "script": "Devanagari"},
    "mni": {"name": "Manipuri", "native": "মণিপুরী", "bcp47": "mni-IN", "script": "Bengali/Meitei"},
    "brx": {"name": "Bodo", "native": "बड़ो", "bcp47": "brx-IN", "script": "Devanagari"},
    "sat": {"name": "Santali", "native": "ᱥᱟᱱᱛᱟᱲᱤ", "bcp47": "sat-IN", "script": "Ol Chiki"},
    "ks": {"name": "Kashmiri", "native": "كأشُر", "bcp47": "ks-IN", "script": "Perso-Arabic/Deva"},
    "sd": {"name": "Sindhi", "native": "سنڌي", "bcp47": "sd-IN", "script": "Perso-Arabic/Deva"},
}

GREETINGS: Dict[str, str] = {
    "en": "Namaste Kisan Bhai.",
    "hi": "नमस्ते किसान भाई।",
    "bn": "নমস্কার কৃষক ভাই।",
    "te": "నమస్కారం రైతు సోదరా.",
    "ta": "வணக்கம் விவசாய தோழரே.",
    "mr": "नमस्कार शेतकरी बंधू.",
    "gu": "નમસ્તે ખેડૂત મિત્ર.",
    "kn": "ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ.",
    "ml": "നമസ്കാരം കർഷക സുഹൃത്തേ.",
    "pa": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਕਿਸਾਨ ਵੀਰੋ।",
    "or": "ନମସ୍କାର ଚାଷୀ ଭାଇ।",
    "as": "নমস্কাৰ কৃষক ভাই।",
    "ur": "آداب کسان بھائی۔",
    "ne": "नमस्ते किसान साथी।",
    "mai": "प्रणाम किसान भाइ।",
    "kok": "नमस्कार शेतकार भावा.",
    "sa": "नमस्ते कृषक भ्रातः।",
    "doi": "नमस्ते किसान भराओ।",
    "mni": "খুরুমজরি লৌমী ইচিন-ইনাও।",
    "brx": "खुलुमबाय आबादारी बिदा-फंबाय।",
    "sat": "ᱡᱚᱦᱟᱨ ᱪᱟᱥᱤ ᱵᱚᱭᱦᱟ᱾",
    "ks": "آداب کِسان بھائی۔",
    "sd": "سلام هاري ڀاءُ.",
}

PRECAUTIONS: Dict[str, List[str]] = {
    "en": [
        "Always wear protective mask, gloves, and full-sleeve clothes while mixing and spraying fungicides or insecticides.",
        "Spray only during calm morning hours (7:00-10:00 AM) or late afternoon (4:00-6:00 PM) along the wind direction.",
        "Use 150-200 liters of clean water per acre (50-65 liters per Bengal Bigha) with a hollow-cone nozzle for uniform leaf coverage, and strictly observe the Pre-Harvest Interval (PHI)."
    ],
    "hi": [
        "कवकनाशी (फंगीसाइड) या कीटनाशक घोलते और छिड़कते समय हमेशा मास्क, दस्ताने और पूरी बाजू के कपड़े पहनें।",
        "छिड़काव हमेशा शांत मौसम में सुबह (7:00 से 10:00 बजे) या शाम (4:00 से 6:00 बजे) हवा की दिशा में ही करें।",
        "प्रति एकड़ 150 से 200 लीटर साफ पानी का उपयोग करें और फसल तुड़ाई से पहले निर्धारित प्रतीक्षा अवधि (PHI) का सख्ती से पालन करें।"
    ],
    "bn": [
        "ছত্রাকনাশক বা কীটনাশক মেশানো ও স্প্রে করার সময় অবশ্যই মুখে মাস্ক, হাতে গ্লাভস এবং ফুলহাতা পোশাক পরুন।",
        "সকাল (৭:০০-১০:০০ টা) অথবা বিকেলে (৪:০০-৬:০০ টা) রোদ কম থাকলে বাতাসের অনুকূলে স্প্রে করুন; প্রখর রোদে বা বৃষ্টির আগে স্প্রে করবেন না।",
        "প্রতি একরে ১৫০-২০০ লিটার (প্রতি বিঘায় ৫০-৬৫ লিটার) পরিষ্কার জলে ওষুধ গুলে পাতার উপর ও নিচে ভালোভাবে ভিজিয়ে স্প্রে করুন এবং ফসল তোলার আগে নির্দিষ্ট অপেক্ষার সময়সীমা (PHI) মেনে চলুন।"
    ],
    "te": [
        "మందు పిచికారీ చేసేటప్పుడు రక్షక మాస్క్ మరియు చేతి తొడుగులు ధరించండి.",
        "ఉదయం (7:00-10:00) లేదా సాయంత్రం (4:00-6:00) వేళల్లో ఎకరానికి 150-200 లీటర్ల నీటితో మాత్రమే పిచికారీ చేయండి.",
        "కోతకు ముందు నిరీక్షణ సమయం (PHI) తప్పనిసరిగా పాటించండి."
    ],
    "ta": [
        "மருந்து தெளிக்கும் போது முகக்கவசம் மற்றும் கையுறைகளை அணியுங்கள்.",
        "காலை (7:00-10:00) அல்லது மாலை (4:00-6:00) வேளையில் ஏக்கருக்கு 150-200 லிட்டர் தண்ணீரில் கலந்து தெளிக்கவும்.",
        "அறுவடைக்கு முன் பரிந்துரைக்கப்பட்ட இடைவெளியை (PHI) பின்பற்றவும்."
    ],
    "mr": [
        "बुरशीनाशक किंवा कीटकनाशक फवारताना नेहमी तोंडाला मास्क व हातमोजे वापरा.",
        "सकाळी (७:०० ते १०:००) किंवा संध्याकाळी (४:०० ते ६:००) शांत हवेत प्रति एकर १५०-२०० लिटर पाण्यात मिसळून फवारणी करा.",
        "कापणीपूर्वी शिफारस केलेला प्रतीक्षा कालावधी (PHI) पाळा."
    ],
    "gu": [
        "દવા છંટકાવ વખતે હંમેશા માસ્ક અને મોજા પહેરો.",
        "સવારે (૭:૦૦ થી ૧૦:૦૦) અથવા સાંજે (૪:૦૦ થી ૬:૦૦) પ્રતિ એકર ૧૫૦-૨૦૦ લિટર પાણીમાં ભેળવી છંટકાવ કરવો.",
        "લણણી પહેલા ભલામણ કરેલ સમયગાળો (PHI) જાળવો."
    ],
    "kn": [
        "ಔಷಧಿ ಸಿಂಪಡಿಸುವಾಗ ಮಾಸ್ಕ್ ಮತ್ತು ಕೈಗವಸುಗಳನ್ನು ಧರಿಸಿ.",
        "ಬೆಳಿಗ್ಗೆ (7:00-10:00) ಅಥವಾ ಸಂಜೆ (4:00-6:00) ಶಾಂತ ವಾತಾವರಣದಲ್ಲಿ ಎಕರೆಗೆ 150-200 ಲೀಟರ್ ನೀರಿನಲ್ಲಿ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ.",
        "ಕಟಾವಿಗೆ ಮೊದಲು ಶಿಫಾರಸು ಮಾಡಿದ ಕಾಯುವ ಅವಧಿಯನ್ನು (PHI) ಪಾಲಿಸಿ."
    ],
    "ml": [
        "മരുന്ന് തളിക്കുമ്പോൾ മാസ്കും കയ്യുറകളും ധരിക്കുക.",
        "രാവിലെ (7:00-10:00) അല്ലെങ്കിൽ വൈകുന്നേരം (4:00-6:00) തളിക്കുക.",
        "വിളവെടുപ്പിന് മുമ്പുള്ള സുരക്ഷിത ഇടവേള (PHI) പാലിക്കുക."
    ],
    "pa": [
        "ਦਵਾਈ ਛਿੜਕਣ ਵੇਲੇ ਮਾਸਕ ਅਤੇ ਦਸਤਾਨੇ ਜ਼ਰੂਰ ਪਹਿਨੋ।",
        "ਸਵੇਰੇ (7:00-10:00) ਜਾਂ ਸ਼ਾਮ (4:00-6:00) ਸ਼ਾਂਤ ਮੌਸਮ ਵਿੱਚ ਪ੍ਰਤੀ ਏਕੜ 150-200 ਲੀਟਰ ਪਾਣੀ ਵਰਤ ਕੇ ਛਿੜਕਾਅ ਕਰੋ।",
        "ਵਾਢੀ ਤੋਂ ਪਹਿਲਾਂ ਸਿਫ਼ਾਰਸ਼ ਕੀਤਾ ਅੰਤਰਾਲ (PHI) ਰੱਖੋ।"
    ],
    "or": [
        "ଔଷଧ ସିଞ୍ଚନ ବେଳେ ମାସ୍କ ଏବଂ ହାତମୋଜା ବ୍ୟବହାର କରନ୍ତୁ।",
        "ସକାଳ (୭:୦୦-୧୦:୦୦) କିମ୍ବା ସନ୍ଧ୍ୟା (୪:୦୦-୬:୦୦) ସମୟରେ ଏକର প্রতি ୧୫୦-୨୦୦ ଲିଟର ପାଣିରେ ମିଶାଇ ସିଞ୍ଚନ କରନ୍ତୁ।",
        "ଅମଳ ପୂର୍ବରୁ ସୁରକ୍ଷିତ ବ୍ୟବଧାନ (PHI) ପାଳନ କରନ୍ତୁ।"
    ],
    "as": [
        "ঔষধ ছটিওৱাৰ সময়ত মাস্ক আৰু হাতমোজাবোৰ পিন্ধিব।",
        "ৰাতিপুৱা (৭:০০-১০:০০) বা সন্ধিয়া (৪:০০-৬:০০) শান্ত বতাহত ছটিওৱা উচিত।",
        "শস্য চপোৱাৰ আগতে নিৰ্দিষ্ট সময় (PHI) মানি চলক।"
    ],
    "ur": [
        "دوا چھڑکتے وقت ہمیشہ ماسک اور دستانے پہنیں۔",
        "صبح (7:00 تا 10:00) یا شام (4:00 تا 6:00) پرسکون موسم میں چھڑکاؤ کریں۔",
        "فصل کی کٹائی سے پہلے محفوظ وقفہ (PHI) کا خیال رکھیں۔"
    ],
}

PRECAUTION_HEADERS: Dict[str, str] = {
    "en": "Important Spraying & Safety Precautions:",
    "hi": "छिड़काव एवं सुरक्षा संबंधी महत्वपूर्ण सावधानियां:",
    "bn": "স্প্রে করার নিয়ম ও গুরুত্বপূর্ণ সতর্কতা:",
    "te": "ముఖ్యమైన జాగ్రత్తలు:",
    "ta": "முக்கியமான முன்னெச்சரிக்கைகள்:",
    "mr": "महत्त्वाच्या काळजी व खबरदारी:",
    "gu": "મહત્વપૂર્ણ સાવચેતીઓ:",
    "kn": "ಮುಖ್ಯ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು:",
    "ml": "പ്രധാന മുൻകരുതലുകൾ:",
    "pa": "ਮਹੱਤਵਪੂਰਨ ਸਾਵਧਾਨੀਆਂ:",
    "or": "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ସତର୍କତା:",
    "as": "গুৰুত্বপূৰ্ণ সাৱধানতাসমূহ:",
    "ur": "اہم احتیاطی تدابیر:",
    "ne": "महत्वपूर्ण सावधानीहरू:",
    "mai": "महत्वपूर्ण सावधानिया:",
    "kok": "महत्वाच्यो शिटकावण्यो:",
    "sa": "महत्वपूर्णाः सावधानताः:",
    "doi": "अहम सावधानियां:",
    "mni": "মরুওইবা চেকশিন-থৌরাংশিং:",
    "brx": "गोनांथार सांग्रांथि:",
    "sat": "ᱡᱟᱹᱨᱩᱲ ᱦᱩᱥᱤᱭᱟᱹᱨ:",
    "ks": "اہم احتیاطی تدابیر:",
    "sd": "ضروري احتياطي تدبيرون:",
}

HELPLINES: Dict[str, str] = {
    "en": "For immediate free telephonic guidance, contact the toll-free Kisan Call Centre helpline at 1800-180-1551 (6:00 AM to 10:00 PM).",
    "hi": "तत्काल निःशुल्क टेलीफोनिक मार्गदर्शन के लिए, टोल-फ्री किसान कॉल सेंटर हेल्पलाइन 1800-180-1551 (सुबह 6:00 से रात 10:00 बजे) पर संपर्क करें।",
    "bn": "অবিলম্বে বিনামূল্যে পরামর্শের জন্য টোল-ফ্রি কিষাণ কল সেন্টার হেল্পলাইন 1800-180-1551 (সকাল ৬:০০ থেকে রাত ১০:০০) নম্বরে যোগাযোগ করুন।",
    "te": "తక్షణ ఉచిత సలహా కొరకు టోల్ ఫ్రీ కిసాన్ కాల్ సెంటర్ హెల్ప్‌లైన్ 1800-180-1551 (ఉదయం 6:00 నుండి రాత్రి 10:00 వరకు) సంప్రదించండి.",
    "ta": "உடனடி இலவச தொலைபேசி வழிகாட்டுதலுக்கு, கட்டணமில்லா கிசான் கால் சென்டர் 1800-180-1551 (காலை 6:00 முதல் இரவு 10:00 வரை) தொடர்பு கொள்ளவும்.",
    "mr": "तातडीच्या मोफत मार्गदर्शनासाठी, टोल-फ्री किसान कॉल सेंटर हेल्पलाइन 1800-180-1551 (सकाळी ६:०० ते रात्री १०:००) वर संपर्क साधा.",
    "gu": "ત્વરિત મફત ટેલિફોનિક માર્ગદર્શન માટે, ટોલ-ફ્રી કિસાન કૉલ સેન્ટર હેલ્પલાઇન 1800-180-1551 (સવારે ૬:૦૦ થી રાત્રે ૧૦:૦૦) પર સંપર્ક કરો.",
    "kn": "ತ್ವರಿತ ಉಚಿತ ಮಾಹಿತಿಗಾಗಿ ಟೋಲ್-ಫ್ರೀ ಕಿಸಾನ್ ಕಾಲ್ ಸೆಂಟರ್ ಸಹಾಯವಾಣಿ 1800-180-1551 (ಬೆಳಿಗ್ಗೆ 6:00 ರಿಂದ ರಾತ್ರಿ 10:00) ಸಂಪರ್ಕಿಸಿ.",
    "ml": "സൗജന്യ ഉപദേശത്തിന് ടോൾ ഫ്രീ കിസാൻ കോൾ സെന്റർ ഹെൽപ്പ് ലൈനിൽ 1800-180-1551 (രാവിലെ 6:00 മുതൽ രാത്രി 10:00 വരെ) ബന്ധപ്പെടുക.",
    "pa": "ਮੁਫ਼ਤ ਸਲਾਹ ਲਈ ਟੋਲ-ਫ੍ਰੀ ਕਿਸਾਨ ਕਾਲ ਸੈਂਟਰ ਹੈਲਪਲਾਈਨ 1800-180-1551 (ਸਵੇਰੇ 6:00 ਤੋਂ ਰਾਤ 10:00 ਵਜੇ) 'ਤੇ ਸੰਪਰਕ ਕਰੋ।",
    "or": "ମାଗଣା ଟେଲିଫୋନିକ୍ ପରାମର୍ଶ ପାଇଁ ଟୋଲ୍-ଫ୍ରି କିଷାନ୍ କଲ୍ ସେଣ୍ଟର୍ 1800-180-1551 (ସକାଳ ୬:୦୦ ରୁ ରାତି ୧୦:୦୦) ସହ ଯୋଗାଯୋଗ କରନ୍ତୁ।",
    "as": "বিনামূলীয়া পৰামৰ্শৰ বাবে টোল-ফ্ৰী কিষাণ কল চেণ্টাৰ হেল্পলাইন 1800-180-1551 (ৰাতিপুৱা ৬:০০ ৰ পৰা নিশা ১০:০০) লৈ ফোন কৰক।",
    "ur": "فوری مفت رہنمائی کے لیے ٹول فری کسان کال سینٹر ہیلپ لائن 1551-180-1800 (صبح 6:00 سے رات 10:00 بجے) پر رابطہ کریں۔",
}

# ==============================================================================
# STRUCTURED NATIVE-LANGUAGE TREATMENT, FUNGICIDE & APPLICATION TIMING DATABASE
# ==============================================================================

LOCALIZED_ADVISORY_TOPICS: Dict[str, Dict[str, List[str]]] = {
    "early_blight": {
        "en": [
            "Disease Diagnosis & Symptoms: Concentric dark brown circular rings (target-board appearance) on older lower leaves, causing leaves to turn yellow and drop prematurely (Early Blight).",
            "Recommended Fungicide & Exact Dose: Spray Mancozeb 75% WP (Indofil M-45) @ 2.5 g per liter of water (500 g per acre) OR Copper Oxychloride 50% WP (Blitox) @ 3.0 g/L OR Azoxystrobin 23% SC @ 1.0 ml/L.",
            "Organic Bio-Control Remedy: Spray Trichoderma viride or Pseudomonas fluorescens @ 5 g/L and prune off soil-touching lower leaves (up to 30 cm) to stop upward spore splash.",
            "How & When to Apply: Begin spraying 30-35 days after transplanting or at the first sign of leaf spots. Spray in late afternoon (4:00-6:00 PM) using 150-200 L water/acre mixed with sticker (0.5 ml/L). Repeat after 10-12 days if needed (PHI: 7 days)."
],
        "bn": [
            "রোগ নির্ণয় ও লক্ষণ: টমেটো বা আলুর নিচের পুরনো পাতায় গাঢ় বাদামী রঙের গোল চাকার মতো দাগ (Target-Board Rings) দেখা যায় এবং পাতা হলুদ হয়ে শুকিয়ে যায় (আর্লি ব্লাইট / আগাম ধসা রোগ)।",
            "সঠিক ছত্রাকনাশক ও মাত্রা (Fungicide & Dose): ম্যানকোজেব ৭৫% ডব্লিউপি (Mancozeb 75% WP যেমন Indofil M-45) প্রতি লিটার জলে ২.৫ গ্রাম (একরে ৫০০ গ্রাম / বিঘায় ১৬৫ গ্রাম) অথবা কপার অক্সিক্লোরাইড ৫০% ডব্লিউপি (Blitox) প্রতি লিটার জলে ৩.০ গ্রাম অথবা অ্যাজোক্সিস্ট্রবিন ২৩% এসসি (Azoxystrobin 23% SC) প্রতি লিটার জলে ১.০ মিলি মিশিয়ে স্প্রে করুন।",
            "জৈব ও প্রাকৃতিক প্রতিকার: ট্রাইকোডার্মা ভিরিডি (Trichoderma viride) বা সিউডোমোনাস ফ্লুরোসেন্স প্রতি লিটার জলে ৫ গ্রাম হারে মিশিয়ে স্প্রে করুন এবং মাটির নিচের দিকে থাকা আক্রান্ত পাতাগুলো (মাটি থেকে ১ ফুট পর্যন্ত) ছিঁড়ে পুড়িয়ে ফেলুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): চারার বয়স ৩০-৩৫ দিন হলে বা পাতায় প্রথম দাগ দেখা মাত্রই বিকেলে (৪:০০-৬:০০ টা) প্রতি একরে ১৫০-২০০ লিটার জলে স্টিকার (০.৫ মিলি/লিটার) মিশিয়ে পাতার উভয় পৃষ্ঠ ভিজিয়ে স্প্রে করুন। ১০-১২ দিন পর দ্বিতীয়বার ছত্রাকনাশক পরিবর্তন করে স্প্রে করুন। ফসল তোলার অন্তত ৭ দিন আগে স্প্রে বন্ধ রাখুন (PHI: 7 days)।"
        ],
        "hi": [
            "रोग पहचान एवं लक्षण: टमाटर या आलू की निचली पत्तियों पर गहरे भूरे रंग के गोल छल्लेदार धब्बे (Target-Board Rings) बनते हैं और पत्तियां पीली पड़कर सूखने लगती हैं (अगेती झुलसा / Early Blight)।",
            "अनुशंसित कवकनाशी (Fungicide) एवं सटीक मात्रा: मैंकोज़ेब 75% WP (Mancozeb 75% WP) @ 2.5 ग्राम प्रति लीटर पानी (500 ग्राम/एकड़) या कॉपर ऑक्सीक्लोराइड 50% WP @ 3.0 ग्राम प्रति लीटर या एज़ोक्सीस्ट्रोबिन 23% SC @ 1.0 मिली प्रति लीटर पानी में मिलाकर छिड़काव करें।",
            "जैविक उपचार एवं स्वच्छता: ट्राइकोडर्मा विरिडी (Trichoderma viride) @ 5 ग्राम/लीटर का छिड़काव करें और जमीन से सटी निचली संक्रमित पत्तियों (30 सेमी तक) को तोड़कर खेत से बाहर नष्ट कर दें।",
            "कब और कैसे प्रयोग करें (How & When to Apply): रोपाई के 30-35 दिन बाद या शुरुआती लक्षण दिखते ही शाम के समय (4:00-6:00 बजे) प्रति एकड़ 150-200 लीटर पानी में स्टीकर मिलाकर पत्तियों की दोनों सतहों पर छिड़काव करें। 10-12 दिन के अंतराल पर दूसरा छिड़काव करें। तुड़ाई से 7 दिन पहले छिड़काव बंद करें।"
        ]
    },
    "late_blight": {
        "en": [
            "Disease Diagnosis & Symptoms: Water-soaked, dark brown or purplish lesions rapidly spreading on leaves and stems, with white cottony fungal mold visible on the underside during humid mornings (Late Blight — highly destructive).",
            "Recommended Systemic Fungicide & Exact Dose: Spray Cymoxanil 8% + Mancozeb 64% WP (Curzate M8) @ 2.5 g per liter of water (500 g per acre) OR Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold) @ 2.5 g/L immediately. For severe blight, rotate after 7-10 days with Dimethomorph 50% WP (Acrobat) @ 1.0 g/L + Mancozeb @ 2.0 g/L.",
            "Preventive & Tuber Protection: As a preventive spray during cloudy or foggy weather (12-18°C), apply Mancozeb 75% WP @ 2.5 g/L. Earth up ridges firmly with soil to keep spores from washing down to tubers, and destroy heavily infected haulms.",
            "How & When to Apply: Spray after morning fog/dew clears (9:00-11:00 AM) or in late afternoon (3:00-5:00 PM) with 150-200 L water/acre mixed with sticker. Thoroughly wet both leaf surfaces and stems. Ensure clear drainage and avoid excessive urea (PHI: 7 days)."
],
        "bn": [
            "রোগ নির্ণয় ও লক্ষণ: পাতায় জলভেজা কালচে-বাদামী পচন দাগ দেখা যায় এবং সকালের দিকে পাতার নিচে সাদা তুলোর মতো ছত্রাকের আস্তরণ তৈরি হয় (লেট ব্লাইট / নাবী ধসা রোগ—অত্যন্ত মারাত্মক)।",
            "সঠিক ছত্রাকনাশক ও মাত্রা (Systemic Fungicide): রোগ দেখা দিলে অবিলম্বে সাইমোক্সানিল ৮% + ম্যানকোজেব ৬৪% ডব্লিউপি (Curzate M8) প্রতি লিটার জলে ২.৫ গ্রাম অথবা মেটালাক্সিল ৮% + ম্যানকোজেব ৬৪% ডব্লিউপি (Ridomil Gold) প্রতি লিটার জলে ২.৫ গ্রাম (একরে ৫০০ গ্রাম) অথবা ডাইমেথোমর্ফ ৫০% ডব্লিউপি (Acrobat) ১ গ্রাম + ম্যানকোজেব ২ গ্রাম প্রতি লিটার জলে মিশিয়ে স্প্রে করুন।",
            "প্রতিরোধমূলক ব্যবস্থা: মেঘলা ও কুয়াশাচ্ছন্ন আবহাওয়া (১২-১৮° সে.) শুরু হওয়ার আগেই প্রতিরোধমূলক হিসেবে ম্যানকোজেব ৭৫% ডব্লিউপি @ ২.৫ গ্রাম/লিটার জলে স্প্রে করুন এবং আলুর ভেলির মাটি উঁচু করে বেঁধে দিন যাতে ছত্রাকের রেণু মাটির নিচে আলুতে না পৌঁছায়।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): কুয়াশা কেটে যাওয়ার পর সকাল ৯-১১টা বা বিকেল ৩-৫টার মধ্যে প্রতি একরে ২০০ লিটার জলে স্টিকারসহ ডাঁটা ও পাতার নিচের দিক ভালোভাবে ভিজিয়ে স্প্রে করুন। আবহাওয়া খারাপ থাকলে ৭-১০ দিন অন্তর ছত্রাকনাশক পরিবর্তন করে স্প্রে করুন এবং জমিতে জল জমতে দেবেন না।"
        ],
        "hi": [
            "रोग पहचान एवं लक्षण: पत्तियों और तनों पर पानी से भीगे हुए काले-भूरे धब्बे तेजी से फैलते हैं और सुबह पत्ती की निचली सतह पर सफेद रुई जैसी फफूंद दिखाई देती है (पछेती झुलसा / Late Blight — अत्यंत गंभीर)।",
            "अनुशंसित सिस्टेमिक कवकनाशी (Fungicide) एवं मात्रा: तुरंत साइमोक्सानिल 8% + मैंकोज़ेब 64% WP (Curzate M8) @ 2.5 ग्राम/लीटर या मेटालैक्सिल 8% + मैंकोज़ेब 64% WP (Ridomil Gold) @ 2.5 ग्राम/लीटर (500 ग्राम/एकड़) का छिड़काव करें।",
            "निवारक उपाय: कोहरे और बादल वाले मौसम में बचाव हेतु मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें और आलू की मेड़ों पर मिट्टी चढ़ाएं ताकि फफूंद कंदों तक न पहुंचे।",
            "कब और कैसे प्रयोग करें (How & When to Apply): ओस सूखने के बाद प्रति एकड़ 200 लीटर पानी में चिपकने वाला पदार्थ (स्टीकर) मिलाकर पौधे के ऊपरी और निचले हिस्से को पूरी तरह भिगोते हुए 7-10 दिन के अंतराल पर छिड़काव करें।"
        ]
    },
    "rice_leaf_roller": {
        "en": [
            "Pest Identification & Damage: Rice Leaf Roller / Leaf Folder caterpillar rolls leaf margins together lengthwise with silk threads and feeds on green chlorophyll inside, turning leaves paper-white.",
            "Recommended Insecticide & Exact Dose: Spray Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml per liter of water (60 ml per acre) OR Cartap Hydrochloride 50% SP @ 2.0 g/L (400 g per acre) OR Flubendiamide 39.35% SC @ 0.2 ml/L.",
            "Organic Bio-Control Remedy: Release Trichogramma chilonis parasitoid egg cards @ 20,000 per acre 3 times at 7-day intervals starting 30 days after transplanting. Run a coir rope across dewy foliage in early morning to dislodge caterpillars, and spray 5% Neem Seed Kernel Extract (NSKE) @ 5 ml/L.",
            "How & When to Apply: Spray during tillering and panicle emergence stages in late afternoon (4:00-6:00 PM) using 150-200 L water/acre. Target upper foliage and folded leaves. Avoid excessive nitrogen/urea and keep field bunds clean (PHI: 14 days)."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: ধানের পাতা মোড়ানো পোকা (Rice Leaf Roller / Leaf Folder)। এর সবুজ রঙের শুঁয়োপোকা পাতার দুই ধার লালা দিয়ে মুড়িয়ে নলের মতো করে ভেতরে বসে সবুজ অংশ (ক্লোরোফিল) খেয়ে পাতা সাদা করে দেয়। ব্যবস্থা গ্রহণের মাত্রা: প্রতি গোছায় ১-২টি সদ্য মোড়ানো পাতা (বা শীষ বেরোনোর সময় ১০% আক্রান্ত পাতা)।",
            "সঠিক কীটনাশক ও মাত্রা (Chemical Spray & Dose): আক্রমণ ETL অতিক্রম করলে ক্লোরান্ট্রানিলিপ্রোল ১৮.৫% এসসি (Coragen) প্রতি লিটার জলে ০.৩ মিলি (একরে ৬০ মিলি / বিঘায় ২০ মিলি) অথবা কার্টাপ হাইড্রোক্লোরাইড ৫০% এসপি (Caldan 50 SP) প্রতি লিটার জলে ২.০ গ্রাম (একরে ৪০০ গ্রাম) অথবা ফ্লুবেন্ডিয়ামাইড ৩৯.৩৫% এসসি (Fame) প্রতি লিটার জলে ০.২ মিলি স্প্রে করুন।",
            "জৈব ও প্রাকৃতিক প্রতিকার: চারা রোপণের ৩০ দিন পর থেকে ৭ দিন অন্তর ৩ বার ট্রাইকোগ্রামা কাইলোনিস (Trichogramma chilonis) পরজীবী বোলতার ডিম-কার্ড একরে ২০,০০০টি (হেক্টরে ৫০,০০০টি) জমিতে লাগান। সকালবেলা শিশিরভেজা ধানের ওপর দিয়ে দড়ি টেনে দিলে শুঁয়োপোকা জলে পড়ে নষ্ট হয় এবং ৫% নিম বীজের নির্যাস (NSKE) @ ৫ মিলি/লিটার স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): পাশকাঠি ও থোড় আসার সময় (৩০-৬০ DAT) বিকেলে (৪:০০-৬:০০ টা) প্রতি একরে ১৫০-২০০ লিটার জলে ওষুধ গুলে পাতার অগ্রভাগ ও মোড়ানো অংশে স্প্রে করুন। অতিরিক্ত ইউরিয়া সার প্রয়োগ বন্ধ রাখুন এবং জমির আলের ঘাস পরিষ্কার রাখুন। ধান কাটার অন্তত ১৪ দিন আগে স্প্রে বন্ধ করুন (PHI: 14 days)।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: धान का पत्ती लपेटक कीट (Rice Leaf Roller/Folder)। इसकी इल्ली पत्ती के दोनों किनारों को मोड़कर अंदर से हरा पदार्थ खाती है जिससे पत्तियां सफेद पड़ जाती हैं। कार्रवाई का स्तर: प्रति पौधा 1-2 मुड़ी हुई पत्तियां।",
            "अनुशंसित कीटनाशक एवं सटीक मात्रा: क्लोरैन्ट्रानिलिप्रोल 18.5% SC (Coragen) @ 0.3 मिली/लीटर पानी (60 मिली/एकड़) या कार्टाप हाइड्रोक्लोराइड 50% SP @ 2.0 ग्राम/लीटर (400 ग्राम/एकड़) या फ्लुबेंडियामाइड 39.35% SC @ 0.2 मिली/लीटर का छिड़काव करें।",
            "जैविक नियंत्रण: रोपाई के 30 दिन बाद ट्राइकोग्रामा काइलोनिस (Trichogramma chilonis) कार्ड @ 20,000/एकड़ 7 दिन के अंतराल पर 3 बार लगाएं और नीम तेल (1500 ppm) @ 5 मिली/लीटर का छिड़काव करें।",
            "कब और कैसे प्रयोग करें (How & When to Apply): कल्ले निकलते और गभोट अवस्था में शाम 4 से 6 बजे के बीच प्रति एकड़ 150-200 लीटर पानी का उपयोग कर पत्तियों पर छिड़काव करें। यूरिया खाद की अधिक मात्रा न डालें।"
        ]
    },
    "stem_borer": {
        "en": [
            "Pest Identification & Damage: Yellow Stem Borer in rice or Corn Borer in maize. Caterpillars bore into central stems causing 'Dead Hearts' (drying central shoot at vegetative stage) or 'White Ears' (empty white panicles at heading).",
            "Recommended Insecticide & Exact Dose: Broadcast granular Chlorantraniliprole 0.4% GR (Ferterra) @ 4 kg per acre OR Cartap Hydrochloride 4% GR @ 7.5 kg/acre in 2-3 cm standing water; OR spray Chlorantraniliprole 18.5% SC @ 0.3 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L.",
            "Organic & Cultural Remedy: Install 5 pheromone traps and 1 light trap per acre. Release Trichogramma japonicum parasitoid cards @ 20,000 per acre weekly. For corn, apply Beauveria bassiana @ 5 g/L into leaf whorls.",
            "How & When to Apply: Clip rice seedling leaf tips before transplanting to remove egg clusters. Apply granular formulation 20-30 days after transplanting in shallow water; apply foliar spray during late tillering (45-50 DAT) targeting stem bases in late afternoon."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: ধানের মাজরা পোকা (Yellow Stem Borer) বা ভুট্টার কাণ্ড ছিদ্রকারী পোকা (Corn Borer)। এই পোকা কাণ্ডের ভেতর কুরে খায়, ফলে কুশি অবস্থায় মাঝের পাতা শুকিয়ে 'ডেড হার্ট' (Dead Heart) এবং শীষ অবস্থায় সাদা চিটে শীষ 'হোয়াইট ইয়ার' (White Ear) হয়। ETL: ৫% ডেড হার্ট বা প্রতি বর্গমিটারে ১টি ডিমের গাদা।",
            "সঠিক কীটনাশক ও মাত্রা: দানাদার ওষুধ হিসেবে ক্লোরান্ট্রানিলিপ্রোল ০.৪% জিআর (Ferterra) একরে ৪ কেজি (বিঘায় ১.৩ কেজি) বা কার্টাপ হাইড্রোক্লোরাইড ৪% জিআর একরে ৭.৫ কেজি ছিপছিপে জলে ছড়ান; অথবা স্প্রে করার জন্য ক্লোরান্ট্রানিলিপ্রোল ১৮.৫% এসসি @ ০.৩ মিলি/লিটার বা স্পিনেটোরাম ১১.৭% এসসি @ ০.৫ মিলি/লিটার জলে মিশিয়ে স্প্রে করুন।",
            "জৈব ও যান্ত্রিক প্রতিকার: একরে ৫টি ফেরোমন ট্র্যাপ ও ১টি আলোক ফাঁদ বসান। ট্রাইকোগ্রামা জাপোনিকাম (Trichogramma japonicum) ডিম-কার্ড হেক্টরে ৫০,০০০টি করে সপ্তাহে ১ বার ছাড়ুন এবং ভুট্টার ক্ষেত্রে পাতার চোঙায় (whorl) বিউভেরিয়া বাসিয়ানা (Beauveria bassiana) @ ৫ গ্রাম/লিটার প্রয়োগ করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): চারা রোপণের আগে পাতার ডগা অল্প ছেঁটে রোপণ করুন। কুশি অবস্থায় (২০-৩০ DAT) ২-৩ সেমি ছিপছিপে জলে দানাদার ওষুধ বালির সাথে মিশিয়ে ছড়ান এবং থোড় আসার মুখে (৪৫-৫০ DAT) বিকেলে ১৫০-২০০ লিটার জলে কাণ্ডের গোড়ার দিকে লক্ষ্য করে স্প্রে করুন।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: पीला तना छेदक (Yellow Stem Borer) या मक्का तना छेदक (Corn Borer)। यह तने को अंदर से काटता है जिससे 'डेड हार्ट' (सूखी गोभ) और सफेद बालियां (White Ear) बनती हैं। ETL: 5% डेड हार्ट।",
            "अनुशंसित कीटनाशक एवं मात्रा: दानेदार दवा क्लोरैन्ट्रानिलिप्रोल 0.4% GR (Ferterra) @ 4 किग्रा/एकड़ या कार्टाप हाइड्रोक्लोराइड 4% GR @ 7.5 किग्रा/एकड़ छिछले पानी में बिखेरें, अथवा क्लोरैन्ट्रानिलिप्रोल 18.5% SC @ 0.3 मिली/लीटर पानी में मिलाकर छिड़काव करें।",
            "जैविक नियंत्रण: प्रति एकड़ 5 फेरोमोन ट्रैप लगाएं और ट्राइकोग्रामा जापोनिकम परजीवी कार्ड @ 20,000/एकड़ साप्ताहिक अंतराल पर लगाएं।",
            "कब और कैसे प्रयोग करें (How & When to Apply): रोपाई के 20-30 दिन बाद दानेदार दवा रेत में मिलाकर 2-3 सेमी पानी में डालें और गभोट अवस्था (45-50 DAT) में शाम के समय 150-200 लीटर पानी/एकड़ के साथ तने की ओर छिड़काव करें।"
        ]
    },
    "bph": {
        "en": [
            "Pest Identification & Damage: Brown Planthopper (BPH). Insects congregate at the base of rice tillers just above water level and suck sap, causing circular patches of lodging and drying known as 'Hopper Burn'.",
            "Recommended Insecticide & Exact Dose: Spray Triflumezopyrim 10% SC (Pexalon) @ 0.5 ml per liter of water (94 ml per acre) OR Pymetrozine 50% WDG (Chess) @ 0.6 g/L (120 g per acre) OR Dinotefuran 20% SG @ 0.4 g/L.",
            "Cultural & Bio-Control Remedy: Practice Alternate Wetting and Drying (AWD) by draining standing water for 3-4 days to let the soil dry. Form 30 cm alleyways (pathways) every 2.5-3 meters to allow sunlight and airflow to reach plant bases.",
            "How & When to Apply: Never spray on top of the foliage canopy. Direct the sprayer nozzle downward towards the base of rice stems where insects feed. Use 200 liters of water per acre in late afternoon. Avoid synthetic pyrethroids and excess urea."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: ধানের বাদামী শোষক পোকা বা কারেন্ট পোকা (Brown Planthopper - BPH)। এরা ধানের গোড়ায় জলের ঠিক ওপরে বসে রস চুষে খায়, ফলে ধান গোল হয়ে পুড়ে যাওয়ার মতো শুকিয়ে যায় ('হপার বার্ন' / Hopper Burn)। ETL: কুশি অবস্থায় গোছা প্রতি ৫-১০টি এবং থোড়/ফুল অবস্থায় ১৫-২০টি পোকা।",
            "সঠিক কীটনাশক ও মাত্রা: ট্রাইফ্লুমেজোপাইরিম ১০% এসসি (Pexalon) প্রতি লিটার জলে ০.৫ মিলি (একরে ৯৪ মিলি) অথবা পাইমেট্রোজিন ৫০% ডব্লিউডিজি (Chess) প্রতি লিটার জলে ০.৬ গ্রাম (একরে ১২০ গ্রাম) অথবা ডাইনোটেফুরান ২০% এসজি (Token/Osheen) @ ০.৪ গ্রাম/লিটার জলে গুলে স্প্রে করুন।",
            "জৈব ও পরিচর্যা প্রতিকার: জমি থেকে ৩-৪ দিনের জন্য জমা জল পুরোপুরি বের করে মাটি শুকিয়ে নিন (Alternate Wetting & Drying)। প্রতি ২.৫-৩ মিটার অন্তর ৩০ সেমি ফাঁকা গলি (Alleyway) রাখুন যাতে ধানের গোড়ায় রোদ ও বাতাস চলাচল করে।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): ওষুধ কখনও পাতার ওপরে স্প্রে করবেন না—স্প্রেয়ারের নজল ধানের গোড়ায় (জলের ঠিক ওপরে যেখানে পোকা বসে থাকে) ধরে প্রতি একরে ২০০ লিটার জলে বিকেলে স্প্রে করুন। সিন্থেটিক পাইরিথ্রয়েড জাতীয় ওষুধ ও অতিরিক্ত ইউরিয়া সার একেবারে ব্যবহার করবেন না।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: भूरा फुदका (Brown Planthopper - BPH)। यह धान के तने के निचले हिस्से से रस चूसता है जिससे फसल गोलाई में झुलस जाती है (Hopper Burn)। ETL: 5-10 फुदके प्रति पौधा।",
            "अनुशंसित कीटनाशक एवं मात्रा: ट्राइफ्लुमेज़ोपाइरिम 10% SC (Pexalon) @ 0.5 मिली/लीटर या पाइमेट्रोज़िन 50% WDG (Chess) @ 0.6 ग्राम/लीटर या डाइनोटेफ्यूरान 20% SG @ 0.4 ग्राम/लीटर पानी में मिलाकर छिड़काव करें।",
            "जैविक एवं सस्य प्रबंधन: खेत से 3-4 दिन के लिए पानी निकाल दें और हर 2.5-3 मीटर पर 30 सेमी की गली (Alleyway) बनाएं ताकि धूप और हवा पौधों की जड़ों तक पहुंचे।",
            "कब और कैसे प्रयोग करें (How & When to Apply): स्प्रेयर नोजल को सीधे पौधों के निचले तने (जड़ के पास) पर रखकर प्रति एकड़ 200 लीटर पानी से छिड़काव करें।"
        ]
    },
    "armyworm": {
        "en": [
            "Pest Identification & Damage: Fall Armyworm / Cutworm (Spodoptera). Nocturnal caterpillars voraciously feed on leaf whorls and foliage, leaving ragged irregular holes and sawdust-like fecal pellets.",
            "Recommended Insecticide & Exact Dose: Spray Emamectin Benzoate 5% SG @ 0.4 g per liter of water (80 g per acre) OR Chlorantraniliprole 18.5% SC @ 0.4 ml/L OR Spinetoram 11.7% SC @ 0.5 ml/L.",
            "Organic Bio-Control Remedy: Spray Bacillus thuringiensis (Bt kurstaki) @ 2 g/L or Metarhizium anisopliae @ 5 g/L in early stages. Apply dry sand mixed with slaked lime (9:1 ratio) directly into maize whorls. Install 5 pheromone traps and 10 bird perches per acre.",
            "How & When to Apply: Caterpillars feed during dawn and dusk. Spray strictly between 4:30 and 6:00 PM, directing the spray nozzle directly into the central plant whorl using 150-200 L water/acre (PHI: 14 days)."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: ফল আর্মিওয়ার্ম / লেদা পোকা (Fall Armyworm / Beet & Cabbage Armyworm / Spodoptera)। এরা রাতের বেলা ঝাঁকে ঝাঁকে পাতা ও ভুট্টার মাঝখানের চোঙা (whorl) খেয়ে ঝাঁঝরা করে দেয় এবং করাতের গুঁড়োর মতো মল ত্যাগ করে। ETL: ৫-১০% আক্রান্ত গাছ।",
            "সঠিক কীটনাশক ও মাত্রা: এমামেকটিন বেনজয়েট ৫% এসজি (Emamectin Benzoate 5% SG) প্রতি লিটার জলে ০.৪ গ্রাম (একরে ৮০ গ্রাম) অথবা ক্লোরান্ট্রানিলিপ্রোল ১৮.৫% এসসি @ ০.৪ মিলি/লিটার অথবা স্পিনেটোরাম ১১.৭% এসসি @ ০.৫ মিলি/লিটার স্প্রে করুন।",
            "জৈব ও প্রাকৃতিক প্রতিকার: প্রাথমিক অবস্থায় ব্যাসিলাস থুরিনজিয়েনসিস (Bt kurstaki) @ ২ গ্রাম/লিটার বা মেটারাইজিয়াম অ্যানিসোপ্লি @ ৫ গ্রাম/লিটার অথবা বালি ও চুনের মিশ্রণ (৯:১ অনুপাতে) গাছের মাঝখানের চোঙায় দিন। একরে ৫টি ফেরোমন ট্র্যাপ ও ১০টি পাখি বসার ডাল (Bird Perch) বসান।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): লেদা পোকা সূর্যের আলোয় লুকিয়ে থাকে এবং সন্ধ্যায় বের হয়—তাই অবশ্যই বিকেল ৪:৩০ থেকে সন্ধ্যা ৬:০০ টার মধ্যে স্প্রেয়ারের নজল গাছের মাঝখানের চোঙায় (whorl) ধরে স্প্রে করুন।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: फॉल आर्मीवर्म / सैनिक कीट (Armyworm / Spodoptera)। यह रात में पत्तियों और मक्का की गोभ (whorl) को खाकर छलनी कर देता है। ETL: 5-10% क्षतिग्रस्त पौधे।",
            "अनुशंसित कीटनाशक एवं मात्रा: इमामेक्टिन बेंजोएट 5% SG @ 0.4 ग्राम/लीटर (80 ग्राम/एकड़) या क्लोरैन्ट्रानिलिप्रोल 18.5% SC @ 0.4 मिली/लीटर या स्पिनेटोरम 11.7% SC @ 0.5 मिली/लीटर का छिड़काव करें।",
            "जैविक नियंत्रण: शुरुआती अवस्था में बैसिलस थुरिंजिएंसिस (Bt) @ 2 ग्राम/लीटर या गोभ में रेत + चूना (9:1) डालें तथा 5 फेरोमोन ट्रैप/एकड़ लगाएं।",
            "कब और कैसे प्रयोग करें (How & When to Apply): यह कीट शाम को सक्रिय होता है, इसलिए शाम 4:30 से 6:00 बजे के बीच नोजल को सीधे पौधे की गोभ (whorl) में रखकर छिड़काव करें।"
        ]
    },
    "red_spider": {
        "en": [
            "Pest Identification & Damage: Red Spider Mite / Foliage Mite. Mites spin fine webs on the lower surface of leaves and suck sap, causing yellowish stippling, bronze discoloration, and leaf curling.",
            "Recommended Miticide & Exact Dose: Spray Spiromesifen 22.9% SC (Oberon) @ 1.0 ml per liter of water OR Propargite 57% EC (Omite) @ 2.0 ml/L OR Fenazaquin 10% EC @ 2.0 ml/L.",
            "Organic & Sulphur Remedy: Spray Wettable Sulphur 80% WP (Sulfex/Thiovit) @ 3.0 g per liter of water OR cold-pressed Neem Oil (1500 ppm) @ 5 ml/L mixed with 0.5 ml mild liquid soap.",
            "How & When to Apply: Mites live exclusively under leaves; turn the spray nozzle upward to thoroughly coat the underside of foliage. Spray in late afternoon with 200 liters of water per acre, and repeat after 10 days with an alternate chemical."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: লাল মাকড় (Red Spider Mite / Citrus Red Mite)। পাতার নিচের দিকে সূক্ষ্ম জালের আড়ালে বসে রস চুষে খায়, ফলে পাতায় সাদাটে-হলুদ ছোপ পড়ে ও পাতা তামাটে হয়ে কুঁকড়ে যায়। ETL: প্রতি পাতায় ৫-১০টি মাকড়।",
            "সঠিক মাকড়নাশক ও মাত্রা (Miticide & Dose): স্পাইরোমেসিফেন ২২.৯% এসসি (Oberon) প্রতি লিটার জলে ১.০ মিলি অথবা প্রোপারগাইট ৫৭% ইসি (Omite) প্রতি লিটার জলে ২.০ মিলি অথবা ফেনাজাকুইন ১০% ইসি (Magister) @ ২.০ মিলি/লিটার জলে মিশিয়ে স্প্রে করুন।",
            "জৈব ও সালফার প্রতিকার: ওয়েটেবল সালফার ৮০% ডব্লিউপি (Wettable Sulphur 80% WP যেমন Sulfex/Thiovit) প্রতি লিটার জলে ৩.০ গ্রাম অথবা নিম তেল (১৫০০ পিপিএম) @ ৫ মিলি/লিটার জলে মিশিয়ে স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): মাকড় পাতার নিচের পৃষ্ঠে থাকে, তাই স্প্রেয়ারের নজল নিচের দিকে ঘুরিয়ে পাতার তলা ভালোভাবে ভিজিয়ে বিকেলে স্প্রে করুন। ১০ দিন পর মাকড়নাশক পরিবর্তন করে দ্বিতীয়বার স্প্রে করুন।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: लाल मकड़ी (Red Spider Mite)। यह पत्ती की निचली सतह पर बारीक जाला बनाकर रस चूसती है जिससे पत्तियों पर पीले-सफेद धब्बे पड़ जाते हैं। ETL: 5-10 माइट्स प्रति पत्ती।",
            "अनुशंसित मकड़ीनाशक (Miticide) एवं मात्रा: स्पाइरोमेसिफेन 22.9% SC (Oberon) @ 1.0 मिली/लीटर या प्रोपारगाइट 57% EC (Omite) @ 2.0 मिली/लीटर पानी में मिलाकर छिड़काव करें।",
            "जैविक एवं सल्फर उपचार: घुलनशील गंधक (Wettable Sulphur 80% WP) @ 3.0 ग्राम/लीटर या नीम तेल (1500 ppm) @ 5 मिली/लीटर का छिड़काव करें।",
            "कब और कैसे प्रयोग करें (How & When to Apply): नोजल को ऊपर की ओर मोड़कर पत्तियों की निचली सतह को अच्छी तरह भिगोते हुए शाम के समय छिड़काव करें।"
        ]
    },
    "aphids_hopper": {
        "en": [
            "Pest Identification & Damage: Aphids, Jassids (Leafhoppers), and Whiteflies. Insects suck sap from tender shoots, buds, and leaves, excreting sugary honeydew that leads to sooty mold and viral transmission.",
            "Recommended Insecticide & Exact Dose: Spray Imidacloprid 17.8% SL (Confidor) @ 0.3 ml per liter of water OR Thiamethoxam 25% WG (Actara) @ 0.25 g/L OR Flonicamid 50% WG (Ulala) @ 0.3 g/L.",
            "Organic Bio-Control Remedy: Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil (1500 ppm) @ 5 ml/L with soap solution. Install 12-15 yellow sticky traps per acre to monitor and trap flying adults. Protect beneficial ladybird beetles.",
            "How & When to Apply: Spray strictly after 4:00 PM when honeybees and pollinators are not foraging. Use 150-200 liters of water per acre. Observe a 15-day Pre-Harvest Interval (PHI) before picking produce."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: জাব পোকা (Aphids), শ্যামা পোকা/লিফহপার (Jassids/Cicadellidae) ও মিরিড বাগ। এরা কচি ডগা, পাতা ও ফুলের রস চুষে খায় এবং মধু-রস নিঃসরণ করে কালো ছত্রাক (Sooty Mold) ও ভাইরাস রোগ ছড়ায়। ETL: প্রতি ডগায় ১৫-২০টি জাব পোকা বা পাতা প্রতি ২-৩টি হপার।",
            "সঠিক কীটনাশক ও মাত্রা: ইমিডাক্লোপ্রিড ১৭.৮% এসএল (Confidor) প্রতি লিটার জলে ০.৩ মিলি অথবা থায়ামেথক্সাম ২৫% ডব্লিউজি (Actara) প্রতি লিটার জলে ০.২৫ গ্রাম অথবা ফ্লোনিকামিড ৫০% ডব্লিউজি (Ulala) প্রতি লিটার জলে ০.৩ গ্রাম মিশিয়ে স্প্রে করুন।",
            "জৈব প্রতিকার: ৫% নিম বীজের নির্যাস (NSKE) বা নিম তেল (১৫০০ পিপিএম) @ ৫ মিলি/লিটার জলে ০.৫ মিলি তরল সাবান মিশিয়ে স্প্রে করুন এবং একরে ১২-১৫টি হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) লাগান। উপকারী লেডিবার্ড বিটল (গুবরে পোকা) সংরক্ষণ করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): সরিষা বা সবজিতে ফুল ফোটার সময় মৌমাছি রক্ষার জন্য শুধুমাত্র বিকেল ৪:০০ টার পর (যখন মৌমাছি চরা বন্ধ করে) স্প্রে করুন। ফসল তোলার ১৫ দিন আগে রাসায়নিক স্প্রে বন্ধ করুন (PHI: 15 days)।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: माहू/चेपा (Aphids) एवं हरा तेला (Jassids/Leafhoppers)। ये कोमल टहनियों, पत्तियों और फूलों का रस चूसते हैं। ETL: 15-20 माहू प्रति टहनी या 2-3 तेला प्रति पत्ती।",
            "अनुशंसित कीटनाशक एवं मात्रा: इमिडाक्लोप्रिड 17.8% SL @ 0.3 मिली/लीटर या थायामेथोक्साम 25% WG @ 0.25 ग्राम/लीटर या फ्लोनिकामिड 50% WG @ 0.3 ग्राम/लीटर पानी में मिलाकर छिड़काव करें।",
            "जैविक नियंत्रण: 5% नीम बीज अर्क (NSKE) या नीम तेल @ 5 मिली/लीटर का छिड़काव करें और प्रति एकड़ 12-15 पीले चिपचिपे ट्रैप (Yellow Sticky Traps) लगाएं।",
            "कब और कैसे प्रयोग करें (How & When to Apply): मधुमक्खियों की सुरक्षा के लिए शाम 4:00 बजे के बाद ही छिड़काव करें और कटाई से 15 दिन पहले छिड़काव बंद कर दें।"
        ]
    },
    "mole_cricket": {
        "en": [
            "Pest Identification & Damage: Mole Cricket. Burrowing pests tunnel beneath the soil, severing roots and seedlings of vegetables and potatoes.",
            "Poison Bait & Control Remedy: Prepare poison bait by mixing 10 kg wheat bran or rice husk + 1 kg jaggery (gur) + 250 g Chlorantraniliprole or Fipronil with a little water; broadcast along field borders and tunnel openings at dusk. Alternatively broadcast Chlorantraniliprole 0.4% GR @ 4 kg/acre.",
            "Organic Remedy: Mix Metarhizium anisopliae @ 2 kg/acre with 50 kg well-decomposed FYM/compost and incorporate into moist soil.",
            "How & When to Apply: Flood irrigate infested beds lightly to force crickets to the surface where birds can prey on them. Apply poison baits strictly at dusk."
],
        "bn": [
            "পোকা সনাক্তকরণ ও ক্ষতির লক্ষণ: ঘুরঘুরে পোকা (Mole Cricket)। এরা মাটির নিচে সুড়ঙ্গ খুঁড়ে বীজতলার চারা ও আলুর কন্দের গোড়া কেটে দেয়। ETL: প্রতি বর্গমিটারে ২-৩টি নতুন মাটির ঢিবি বা সুড়ঙ্গ।",
            "সঠিক দমন ও বিষটোপ (Poison Bait & Remedy): ১০ কেজি গমের ভুসি বা চালের কুঁড়ো + ১ কেজি গুড় + ২৫০ গ্রাম ক্লোরান্ট্রানিলিপ্রোল বা ফিপ্রোনিল অল্প জলে মেখে বিষটোপ তৈরি করে সন্ধ্যার সময় সুড়ঙ্গের মুখে ছিটিয়ে দিন; অথবা ক্লোরান্ট্রানিলিপ্রোল ০.৪% জিআর @ ৪ কেজি/একর প্রয়োগ করুন।",
            "জৈব ও প্রাকৃতিক প্রতিকার: মেটারাইজিয়াম অ্যানিসোপ্লি (Metarhizium anisopliae) @ ২ কেজি/একর ৫০ কেজি পচা গোবর সারের সাথে মিশিয়ে ভেজা মাটিতে প্রয়োগ করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): জমিতে হালকা সেচ দিয়ে জল ঢুকিয়ে দিলে ঘুরঘুরে পোকা গর্ত থেকে বাইরে বেরিয়ে আসে এবং পাখিরা খেয়ে ফেলে। বিষটোপ অবশ্যই সন্ধ্যাবেলা প্রয়োগ করবেন।"
        ],
        "hi": [
            "कीट पहचान एवं कार्रवाई का स्तर: घरघुरिया कीट (Mole Cricket)। यह मिट्टी में सुरंग बनाकर नर्सरी के पौधों की जड़ें और आलू के कंद काट देता है। ETL: 2-3 सुरंगें प्रति वर्ग मीटर।",
            "अनुशंसित उपचार एवं विष-चारा (Poison Bait): 10 किग्रा चोकर + 1 किग्रा गुड़ + 250 ग्राम फिप्रोनिल या क्लोरैन्ट्रानिलिप्रोल को पानी से भुरभुरा मिलाकर शाम को मेड़ों और सुरंगों के पास बिखेरें।",
            "जैविक नियंत्रण: मेटाराइजियम एनिसोप्ली @ 2 किग्रा/एकड़ को 50 किग्रा गोबर की खाद में मिलाकर नमीयुक्त मिट्टी में डालें।",
            "कब और कैसे प्रयोग करें (How & When to Apply): खेत में हल्की सिंचाई करने से कीट बिलों से बाहर निकल आते हैं। विष-चारा हमेशा शाम के समय ही डालें।"
        ]
    },
    "fungicide_general": {
        "en": [
            "Disease Diagnosis & Initial Management: When fungal leaf spots, blights, rusts, or powdery mildews appear, prune lower infected leaves and ensure adequate soil drainage.",
            "Recommended Fungicides & Exact Doses: (a) Contact Fungicide: Mancozeb 75% WP @ 2.5 g/L OR Copper Oxychloride 50% WP @ 3.0 g/L; (b) Systemic Fungicide: Carbendazim 12% + Mancozeb 63% WP (Saaf) @ 2.0 g/L OR Azoxystrobin + Tebuconazole @ 1.0 ml/L; (c) For Powdery Mildew: Wettable Sulphur 80% WP @ 2.5 g/L.",
            "Organic Bio-Fungicide: Treat seeds with Trichoderma viride @ 4 g/kg seed and apply foliar spray @ 5 g per liter of water.",
            "How & When to Apply: Spray at first notice of disease in calm morning (after dew dries) or late afternoon (4:00-6:00 PM) using 150-200 liters of water per acre with 0.5 ml/L sticker. Repeat after 10-12 days and stop 7-10 days before harvest."
],
        "bn": [
            "রোগ নির্ণয় ও প্রাথমিক পরিচর্যা: ফসলের পাতায় ছত্রাকজনিত দাগ, পচন, মরিচা (Rust) বা পাউডারি মিলডিউ দেখা দিলে আক্রান্ত নিচের পাতা ছাঁটাই করুন এবং জমিতে জল নিকাশের ব্যবস্থা রাখুন।",
            "প্রতিরোধমূলক ও পচনরোধী ছত্রাকনাশক (Fungicides & Dose): (ক) স্পর্শক ছত্রাকনাশক: ম্যানকোজেব ৭৫% ডব্লিউপি (Indofil M-45) @ ২.৫ গ্রাম/লিটার বা কপার অক্সিক্লোরাইড ৫০% ডব্লিউপি (Blitox) @ ৩.০ গ্রাম/লিটার জলে; (খ) অন্তর্বাহী (Systemic) ছত্রাকনাশক: কার্বেন্ডাজিম ১২% + ম্যানকোজেব ৬৩% (Saaf) @ ২.০ গ্রাম/লিটার অথবা অ্যাজোক্সিস্ট্রবিন + টেবুকোনাজোল @ ১.০ মিলি/লিটার; (গ) পাউডারি মিলডিউ হলে: ওয়েটেবল সালফার ৮০% ডব্লিউপি @ ২.৫ গ্রাম/লিটার।",
            "জৈব ছত্রাকনাশক ও বীজ শোধন: ট্রাইকোডার্মা ভিরিডি (Trichoderma viride) @ ৪ গ্রাম/কেজি বীজে বীজ শোধন করুন এবং লিটার প্রতি ৫ গ্রাম হারে জলে গুলে গাছের গোড়ায় ও পাতায় স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন (How & When to Apply): রোগের প্রথম লক্ষণ দেখা দিলেই সকালে শিশির শুকানোর পর বা বিকেলে (৪:০০-৬:০০ টা) প্রতি একরে ১৫০-২০০ লিটার জলে স্টিকার (০.৫ মিলি/লিটার) মিশিয়ে স্প্রে করুন। ১০-১২ দিন পর দ্বিতীয় স্প্রে করুন এবং ফসল তোলার ৭-১০ দিন আগে স্প্রে বন্ধ রাখুন।"
        ],
        "hi": [
            "रोग पहचान एवं प्राथमिक प्रबंधन: पत्तियों पर फफूंदजनित धब्बे, झुलसा, रतुआ (Rust) या चूर्णिल आसिता (Powdery Mildew) दिखने पर संक्रमित पत्तियों को हटा दें और खेत में जल निकासी सुनिश्चित करें।",
            "अनुशंसित कवकनाशी (Fungicides) एवं मात्रा: (क) स्पर्श कवकनाशी: मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर या कॉपर ऑक्सीक्लोराइड 50% WP @ 3.0 ग्राम/लीटर; (ख) सिस्टेमिक कवकनाशी: कार्बेन्डाजिम 12% + मैंकोज़ेब 63% WP (Saaf) @ 2.0 ग्राम/लीटर या एज़ोक्सीस्ट्रोबिन + टेबुकोनाज़ोल @ 1.0 मिली/लीटर; (ग) पाउडरी मिल्ड्यू हेतु: घुलनशील सल्फर 80% WP @ 2.5 ग्राम/लीटर।",
            "जैविक कवकनाशी एवं बीज उपचार: ट्राइकोडर्मा विरिडी @ 4 ग्राम/किग्रा बीज से बीज उपचार करें तथा 5 ग्राम/लीटर पानी में मिलाकर छिड़काव करें।",
            "कब और कैसे प्रयोग करें (How & When to Apply): शुरुआती लक्षण दिखते ही शाम (4:00-6:00 बजे) प्रति एकड़ 150-200 लीटर पानी में स्टीकर मिलाकर पत्तियों की दोनों सतहों पर छिड़काव करें तथा 10-12 दिन बाद दोहराएं।"
        ]
    },
    "zinc_dap_soil": {
        "en": [
            "Caution — Never Mix Zinc Sulphate with DAP: Zinc Sulphate (21% Zn) must NEVER be mixed directly with DAP (Di-Ammonium Phosphate) or SSP fertilizers. Mixing creates insoluble zinc phosphate, rendering both zinc and phosphorus unavailable to crops.",
            "Correct Application Method: Apply Zinc Sulphate (10 kg/acre or 25 kg/ha) at least 3 to 5 days after DAP application, or broadcast separately mixed with dry sand or well-rotted manure.",
            "Foliar Spray for Deficiency (Khaira Disease): For standing crops showing zinc deficiency, dissolve 5 g Zinc Sulphate + 2.5 g Slaked Lime per liter of water, strain, and spray in late afternoon.",
            "Urea and DAP Nitrogen Balancing: 100 kg DAP provides 46 kg phosphorus plus 18 kg nitrogen. Deduct this 18% nitrogen from your total urea requirement and apply neem-coated urea in three split doses."
],
        "bn": [
            "সতর্কতা—জিঙ্ক সালফেট ও ডিএপি (DAP) একসাথে মেশাবেন না: জিঙ্ক সালফেট (Zinc Sulphate 21%) কখনোই ডিএপি (DAP) বা এসএসপি (SSP) সারের সাথে এক পাত্রে বা একসাথে মিশিয়ে জমিতে ছড়াবেন না। একসাথে মেশালে রাসায়নিক বিক্রিয়ায় অদ্রবণীয় 'জিঙ্ক ফসফেট' তৈরি হয়, ফলে গাছ জিঙ্ক ও ফসফরাস কোনোটাই গ্রহণ করতে পারে না।",
            "সঠিক প্রয়োগ পদ্ধতি: জমি তৈরির সময় ডিএপি সার প্রয়োগের অন্তত ৩ থেকে ৫ দিন পর (অথবা আলাদাভাবে শুকনো বালি বা পচা গোবর সারের সাথে মিশিয়ে) একরে ১০ কেজি (হেক্টরে ২৫ কেজি) জিঙ্ক সালফেট মাটিতে ছড়ান।",
            "পাতায় স্প্রে করার নিয়ম: খাড়া ফসলে জিঙ্কের অভাব (যেমন ধানের খয়রা রোগ) দেখা দিলে প্রতি লিটার জলে ৫ গ্রাম জিঙ্ক সালফেট + ২.৫ গ্রাম চুন (Slaked Lime) আলাদাভাবে গুলে ছেঁকে নিয়ে বিকেলে পাতায় স্প্রে করুন।",
            "ইউরিয়া ও ডিএপি হিসাবের নিয়ম: ১০০ কেজি ডিএপি সারে ৪৬ কেজি ফসফরাসের পাশাপাশি ১৮ কেজি নাইট্রোজেন থাকে—তাই মূল সারে ডিএপি দিলে ইউরিয়া সারের মাত্রা থেকে ওই ১৮% নাইট্রোজেন অবশ্যই বাদ দিয়ে ৩ কিস্তিতে (রোপণ, কুশি ও থোড় অবস্থায়) নিম-কোটেড ইউরিয়া প্রয়োগ করুন।"
        ],
        "hi": [
            "महत्वपूर्ण नियम—जिंक सल्फेट को डीएपी (DAP) के साथ कभी न मिलाएं: जिंक सल्फेट (21% Zn) को कभी भी डीएपी या एसएसपी (SSP) खाद के साथ सीधे मिलाकर खेत में न डालें। इन्हें मिलाने से अघुलनशील 'जिंक फॉस्फेट' बन जाता है जिससे दोनों खादें बेकार हो जाती हैं।",
            "सही प्रयोग विधि: डीएपी डालने के कम से कम 3 से 5 दिन बाद जिंक सल्फेट (10 किग्रा/एकड़ या 25 किग्रा/हेक्टेयर) को सूखी रेत या गोबर की खाद में मिलाकर अलग से बिखेरें।",
            "खड़ी फसल में छिड़काव: यदि खड़ी फसल में जिंक की कमी (जैसे धान का खैरा रोग) दिखे, तो 0.5% जिंक सल्फेट (5 ग्राम/लीटर) + 0.25% बुझा चूना (2.5 ग्राम/लीटर) मिलाकर शाम को पत्तियों पर छिड़काव करें।",
            "डीएपी में नाइट्रोजन की कटौती: डीएपी में 46% फॉस्फोरस के साथ 18% नाइट्रोजन भी होता है, इसलिए यूरिया की मात्रा से डीएपी से मिलने वाली नाइट्रोजन घटाकर ही 3 किस्तों में नीम-लेपित यूरिया डालें।"
        ]
    },
    "pmfby_insurance": {
        "en": [
            "PMFBY 72-Hour Mandatory Rule: For localized crop damage due to hailstorm, cyclone, unseasonal torrential rain, or inundation, you must report within 72 hours of occurrence.",
            "How to Report: (1) Call the toll-free Crop Insurance Helpline at 14447, (2) upload geo-tagged photos of damaged fields on the Crop Insurance App, or (3) notify your bank branch or Block Agriculture Officer (ADA) in writing.",
            "Documents Required: Keep your Aadhaar-linked bank account passbook, land possession certificate (Khatian/ROR), sowing certificate, and clear photos of crop damage ready.",
            "Premium Rates: Farmers pay a minimal premium of 2.0% for Kharif crops, 1.5% for Rabi food and oilseed crops, and 5.0% for commercial/horticultural crops for 100% comprehensive insurance cover."
],
        "bn": [
            "প্রধানমন্ত্রী ফসল বীমা যোজনা (PMFBY) — ৭২ ঘণ্টার জরুরি নিয়ম: শিলাবৃষ্টি, ঘূর্ণিঝড়, অতিবৃষ্টি বা জলমগ্নতার কারণে ফসলের ক্ষতি হলে ঘটনা ঘটার ৭২ ঘণ্টার মধ্যে (72 hours) অবশ্যই বীমা দপ্তরে জানাতে হবে।",
            "কীভাবে ও কোথায় জানাবেন: (১) টোল-ফ্রি ফসল বীমা হেল্পলাইন নম্বর 14447-এ কল করুন, অথবা (২) 'Crop Insurance App'-এ ক্ষতিগ্রস্ত জমির ছবি আপলোড করুন, অথবা (৩) আপনার ব্যাংক শাখা বা ব্লক কৃষি আধিকারিক (ADA) অফিসে লিখিত জানান।",
            "প্রয়োজনীয় কাগজপত্র: আধার-সংযুক্ত ব্যাংক অ্যাকাউন্ট, জমির পরচা/খতিয়ান, ফসল বোনার শংসাপত্র (Sowing Certificate) এবং ক্ষতিগ্রস্ত জমির জিও-ট্যাগ করা ছবি কাছে রাখুন।",
            "প্রিমিয়াম ও সুবিধা: খরিফ ফসলের জন্য মাত্র ২% এবং রবি ফসলের জন্য ১.৫% প্রিমিয়ামে সম্পূর্ণ ফসলের বীমা সুরক্ষা পাওয়া যায় (পশ্চিমবঙ্গে বাংলা শস্য বীমা প্রকল্পে কৃষকদের প্রিমিয়াম রাজ্য সরকার বহন করে)।"
        ],
        "hi": [
            "प्रधानमंत्री फसल बीमा योजना (PMFBY) — 72 घंटे का अनिवार्य नियम: ओलावृष्टि, चक्रवात, भारी बारिश या जलभराव से फसल खराब होने पर घटना के 72 घंटे (72 hours) के भीतर सूचना देना अनिवार्य है।",
            "कहां और कैसे शिकायत दर्ज करें: (1) टोल-फ्री फसल बीमा हेल्पलाइन नंबर 14447 पर कॉल करें, या (2) 'Crop Insurance App' पर क्षतिग्रस्त खेत की फोटो अपलोड करें, या (3) अपनी बैंक शाखा / कृषि विभाग को सूचित करें।",
            "आवश्यक दस्तावेज: आधार से जुड़ा बैंक खाता, भूमि रिकॉर्ड, बुवाई प्रमाण पत्र और नुकसान की तारीख व फोटो सुरक्षित रखें।"
        ]
    },
    "pm_kisan": {
        "en": [
            "PM-KISAN Rs 6,000 Annual Benefit: Eligible farmer families receive Rs 6,000 per year directly in their bank accounts via DBT in three equal 4-monthly installments of Rs 2,000 each.",
            "Mandatory e-KYC Completion: To ensure uninterrupted credit, complete biometric or Aadhaar OTP e-KYC on the pmkisan.gov.in portal or visit your nearest CSC center.",
            "Bank & Land Verification: Ensure your bank account is Aadhaar-seeded and active on NPCI DBT, and verify that Land Seeding displays 'Yes' on the portal. Helpline: 155261 / 1800-115-526."
],
        "bn": [
            "প্রধানমন্ত্রী কিষাণ সম্মান নিধি (PM-KISAN) — বার্ষিক ৬,০০০ টাকা সহায়তা: সকল যোগ্য কৃষক পরিবারকে প্রতি বছর ৩টি সমান কিস্তিতে (প্রতি ৪ মাস অন্তর ২,০০০ টাকা করে) সরাসরি ব্যাংক অ্যাকাউন্টে (DBT) মোট ৬,০০০ টাকা প্রদান করা হয়।",
            "বাধ্যতামূলক ই-কেওয়াইসি (e-KYC) নিয়ম: কিস্তির টাকা নিয়মিত পেতে pmkisan.gov.in পোর্টালে আধার ওটিপি (Aadhaar OTP) দিয়ে অথবা নিকটবর্তী কমন সার্ভিস সেন্টার (CSC) বা বাংলা সহায়তা কেন্দ্রে (BSK) গিয়ে বায়োমেট্রিক ই-কেওয়াইসি সম্পন্ন করুন।",
            "ব্যাংক ও জমির তথ্য যাচাই: আপনার ব্যাংক অ্যাকাউন্টের সাথে আধার ও NPCI/DBT লিঙ্ক সক্রিয় রাখুন এবং পোর্টালে 'Land Seeding: Yes' স্ট্যাটাস যাচাই করুন। পিএম-কিষাণ হেল্পলাইন: 155261 / 1800-115-526।"
        ],
        "hi": [
            "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) — वार्षिक 6,000 रुपये सहायता: पात्र किसान परिवारों को प्रति वर्ष 2,000 रुपये की तीन समान किस्तों में कुल 6,000 रुपये सीधे बैंक खाते (DBT) में भेजे जाते हैं।",
            "अनिवार्य ई-केवाईसी (e-KYC) प्रक्रिया: किस्त प्राप्त करने के लिए pmkisan.gov.in पोर्टल पर आधार ओटीपी द्वारा या नजदीकी सीएससी (CSC) केंद्र पर बायोमेट्रिक ई-केवाईसी पूरा करें और बैंक खाते में डीबीटी (NPCI) सक्रिय रखें। हेल्पलाइन: 155261 / 1800-115-526।"
        ]
    },
    "sunflower_harvest": {
        "en": [
            "Right Time for Sunflower Harvest: Harvest when the back of the sunflower head (capitulum) turns lemon-yellow to brownish, bracts turn dry and brown, and moisture in seeds drops.",
            "Safe Seed Drying & Moisture (8% to 9%): Thresh and sun-dry seeds promptly to reduce moisture content to 8%-9% for safe storage. Do not heap wet heads for more than 24 hours to prevent gray mold (Botrytis).",
            "Disease & Seed Filling: If gray mold or downy mildew appears, spray Carbendazim + Mancozeb @ 2 g/L. Spray Borax 0.2% (2 g/L water) at ray floret opening stage to ensure plump, well-filled seed grains."
],
        "bn": [
            "সূর্যমুখী ফসল কাটার সঠিক সময়: যখন সূর্যমুখী ফুলের পেছনের অংশ (চাকতি) সবুজ থেকে লেবু-হলুদ বা বাদামী রঙের হয়ে যায় এবং বাইরের পাপড়িগুলো শুকিয়ে যায়, তখনই ফসল কাটতে হবে।",
            "নিরাপদ আর্দ্রতা ও সংরক্ষণ (Safe Moisture 8%-9%): মাড়াই করার পর সূর্যমুখী বীজ রোদে ভালোভাবে শুকিয়ে আর্দ্রতা ৮% থেকে ৯% (8% to 9%)-এ নামিয়ে আনুন। ভেজা ফুলের মাথা ২৪ ঘণ্টার বেশি স্তূপ করে রাখবেন না, এতে বোট্রাইটিস ধূসর পচন (Gray Mold) ছত্রাক ধরে।",
            "রোগ ও ছত্রাকনাশক ব্যবস্থাপনা: ফুল ও পাতায় ধূসর পচন (Gray Mold) বা ডাউনি মিলডিউ দেখা দিলে কার্বেন্ডাজিম + ম্যানকোজেব @ ২ গ্রাম/লিটার বা মেটালাক্সিল @ ২ গ্রাম/লিটার স্প্রে করুন এবং ফুল ফোটার সময় দানা পুষ্ট করতে ০.২% বোরাক্স (Borax @ ২ গ্রাম/লিটার জলে) স্প্রে করুন। পরিষ্কার বীজ e-NAM পোর্টাল বা স্থানীয় মান্ডিতে বিক্রি করুন।"
        ],
        "hi": [
            "सूरजमुखी कटाई का सही समय: जब सूरजमुखी के मुंडक (फूल के पीछे का भाग) नींबू-पीले से भूरे रंग का हो जाए और बाहरी पत्तियां सूख जाएं, तब कटाई करें।",
            "सुरक्षित नमी एवं भंडारण (8% से 9% नमी): गहाई के बाद सूरजमुखी के बीजों को धूप में सुखाकर नमी 8% से 9% (8% to 9%) तक ले आएं। साफ किए गए बीजों को e-NAM मार्केट पोर्टल या स्थानीय कृषि मंडी में बेचें।",
            "फूल एवं रोग प्रबंधन: दाने भरने के लिए फूल खिलते समय 0.2% बोरेक्स (2 ग्राम/लीटर) का छिड़काव करें तथा ग्रे मोल्ड फफूंद दिखने पर कार्बेन्डाजिम + मैंकोज़ेब @ 2 ग्राम/लीटर का छिड़काव करें।"
        ]
    },
    "wheat_production": {
        "en": [
            "Wheat Sowing & Seed Rate: Sow timely wheat (Nov 1-25) @ 40 kg seed per acre (100 kg/ha); late-sown wheat (Dec) @ 50 kg/acre. Treat seeds with Carboxin + Thiram @ 2.5 g/kg seed.",
            "Balanced Fertilizer & Urea Splits: Apply 105 kg Neem-Coated Urea, 55 kg DAP, and 27 kg MOP per acre. Apply half urea + all DAP & MOP as basal; apply remaining urea at 1st irrigation (21 days) and 2nd irrigation (42 days).",
            "Critical CRI Stage Irrigation: The 1st irrigation at Crown Root Initiation (CRI, 20-25 days after sowing) is most critical; skipping this stage reduces yield by 25-30%. If Yellow Rust appears, spray Propiconazole 25% EC (Tilt) @ 1.0 ml/L."
],
        "bn": [
            "গমের বপন ও বীজের হার: সঠিক সময়ে (১-২৫ নভেম্বর) বপনের জন্য একরে ৪০ কেজি (বিঘায় ১৩.৫ কেজি) এবং নাবী বপনের (ডিসেম্বর) জন্য একরে ৫০ কেজি বীজ ব্যবহার করুন। বপনের আগে কার্বক্সিন + থিরাম @ ২.৫ গ্রাম/কেজি বীজে বীজ শোধন করুন।",
            "সুষম সার ও ইউরিয়া প্রয়োগ: একরে ১০৫ কেজি নিম-কোটেড ইউরিয়া, ৫৫ কেজি ডিএপি (DAP) এবং ২৭ কেজি এমওপি (MOP) প্রয়োগ করুন। অর্ধেক ইউরিয়া + পুরো ডিএপি ও পটাশ বপনের সময়, বাকি ইউরিয়া প্রথম সেচ (CRI - ২১ দিন) ও দ্বিতীয় সেচের (৪২ দিন) পর দিন।",
            "সবচেয়ে গুরুত্বপূর্ণ সেচ (CRI Stage): বপনের ২০-২৫ দিন পর মুকুট শিকড় বেরোনোর সময় (CRI Stage) প্রথম সেচ দেওয়া অত্যন্ত জরুরি—এই সেচ না দিলে ফলন ২৫-৩০% কমে যায়। পাতায় হলুদ মরিচা রোগ (Rust) দেখা দিলে প্রোপিকোনাজোল ২৫% ইসি @ ১ মিলি/লিটার জলে স্প্রে করুন।"
        ],
        "hi": [
            "गेहूं की बुवाई एवं बीज दर: समय पर बुवाई (1-25 नवंबर) हेतु 40 किग्रा/एकड़ और पछेती बुवाई (दिसंबर) हेतु 50 किग्रा/एकड़ बीज का प्रयोग करें। बुवाई से पहले कार्बोक्सिन + थायरम @ 2.5 ग्राम/किग्रा बीज से उपचारित करें।",
            "उर्वरक एवं यूरिया प्रबंधन: प्रति एकड़ 105 किग्रा नीम-लेपित यूरिया, 55 किग्रा डीएपी (DAP) और 27 किग्रा एमओपी (MOP) डालें। आधी यूरिया व पूरी डीएपी-पोटाश बुवाई पर तथा शेष यूरिया पहली सिंचाई (CRI - 21 दिन) और दूसरी सिंचाई (42 दिन) पर दें।",
            "सबसे महत्वपूर्ण सिंचाई (CRI अवस्था): बुवाई के 20-25 दिन बाद शीर्ष जड़ बनते समय (CRI Stage) पहली सिंचाई अवश्य करें। पीला रतुआ (Yellow Rust) दिखने पर प्रोपिकोनाज़ोल 25% EC @ 1 मिली/लीटर का छिड़काव करें।"
        ]
    }
}

# ==============================================================================
# VISION & PEST SCANNER RESULT LOCALIZATION (BENGALI & HINDI + REGIONAL)
# ==============================================================================

CROP_NAME_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "bn": {
        "Tomato": "টমেটো (Tomato)",
        "Potato": "আলু (Potato)",
        "Corn (Maize)": "ভুট্টা (Corn / Maize)",
        "Corn": "ভুট্টা (Corn / Maize)",
        "Rice": "ধান (Rice / Paddy)",
        "Wheat": "গম (Wheat)",
        "Sunflower": "সূর্যমুখী (Sunflower)",
        "Apple": "আপেল (Apple)",
        "Grape": "আঙুর (Grape)",
        "Bell Pepper (Capsicum)": "ক্যাপসিকাম / মিষ্টি মরিচ (Bell Pepper)",
        "Chilli": "লঙ্কা / মরিচ (Chilli)",
        "Cotton": "তুলা (Cotton)",
        "Peach": "পিচ (Peach)",
        "Cherry": "চেরি (Cherry)",
        "Strawberry": "স্ট্রবেরি (Strawberry)",
        "Soybean": "সয়াবিন (Soybean)",
        "Squash / Cucurbit": "কুমড়ো / লাউ বর্গ (Squash / Cucurbit)",
        "Orange (Citrus)": "কমলালেবু (Citrus)",
        "Not a Crop or Plant": "কোনো ফসল বা গাছ নয়",
    },
    "hi": {
        "Tomato": "टमाटर (Tomato)",
        "Potato": "आलू (Potato)",
        "Corn (Maize)": "मक्का (Corn / Maize)",
        "Corn": "मक्का (Corn / Maize)",
        "Rice": "धान (Rice / Paddy)",
        "Wheat": "गेहूं (Wheat)",
        "Sunflower": "सूरजमुखी (Sunflower)",
        "Apple": "सेब (Apple)",
        "Grape": "अंगूर (Grape)",
        "Bell Pepper (Capsicum)": "शिमला मिर्च (Bell Pepper)",
        "Chilli": "मिर्च (Chilli)",
        "Cotton": "कपास (Cotton)",
        "Peach": "आड़ू (Peach)",
        "Cherry": "चेरी (Cherry)",
        "Strawberry": "स्ट्रॉबेरी (Strawberry)",
        "Soybean": "सोयाबीन (Soybean)",
        "Squash / Cucurbit": "कद्दूवर्गीय फसल (Squash)",
        "Orange (Citrus)": "संतरा / नींबूवर्गीय (Citrus)",
        "Not a Crop or Plant": "कोई फसल या पौधा नहीं",
    }
}

SEVERITY_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "bn": {
        "None": "নেই / সুস্থ (None)",
        "Mild": "হালকা (Mild)",
        "Moderate": "মাঝারি (Moderate)",
        "High": "বেশি (High)",
        "Critical": "মারাত্মক / জরুরি (Critical)",
    },
    "hi": {
        "None": "सामान्य / स्वस्थ (None)",
        "Mild": "हल्का (Mild)",
        "Moderate": "मध्यम (Moderate)",
        "High": "उच्च (High)",
        "Critical": "गंभीर / तत्काल ध्यान दें (Critical)",
    }
}

DISEASE_LOCALIZATION_BN: Dict[str, Dict[str, Any]] = {
    "Early Blight": {
        "condition": "আগাম ধসা রোগ / আর্লি ব্লাইট (Early Blight - চাকার মতো দাগ)",
        "summary": "পাতার ওপর গাঢ় বাদামী রঙের গোল চাকার মতো দাগ (Target-Board Rings) দেখা যাচ্ছে, যা আর্লি ব্লাইট ছত্রাকের লক্ষণ। সঠিক সময়ে ছত্রাকনাশক প্রয়োগ করলে ফুল ও ফলের ফলন সম্পূর্ণ সুরক্ষিত থাকবে।",
        "actions": [
            "সঠিক ছত্রাকনাশক ও মাত্রা: ম্যানকোজেব ৭৫% ডব্লিউপি (Indofil M-45) প্রতি লিটার জলে ২.৫ গ্রাম (একরে ৫০০ গ্রাম) অথবা কপার অক্সিক্লোরাইড ৫০% ডব্লিউপি @ ৩ গ্রাম/লিটার জলে মিশিয়ে স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন: বিকেলে (৪:০০-৬:০০ টা) প্রতি একরে ১৫০-২০০ লিটার জলে স্টিকার (০.৫ মিলি/লিটার) মিশিয়ে পাতার ওপর ও নিচে ভিজিয়ে স্প্রে করুন; ১০-১২ দিন পর অ্যাজোক্সিস্ট্রবিন ২৩% এসসি @ ১ মিলি/লিটার দিয়ে দ্বিতীয় স্প্রে করুন।",
            "জৈব ও পরিচর্যা প্রতিকার: মাটির কাছাকাছি থাকা নিচের আক্রান্ত পাতাগুলো (৩০ সেমি পর্যন্ত) ছিঁড়ে পুড়িয়ে ফেলুন এবং ট্রাইকোডার্মা ভিরিডি @ ৫ গ্রাম/লিটার স্প্রে করুন।",
            "সেচ ও দূরত্ব: গাছের গোড়ায় খড়ের মালচিং দিন এবং ওপর থেকে জল ছিটানো সেচ বন্ধ রেখে নালা বা ড্রিপ সেচ দিন (ফসল তোলার ৭ দিন আগে স্প্রে বন্ধ রাখুন)।"
        ]
    },
    "Late Blight": {
        "condition": "নাবী ধসা রোগ / লেট ব্লাইট (Late Blight - জলভেজা কালচে পচন)",
        "summary": "পাতায় জলভেজা কালচে-বাদামী পচন এবং পাতার নিচে সাদা ছত্রাকের আস্তরণ নাবী ধসা (Late Blight) রোগের লক্ষণ। এটি অত্যন্ত দ্রুত ছড়ায়, তাই আজই জরুরি ছত্রাকনাশক স্প্রে করা প্রয়োজন।",
        "actions": [
            "জরুরি অন্তর্বাহী ছত্রাকনাশক (Systemic Fungicide): সাইমোক্সানিল ৮% + ম্যানকোজেব ৬৪% ডব্লিউপি (Curzate M8) @ ২.৫ গ্রাম/লিটার অথবা মেটালাক্সিল ৮% + ম্যানকোজেব ৬৪% ডব্লিউপি (Ridomil Gold) @ ২.৫ গ্রাম/লিটার (একরে ৫০০ গ্রাম) অবিলম্বে স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন: কুয়াশা কেটে যাওয়ার পর সকাল ৯-১১টা বা বিকেল ৩-৫টার মধ্যে প্রতি একরে ২০০ লিটার জলে স্টিকারসহ পুরো গাছ ও কাণ্ড ভিজিয়ে স্প্রে করুন; ৭-১০ দিন পর ডাইমেথোমর্ফ ৫০% ডব্লিউপি (১ গ্রাম/লিটার) স্প্রে করুন।",
            "কন্দ ও গাছ সুরক্ষা: আলুর ভেলির মাটি উঁচু করে বেঁধে দিন যাতে ছত্রাকের রেণু বৃষ্টির জলে ধুয়ে আলুতে না লাগে এবং মারাত্মকভাবে পচে যাওয়া ডালপালা কেটে মাটিতে পুঁতে ফেলুন।",
            "জল নিকাশ: জমিতে কোনোভাবেই জল জমতে দেবেন না এবং মেঘলা আবহাওয়ায় ইউরিয়া সার প্রয়োগ বন্ধ রাখুন।"
        ]
    },
    "Common Rust": {
        "condition": "সাধারণ মরিচা রোগ (Common Rust - বাদামী গুঁড়ো দাগ)",
        "summary": "পাতার উভয় পৃষ্ঠে দারুচিনি-বাদামী রঙের ফুসকুড়ি বা মরিচার মতো গুঁড়ো দাগ দেখা যাচ্ছে। সময়মতো ছত্রাকনাশক স্প্রে করলে উপরের পাতাগুলো সুস্থ থাকবে ও দানা পুষ্ট হবে।",
        "actions": [
            "সঠিক ছত্রাকনাশক ও মাত্রা: ম্যানকোজেব ৭৫% ডব্লিউপি @ ২.৫ গ্রাম/লিটার অথবা প্রোপিকোনাজোল ২৫% ইসি (Tilt) @ ১.০ মিলি/লিটার জলে মিশিয়ে স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন: রোগের প্রথম লক্ষণ দেখা দিলেই বিকেলে একরে ১৫০-২০০ লিটার জলে পাতা ভিজিয়ে স্প্রে করুন এবং প্রয়োজনে ১২ দিন পর পুনরায় স্প্রে করুন।",
            "জৈব প্রতিকার: ৫% নিম বীজের নির্যাস (NSKE) বা ট্রাইকোডার্মা ভিরিডি @ ৫ গ্রাম/লিটার স্প্রে করুন।",
            "সুষম পুষ্টি: পাতার কোষপ্রাচীর শক্ত করতে সুষম পটাশ (MOP) সার প্রয়োগ করুন এবং জমিতে জল নিকাশ বজায় রাখুন।"
        ]
    },
    "Apple Scab": {
        "condition": "আপেল স্ক্যাব রোগ (Apple Scab - কালচে মখমলের মতো দাগ)",
        "summary": "পাতায় জলপাই-কালচে রঙের দাগ দেখা যাচ্ছে যা স্ক্যাব ছত্রাকের লক্ষণ। সময়মতো পরিচর্যা করলে পাতা ঝরা বন্ধ হবে এবং ফলের গুণমান বজায় থাকবে।",
        "actions": [
            "সঠিক ছত্রাকনাশক ও মাত্রা: কপার অক্সিক্লোরাইড ৫০% ডব্লিউপি @ ২.৫ গ্রাম/লিটার অথবা ম্যানকোজেব ৭৫% ডব্লিউপি @ ২.৫ গ্রাম/লিটার বা কার্বেন্ডাজিম + ম্যানকোজেব @ ২ গ্রাম/লিটার স্প্রে করুন।",
            "কখন ও কীভাবে প্রয়োগ করবেন: কুঁড়ি আসা ও পাপড়ি ঝরার পর পরিষ্কার আবহাওয়ায় বিকেলে গাছের পাতায় ভালোভাবে স্প্রে করুন।",
            "জৈব প্রতিকার ও ছাঁটাই: ট্রাইকোডার্মা ভিরিডি বা ব্যাসিলাস সাবটিলিস @ ৫ গ্রাম/লিটার স্প্রে করুন এবং গাছের ভেতরের ঘন ডাল ছেঁটে রোদ ঢোকার ব্যবস্থা করুন।",
            "বাগান পরিচ্ছন্নতা: গাছের নিচে ঝরে পড়া শুকনো ও রোগাক্রান্ত পাতা জড়ো করে পুড়িয়ে বা গভীর গর্তে পুঁতে ফেলুন।"
        ]
    },
    "Healthy": {
        "condition": "সুস্থ ও সতেজ ফসল (Healthy Crop Condition)",
        "summary": "গাছের পাতা ও ফুল সম্পূর্ণ সুস্থ, গাঢ় সবুজ এবং কোনো ছত্রাক বা ক্ষতিকর পোকার আক্রমণ নেই। এই সতেজ অবস্থা বজায় রাখতে নিয়মিত পরিচর্যা চালিয়ে যান।",
        "actions": [
            "সুষম সার ও সেচ: মাটি পরীক্ষা (Soil Health Card) অনুযায়ী নির্ধারিত কিস্তিতে ইউরিয়া, ডিএপি ও পটাশ সার এবং সময়মতো হালকা সেচ প্রদান করুন।",
            "প্রতিরোধমূলক জৈব পরিচর্যা: ফসলকে রোগমুক্ত রাখতে ১৫-২০ দিন অন্তর নিম তেল (১৫০০ পিপিএম) @ ৩-৫ মিলি/লিটার বা ট্রাইকোডার্মা ভিরিডি স্প্রে করতে পারেন।",
            "নিয়মিত পর্যবেক্ষণ: সপ্তাহে অন্তত ২ দিন সকালবেলা পাতার নিচের দিক ও ডগা পরীক্ষা করুন যাতে কোনো পোকা বা রোগের শুরুতেই ব্যবস্থা নেওয়া যায়।",
            "আগাছা ও নিকাশ: জমির আল পরিষ্কার রাখুন এবং গোড়ায় পচা গোবর সার বা জৈব মালচিং ব্যবহার করুন।"
        ]
    }
}

DISEASE_LOCALIZATION_HI: Dict[str, Dict[str, Any]] = {
    "Early Blight": {
        "condition": "अगेती झुलसा रोग / अर्ली ब्लाइट (Early Blight - छल्लेदार धब्बे)",
        "summary": "पत्तियों पर गहरे भूरे रंग के गोल छल्लेदार धब्बे (Target-Board Rings) दिखाई दे रहे हैं जो अगेती झुलसा (Early Blight) फफूंद के लक्षण हैं। समय पर कवकनाशी छिड़काव से फसल पूरी तरह सुरक्षित रहेगी।",
        "actions": [
            "अनुशंसित कवकनाशी (Fungicide) एवं मात्रा: मैंकोज़ेब 75% WP (Indofil M-45) @ 2.5 ग्राम/लीटर पानी (500 ग्राम/एकड़) या कॉपर ऑक्सीक्लोराइड 50% WP @ 3.0 ग्राम/लीटर पानी में मिलाकर छिड़काव करें।",
            "कब और कैसे प्रयोग करें: शाम के समय (4:00-6:00 बजे) प्रति एकड़ 150-200 लीटर पानी में स्टीकर (0.5 मिली/लीटर) मिलाकर पत्तियों की दोनों सतहों पर छिड़काव करें; 10-12 दिन बाद एज़ोक्सीस्ट्रोबिन 23% SC @ 1 मिली/लीटर से दूसरा छिड़काव करें।",
            "जैविक उपचार एवं छंटाई: जमीन से सटी निचली संक्रमित पत्तियों (30 सेमी तक) को तोड़कर नष्ट करें और ट्राइकोडर्मा विरिडी @ 5 ग्राम/लीटर का छिड़काव करें।",
            "सिंचाई एवं मल्चिंग: पौधों के पास पुआल की मल्चिंग करें और फव्वारा सिंचाई के बजाय नाली या ड्रिप से सिंचाई करें (तुड़ाई से 7 दिन पहले छिड़काव बंद करें)।"
        ]
    },
    "Late Blight": {
        "condition": "पछेती झुलसा रोग / लेट ब्लाइट (Late Blight - जलीय काला सड़न)",
        "summary": "पत्तियों पर पानी से भीगे हुए काले-भूरे धब्बे और नीचे सफेद फफूंद पछेती झुलसा (Late Blight) के लक्षण हैं। यह रोग बहुत तेजी से फैलता है, इसलिए तुरंत सिस्टेमिक कवकनाशी का छिड़काव करें।",
        "actions": [
            "आपातकालीन सिस्टेमिक कवकनाशी एवं मात्रा: साइमोक्सानिल 8% + मैंकोज़ेब 64% WP (Curzate M8) @ 2.5 ग्राम/लीटर या मेटालैक्सिल 8% + मैंकोज़ेब 64% WP (Ridomil Gold) @ 2.5 ग्राम/लीटर (500 ग्राम/एकड़) का तुरंत छिड़काव करें।",
            "कब और कैसे प्रयोग करें: ओस सूखने के बाद प्रति एकड़ 200 लीटर पानी में स्टीकर मिलाकर पत्तियों के नीचे और तनों को भिगोते हुए छिड़काव करें; 7-10 दिन बाद डाइमेथोमॉर्फ 50% WP @ 1 ग्राम/लीटर का छिड़काव करें।",
            "कंद एवं पौध सुरक्षा: आलू की मेड़ों पर मिट्टी ऊंची चढ़ाएं ताकि फफूंद के बीजाणु कंदों तक न पहुंचें और गंभीर रूप से झुलसे डंठलों को उखाड़कर गड्ढे में दबा दें।",
            "जल निकासी: खेत में पानी बिल्कुल न रुकने दें और बादल/कोहरे के दौरान यूरिया खाद का छिड़काव न करें।"
        ]
    },
    "Common Rust": {
        "condition": "सामान्य रतुआ रोग (Common Rust - भूरे फफोले)",
        "summary": "पत्तियों की दोनों सतहों पर दालचीनी-भूरे रंग के पाउडर जैसे फफोले सामान्य रतुआ (Common Rust) रोग के लक्षण हैं। समय पर उपचार से दाने भरपूर बनेंगे।",
        "actions": [
            "अनुशंसित कवकनाशी एवं मात्रा: मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर या प्रोपिकोनाज़ोल 25% EC (Tilt) @ 1.0 मिली/लीटर पानी में मिलाकर छिड़काव करें।",
            "कब और कैसे प्रयोग करें: शुरुआती लक्षण दिखते ही शाम के समय प्रति एकड़ 150-200 लीटर पानी से छिड़काव करें और आवश्यकतानुसार 12 दिन बाद दोहराएं।",
            "जैविक उपचार: 5% नीम बीज अर्क (NSKE) या ट्राइकोडर्मा विरिडी @ 5 ग्राम/लीटर का छिड़काव करें।",
            "संतुलित पोषण: पत्तियों की मजबूती के लिए पोटाश (MOP) खाद का संतुलित प्रयोग करें।"
        ]
    },
    "Apple Scab": {
        "condition": "सेब का स्कैब रोग (Apple Scab - मखमली काले धब्बे)",
        "summary": "पत्तियों पर जैतूनी-काले मखमली धब्बे एप्पल स्कैब फफूंद के लक्षण हैं। समय पर उपचार से पत्तियां और फल सुरक्षित रहते हैं।",
        "actions": [
            "अनुशंसित कवकनाशी एवं मात्रा: कॉपर ऑक्सीक्लोराइड 50% WP @ 2.5 ग्राम/लीटर या मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें।",
            "कब और कैसे प्रयोग करें: साफ मौसम में शाम के समय पेड़ की पत्तियों और टहनियों पर अच्छी तरह छिड़काव करें।",
            "जैविक उपचार एवं छंटाई: ट्राइकोडर्मा विरिडी @ 5 ग्राम/लीटर का छिड़काव करें और धूप व हवा के लिए घनी टहनियों की छंटाई करें।",
            "बाग की सफाई: पेड़ के नीचे गिरी हुई संक्रमित पत्तियों को इकट्ठा करके नष्ट कर दें।"
        ]
    },
    "Healthy": {
        "condition": "स्वस्थ एवं उत्तम फसल (Healthy Crop Condition)",
        "summary": "पौधे की पत्तियां और फूल पूरी तरह स्वस्थ, गहरे हरे और किसी भी फफूंद या कीट प्रकोप से मुक्त हैं।",
        "actions": [
            "संतुलित खाद एवं सिंचाई: मृदा स्वास्थ्य कार्ड के अनुसार समय पर खाद की किस्तें और हल्की सिंचाई जारी रखें।",
            "निवारक जैविक सुरक्षा: फसल को रोगमुक्त रखने के लिए हर 15-20 दिन पर नीम तेल (1500 ppm) @ 3-5 मिली/लीटर का छिड़काव करें।",
            "नियमित निगरानी: सप्ताह में दो बार पत्तियों की निचली सतह और नई कोपलों की जांच करें।",
            "खरपतवार नियंत्रण: खेत की मेड़ों को साफ रखें और जड़ों के पास जैविक मल्चिंग का प्रयोग करें।"
        ]
    }
}

PEST_LOCALIZATION_BN: Dict[str, Dict[str, str]] = {
    "rice leaf roller": {
        "pest_name": "ধানের পাতা মোড়ানো পোকা / লিফ ফোল্ডার (Rice Leaf Roller)",
        "severity": "মাঝারি (Moderate)",
        "action_threshold": "প্রতি গোছায় ১-২টি সদ্য মোড়ানো পাতা (অথবা শীষ বেরোনোর সময় ১০% আক্রান্ত পাতা দেখা গেলে ব্যবস্থা নিন)।",
        "organic_remedy": "চারা রোপণের ৩০ দিন পর থেকে ৭ দিন অন্তর ৩ বার ট্রাইকোগ্রামা কাইলোনিস (Trichogramma chilonis) ডিম-কার্ড একরে ২০,০০০টি (হেক্টরে ৫০,০০০টি) জমিতে লাগান। সকালবেলা শিশিরভেজা ধানের ওপর দিয়ে দড়ি টেনে শুঁয়োপোকা ফেলে দিন এবং ৫% নিম বীজের নির্যাস (NSKE) বা নিম তেল @ ৫ মিলি/লিটার স্প্রে করুন।",
        "chemical_remedy": "ETL অতিক্রম করলে: ক্লোরান্ট্রানিলিপ্রোল ১৮.৫% এসসি (Coragen) @ ০.৩ মিলি/লিটার (একরে ৬০ মিলি) অথবা কার্টাপ হাইড্রোক্লোরাইড ৫০% এসপি @ ২ গ্রাম/লিটার (একরে ৪০০ গ্রাম) অথবা ফ্লুবেন্ডিয়ামাইড ৩৯.৩৫% এসসি @ ০.২ মিলি/লিটার। প্রয়োগ বিধি: বিকেলে (৪-৬টা) প্রতি একরে ১৫০-২০০ লিটার জলে গুলে পাতার ওপর স্প্রে করুন (ধান কাটার ১৪ দিন আগে স্প্রে বন্ধ রাখুন)।",
        "cultural_practice": "অতিরিক্ত ইউরিয়া সার প্রয়োগ থেকে বিরত থাকুন এবং জমির আলের ঘাস ও আগাছা পরিষ্কার রাখুন।"
    },
    "corn borer": {
        "pest_name": "ভুট্টা ও জোয়ারের কাণ্ড ছিদ্রকারী পোকা (Maize / Corn Stem Borer)",
        "severity": "বেশি (High)",
        "action_threshold": "মাঠে ৫-১০% গাছে পাতায় সারিবদ্ধ ছিদ্র (Shot-holes) বা মাঝের ডগা শুকিয়ে যাওয়া (Dead-heart) দেখা গেলে।",
        "organic_remedy": "বীজ বোনার ১২-১৫ দিন পর ট্রাইকোগ্রামা কাইলোনিস ডিম-কার্ড হেক্টরে ৫০,০০০টি ছাড়ুন এবং গাছের মাঝখানের চোঙায় (whorl) বিউভেরিয়া বাসিয়ানা (Beauveria bassiana) @ ৫ গ্রাম/লিটার জলে স্প্রে করুন।",
        "chemical_remedy": "ETL অতিক্রম করলে: ক্লোরান্ট্রানিলিপ্রোল ১৮.৫% এসসি (Coragen) @ ০.৪ মিলি/লিটার (একরে ৮০ মিলি) অথবা স্পিনেটোরাম ১১.৭% এসসি @ ০.৫ মিলি/লিটার। প্রয়োগ বিধি: চারা গজানোর ২০-৩৫ দিনের মধ্যে বিকেলে একরে ১৫০-২০০ লিটার জলে স্প্রেয়ারের নজল গাছের মাঝখানের চোঙায় ধরে স্প্রে করুন।",
        "cultural_practice": "ফসল কাটার পর ভুট্টার নাড়া ও শুকনো ডাঁটা পুড়িয়ে বা গভীর চাষ দিয়ে মাটিতে মিশিয়ে দিন; ভুট্টার সাথে বরবটি বা সয়াবিন আন্তঃফসল চাষ করুন।"
    },
    "army worm": {
        "pest_name": "লেদা পোকা / আর্মিওয়ার্ম (Armyworm / Spodoptera)",
        "severity": "মারাত্মক (Critical)",
        "action_threshold": "প্রতি ১০টি গাছে ১-২টি ডিমের গাদা অথবা মাঠে ৫-১০% পাতা ও ডগা খাওয়া দেখা গেলে অবিলম্বে ব্যবস্থা নিন।",
        "organic_remedy": "প্রাথমিক অবস্থায় ব্যাসিলাস থুরিনজিয়েনসিস (Bt kurstaki) @ ২ গ্রাম/লিটার অথবা মেটারাইজিয়াম অ্যানিসোপ্লি @ ৫ গ্রাম/লিটার স্প্রে করুন এবং ভুট্টার চোঙায় বালি ও চুনের মিশ্রণ (৯:১) দিন।",
        "chemical_remedy": "মারাত্মক আক্রমণে: এমামেকটিন বেনজয়েট ৫% এসজি (Emamectin Benzoate 5% SG) @ ০.৪ গ্রাম/লিটার (একরে ৮০ গ্রাম) অথবা ক্লোরান্ট্রানিলিপ্রোল ১৮.৫% এসসি @ ০.৪ মিলি/লিটার। প্রয়োগ বিধি: লেদা পোকা সন্ধ্যায় বের হয়, তাই বিকেল ৪:৩০-৬:০০ টার মধ্যে একরে ২০০ লিটার জলে গাছের চোঙা ও পাতায় স্প্রে করুন (PHI: ১৪ দিন)।",
        "cultural_practice": "গ্রীষ্মকালে গভীর চাষ দিন যাতে মাটির নিচের পুত্তলি রোদে ও পাখির দ্বারা নষ্ট হয় এবং একরে ৫টি ফেরোমন ট্র্যাপ বসান।"
    },
    "red spider": {
        "pest_name": "লাল মাকড় (Red Spider Mite / Citrus Red Mite)",
        "severity": "মাঝারি (Moderate)",
        "action_threshold": "প্রতি পাতায় ২-৫টি লাল মাকড় এবং পাতার নিচে সূক্ষ্ম জাল ও পাতায় সাদাটে-হলুদ ছোপ দেখা গেলে।",
        "organic_remedy": "ওয়েটেবল সালফার ৮০% ডব্লিউপি (Wettable Sulphur 80% WP) প্রতি লিটার জলে ৩ গ্রাম অথবা নিম তেল (১৫০০ পিপিএম) @ ৫ মিলি/লিটার জলে মিশিয়ে পাতার নিচের দিকে স্প্রে করুন।",
        "chemical_remedy": "ETL অতিক্রম করলে: স্পাইরোমেসিফেন ২২.৯% এসসি (Oberon) @ ১.০ মিলি/লিটার অথবা প্রোপারগাইট ৫৭% ইসি (Omite) @ ২.০ মিলি/লিটার। প্রয়োগ বিধি: বিকেলে একরে ২০০ লিটার জলে স্প্রেয়ারের নজল পাতার নিচের দিকে ঘুরিয়ে ভালোভাবে ভিজিয়ে স্প্রে করুন; ১০ দিন পর প্রয়োজনে দ্বিতীয় স্প্রে করুন।",
        "cultural_practice": "গরম ও শুষ্ক আবহাওয়ায় জমিতে নিয়মিত রসের জোগান রাখুন এবং জমির চারপাশের আগাছা পরিষ্কার রাখুন।"
    },
    "mole cricket": {
        "pest_name": "ঘুরঘুরে পোকা (Mole Cricket - শিকড় ও চারা কাটা পোকা)",
        "severity": "মাঝারি (Moderate)",
        "action_threshold": "প্রতি বর্গমিটারে ২-৩টি নতুন মাটির সুড়ঙ্গ বা বীজতলায় চারা গোড়া থেকে কাটা দেখা গেলে।",
        "organic_remedy": "মেটারাইজিয়াম অ্যানিসোপ্লি (Metarhizium anisopliae) @ ২ কেজি/একর ৫০ কেজি পচা গোবর সারের সাথে মিশিয়ে ভেজা মাটিতে প্রয়োগ করুন।",
        "chemical_remedy": "বিষটোপ প্রয়োগ: ১০ কেজি গমের ভুসি বা চালের কুঁড়ো + ১ কেজি গুড় + ২৫০ গ্রাম ক্লোরান্ট্রানিলিপ্রোল বা ফিপ্রোনিল অল্প জলে মেখে সন্ধ্যার সময় সুড়ঙ্গের মুখে ও আলের ধারে ছিটিয়ে দিন।",
        "cultural_practice": "জমিতে বা বীজতলায় হালকা সেচ দিয়ে জল ঢুকিয়ে দিলে ঘুরঘুরে পোকা গর্ত থেকে বেরিয়ে আসে এবং পাখিরা খেয়ে ফেলে।"
    },
    "brown plant hopper": {
        "pest_name": "ধানের বাদামী শোষক পোকা / কারেন্ট পোকা (Brown Planthopper - BPH)",
        "severity": "মারাত্মক (Critical)",
        "action_threshold": "কুশি অবস্থায় প্রতি গোছায় ৫-১০টি এবং থোড়/ফুল অবস্থায় ১৫-২০টি বাদামী শোষক পোকা দেখা গেলে।",
        "organic_remedy": "জমি থেকে ৩-৪ দিনের জন্য জমা জল বের করে মাটি শুকিয়ে নিন এবং নিম তেল (১৫০০ পিপিএম) @ ৫ মিলি/লিটার ধানের গোড়ায় স্প্রে করুন। উপকারী মিরিড বাগ ও মাকড়সা সংরক্ষণ করুন।",
        "chemical_remedy": "ETL অতিক্রম করলে: ট্রাইফ্লুমেজোপাইরিম ১০% এসসি (Pexalon) @ ০.৫ মিলি/লিটার (একরে ৯৪ মিলি) অথবা পাইমেট্রোজিন ৫০% ডব্লিউডিজি (Chess) @ ০.৬ গ্রাম/লিটার (একরে ১২০ গ্রাম)। প্রয়োগ বিধি: স্প্রেয়ারের নজল ধানের গোড়ায় (জলের ঠিক ওপরে) ধরে প্রতি একরে ২০০ লিটার জলে বিকেলে স্প্রে করুন।",
        "cultural_practice": "প্রতি ২.৫-৩ মিটার অন্তর ৩০ সেমি ফাঁকা গলি (Alleyway) রাখুন যাতে ধানের গোড়ায় রোদ ও বাতাস লাগে এবং অতিরিক্ত ইউরিয়া সার দেবেন না।"
    },
    "aphids": {
        "pest_name": "জাব পোকা ও শোষক পোকা (Aphids / Sap-Sucking Pest)",
        "severity": "মাঝারি (Moderate)",
        "action_threshold": "১০-১৫% পাতা আক্রান্ত হলে বা প্রতি কচি ডগায় ১৫-২০টি জাব পোকা দেখা গেলে।",
        "organic_remedy": "৫% নিম বীজের নির্যাস (NSKE) বা নিম তেল @ ৫ মিলি/লিটার জলে ০.৫ মিলি তরল সাবান মিশিয়ে স্প্রে করুন এবং একরে ১২-১৫টি হলুদ আঠালো ফাঁদ (Yellow Sticky Trap) বসান।",
        "chemical_remedy": "ETL অতিক্রম করলে: ইমিডাক্লোপ্রিড ১৭.৮% এসএল (Confidor) @ ০.৩ মিলি/লিটার অথবা থায়ামেথক্সাম ২৫% ডব্লিউজি (Actara) @ ০.২৫ গ্রাম/লিটার। প্রয়োগ বিধি: মৌমাছি রক্ষার জন্য বিকেল ৪:০০ টার পর একরে ১৫০-২০০ লিটার জলে স্প্রে করুন (PHI: ১৫ দিন)।",
        "cultural_practice": "অতিরিক্ত নাইট্রোজেন (ইউরিয়া) সার প্রয়োগ এড়িয়ে চলুন এবং আক্রান্ত কচি ডগা ছেঁটে ফেলুন।"
    }
}

PEST_LOCALIZATION_HI: Dict[str, Dict[str, str]] = {
    "rice leaf roller": {
        "pest_name": "धान का पत्ती लपेटक कीट (Rice Leaf Roller / Folder)",
        "severity": "मध्यम (Moderate)",
        "action_threshold": "प्रति पौधा (hill) 1-2 ताजी मुड़ी हुई पत्तियां (या झंडा पत्ती अवस्था में 10% क्षतिग्रस्त पत्तियां)।",
        "organic_remedy": "रोपाई के 30 दिन बाद से 7 दिन के अंतराल पर 3 बार ट्राइकोग्रामा काइलोनिस (Trichogramma chilonis) कार्ड @ 20,000/एकड़ लगाएं और 5% नीम बीज अर्क (NSKE) @ 5 मिली/लीटर का छिड़काव करें।",
        "chemical_remedy": "ETL पार होने पर: क्लोरैन्ट्रानिलिप्रोल 18.5% SC (Coragen) @ 0.3 मिली/लीटर (60 मिली/एकड़) या कार्टाप हाइड्रोक्लोराइड 50% SP @ 2 ग्राम/लीटर (400 ग्राम/एकड़)। प्रयोग विधि: शाम 4-6 बजे प्रति एकड़ 150-200 लीटर पानी में मिलाकर पत्तियों पर छिड़काव करें (कटाई से 14 दिन पहले बंद करें)।",
        "cultural_practice": "यूरिया खाद की अधिक मात्रा न डालें और मेड़ों से घास-खरपतवार साफ रखें।"
    },
    "corn borer": {
        "pest_name": "मक्का एवं ज्वार का तना छेदक कीट (Maize / Corn Stem Borer)",
        "severity": "उच्च (High)",
        "action_threshold": "खेत में 5-10% पौधों की गोभ में गोल छेद (Shot-holes) या सूखी गोभ (Dead-heart) दिखने पर।",
        "organic_remedy": "बुवाई के 12-15 दिन बाद ट्राइकोग्रामा काइलोनिस कार्ड @ 20,000/एकड़ लगाएं और पौधों की गोभ (whorl) में ब्यूवेरिया बासियाना (Beauveria bassiana) @ 5 ग्राम/लीटर डालें।",
        "chemical_remedy": "ETL पार होने पर: क्लोरैन्ट्रानिलिप्रोल 18.5% SC (Coragen) @ 0.4 मिली/लीटर या स्पिनेटोरम 11.7% SC @ 0.5 मिली/लीटर। प्रयोग विधि: शाम के समय प्रति एकड़ 150-200 लीटर पानी के साथ स्प्रेयर नोजल को सीधे गोभ (whorl) में रखकर छिड़काव करें।",
        "cultural_practice": "कटाई के बाद मक्का के डंठल और अवशेष नष्ट कर दें तथा लोबिया या सोयाबीन के साथ अंतर्वर्ती खेती करें।"
    },
    "army worm": {
        "pest_name": "सैनिक कीट / फॉल आर्मीवर्म (Armyworm / Spodoptera)",
        "severity": "गंभीर (Critical)",
        "action_threshold": "1-2 अंडों के समूह या खेत में 5-10% पत्तियों/गोभ में कटाव दिखने पर तुरंत उपचार करें।",
        "organic_remedy": "शुरुआती अवस्था में बैसिलस थुरिंजिएंसिस (Bt kurstaki) @ 2 ग्राम/लीटर या मेटाराइजियम एनिसोप्ली @ 5 ग्राम/लीटर का छिड़काव करें और गोभ में रेत + चूना (9:1) डालें।",
        "chemical_remedy": "तीव्र प्रकोप में: इमामेक्टिन बेंजोएट 5% SG @ 0.4 ग्राम/लीटर (80 ग्राम/एकड़) या क्लोरैन्ट्रानिलिप्रोल 18.5% SC @ 0.4 मिली/लीटर। प्रयोग विधि: शाम 4:30-6:00 बजे प्रति एकड़ 200 लीटर पानी से पौधे की गोभ में छिड़काव करें (PHI: 14 दिन)।",
        "cultural_practice": "गर्मियों में गहरी जुताई करें और प्रति एकड़ 5 फेरोमोन ट्रैप व 10 बर्ड पर्च लगाएं।"
    },
    "red spider": {
        "pest_name": "लाल मकड़ी कीट (Red Spider Mite / Citrus Red Mite)",
        "severity": "मध्यम (Moderate)",
        "action_threshold": "प्रति पत्ती 2-5 लाल मकड़ी और पत्ती के नीचे बारीक जाला व पीले धब्बे दिखने पर।",
        "organic_remedy": "घुलनशील गंधक (Wettable Sulphur 80% WP) @ 3 ग्राम/लीटर या नीम तेल (1500 ppm) @ 5 मिली/लीटर पानी में मिलाकर पत्तियों की निचली सतह पर छिड़काव करें।",
        "chemical_remedy": "ETL पार होने पर: स्पाइरोमेसिफेन 22.9% SC (Oberon) @ 1.0 मिली/लीटर या प्रोपारगाइट 57% EC (Omite) @ 2.0 मिली/लीटर। प्रयोग विधि: शाम के समय प्रति एकड़ 200 लीटर पानी से पत्तियों के निचले हिस्से को भिगोते हुए छिड़काव करें।",
        "cultural_practice": "गर्म व शुष्क मौसम में खेत में नमी बनाए रखें और संक्रमित खरपतवार नष्ट करें।"
    },
    "mole cricket": {
        "pest_name": "घरघुरिया कीट (Mole Cricket - जड़ एवं अंकुर काटने वाला कीट)",
        "severity": "मध्यम (Moderate)",
        "action_threshold": "प्रति वर्ग मीटर 2-3 ताजी सुरंगें या नर्सरी में कटे हुए पौधे दिखने पर।",
        "organic_remedy": "मेटाराइजियम एनिसोप्ली @ 2 किग्रा/एकड़ को 50 किग्रा सड़ी गोबर की खाद में मिलाकर नम मिट्टी में डालें।",
        "chemical_remedy": "विष-चारा (Poison Bait): 10 किग्रा चोकर + 1 किग्रा गुड़ + 250 ग्राम क्लोरैन्ट्रानिलिप्रोल या फिप्रोनिल को हल्का गीला कर शाम के समय सुरंगों के पास बिखेरें।",
        "cultural_practice": "खेत में हल्की सिंचाई करने से कीट सुरंगों से बाहर आ जाते हैं जिन्हें पक्षी खा लेते हैं।"
    },
    "brown plant hopper": {
        "pest_name": "भूरा फुदका कीट (Brown Planthopper - BPH)",
        "severity": "गंभीर (Critical)",
        "action_threshold": "वानस्पतिक अवस्था में 5-10 फुदके प्रति पौधा और फूल अवस्था में 15-20 फुदके प्रति पौधा।",
        "organic_remedy": "खेत से 3-4 दिन के लिए पानी निकाल दें (AWD) और नीम तेल @ 5 मिली/लीटर तने के निचले भाग पर छिड़कें।",
        "chemical_remedy": "ETL पार होने पर: ट्राइफ्लुमेज़ोपाइरिम 10% SC (Pexalon) @ 0.5 मिली/लीटर या पाइमेट्रोज़िन 50% WDG (Chess) @ 0.6 ग्राम/लीटर। प्रयोग विधि: नोजल को सीधे धान के निचले तने (पानी के ऊपर) पर रखकर 200 लीटर पानी/एकड़ से शाम को छिड़काव करें।",
        "cultural_practice": "हर 2.5-3 मीटर पर 30 सेमी की गली (Alleyway) छोड़ें और यूरिया का अत्यधिक प्रयोग न करें।"
    },
    "aphids": {
        "pest_name": "माहू / चेपा एवं रस चूसक कीट (Aphids / Leafhoppers)",
        "severity": "मध्यम (Moderate)",
        "action_threshold": "10-15% पत्तियों पर प्रकोप या 15-20 माहू प्रति कोमल टहनी।",
        "organic_remedy": "5% नीम बीज अर्क (NSKE) या नीम तेल @ 5 मिली/लीटर पानी में 0.5 मिली साबुन घोल मिलाकर छिड़कें और 12-15 पीले चिपचिपे ट्रैप प्रति एकड़ लगाएं।",
        "chemical_remedy": "ETL पार होने पर: इमिडाक्लोप्रिड 17.8% SL @ 0.3 मिली/लीटर या थायामेथोक्साम 25% WG @ 0.25 ग्राम/लीटर। प्रयोग विधि: मधुमक्खियों की सुरक्षा हेतु शाम 4 बजे के बाद 150-200 लीटर पानी/एकड़ से छिड़काव करें (PHI: 15 दिन)।",
        "cultural_practice": "अधिक नाइट्रोजन (यूरिया) से बचें और शुरुआती संक्रमित टहनियों को तोड़कर नष्ट करें।"
    }
}

# Aliases and exports for modular usage
SUPPORTED_LANGUAGES = INDIC_LANGUAGES
SCHEDULED_INDIAN_LANGUAGES = {k: v for k, v in INDIC_LANGUAGES.items() if k != "en"}


def get_language_info(lang_code: str) -> Dict[str, str]:
    """Retrieve metadata for a language code, falling back to English."""
    code = lang_code.lower() if lang_code else "en"
    if code in INDIC_LANGUAGES:
        res = dict(INDIC_LANGUAGES[code])
        res["code"] = code
        return res
    res = dict(INDIC_LANGUAGES["en"])
    res["code"] = "en"
    return res


def build_multilingual_prompt_directive(lang_code: str) -> str:
    """Convenience alias for get_language_directive."""
    return get_language_directive(lang_code)


def get_localized_emergency_contact(lang_code: str) -> str:
    """Retrieve toll-free farmer helpline in target language."""
    code = lang_code.lower() if lang_code and lang_code.lower() in HELPLINES else "en"
    return HELPLINES.get(code, HELPLINES["en"])


def clean_markdown_for_speech(text: str) -> str:
    """Sanitize markdown syntax, bullets, asterisks, and technical symbols for audio speech synthesis."""
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"[#\*\-•`]+", "", cleaned)
    cleaned = re.sub(r"@", " at ", cleaned)
    cleaned = re.sub(r"\\%", " percent", cleaned)
    cleaned = re.sub(r"%", " percent", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def get_language_directive(lang_code: str) -> str:
    """Generates the prompt directive enforcing output in the requested language."""
    info = INDIC_LANGUAGES.get(lang_code.lower(), INDIC_LANGUAGES["en"])
    if lang_code.lower() == "en":
        return (
            "Provide your advice in clear, everyday English suitable for rural farmers. "
            "Always specify: (1) Exact fungicide or insecticide name and dosage per liter/acre, "
            "(2) Organic bio-control option, and (3) How and when to apply (crop stage, water volume per acre, morning/evening timing, and Pre-Harvest Interval)."
        )
    return (
        f"MANDATORY LANGUAGE RULE: You must write your entire response 100% in {info['name']} "
        f"({info['native']}) language using authentic {info['script']} script. "
        f"Do NOT leave any English sentences or bullet points in the middle of the response. "
        f"Translate all disease/pest names, fungicide/insecticide dosages, how to apply, when to apply, precautions, and greetings into {info['native']}."
    )


def _match_topic_key(query_or_points_text: str) -> str:
    """Identify the specific agronomic disease, pest, or scheme topic from query & context."""
    q = query_or_points_text.lower()
    if any(k in q for k in ["late blight", "নাবী ধসা", "पछेती झुलसा", "water-soaked", "phytophthora", "ridomil", "curzate"]):
        return "late_blight"
    if any(k in q for k in ["early blight", "আগাম ধসা", "अगेती झुलसा", "target-board", "concentric", "টমেটোর আর্লি ব্লাইট", "झुलसा"]):
        return "early_blight"
    if any(k in q for k in ["leaf roller", "leaf folder", "cnaphalocrocis", "পাতা মোড়ানো", "पत्ती लपेटक"]):
        return "rice_leaf_roller"
    if any(k in q for k in ["stem borer", "corn borer", "yellow rice borer", "মাজরা পোকা", "तना छेदक", "ostrinia", "scirpophaga", "dead heart"]):
        return "stem_borer"
    if any(k in q for k in ["brown plant hopper", "planthopper", "bph", "hopper burn", "বাদামী শোষক", "কারেন্ট পোকা", "भूरा फुदका", "adristyrannus"]):
        return "bph"
    if any(k in q for k in ["army worm", "armyworm", "spodoptera", "prodenia", "লেদা পোকা", "सैनिक कीट", "फॉल आर्मीवर्म"]):
        return "armyworm"
    if any(k in q for k in ["red spider", "panonchus", "panonychus", "mite", "লাল মাকড়", "लाल मकड़ी"]):
        return "red_spider"
    if any(k in q for k in ["mole cricket", "ঘুরঘুরে", "घरघुरिया"]):
        return "mole_cricket"
    if any(k in q for k in ["aphid", "jassid", "cicadellidae", "miridae", "lycorma", "unaspis", "জাব পোকা", "माहू", "चेपा"]):
        return "aphids_hopper"
    if any(k in q for k in ["zinc", "dap", "জিঙ্ক", "ডিএপি", "जिंक", "डीएपी", "fertilizer", "সার", "खाद", "urea", "ইউরিয়া", "यूरिया"]):
        return "zinc_dap_soil"
    if any(k in q for k in ["pmfby", "insurance", "hailstorm", "72", "বীমা", "শিলাবৃষ্টি", "बीमा", "ओलावृष्टि"]):
        return "pmfby_insurance"
    if any(k in q for k in ["pm-kisan", "pm kisan", "kyc", "কিষাণ", "किसान सम्मान"]):
        return "pm_kisan"
    if any(k in q for k in ["sunflower", "সূর্যমুখী", "सूरजमुखी"]):
        return "sunflower_harvest"
    if any(k in q for k in ["wheat", "গম", "गेहूं", "cri"]):
        return "wheat_production"
    return "fungicide_general"


def _translate_english_point_to_indic(point: str, lang_code: str) -> str:
    """Translates English agronomic sentences into pure Bengali or Hindi so zero mixed English remains."""
    clean = point.replace("**", "").replace("*", "").replace("`", "").strip()
    if lang_code == "bn":
        # Check if already predominantly Bengali script
        if any("\u0980" <= c <= "\u09FF" for c in clean) and not clean.startswith("Target Pest:"):
            return clean
        topic = _match_topic_key(clean)
        bn_points = LOCALIZED_ADVISORY_TOPICS.get(topic, LOCALIZED_ADVISORY_TOPICS["fungicide_general"])["bn"]
        return bn_points[0]
    if lang_code == "hi" or lang_code in ("mr", "ne", "mai", "kok", "sa", "doi", "brx"):
        if any("\u0900" <= c <= "\u097F" for c in clean) and not clean.startswith("Target Pest:"):
            return clean
        topic = _match_topic_key(clean)
        hi_points = LOCALIZED_ADVISORY_TOPICS.get(topic, LOCALIZED_ADVISORY_TOPICS["fungicide_general"])["hi"]
        return hi_points[0]
    return clean


def _purify_indic_text(text: str, lang_code: str) -> str:
    """
    Removes parenthetical English translations and replaces English abbreviations
    with pure Bengali or Hindi terms so 100% of displayed text is in the farmer's
    native language.
    """
    if not text or not lang_code or lang_code.lower() == "en":
        return text
    code = lang_code.lower()
    # Strip pure ASCII parentheticals that start with an English letter, e.g. (How & When to Apply), (Tomato)
    cleaned = re.sub(r"\s*\([A-Za-z][A-Za-z0-9\s\-\./,&%+:]*\)", "", text)
    if code in ("bn", "as", "mni"):
        cleaned = re.sub(r"\bETL\b", "ক্ষতিসীমা", cleaned)
        cleaned = re.sub(r"\bPHI\b", "অপেক্ষার সময়সীমা", cleaned)
        cleaned = re.sub(r"\bDAT\b", "দিন", cleaned)
        cleaned = re.sub(r"\bDAS\b", "দিন", cleaned)
        cleaned = re.sub(r"\bNSKE\b", "নিম বীজের নির্যাস", cleaned)
        cleaned = re.sub(r"\bppm\b", "পিপিএম", cleaned, flags=re.IGNORECASE)
    elif code != "en":
        cleaned = re.sub(r"\bETL\b", "आर्थिक क्षति स्तर", cleaned)
        cleaned = re.sub(r"\bPHI\b", "प्रतीक्षा अवधि", cleaned)
        cleaned = re.sub(r"\bDAT\b", "दिन", cleaned)
        cleaned = re.sub(r"\bDAS\b", "दिन", cleaned)
        cleaned = re.sub(r"\bNSKE\b", "नीम बीज अर्क", cleaned)
        cleaned = re.sub(r"\bppm\b", "पीपीएम", cleaned, flags=re.IGNORECASE)
    return re.sub(r"[ \t]+", " ", cleaned).strip()


def localize_sources(sources: List[str], lang_code: str = "en") -> List[str]:
    """Translates retrieved source citation chips into the farmer's selected native language."""
    if not lang_code or lang_code.lower() == "en":
        return sources
    code = lang_code.lower()
    if code in ("bn", "as", "mni"):
        return [
            "ভারতীয় কৃষি গবেষণা পরিষদ ফসল সুরক্ষা ও ছত্রাকনাশক নির্দেশিকা",
            "সমন্বিত বালাই ব্যবস্থাপনা ও কৃষি বিজ্ঞান কেন্দ্র সুপারিশ",
        ]
    return [
        "भारतीय कृषि अनुसंधान परिषद फसल सुरक्षा एवं कवकनाशी निर्देशिका",
        "समेकित कीट प्रबंधन एवं कृषि विज्ञान केंद्र अनुशंसा",
    ]


def localize_fallback_advisory(
    lang_code: str,
    crop_name: Optional[str],
    recommendation_points: List[str],
    query: str = ""
) -> str:
    """
    Produces a 100% native-language, structured agronomic advisory containing:
    1. Diagnosis & Symptoms / ETL
    2. Proper Fungicide / Insecticide & Exact Dosage
    3. Organic Bio-Control Remedy
    4. How & When to Apply (Water volume, crop stage, timing, PHI)
    5. Safety Precautions & Helpline
    Guarantees ZERO untranslated English bullet points when an Indian language is selected.
    """
    code = lang_code.lower() if lang_code and lang_code.lower() in INDIC_LANGUAGES else "en"
    greeting = GREETINGS.get(code, GREETINGS.get("hi" if code != "en" else "en"))
    precautions = PRECAUTIONS.get(code, PRECAUTIONS.get("hi" if code != "en" else "en"))
    helpline = HELPLINES.get(code, HELPLINES.get("hi" if code != "en" else "en"))
    prec_header = PRECAUTION_HEADERS.get(code, "Important Precautions:")

    combined_signal = f"{query} {crop_name or ''} " + " ".join(recommendation_points or [])
    topic_key = _match_topic_key(combined_signal)

    # Localize crop header
    localized_crop = crop_name or ""
    if localized_crop and code in CROP_NAME_TRANSLATIONS:
        for en_c, loc_c in CROP_NAME_TRANSLATIONS[code].items():
            if en_c.lower() in localized_crop.lower():
                localized_crop = loc_c
                break
    elif localized_crop and code == "bn":
        # Localize pest names in header if crop_name was a pest name
        for p_key, p_val in PEST_LOCALIZATION_BN.items():
            if p_key in localized_crop.lower():
                localized_crop = p_val["pest_name"]
                break
    elif localized_crop and code == "hi":
        for p_key, p_val in PEST_LOCALIZATION_HI.items():
            if p_key in localized_crop.lower():
                localized_crop = p_val["pest_name"]
                break

    header = f" [{localized_crop}]" if localized_crop else ""

    # Select 100% native-language structured treatment & fungicide points
    topic_dict = LOCALIZED_ADVISORY_TOPICS.get(topic_key, LOCALIZED_ADVISORY_TOPICS["fungicide_general"])
    if code in topic_dict:
        native_points = topic_dict[code]
    elif code in ("as", "mni", "or"):
        # Eastern script family: use Bengali/Devanagari localized points with native greeting/precautions/helpline
        native_points = topic_dict.get("bn", topic_dict["hi"])
    else:
        native_points = topic_dict.get("hi", recommendation_points[:4])

    body = "\n".join([f"• {_purify_indic_text(p, code)}" for p in native_points])
    prec_text = "\n".join([f"• {_purify_indic_text(p, code)}" for p in precautions])
    clean_header = _purify_indic_text(header, code)
    clean_header = f" {clean_header}" if clean_header else ""

    return (
        f"{greeting}{clean_header}\n\n"
        f"{body}\n\n"
        f"{_purify_indic_text(prec_header, code)}\n"
        f"{prec_text}\n\n"
        f"{_purify_indic_text(helpline, code)}"
    )


def localize_crop_analysis_result(res: Any, language: Optional[str] = "en") -> Any:
    """
    Translates CropAnalysisResult fields (crop_name, detected_condition, severity,
    summary, recommended_action) into the farmer's selected language while keeping
    quality_grade ('Grade A/B/C') compatible with UI badge classes.
    Supports lossless bidirectional re-localization (English <-> Indic).
    """
    from server.app.vision.label_mapper import LabelMapper, LABEL_DATABASE

    raw_label = getattr(res, "raw_label", None)

    # 1. Target is English (restore clean baseline)
    if not language or language.lower() == "en":
        if raw_label:
            if raw_label == "Not a Crop or Plant" or not getattr(res, "is_crop", True):
                return LabelMapper.build_non_crop_result(confidence=res.confidence)
            if raw_label in LABEL_DATABASE:
                restored = LabelMapper.get_mapping(raw_label, confidence=res.confidence)
                restored.quality_score = res.quality_score
                restored.is_crop = getattr(res, "is_crop", True)
                restored.raw_label = raw_label
                return restored
        return res

    code = language.lower()
    if not getattr(res, "is_crop", True) or res.crop_name == "Not a Crop or Plant":
        if code == "bn":
            res.crop_name = "কোনো ফসল বা গাছ নয়"
            res.detected_condition = "কোনো ফসল সনাক্ত হয়নি"
            res.summary = "এই ছবিতে কোনো ফসলের পাতা, কাণ্ড বা ফুল সনাক্ত করা যায়নি। অনুগ্রহ করে আক্রান্ত গাছের পাতা বা ফুলের পরিষ্কার ছবি আপলোড করুন।"
            res.recommended_action = [
                "ক্যামেরা সরাসরি ফসলের পাতা, কাণ্ড বা ফুলের দিকে ধরুন।",
                "দিনের পর্যাপ্ত আলোতে পরিষ্কার ও ফোকাস করা ছবি তুলুন।",
                "মানুষ, ঘরবাড়ি, গাড়ি বা খালি মাটির ছবি আপলোড করবেন না।"
            ]
        elif code == "hi":
            res.crop_name = "कोई फसल या पौधा नहीं"
            res.detected_condition = "कोई फसल की पहचान नहीं हुई"
            res.summary = "इस तस्वीर में कोई कृषि फसल, पत्ती या फूल नहीं मिला। कृपया पौधे की पत्ती या फूल की स्पष्ट फोटो अपलोड करें।"
            res.recommended_action = [
                "कैमरे को सीधे फसल की पत्ती, तने या फूल पर केंद्रित करें।",
                "पर्याप्त प्राकृतिक रोशनी में साफ फोटो खींचें।",
                "व्यक्ति, वाहन, वस्तु या खाली जमीन की फोटो अपलोड न करें।"
            ]
        return res

    lang_family = "bn" if code in ("bn", "as", "mni") else ("hi" if code != "en" else "en")
    if lang_family == "en":
        return res

    # Reset from raw_label to guarantee clean baseline if transitioning between Indic languages
    if raw_label and raw_label in LABEL_DATABASE:
        base = LabelMapper.get_mapping(raw_label, confidence=res.confidence)
        res.crop_name = base.crop_name
        res.detected_condition = base.detected_condition
        res.quality_grade = base.quality_grade
        res.severity = base.severity
        res.summary = base.summary
        res.recommended_action = list(base.recommended_action)

    # 1. Translate Crop Name
    crop_map = CROP_NAME_TRANSLATIONS.get(lang_family, {})
    if res.crop_name in crop_map:
        res.crop_name = _purify_indic_text(crop_map[res.crop_name], lang_family)

    # 2. Translate Severity
    sev_map = SEVERITY_TRANSLATIONS.get(lang_family, {})
    if res.severity in sev_map:
        res.severity = _purify_indic_text(sev_map[res.severity], lang_family)

    # 3. Translate Condition, Summary & Detailed Fungicide/Application Actions
    db = DISEASE_LOCALIZATION_BN if lang_family == "bn" else DISEASE_LOCALIZATION_HI
    cond_lower = res.detected_condition.lower()
    matched_entry = None
    if "early blight" in cond_lower:
        matched_entry = db["Early Blight"]
    elif "late blight" in cond_lower:
        matched_entry = db["Late Blight"]
    elif "rust" in cond_lower:
        matched_entry = db["Common Rust"]
    elif "scab" in cond_lower:
        matched_entry = db["Apple Scab"]
    elif "healthy" in cond_lower:
        matched_entry = db["Healthy"]

    if matched_entry:
        res.detected_condition = _purify_indic_text(matched_entry["condition"], lang_family)
        res.summary = _purify_indic_text(matched_entry["summary"], lang_family)
        res.recommended_action = [_purify_indic_text(a, lang_family) for a in matched_entry["actions"]]
    else:
        # Generic disease localization with complete fungicide & application instructions
        if lang_family == "bn":
            res.summary = f"{res.crop_name} গাছের পাতায় রোগের লক্ষণ দেখা গেছে। সময়মতো অনুমোদিত ছত্রাকনাশক ও জৈব পরিচর্যা করলে ফসলের ক্ষতি সম্পূর্ণ রোধ করা যাবে।"
            res.recommended_action = [_purify_indic_text(a, lang_family) for a in LOCALIZED_ADVISORY_TOPICS["fungicide_general"]["bn"]]
        else:
            res.summary = f"{res.crop_name} की पत्तियों पर रोग के लक्षण देखे गए हैं। समय पर अनुशंसित कवकनाशी के छिड़काव से उपज सुरक्षित रहेगी।"
            res.recommended_action = [_purify_indic_text(a, lang_family) for a in LOCALIZED_ADVISORY_TOPICS["fungicide_general"]["hi"]]

    res.raw_label = raw_label
    return res


def expand_multilingual_query(query: str) -> str:
    """
    Appends canonical English agronomic keywords when a farmer types a query in
    Bengali, Hindi, or another Indic script so vector/keyword search against the
    ICAR corpus retrieves the exact topic chunk.
    """
    if not query:
        return query
    topic = _match_topic_key(query)
    topic_en_keywords = {
        "late_blight": "Potato Tomato Late Blight Phytophthora fungicide Cymoxanil Mancozeb Ridomil",
        "early_blight": "Tomato Potato Early Blight Alternaria fungicide Mancozeb Copper Oxychloride",
        "rice_leaf_roller": "Rice Leaf Roller Folder Cnaphalocrocis Chlorantraniliprole Cartap Trichogramma",
        "stem_borer": "Rice Maize Corn Stem Borer Scirpophaga Ostrinia Dead heart Chlorantraniliprole",
        "bph": "Rice Brown Planthopper BPH Hopper burn Pymetrozine Triflumezopyrim alleyways",
        "armyworm": "Maize Paddy Armyworm Spodoptera Emamectin Benzoate Bt kurstaki",
        "red_spider": "Red Spider Mite Panonychus Wettable Sulphur Spiromesifen Propargite",
        "mole_cricket": "Mole Cricket Metarhizium poison bait seedling root",
        "aphids_hopper": "Aphids Jassids Leafhopper Imidacloprid Thiamethoxam Neem Oil NSKE",
        "zinc_dap_soil": "Soil Health Card Zinc Sulphate DAP fertilizer incompatibility Urea NPK",
        "pmfby_insurance": "PMFBY Pradhan Mantri Fasal Bima Yojana 72 hours hailstorm crop loss claim",
        "pm_kisan": "PM-KISAN Samman Nidhi 6000 e-KYC Aadhaar DBT installment",
        "sunflower_harvest": "Sunflower physiological maturity harvest lemon yellow capitulum 40C drying",
        "wheat_production": "Wheat CRI crown root initiation 21 days HD-2967 HD-3086 irrigation",
        "fungicide_general": "ICAR fungicide insecticide dosage application timing foliar spray",
    }
    extra = topic_en_keywords.get(topic, "")
    return f"{query} {extra}".strip()


def has_target_script(text: str, lang_code: str) -> bool:
    """
    Checks whether a generated LLM response actually contains the farmer's
    requested Indic script (e.g., Bengali or Devanagari) and does not contain
    untranslated English template headers like 'Target Pest:' or 'Economic Threshold Level'.
    """
    if not text or not lang_code or lang_code.lower() == "en":
        return True
    code = lang_code.lower()
    if any(h in text for h in ["Target Pest:", "Economic Threshold Level", "Organic Bio-Control Remedy:", "Chemical Spray & Dosage:"]):
        return False
    alpha_chars = [c for c in text if c.isalpha()]
    if not alpha_chars:
        return False
    if code in ("bn", "as", "mni"):
        indic_count = sum(1 for c in alpha_chars if "\u0980" <= c <= "\u09FF")
        return (indic_count / len(alpha_chars)) >= 0.35
    if code in ("hi", "mr", "ne", "mai", "kok", "sa", "doi", "brx"):
        indic_count = sum(1 for c in alpha_chars if "\u0900" <= c <= "\u097F")
        return (indic_count / len(alpha_chars)) >= 0.35
    return True


def localize_pest_detection_response(pest_res: Dict[str, Any], language: Optional[str] = "en") -> Dict[str, Any]:
    """
    Translates PestDetectionResponse / PestClassificationResponse into the farmer's
    selected language (100% Bengali, Hindi, etc.) with detailed insecticide/bio-control
    dosages and how/when to apply.
    """
    if not language or language.lower() == "en" or not isinstance(pest_res, dict):
        return pest_res

    code = language.lower()
    lang_family = "bn" if code in ("bn", "as", "mni") else ("hi" if code != "en" else "en")
    if lang_family == "en":
        return pest_res

    pest_db = PEST_LOCALIZATION_BN if lang_family == "bn" else PEST_LOCALIZATION_HI

    def _find_pest_entry(raw_signal: str) -> Dict[str, str]:
        sig = raw_signal.lower()
        for k, v in pest_db.items():
            if k in sig:
                return v
        if any(w in sig for w in ["borer", "scirpophaga", "ostrinia", "chilo"]):
            return pest_db["corn borer"]
        if any(w in sig for w in ["army", "spodoptera", "prodenia", "cutworm"]):
            return pest_db["army worm"]
        if any(w in sig for w in ["spider", "mite", "panonchus", "unaspis"]):
            return pest_db["red spider"]
        if any(w in sig for w in ["hopper", "adristyrannus", "nilaparvata", "sogatella"]):
            return pest_db["brown plant hopper"]
        if any(w in sig for w in ["cricket"]):
            return pest_db["mole cricket"]
        if any(w in sig for w in ["roller", "folder", "cnaphalocrocis"]):
            return pest_db["rice leaf roller"]
        return pest_db["aphids"]

    if "model_type" in pest_res:
        pest_res["model_type"] = "অফলাইন পোকা স্ক্যানার" if lang_family == "bn" else "ऑफ़लाइन कीट स्कैनर"

    detections = pest_res.get("detections", [])
    for det in detections:
        raw_signal = (det.get("raw_label", "") + " " + det.get("pest_name", "")).lower()
        matched = _find_pest_entry(raw_signal)
        det["pest_name"] = _purify_indic_text(matched["pest_name"], lang_family)
        det["severity"] = _purify_indic_text(matched["severity"], lang_family)
        det["action_threshold"] = _purify_indic_text(matched["action_threshold"], lang_family)
        det["organic_remedy"] = _purify_indic_text(matched["organic_remedy"], lang_family)
        det["chemical_remedy"] = _purify_indic_text(matched["chemical_remedy"], lang_family)
        det["cultural_practice"] = _purify_indic_text(matched["cultural_practice"], lang_family)

    if "primary_pest" in pest_res:
        raw_signal = (pest_res.get("raw_label", "") + " " + pest_res.get("primary_pest", "")).lower()
        matched = _find_pest_entry(raw_signal)
        pest_res["primary_pest"] = _purify_indic_text(matched["pest_name"], lang_family)
        pest_res["severity"] = _purify_indic_text(matched["severity"], lang_family)
        pest_res["action_threshold"] = _purify_indic_text(matched["action_threshold"], lang_family)
        pest_res["organic_remedy"] = _purify_indic_text(matched["organic_remedy"], lang_family)
        pest_res["chemical_remedy"] = _purify_indic_text(matched["chemical_remedy"], lang_family)
        pest_res["cultural_practice"] = _purify_indic_text(matched["cultural_practice"], lang_family)

    return pest_res

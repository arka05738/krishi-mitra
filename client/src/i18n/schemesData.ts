/**
 * Localized Government Agricultural Schemes Data for Krishi Mitra.
 * Supports all 22 Scheduled Indian Languages + English with safe hierarchical fallbacks.
 */
import type { LanguageCode } from './translations.ts';
import type { GovernmentScheme } from '../types/index.ts';

export const LOCALIZED_SCHEMES: Record<string, GovernmentScheme[]> = {
  "en": [
    {
      "id": "pm-kisan",
      "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      "category": "Financial Assistance",
      "benefit": "Direct income support of Rs 6,000 per year transferred in three equal 4-monthly installments of Rs 2,000 into bank accounts.",
      "eligibility": "All landholding farmer families across India subject to exclusion criteria for higher economic status.",
      "key_actions": [
        "Complete mandatory e-KYC using Aadhaar OTP on pmkisan.gov.in or biometric at CSC centre.",
        "Ensure bank account is Aadhaar-seeded with active direct benefit transfer (DBT).",
        "Verify land seeding status on portal beneficiary status page."
      ],
      "helpline": "155261 / 1800-115-526",
      "portal_url": "https://pmkisan.gov.in"
    },
    {
      "id": "pmfby",
      "title": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
      "category": "Crop Insurance",
      "benefit": "Comprehensive yield loss, prevented sowing, and localized post-harvest calamity insurance with farmer premium of only 1.5% for Rabi and 2% for Kharif crops.",
      "eligibility": "All farmers cultivating notified crops in notified areas, including sharecroppers and tenant farmers.",
      "notice_period": "Mandatory 72-hour reporting rule for localized calamities (hailstorm, cloudburst, landslide, inundation).",
      "key_actions": [
        "Report localized damage within 72 hours via the Crop Insurance App, helpline 14447, or local bank.",
        "Keep photograph of damaged field and sowing certificate ready for joint survey.",
        "Check claim credit directly into Aadhaar-linked bank account."
      ],
      "helpline": "14447 (Crop Insurance Toll-Free)",
      "portal_url": "https://pmfby.gov.in"
    },
    {
      "id": "kcc",
      "title": "Kisan Credit Card (KCC Scheme)",
      "category": "Credit & Markets",
      "benefit": "Flexible institutional credit at effective 4% interest rate per annum (with 3% prompt repayment incentive) for cultivation expenses and post-harvest needs.",
      "eligibility": "Individual/joint farmers, tenant farmers, oral lessees, sharecroppers, and SHGs of farmers.",
      "key_actions": [
        "Apply at nearest commercial, rural, or cooperative bank branch with land record and Aadhaar.",
        "No collateral requirement for loans up to Rs 1.60 Lakh.",
        "Simplified single-page application form available at all bank branches."
      ],
      "helpline": "1800-180-1551"
    },
    {
      "id": "soil-health-card",
      "title": "Soil Health Card Scheme",
      "category": "Soil & Advisory",
      "benefit": "Periodic assessment of 12 soil parameters issued every 2 years with crop-wise customized chemical and organic fertilizer recommendations.",
      "eligibility": "All agricultural landowners and cultivating farmers in India.",
      "key_actions": [
        "Collect representative soil samples from 0-15 cm depth across farm zig-zag transects.",
        "Deposit sample with village agricultural assistant or nearest Krishi Vigyan Kendra (KVK).",
        "Download updated report online using soil health card portal with state and district code."
      ],
      "helpline": "1800-180-1551",
      "portal_url": "https://soilhealth.dac.gov.in"
    },
    {
      "id": "enam",
      "title": "e-NAM (National Agriculture Market)",
      "category": "Credit & Markets",
      "benefit": "Pan-India electronic trading marketplace integrating physical wholesale mandis for competitive online bidding and direct payments.",
      "eligibility": "Individual farmers, Farmer Producer Organizations (FPOs), and licensed mandi traders.",
      "key_actions": [
        "Register on enam.gov.in or e-NAM mobile app with bank account passbook copy.",
        "Bring produce to registered mandi gate for sampling, assaying, and lot generation.",
        "Receive payment directly into bank account after online trader bid acceptance."
      ],
      "helpline": "1800-270-0224",
      "portal_url": "https://enam.gov.in"
    },
    {
      "id": "kisan-call-centre",
      "title": "Kisan Call Centre (KCC Helpline)",
      "category": "Soil & Advisory",
      "benefit": "Instant toll-free phone consultation with agricultural scientists and extension specialists in 22 local Indian languages.",
      "eligibility": "Open to every farmer across India without charge.",
      "key_actions": [
        "Dial toll-free 1800-180-1551 from any mobile or landline phone.",
        "Operates from 6:00 AM to 10:00 PM on all 365 days of the year.",
        "Queries requiring specialist research are escalated to Level-2 subject matter experts at ICAR/SAU."
      ],
      "helpline": "1800-180-1551 (Toll-Free)"
    }
  ],
  "hi": [
    {
      "id": "pm-kisan",
      "title": "पीएम-किसान (प्रधानमंत्री किसान सम्मान निधि)",
      "category": "वित्तीय सहायता",
      "benefit": "प्रति वर्ष ₹6,000 की सीधी आय सहायता, जो ₹2,000 की तीन समान किस्तों में बैंक खातों में सीधे हस्तांतरित की जाती है।",
      "eligibility": "उच्च आर्थिक स्थिति के अपवर्जन मानदंडों को छोड़कर भारत के सभी भूमिधारक किसान परिवार।",
      "key_actions": [
        "pmkisan.gov.in पर आधार ओटीपी या सीएससी केंद्र पर बायोमेट्रिक से अनिवार्य ई-केवाईसी पूर्ण करें।",
        "सुनिश्चित करें कि बैंक खाता आधार से जुड़ा (Aadhaar Seeded) और डीबीटी (DBT) सक्रिय है।",
        "पोर्टल पर लाभार्थी स्थिति पेज पर भूलेख लिंकिंग (Land Seeding) स्थिति जांचें।"
      ],
      "helpline": "155261 / 1800-115-526",
      "portal_url": "https://pmkisan.gov.in"
    },
    {
      "id": "pmfby",
      "title": "पीएमएफबीवाई (प्रधानमंत्री फसल बीमा योजना)",
      "category": "फसल बीमा",
      "benefit": "व्यापक उपज हानि, बुवाई न हो पाने तथा स्थानीय आपदाओं पर बीमा। रबी फसलों पर केवल 1.5% तथा खरीफ फसलों पर 2% किसान प्रीमियम।",
      "eligibility": "अधिसूचित क्षेत्रों में अधिसूचित फसल उगाने वाले सभी किसान, जिनमें बटाईदार व पट्टेदार किसान शामिल हैं।",
      "notice_period": "स्थानीय आपदाओं (ओलावृष्टि, बादल फटना, भूस्खलन, जलभराव) पर अनिवार्य 72 घंटे की सूचना नियम।",
      "key_actions": [
        "फसल नुकसान के 72 घंटे के भीतर फसल बीमा ऐप, हेल्पलाइन 14447 या स्थानीय बैंक को सूचित करें।",
        "संयुक्त सर्वेक्षण के लिए क्षतिग्रस्त खेत की तस्वीर और बुवाई प्रमाण पत्र तैयार रखें।",
        "आधार से जुड़े बैंक खाते में सीधे बीमा क्लेम की राशि प्राप्त करें।"
      ],
      "helpline": "14447 (टोल-फ्री फसल बीमा)",
      "portal_url": "https://pmfby.gov.in"
    },
    {
      "id": "kcc",
      "title": "किसान क्रेडिट कार्ड (केसीसी योजना)",
      "category": "ऋण व बाजार",
      "benefit": "समय पर भुगतान पर 3% छूट के साथ प्रभावी 4% वार्षिक ब्याज दर पर खेती व कटाई-उपरांत जरूरतों के लिए संस्थागत ऋण।",
      "eligibility": "व्यक्तिगत/संयुक्त किसान, काश्तकार किसान, बटाईदार एवं किसानों के स्वयं सहायता समूह (SHGs)।",
      "key_actions": [
        "भू-अभिलेख व आधार कार्ड के साथ नजदीकी वाणिज्यिक, ग्रामीण या सहकारी बैंक शाखा में आवेदन करें।",
        "₹1.60 लाख तक के ऋण के लिए किसी बंधक (Collateral) की आवश्यकता नहीं।",
        "सभी बैंक शाखाओं में सरल एकल-पृष्ठ आवेदन फॉर्म उपलब्ध है।"
      ],
      "helpline": "1800-180-1551"
    },
    {
      "id": "soil-health-card",
      "title": "मृदा स्वास्थ्य कार्ड योजना (Soil Health Card)",
      "category": "मृदा एवं सलाह",
      "benefit": "प्रत्येक 2 वर्ष में 12 मृदा पोषक तत्वों की जांच और फसल अनुसार संतुलित रासायनिक व जैविक उर्वरक सिफारिशें।",
      "eligibility": "भारत के सभी कृषि भूमि मालिक और खेती करने वाले किसान।",
      "key_actions": [
        "खेत से 0-15 सेमी गहराई से ज़िग-ज़ैग तरीके से मिट्टी के प्रतिनिधि नमूने एकत्र करें।",
        "नमूना ग्राम कृषि सहायक या नजदीकी कृषि विज्ञान केंद्र (KVK) में जमा करें।",
        "मृदा स्वास्थ्य कार्ड पोर्टल से राज्य और जिला कोड द्वारा रिपोर्ट डाउनलोड करें।"
      ],
      "helpline": "1800-180-1551",
      "portal_url": "https://soilhealth.dac.gov.in"
    },
    {
      "id": "enam",
      "title": "ई-नाम (राष्ट्रीय कृषि बाजार)",
      "category": "ऋण व बाजार",
      "benefit": "भौतिक थोक मंडियों को जोड़ने वाला अखिल भारतीय इलेक्ट्रॉनिक व्यापार मंच, पारदर्शी ऑनलाइन बोली और प्रत्यक्ष बैंक भुगतान।",
      "eligibility": "व्यक्तिगत किसान, किसान उत्पादक संगठन (FPO) और पंजीकृत मंडी व्यापारी।",
      "key_actions": [
        "बैंक पासबुक प्रति के साथ enam.gov.in या मोबाइल ऐप पर निःशुल्क पंजीकरण करें।",
        "उपज को पंजीकृत मंडी में लाएं और सैंपलिंग व ग्रेडिंग लॉट बनवाएं।",
        "ऑनलाइन बोली स्वीकार होने के बाद बैंक खाते में सीधे डिजिटल भुगतान पाएं।"
      ],
      "helpline": "1800-270-0224",
      "portal_url": "https://enam.gov.in"
    },
    {
      "id": "kisan-call-centre",
      "title": "किसान कॉल सेंटर (केसीसी हेल्पलाइन)",
      "category": "मृदा एवं सलाह",
      "benefit": "22 स्थानीय भारतीय भाषाओं में कृषि वैज्ञानिकों और विशेषज्ञों से तुरंत निःशुल्क टेलीफोनिक परामर्श।",
      "eligibility": "भारत के प्रत्येक किसान के लिए पूर्णतः निःशुल्क और खुला।",
      "key_actions": [
        "किसी भी मोबाइल या लैंडलाइन फोन से टोल-फ्री 1800-180-1551 डायल करें।",
        "वर्ष के सभी 365 दिन सुबह 6:00 बजे से रात 10:00 बजे तक सेवा उपलब्ध।",
        "विशिष्ट समस्याओं को आईसीएआर (ICAR) के स्तर-2 विषय विशेषज्ञों को अग्रेषित किया जाता है।"
      ],
      "helpline": "1800-180-1551 (टोल-फ्री)"
    }
  ],
  "bn": [
    {
      "id": "pm-kisan",
      "title": "পিএম-কিষাণ (প্রধানমন্ত্রী কিষাণ সম্মান নিধি)",
      "category": "আর্থিক সহায়তা",
      "benefit": "বার্ষিক ৬,০০০ টাকার প্রত্যক্ষ অনুদান, ৪ মাস অন্তর ২,০০০ টাকার ৩টি সমান কিস্তিতে সরাসরি ব্যাঙ্ক অ্যাকাউন্টে পাঠানো হয়।",
      "eligibility": "উচ্চ অর্থনৈতিক শ্রেণির শর্ত সাপেক্ষে ভারতের সকল কৃষক পরিবার।",
      "key_actions": [
        "pmkisan.gov.in এ আধার ওটিপি অথবা সিএসসি কেন্দ্রে বায়োমেট্রিক দ্বারা বাধ্যতামূলক ই-কেওয়াইসি সম্পন্ন করুন।",
        "ব্যাঙ্ক অ্যাকাউন্টে আধার সংযুক্তি এবং ডিবিটি সক্রিয় রয়েছে কিনা তা নিশ্চিত করুন।",
        "পোর্টালের সুবিধাভোগী পেজে জমির রেকর্ড সংযোগ অবস্থা যাচাই করুন।"
      ],
      "helpline": "155261 / 1800-115-526",
      "portal_url": "https://pmkisan.gov.in"
    },
    {
      "id": "pmfby",
      "title": "পিএমএফবিওয়াই (প্রধানমন্ত্রী ফসল বীমা যোজনা)",
      "category": "ফসল বীমা",
      "benefit": "ফসল নষ্ট বা প্রাকৃতিক দুর্যোগে ব্যাপক বীমা সুরক্ষা। রবি ফসলে মাত্র ১.৫% এবং খরিফ ফসলে ২% প্রিমিয়াম দিতে হয়।",
      "eligibility": "বিজ্ঞাপিত এলাকায় বিজ্ঞাপিত ফসল চাষকারী সকল কৃষক (বর্গাদার সহ)।",
      "notice_period": "স্থানীয় দুর্যোগে (শিলাবৃষ্টি, অতিবৃষ্টি) ৭২ ঘণ্টার মধ্যে জানানোর বাধ্যতামূলক নিয়ম।",
      "key_actions": [
        "ফসল ক্ষতির ৭২ ঘণ্টার মধ্যে ক্রপ ইন্স্যুরেন্স অ্যাপ বা হেল্পলাইন ১৪৪৪৭ বা স্থানীয় ব্যাঙ্কে রিপোর্ট করুন।",
        "যৌথ পরিদর্শনের জন্য ক্ষতিগ্রস্ত জমির ছবি ও চাষের প্রমাণপত্র প্রস্তুত রাখুন।",
        "আধার লিঙ্কযুক্ত ব্যাঙ্ক অ্যাকাউন্টে সরাসরি ক্ষতিপূরণ পান।"
      ],
      "helpline": "14447 (টোল-ফ্রি ফসল বীমা)",
      "portal_url": "https://pmfby.gov.in"
    },
    {
      "id": "kcc",
      "title": "কিষাণ ক্রেডিট কার্ড (কেসিসি যোজনা)",
      "category": "ঋণ ও বাজার",
      "benefit": "সময়মতো পরিশোধে ৩% ছাড়সহ কার্যকর ৪% বার্ষিক সুদের হারে চাষাবাদ ও পরবর্তী খরচের জন্য নমনীয় ঋণ।",
      "eligibility": "ব্যক্তিগত বা যৌথ কৃষক, ভাগচাষী, বর্গাদার এবং কৃষকদের স্বনির্ভর গোষ্ঠী।",
      "key_actions": [
        "জমির রেকর্ড ও আধার নিয়ে নিকটস্থ ব্যাঙ্ক শাখায় আবেদন করুন।",
        "১.৬০ লক্ষ টাকা পর্যন্ত ঋণের জন্য কোনো বন্ধকের প্রয়োজন নেই।",
        "সকল ব্যাঙ্ক শাখায় সহজ এক পাতার আবেদন ফর্ম উপলব্ধ।"
      ],
      "helpline": "1800-180-1551"
    },
    {
      "id": "soil-health-card",
      "title": "মৃত্তিকা স্বাস্থ্য কার্ড যোজনা (Soil Health Card)",
      "category": "মৃত্তিকা ও পরামর্শ",
      "benefit": "প্রতি ২ বছরে ১২টি মাটির উপাদান পরীক্ষা এবং ফসল অনুযায়ী সুষম সার ব্যবহারের বৈজ্ঞানিক পরামর্শ।",
      "eligibility": "ভারতের সকল কৃষি জমির মালিক ও চাষী।",
      "key_actions": [
        "জমি থেকে ০-১৫ সেমি গভীরতার নমুনা সংগ্রহ করুন।",
        "নমুনাটি গ্রামীণ কৃষি সহকারী বা কৃষি বিজ্ঞান কেন্দ্রে জমা দিন।",
        "অনলাইনে জেলা ও ব্লক কোড দিয়ে রিপোর্ট ডাউনলোড করুন।"
      ],
      "helpline": "1800-180-1551",
      "portal_url": "https://soilhealth.dac.gov.in"
    },
    {
      "id": "enam",
      "title": "ই-ন্যাম (জাতীয় কৃষি বাজার)",
      "category": "ঋণ ও বাজার",
      "benefit": "সারা ভারতের পাইকারি মাণ্ডিগুলির সমন্বিত অনলাইন প্ল্যাটফর্ম, স্বচ্ছ দরপত্র এবং সরাসরি ব্যাঙ্ক পেমেন্ট।",
      "eligibility": "ব্যক্তিগত কৃষক, কৃষক উৎপাদক সংস্থা (FPO) এবং লাইসেন্সপ্রাপ্ত ব্যবসায়ী।",
      "key_actions": [
        "enam.gov.in এ ব্যাঙ্ক পাসবই দিয়ে বিনামূল্যে নিবন্ধন করুন।",
        "নিবন্ধিত মাণ্ডিতে ফসল এনে গ্রেডিং করান।",
        "অনলাইন নিলামের পর সরাসরি ব্যাঙ্ক অ্যাকাউন্টে টাকা গ্রহণ করুন।"
      ],
      "helpline": "1800-270-0224",
      "portal_url": "https://enam.gov.in"
    },
    {
      "id": "kisan-call-centre",
      "title": "কিষাণ কল সেন্টার (কেসিসি হেল্পলাইন)",
      "category": "মৃত্তিকা ও পরামর্শ",
      "benefit": "২২টি ভারতীয় ভাষায় কৃষি বিশেষজ্ঞদের সঙ্গে তাৎক্ষণিক বিনামূল্যে টেলিফোনিক পরামর্শ।",
      "eligibility": "ভারতের যে কোনো কৃষকের জন্য সম্পূর্ণ বিনামূল্যে উন্মুক্ত।",
      "key_actions": [
        "টোল-ফ্রি 1800-180-1551 নম্বরে ফোন করুন।",
        "বছরের ৩৬৫ দিন সকাল ৬:০০ টা থেকে রাত ১০:০০ টা পর্যন্ত খোলা।",
        "জটিল প্রশ্নে আইসিএআর (ICAR) বিজ্ঞানীদের কাছে স্থানান্তর করা হয়।"
      ],
      "helpline": "1800-180-1551 (টোল-ফ্রি)"
    }
  ],
  "te": [
    {
      "id": "pm-kisan",
      "title": "పీఎం-కిసాన్ (ప్రధానమంత్రి కిసాన్ సమ్మాన్ నిధి)",
      "category": "ఆర్థిక సహాయం",
      "benefit": "ఏటా రూ. 6,000 ప్రత్యక్ష ఆర్థిక సహాయం, మూడు విడతల్లో రూ. 2,000 చొప్పున నేరుగా బ్యాంక్ ఖాతాలో జమ.",
      "eligibility": "మినహాయింపు పరిమితులు మినహా భారతదేశంలోని భూమి కలిగిన రైతు కుటుంబాలన్నీ అర్హులు.",
      "key_actions": [
        "pmkisan.gov.in లో ఆధార్ ఓటీపీ లేదా సీఎస్‌సీ కేంద్రంలో బయోమెట్రిక్ ఈ-కేవైసీ పూర్తి చేయండి.",
        "బ్యాంక్ ఖాతాకు ఆధార్ లింక్ మరియు డీబీటీ యాక్టివ్‌గా ఉండేలా చూసుకోండి.",
        "పోర్టల్ లో ల్యాండ్ సీడింగ్ స్థితిని తనిఖీ చేయండి."
      ],
      "helpline": "155261 / 1800-115-526",
      "portal_url": "https://pmkisan.gov.in"
    },
    {
      "id": "pmfby",
      "title": "పీఎంఎఫ్‌బీవై (ప్రధానమంత్రి ఫసల్ బీమా యోజన)",
      "category": "పంట బీమా",
      "benefit": "పంట నష్టం మరియు ప్రకృతి వైపరీత్యాల నుంచి సమగ్ర రక్షణ. రబీకి 1.5%, ఖరీఫ్‌కు 2% అతి తక్కువ ప్రీమియం.",
      "eligibility": "నోటిఫైడ్ పంటలు సాగుచేసే కౌలు రైతులు మరియు సొంత భూమి ఉన్న రైతులందరూ.",
      "notice_period": "స్థానిక విపత్తులు (వడగండ్లు, వరదలు) జరిగిన 72 గంటల్లోగా సమాచారం ఇవ్వడం తప్పనిసరి.",
      "key_actions": [
        "72 గంటల్లో క్రాప్ ఇన్సూరెన్స్ యాప్ లేదా టోల్ ఫ్రీ 14447 ద్వారా ఫిర్యాదు నమోదు చేయండి.",
        "సర్వే కోసం నష్టపోయిన పంట పొలం ఫోటోలను భద్రపరచండి.",
        "నేరుగా ఆధార్ అనుసంధానిత బ్యాంక్ ఖాతాలో క్లెయిమ్ పొందండి."
      ],
      "helpline": "14447 (పంట బీమా టోల్-ఫ్రీ)",
      "portal_url": "https://pmfby.gov.in"
    },
    {
      "id": "kcc",
      "title": "కిసాన్ క్రెడిట్ కార్డు (కేసీసీ పథకం)",
      "category": "రుణం మరియు మార్కెట్",
      "benefit": "సకాలంలో చెల్లిస్తే కేవలం 4% వార్షిక వడ్డీ రేటుతో సాగు ఖర్చులకు సులభమైన బ్యాంక్ రుణం.",
      "eligibility": "రైతులు, కౌలు రైతులు, వాటాదారులు మరియు రైతు స్వయం సహాయక సంఘాలు.",
      "key_actions": [
        "భూమి రికార్డులు, ఆధార్‌తో సమీప బ్యాంక్ శాఖలో దరఖాస్తు చేసుకోండి.",
        "రూ. 1.60 లక్షల వరకు ఎటువంటి హామీ (సెక్యూరిటీ) అవసరం లేదు.",
        "అన్ని బ్యాంకుల్లో సింగిల్ పేజీ దరఖాస్తు ఫారం లభిస్తుంది."
      ],
      "helpline": "1800-180-1551"
    },
    {
      "id": "soil-health-card",
      "title": "సాయిల్ హెల్త్ కార్డ్ పథకం (మృత్తికా ఆరోగ్య పత్రం)",
      "category": "నేల మరియు సలహా",
      "benefit": "ప్రతి 2 సంవత్సరాలకు 12 రకాల నేల పోషకాల పరీక్ష మరియు పంటకు తగిన ఎరువుల సిఫార్సు.",
      "eligibility": "దేశంలోని వ్యవసాయ భూమి యజమానులు మరియు సాగుదారులు అందరూ.",
      "key_actions": [
        "పొలం నుంచి 0-15 సెం.మీ లోతులో మట్టి నమూనాలు సేకరించండి.",
        "గ్రామ వ్యవసాయ సహాయకుడికి లేదా కేవీకే కేంద్రంలో నమూనా ఇవ్వండి.",
        "పోర్టల్ నుండి సాయిల్ హెల్త్ కార్డు రిపోర్టును డౌన్‌లోడ్ చేసుకోండి."
      ],
      "helpline": "1800-180-1551",
      "portal_url": "https://soilhealth.dac.gov.in"
    },
    {
      "id": "enam",
      "title": "ఈ-నామ్ (జాతీయ వ్యవసాయ మార్కెట్)",
      "category": "రుణం మరియు మార్కెట్",
      "benefit": "దేశవ్యాప్త వ్యవసాయ మార్కెట్ల అనుసంధానం, పారదర్శక ఆన్‌లైన్ బిడ్డింగ్ మరియు నేరుగా బ్యాంక్ చెల్లింపులు.",
      "eligibility": "రైతులు, రైతు ఉత్పత్తిదారుల సంఘాలు (FPOలు) మరియు లైసెన్స్ ఉన్న వ్యాపారులు.",
      "key_actions": [
        "enam.gov.in లో లేదా యాప్‌లో బ్యాంక్ పాస్‌బుక్‌తో ఉచితంగా నమోదు చేసుకోండి.",
        "పంటను మార్కెట్ యార్డుకు తీసుకెళ్లి గ్రేడింగ్ చేయించండి.",
        "ఆన్‌లైన్ బిడ్డింగ్ ద్వారా నేరుగా బ్యాంక్ ఖాతాలో డబ్బులు పొందండి."
      ],
      "helpline": "1800-270-0224",
      "portal_url": "https://enam.gov.in"
    },
    {
      "id": "kisan-call-centre",
      "title": "కిసాన్ కాల్ సెంటర్ (కేసీసీ హెల్ప్‌లైన్)",
      "category": "నేల మరియు సలహా",
      "benefit": "22 స్థానిక భారతీయ భాషలలో వ్యవసాయ శాస్త్రవేత్తలతో తక్షణ ఉచిత ఫోన్ సంప్రదింపులు.",
      "eligibility": "భారతదేశంలోని రైతులందరికీ ఉచిత సేవ.",
      "key_actions": [
        "టోల్-ఫ్రీ 1800-180-1551 కి డయల్ చేయండి.",
        "సంవత్సరంలో 365 రోజులు ఉదయం 6:00 నుండి రాత్రి 10:00 వరకు అందుబాటులో ఉంటుంది.",
        "ప్రత్యేక సమస్యలను ఐసీఏఆర్ శాస్త్రవేత్తలకు సూచిస్తారు."
      ],
      "helpline": "1800-180-1551 (టోల్-ఫ్రీ)"
    }
  ],
  "ta": [
    {
      "id": "pm-kisan",
      "title": "பிஎம்-கிசான் (பிரதம மந்திரி கிசான் சம்மான் நிதி)",
      "category": "நிதி உதவி",
      "benefit": "ஆண்டுக்கு ரூ. 6,000 நேரடி வருமான உதவி, தலா ரூ. 2,000 வீதம் மூன்று தவணைகளில் வங்கி கணக்கில் செலுத்தப்படுகிறது.",
      "eligibility": "இந்தியாவில் நிலமுள்ள அனைத்து விவசாயக் குடும்பங்களும் தகுதியுடையவர்கள்.",
      "key_actions": [
        "pmkisan.gov.in அல்லது பொதுச் சேவை மையத்தில் ஆதார் ஓடிபி மூலம் இ-கேஒய்சி முடிக்கவும்.",
        "வங்கி கணக்கு ஆதாருடன் இணைக்கப்பட்டுள்ளதா என்பதை உறுதிப்படுத்தவும்.",
        "போர்ட்டலில் நில இணைப்பு நிலையை சரிபார்க்கவும்."
      ],
      "helpline": "155261 / 1800-115-526",
      "portal_url": "https://pmkisan.gov.in"
    },
    {
      "id": "pmfby",
      "title": "பிஎம்எஃப்பிஒய் (பிரதம மந்திரி பயிர் காப்பீட்டுத் திட்டம்)",
      "category": "பயிர் காப்பீடு",
      "benefit": "பயிர் இழப்பு மற்றும் இயற்கை சீற்றங்களுக்கு முழுமையான காப்பீடு. ராபி பயிருக்கு 1.5%, காரிஃப் பயிருக்கு 2% மட்டுமே பிரீமியம்.",
      "eligibility": "அறிவிக்கப்பட்ட பகுதிகளில் அறிவிக்கப்பட்ட பயிர்களை பயிரிடும் அனைத்து விவசாயிகள் மற்றும் குத்தகைதாரர்கள்.",
      "notice_period": "இயற்கை சீற்றங்கள் ஏற்பட்டால் கட்டாயமாக 72 மணி நேரத்திற்குள் தெரிவிக்க வேண்டும்.",
      "key_actions": [
        "72 மணி நேரத்திற்குள் பயிர் காப்பீட்டு செயலி அல்லது 14447 என்ற எண்ணில் தெரிவிக்கவும்.",
        "ஆய்வுக்காக பாதிக்கப்பட்ட நிலத்தின் புகைப்படங்களை தயாராக வைத்திருக்கவும்.",
        "இழப்பீட்டுத் தொகை நேரடியாக வங்கிக் கணக்கில் வரவு வைக்கப்படும்."
      ],
      "helpline": "14447 (பயிர் காப்பீடு கட்டணமில்லா எண்)",
      "portal_url": "https://pmfby.gov.in"
    },
    {
      "id": "kcc",
      "title": "கிசான் கடன் அட்டை (கேசிசி திட்டம்)",
      "category": "கடன் மற்றும் சந்தை",
      "benefit": "சரியான நேரத்தில் திருப்பி செலுத்தினால் 4% வட்டியில் விவசாயத்திற்கு வங்கிக் கடன் உதவி.",
      "eligibility": "தனிநபர் விவசாயிகள், குத்தகை விவசாயிகள் மற்றும் மகளிர் சுய உதவிக்குழுக்கள்.",
      "key_actions": [
        "நில ஆவணங்கள் மற்றும் ஆதாருடன் அருகில் உள்ள வங்கியில் விண்ணப்பிக்கவும்.",
        "ரூ. 1.60 லட்சம் வரை எவ்வித அடமானமும் தேவையில்லை.",
        "எளிய ஒரு பக்க விண்ணப்பப் படிவம் அனைத்து வங்கிகளிலும் கிடைக்கிறது."
      ],
      "helpline": "1800-180-1551"
    },
    {
      "id": "soil-health-card",
      "title": "மண் வள அட்டை திட்டம் (Soil Health Card)",
      "category": "மண் மற்றும் ஆலோசனை",
      "benefit": "ஒவ்வொரு 2 ஆண்டுகளுக்கும் 12 மண் ஊட்டச்சத்து பரிசோதனை மற்றும் உரம் பயன்பாட்டு வழிகாட்டுதல்.",
      "eligibility": "இந்தியாவில் உள்ள அனைத்து விவசாய நில உரிமையாளர்களும் பயிரிடுபவர்களும்.",
      "key_actions": [
        "நிலத்திலிருந்து 0-15 செ.மீ ஆழத்தில் மண் மாதிரிகளை சேகரிக்கவும்.",
        "கிராம வேளாண்மை அலுவலகம் அல்லது கேவிகே மையத்தில் ஒப்படைக்கவும்.",
        "போர்ட்டலில் இருந்து மண் வள அட்டை அறிக்கையை பதிவிறக்கவும்."
      ],
      "helpline": "1800-180-1551",
      "portal_url": "https://soilhealth.dac.gov.in"
    },
    {
      "id": "enam",
      "title": "இ-நாம் (தேசிய வேளாண் சந்தை)",
      "category": "கடன் மற்றும் சந்தை",
      "benefit": "நாடு தழுவிய மின் வர்த்தக சந்தை, வெளிப்படையான இணைய ஏலம் மற்றும் நேரடி வங்கி பணப்பரிமாற்றம்.",
      "eligibility": "விவசாயிகள், உழவர் உற்பத்தியாளர் அமைப்புகள் மற்றும் உரிமம் பெற்ற வர்த்தகர்கள்.",
      "key_actions": [
        "enam.gov.in இணையதளத்தில் வங்கி பாஸ்புக் கொண்டு பதிவு செய்யவும்.",
        "விளைபொருளை சந்தைக்கு கொண்டு சென்று தரம் பிரிக்கவும்.",
        "ஏலம் முடிந்ததும் நேரடியாக வங்கி கணக்கில் பணம் பெறவும்."
      ],
      "helpline": "1800-270-0224",
      "portal_url": "https://enam.gov.in"
    },
    {
      "id": "kisan-call-centre",
      "title": "கிசான் அழைப்பு மையம் (கேசிசி உதவி எண்)",
      "category": "மண் மற்றும் ஆலோசனை",
      "benefit": "22 இந்திய மொழிகளில் வேளாண் விஞ்ஞானிகளுடன் உடனடி இலவச தொலைபேசி ஆலோசனை.",
      "eligibility": "அனைத்து விவசாயிகளுக்கும் முற்றிலும் இலவசம்.",
      "key_actions": [
        "1800-180-1551 என்ற இலவச எண்ணை தொடர்பு கொள்ளவும்.",
        "ஆண்டு முழுவதும் காலை 6:00 மணி முதல் இரவு 10:00 மணி வரை செயல்படும்.",
        "முக்கிய சந்தேகங்கள் ஐசிஏஆர் (ICAR) விஞ்ஞானிகளுக்கு அனுப்பப்படும்."
      ],
      "helpline": "1800-180-1551 (கட்டணமில்லா எண்)"
    }
  ],
  "mr": [
    {
      "id": "pm-kisan",
      "title": "पीएम-किसान (प्रधानमंत्री किसान सन्मान निधी)",
      "category": "आर्थिक सहाय्य",
      "benefit": "दरवर्षी ₹६,००० चे थेट उत्पन्न सहाय्य, ₹२,००० च्या ३ समान हप्त्यांमध्ये थेट बँक खात्यात जमा.",
      "eligibility": "उच्च आर्थिक स्थिती वगळता देशातील सर्व शेतकरी कुटुंबे.",
      "key_actions": [
        "pmkisan.gov.in वर आधार ओटीपी किंवा सीएससी केंद्रावर बायोमेट्रिक ई-केवायसी पूर्ण करा.",
        "बँक खाते आधारशी जोडलेले आणि डीबीटी सक्रिय असल्याची खात्री करा.",
        "पोर्टलवर लँड सीडिंग स्थिती तपासा."
      ],
      "helpline": "155261 / 1800-115-526",
      "portal_url": "https://pmkisan.gov.in"
    },
    {
      "id": "pmfby",
      "title": "पीएमएफबीवाय (प्रधानमंत्री पीक विमा योजना)",
      "category": "पीक विमा",
      "benefit": "नैसर्गिक आपत्ती व पीक नुकसानीवर सर्वसमावेशक विमा संरक्षण. रब्बी पिकांसाठी केवळ १.५% व खरीप पिकांसाठी २% शेतकरी प्रीमियम.",
      "eligibility": "अधिसूचित क्षेत्रातील अधिसूचित पिके घेणारे सर्व शेतकरी (भाडेकरू शेतकऱ्यांसह).",
      "notice_period": "स्थानिक आपत्ती घडल्यास ७२ तासांच्या आत नुकसानीची पूर्वसूचना देणे बंधनकारक.",
      "key_actions": [
        "७२ तासांच्या आत क्रॉप इन्शुरन्स ॲप, १४४४७ किंवा स्थानिक बँकेत माहिती नोंदवा.",
        "पंचनाम्यासाठी बाधित शेताचे फोटो व पेरणी प्रमाणपत्र तयार ठेवा.",
        "थेट आधार संलग्न बँक खात्यात विम्याची रक्कम मिळवा."
      ],
      "helpline": "14447 (टोल-फ्री पीक विमा)",
      "portal_url": "https://pmfby.gov.in"
    },
    {
      "id": "kcc",
      "title": "किसान क्रेडिट कार्ड (केसीसी योजना)",
      "category": "कर्ज आणि बाजार",
      "benefit": "वेळेवर परतफेडीवर ३% सवलतीसह केवळ ४% वार्षिक व्याजदराने शेतीसाठी संस्थात्मक कर्ज.",
      "eligibility": "वैयक्तिक शेतकरी, कुळ शेतकरी, बटाईदार व शेतकरी बचत गट.",
      "key_actions": [
        "जमीन महसूल नोंद व आधारसह जवळच्या बँक शाखेत अर्ज करा.",
        "₹१.६० लाखांपर्यंतच्या कर्जासाठी कोणत्याही तारणाची गरज नाही.",
        "सर्व बँकांमध्ये एका पानाचा सोपा अर्ज उपलब्ध आहे."
      ],
      "helpline": "1800-180-1551"
    },
    {
      "id": "soil-health-card",
      "title": "मृदा आरोग्य पत्रिका योजना (Soil Health Card)",
      "category": "मृदा आणि सल्ला",
      "benefit": "दर २ वर्षांनी १२ मृदा घटकांची तपासणी आणि पिकांनुसार संतुलित खत शिफारसी.",
      "eligibility": "भारतातील सर्व शेतजमीन मालक आणि कसणारे शेतकरी.",
      "key_actions": [
        "शेतातून ०-१५ सेमी खोलीवरून जिग-जॅग पद्धतीने मातीचा नमुना गोळा करा.",
        "नमुना कृषी सहाय्यक किंवा नजीकच्या कृषी विज्ञान केंद्रात जमा करा.",
        "पोर्टलवरून जिल्हा व ब्लॉक कोडद्वारे अहवाल डाऊनलोड करा."
      ],
      "helpline": "1800-180-1551",
      "portal_url": "https://soilhealth.dac.gov.in"
    },
    {
      "id": "enam",
      "title": "ई-नाम (राष्ट्रीय कृषी बाजार)",
      "category": "कर्ज आणि बाजार",
      "benefit": "घाऊक बाजारपेठांचे देशव्यापी ऑनलाइन व्यासपीठ, पारदर्शक ई-लिलाव आणि थेट बँक खात्यात पैसे.",
      "eligibility": "शेतकरी, शेतकरी उत्पादक कंपन्या (FPO) आणि परवानाधारक व्यापारी.",
      "key_actions": [
        "enam.gov.in वर बँक पासबुकसह विनामूल्य नोंदणी करा.",
        "शेतमाल बाजार समितीत आणून लॉट व प्रतवारी करून घ्या.",
        "ऑनलाइन बोली स्वीकारल्यानंतर थेट खात्यात पैसे जमा होतील."
      ],
      "helpline": "1800-270-0224",
      "portal_url": "https://enam.gov.in"
    },
    {
      "id": "kisan-call-centre",
      "title": "किसान कॉल सेंटर (केसीसी हेल्पलाईन)",
      "category": "मृदा आणि सल्ला",
      "benefit": "२२ भारतीय भाषांमध्ये कृषी शास्त्रज्ञ आणि तज्ज्ञांशी मोफत थेट फोन सल्ला.",
      "eligibility": "देशातील सर्व शेतकऱ्यांसाठी विनामूल्य.",
      "key_actions": [
        "टोल-फ्री १८००-१८०-१५५१ वर संपर्क साधा.",
        "वर्षाचे ३६५ दिवस सकाळी ६:०० ते रात्री १०:०० वाजेपर्यंत सुरू.",
        "महत्त्वाच्या समस्या आयसीएआर (ICAR) शास्त्रज्ञांकडे वर्ग केल्या जातात."
      ],
      "helpline": "1800-180-1551 (टोल-फ्री)"
    }
  ]
};

export function getLocalizedSchemes(lang: LanguageCode): GovernmentScheme[] {
  return LOCALIZED_SCHEMES[lang] || LOCALIZED_SCHEMES['en'];
}

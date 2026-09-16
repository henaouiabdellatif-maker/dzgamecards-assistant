import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="DZGAMECARDS OMNI-AI 2050",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة فخمة ومستقبلية لعام 2050 (Dark Glassmorphism & Neon Glows)
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    .main {
        background: transparent;
    }
    /* أزرار نيون متوهجة */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #020617;
        border-radius: 14px;
        border: none;
        padding: 12px 24px;
        font-weight: 800;
        letter-spacing: 0.5px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 35px rgba(79, 172, 254, 0.8);
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    /* صناديق الإدخال الزجاجية */
    div.stSelectbox, div.stTextInput, div.stTextArea {
        background-color: rgba(30, 41, 59, 0.7);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
    }
    h1, h2, h3 {
        color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    .title-glow {
        background: linear-gradient(90deg, #00f2fe, #4facfe, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي المستقبلي
with st.sidebar:
    st.markdown("<h2 style='text-align: center;' class='title-glow'>🌌 OMNI-AI 2050</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>دمج قوى Claude + ChatGPT + Gemini</p>", unsafe_allow_html=True)
    st.divider()
    
    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    if not api_key:
        api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
    else:
        st.success("النواة الخارقة متصلة بنجاح 🔒")
        
    st.divider()
    
    # اختيار شخصية وتخصص الذكاء الاصطناعي (ليخدم أي شخص: طباخ، تاجر، مبرمج، إلخ)
    ai_persona = st.selectbox(
        "🧠 اختر عقلية وخبيرة الذكاء الاصطناعي:",
        [
            "عقلية Omni الخارقة (Claude + ChatGPT + Gemini مدمجون)",
            "خبير التجارة الإلكترونية وإدارة DZGAMECARDS",
            "مهندس البروموتات الأسطوري (Prompt Master)",
            "شيف عالمي وخبير وصفات طهي وأغذية",
            "مستشار قانوني ومالي وتجاري متقدم",
            "مبرمج خارق ومهندس برمجيات محترف"
        ]
    )

    st.divider()
    app_mode = st.radio(
        "⚡ الأنظمة الأساسية:",
        [
            "💬 المحادثة الخارقة (صوت + كتابة + ذاكرة)",
            "🎨 استوديو خلق الصور والبوسترات (Imagen 3)",
            "🛠️ مصنع المحتوى، البروموتات، والردود الفورية"
        ]
    )
    
    st.divider()
    if st.button("🗑️ فرمتة الذاكرة وبدء محادثة جديدة"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح الـ API في الشريط الجانبي لتفعيل طاقة الذكاء الاصطناعي الخارق.")
else:
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-3.6-flash"

    # تخصيص النظام بناءً على الاختيار
    persona_prompts = {
        "عقلية Omni الخارقة (Claude + ChatGPT + Gemini مدمجون)": "أنت نظام ذكاء اصطناعي خارق ومتطور لعام 2050 يدمج العمق التحليلي لـ Claude، طلاقة ChatGPT، وسرعة وقوة Gemini. قدم إجابات عبقرية، دقيقة، عميقة، ومفيدة لأي مستخدم في العالم.",
        "خبير التجارة الإلكترونية وإدارة DZGAMECARDS": "أنت مستشار تجاري وتسويقي عالمي خبير في إدارة المتاجر الرقمية مثل متجر 'DZGAMECARDS' للبطاقات الرقمية. ساعد المستخدم في زيادة المبيعات، صياغة الإعلانات، وإدارة الزبائن باحترافية.",
        "مهندس البروموتات الأسطوري (Prompt Master)": "أنت أفضل مهندس بروموتات (Prompt Engineer) على وجه الأرض. مهمتك تحويل أفكار المستخدم البسيطة إلى بروموتات خارقة ومفصلة لنماذج الذكاء الاصطناعي.",
        "شيف عالمي وخبير وصفات طهي وأغذية": "أنت شيف عالمي حائز على نجوم ميشلان وخبير تغذية. ساعد المستخدم في ابتكار وصفات طهي مذهلة، أسرار المطبخ، وتخطيط وجبات صحية ولذيذة.",
        "مستشار قانوني ومالي وتجاري متقدم": "أنت مستشار مالي وقانوني ذكي ومحترف. قدم تحليلات منطقية، استراتيجيات استثمارية، وإرشادات واضحة وآمنة.",
        "مبرمج خارق ومهندس برمجيات محترف": "أنت مطور برمجيات عبقري ومبرمج أسطوري. اكتب أكواد نظيفة، آمنة، ومثالية بأي لغة برمجة يطلبها المستخدم."
    }
    active_system_prompt = persona_prompts.get(ai_persona, persona_prompts["عقلية Omni الخارقة (Claude + ChatGPT + Gemini مدمجون)"])

    # ================= 1. المحادثة الخارقة =================
    if app_mode == "💬 المحادثة الخارقة (صوت + كتابة + ذاكرة)":
        st.markdown("<h1 class='title-glow'>💬 المحادثة الخارقة الشاملة</h1>", unsafe_allow_html=True)
        st.markdown("تحدث معي في أي شيء تريده (برمجة، طبخ، تجارة، فلسفة، تخطيط). يمكنك الكتابة أو استخدام **الميكروفون** للتحدث صوتياً وسأجيبك فوراً.")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "model", 
                    "content": "أهلاً بك في نظام Omni-AI الخارق. لقد تم دمج قوى Claude و ChatGPT و Gemini خصيصاً لك. بماذا سنبدأ الإبداع اليوم؟"
                }
            ]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("اكتب طلبك أو سؤالك الخارق هنا...")
            
        st.markdown("---")
        st.subheader("🎙️ أو تحدث معي صوتياً مباشرة:")
        audio_file = st.audio_input("اضغط لتسجيل رسالتك الصوتية")

        if audio_file is not None:
            audio_bytes = audio_file.read()
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            
            with st.spinner("🎧 جاري الاستماع لصوتك وتحليله عبر العقل الخارق..."):
                try:
                    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[audio_part, f"بصفتك {ai_persona}، أجب على هذا التسجيل الصوتى بدقة واحترافية فائقة."]
                    )
                    reply = response.text
                    st.session_state.messages.append({"role": "user", "content": "🎙️ [رسالة صوتية مرسلة]"})
                    st.session_state.messages.append({"role": "model", "content": reply})
                    st.rerun()
                except Exception as e:
                    err_str = str(e)
                    if "503" in err_str:
                        st.warning("⏳ خوادم جوجل تشهد ضغطاً مؤقتاً (503). يرجى المحاولة بعد ثوانٍ.")
                    elif "429" in err_str:
                        st.warning("⏳ تم الوصول للحد المؤقت للطلبات. انتظر قليلاً وجرب مجدداً.")
                    else:
                        st.error(f"خطأ في معالجة الصوت: {e}")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("model"):
                with st.spinner("✨ جاري التفكير ومعالجة الرد الخارق..."):
                    try:
                        formatted_msgs = [
                            types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
                            for m in st.session_state.messages
                        ]
                        res = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=formatted_msgs,
                            config=types.GenerateContentConfig(system_instruction=active_system_prompt, temperature=0.7)
                        )
                        reply = res.text
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "model", "content": reply})
                    except Exception as e:
                        err_str = str(e)
                        if "503" in err_str:
                            st.warning("⏳ ضغط مؤقت في الخوادم (503). اضغط أرسل مرة أخرى بعد ثوانٍ.")
                        elif "429" in err_str:
                            st.warning("⏳ تم الوصول للحد المسموح مؤقتاً. انتظر قليلاً.")
                        else:
                            st.error(f"خطأ: {e}")

    # ================= 2. استوديو الصور (Imagen 3) =================
    elif app_mode == "🎨 استوديو خلق الصور والبوسترات (Imagen 3)":
        st.markdown("<h1 class='title-glow'>🎨 استوديو التصميم والخلق البصري</h1>", unsafe_allow_html=Task := "🎨")
        st.markdown("صف أي صورة تخيلية، بوستر إعلاني، تصميم مستقبل لعام 2050، أو إعلان لمتجرك، وسيقوم الذكاء الاصطناعي برسمها بجودة سينمائية فائقة.")

        img_prompt = st.text_area(
            "اكتب وصف الصورة بالتفصيل الدقيق:",
            "Futuristic cyberpunk store banner for digital cards named DZGAMECARDS, neon blue and purple lights, ultra realistic, cinematic lighting, 8k resolution"
        )
        
        aspect_ratio = st.selectbox("اختر أبعاد التصميم:", ["1:1 (مربع للإنستغرام)", "16:9 (أفقي للفيسبوك والويب)", "9:16 (عمودي للريلز والتيك توك)"])
        
        if st.button("🚀 توليد الصورة الخارقة الآن"):
            if img_prompt.strip():
                with st.spinner("🎨 جاري رسم وتوليد الصورة عبر محرك Imagen 3..."):
                    try:
                        ratio_map = {"1:1 (مربع للإنستغرام)": "1:1", "16:9 (أفقي للفيسبوك والويب)": "16:9", "9:16 (عمودي للريلز والتيك توك)": "9:16"}
                        selected_ratio = ratio_map.get(aspect_ratio, "1:1")

                        result = client.models.generate_images(
                            model='imagen-3.0-generate-002',
                            prompt=img_prompt,
                            config=types.GenerateImagesConfig(
                                number_of_images=1,
                                output_mime_type="image/jpeg",
                                aspect_ratio=selected_ratio
                            )
                        )
                        st.success("✨ تم توليد التحفة البصرية بنجاح!")
                        for generated_image in result.generated_images:
                            image = Image.open(BytesIO(generated_image.image.image_bytes))
                            st.image(image, caption="التصميم المولد بالذكاء الاصطناعي الخارق", use_container_width=True)
                    except Exception as e:
                        err_str = str(e)
                        if "503" in err_str:
                            st.warning("⏳ خوادم توليد الصور مشغولة مؤقتاً (503). انتظر دقيقة وجرب مجدداً.")
                        else:
                            st.error(f"خطأ في توليد الصورة: {e}")
            else:
                st.warning("الرجاء كتابة وصف الصورة أولاً.")

    # ================= 3. مصنع المحتوى والبروموتات =================
    elif app_mode == "🛠️ مصنع المحتوى، البروموتات، والردود الفورية":
        st.markdown("<h1 class='title-glow'>🛠️ مصنع الأدوات والبروموتات الخارقة</h1>", unsafe_allow_html=True)
        st.markdown("أداة متخصصة لإنشاء الردود التجارية، هندسة البروموتات المعقدة، أو توليد محتوى تسويقي وإبداعي لأي مجال.")

        sub_tool = st.radio("اختر الوظيفة المطلوبة:", ["صياغة ردود تجارية للزبائن", "هندسة بروموت احترافي متكامل", "توليد إستراتيجية تسويقية أو خطة عمل كاملة"])

        if sub_tool == "صياغة ردود تجارية للزبائن":
            c_msg = st.text_area("أدخل رسالة أو استفسار الزبون:")
            if st.button("✨ توليد رد تسويقي ساحر وجاهز للنسخ"):
                if c_msg.strip():
                    with st.spinner("جاري صياغة رد احترافي..."):
                        try:
                            p = f"بصفتك خبير مبيعات وتجارة، اكتب رداً تجارياً احترافياً ومقنعاً لرسالة زبون تقول: '{c_msg}'."
                            res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=active_system_prompt))
                            st.success("الرد الجاهز للنسخ:")
                            st.markdown(res.text)
                        except Exception as e:
                            st.warning(f"خطأ مؤقت: {e}")
                else:
                    st.warning("الرجاء كتابة رسالة الزبون.")
        elif sub_tool == "هندسة بروموت احترافي متكامل":
            p_topic = st.text_input("ما هو موضوع أو هدف البروموت الذي تريده؟", "إعلان ترويجي لبطاقات جوجل بلاي مع خصم خاص")
            if st.button("🚀 هندسة بروموت أسطوري"):
                with st.spinner("جاري هندسة البروموت الخارق..."):
                    try:
                        p = f"اعمل كأفضل Prompt Engineer في العالم. اكتب بروموت مفصل، احترافي، ومذهل لنماذج الذكاء الاصطناعي بناءً على هذا الطلب: '{p_topic}'."
                        res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=active_system_prompt))
                        st.success("البروموت المهندس جاهز:")
                        st.markdown(res.text)
                    except Exception as e:
                        st.warning(f"خطأ مؤقت: {e}")
        else:
            plan_topic = st.text_input("ما هو المشروع أو المجال الذي تريد خطة له؟", "مشروع متجر بطاقات رقمية مصغر")
            if st.button("📈 توليد خطة عمل استراتيجية شاملة"):
                with st.spinner("جاري صياغة الخطة الاستراتيجية..."):
                    try:
                        p = f"اكتب خطة عمل استراتيجية، مفصلة، وعميقة جداً لمشروع: '{plan_topic}'. ضع خطوات واضحة، أفكار تسويقية، وتحليلاً للمخاطر."
                        res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=active_system_prompt))
                        st.success("الخطة الاستراتيجية جاهزة:")
                        st.markdown(res.text)
                    except Exception as e:
                        st.warning(f"خطأ مؤقت: {e}")

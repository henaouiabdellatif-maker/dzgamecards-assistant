import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="DZGAMECARDS Omni-AI Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم عصري فاخر
st.markdown("""
<style>
    .main {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
    }
    div.stSelectbox, div.stTextInput, div.stTextArea {
        background-color: #161b22;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    h1, h2, h3 {
        color: #f0f6fc;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌌 DZGAMECARDS OMNI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 14px;'>المساعد الخارق لمتجرك الرقمي</p>", unsafe_allow_html=True)
    st.divider()
    
    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    if not api_key:
        api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
    else:
        st.success("المفتاح الذكي متصل بنجاح 🔒")
        
    st.divider()
    app_mode = st.radio(
        "🎯 اختر النظام الخارق:",
        [
            "💬 المحادثة الشاملة والمساعد الصوتي",
            "🎨 استوديو توليد الصور الإعلانية (Imagen)",
            "🤝 صانع الردود والبروموتات الاحترافية"
        ]
    )
    
    st.divider()
    if st.button("🗑️ مسح الذاكرة والمحادثات"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح الـ API الخاص بك في الشريط الجانبي للبدء.")
else:
    client = genai.Client(api_key=api_key)
    # استخدام النموذج الأكثر استقراراً وسرعة لتجنب أخطاء الضغط
    STABLE_MODEL = "gemini-2.5-flash"

    # ================= 1. المحادثة الشاملة =================
    if app_mode == "💬 المحادثة الشاملة والمساعد الصوتي":
        st.header("💬 المحادثة الخارقة (Omni-Chat)")
        st.markdown("تحدث بحرية تامة، اطلب استراتيجيات تسويقية، صياغة محتوى، أو استخدم **الميكروفون** للتحدث صوتياً.")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "model", 
                    "content": "أهلاً بك يا صاحبي. أنا نظامك الذكي المدمج لمتجر **DZGAMECARDS**. كيف أساعدك اليوم؟"
                }
            ]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("اكتب أي شيء تريده هنا...")
            
        st.markdown("---")
        st.subheader("🎙️ أو تحدث صوتياً مباشرة:")
        audio_file = st.audio_input("اضغط لتسجيل رسالتك الصوتية")

        if audio_file is not None:
            audio_bytes = audio_file.read()
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            
            with st.spinner("🎧 جاري الاستماع لصوتك وتحليله..."):
                try:
                    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
                    response = client.models.generate_content(
                        model=STABLE_MODEL,
                        contents=[audio_part, "أجب على هذا التسجيل الصوتي باللغة العربية بطريقة احترافية لمتجر بطاقات رقمية DZGAMECARDS."]
                    )
                    reply = response.text
                    st.session_state.messages.append({"role": "user", "content": "🎙️ [رسالة صوتية]"})
                    st.session_state.messages.append({"role": "model", "content": reply})
                    st.rerun()
                except Exception as e:
                    if "503" in str(e):
                        st.warning("⏳ خوادم جوجل تشهد ضغطاً مؤقتاً (503). يرجى المحاولة بعد ثوانٍ قليلة.")
                    elif "429" in str(e):
                        st.warning("⏳ تم الوصول للحد المؤقت للطلبات. انتظر قليلاً وجرب مرة أخرى.")
                    else:
                        st.error(f"خطأ في المعالجة الصوتية: {e}")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("model"):
                with st.spinner("✨ جاري صياغة الرد المذهل..."):
                    try:
                        system_inst = "أنت مساعد ذكي خارق ومتقدم لمتجر 'DZGAMECARDS' للبطاقات الرقمية. قدم إجابات عميقة، منطقية، ومفيدة للغاية."
                        formatted_msgs = [
                            types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
                            for m in st.session_state.messages
                        ]
                        res = client.models.generate_content(
                            model=STABLE_MODEL,
                            contents=formatted_msgs,
                            config=types.GenerateContentConfig(system_instruction=system_inst, temperature=0.7)
                        )
                        reply = res.text
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "model", "content": reply})
                    except Exception as e:
                        if "503" in str(e):
                            st.warning("⏳ خوادم جوجل تشهد ضغطاً مؤقتاً (503). يرجى المحاولة بعد قليل.")
                        elif "429" in str(e):
                            st.warning("⏳ تم الوصول للحد المؤقت للطلبات. انتظر قليلاً.")
                        else:
                            st.error(f"خطأ: {e}")

    # ================= 2. استوديو توليد الصور الإعلانية =================
    elif app_mode == "🎨 استوديو توليد الصور الإعلانية (Imagen)":
        st.header("🎨 صانع الصور الإعلانية والتصميمات (AI Image Studio)")
        st.markdown("اكتب وصفاً لأي إعلان أو بوستر لبطاقات متجرك، وسيقوم الذكاء الاصطناعي برسمه فوراً.")

        img_prompt = st.text_area(
            "صف الصورة التي تريدها بالتفصيل:",
            "Professional promotional banner for digital gift cards store named DZGAMECARDS, glowing blue and dark futuristic aesthetic, high quality marketing design"
        )
        
        aspect_ratio = st.selectbox("أبعاد الصورة:", ["1:1 (مربع للإنستغرام)", "16:9 (أفقي للفيسبوك)", "9:16 (عمودي للتيك توك)"])
        
        if st.button("🚀 توليد الصورة الآن"):
            if img_prompt.strip():
                with st.spinner("🎨 جاري رسم وتوليد الصورة..."):
                    try:
                        ratio_map = {"1:1 (مربع للإنستغرام)": "1:1", "16:9 (أفقي للفيسبوك)": "16:9", "9:16 (عمودي للتيك توك)": "9:16"}
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
                        st.success("✨ تم توليد الصورة بنجاح!")
                        for generated_image in result.generated_images:
                            image = Image.open(BytesIO(generated_image.image.image_bytes))
                            st.image(image, caption="الصورة الإعلانية لمتجر DZGAMECARDS", use_container_width=True)
                    except Exception as e:
                        if "503" in str(e):
                            st.warning("⏳ خوادم توليد الصور مشغولة مؤقتاً (503). انتظر دقيقة وجرب مجدداً.")
                        else:
                            st.error(f"خطأ في توليد الصورة: {e}")
            else:
                st.warning("الرجاء كتابة وصف الصورة أولاً.")

    # ================= 3. صانع الردود والبروموتات =================
    elif app_mode == "🤝 صانع الردود والبروموتات الاحترافية":
        st.header("⚡ صانع البروموتات والردود الذكية")
        tool_choice = st.radio("اختر الوظيفة:", ["رد ذكي على رسائل الزبائن", "هندسة بروموت لـ OmniFlash/Gemini"])

        if tool_choice == "رد ذكي على رسائل الزبائن":
            cust_msg = st.text_area("أدخل رسالة الزبون:")
            if st.button("✨ صياغة رد تسويقي محترف"):
                if cust_msg.strip():
                    with st.spinner("جاري صياغة الرد..."):
                        try:
                            p = f"اكتب رداً تجارياً احترافياً ومقنعاً لرسالة زبون على صفحة متجر 'DZGAMECARDS': '{cust_msg}'."
                            res = client.models.generate_content(model=STABLE_MODEL, contents=p)
                            st.success("الرد الجاهز للنسخ:")
                            st.markdown(res.text)
                        except Exception as e:
                            st.warning("⏳ خوادم جوجل مشغولة مؤقتاً، جرب مرة أخرى بعد قليل.")
                else:
                    st.warning("الرجاء إدخال رسالة الزبون.")
        else:
            p_name = st.text_input("اسم المنتج:", "بطاقات فري فاير")
            p_details = st.text_input("تفاصيل العرض:", "تسليم فوري")
            if st.button("🚀 هندسة بروموت احترافي"):
                with st.spinner("جاري هندسة البروموت..."):
                    try:
                        p = f"اكتب بروموت مفصل وموجه لنماذج الذكاء الاصطناعي لمتجر 'DZGAMECARDS'. المنتج: {p_name}, التفاصيل: {p_details}."
                        res = client.models.generate_content(model=STABLE_MODEL, contents=p)
                        st.success("البروموت المهندس جاهز:")
                        st.markdown(res.text)
                    except Exception as e:
                        st.warning("⏳ خوادم جوجل مشغولة مؤقتاً، جرب مرة أخرى بعد قليل.")

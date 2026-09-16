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

# تصميم عصري فخم مستوحى من أحدث منصات الذكاء الاصطناعي العالمية
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
        box-shadow: 0 6px 16px rgba(168, 85, 247, 0.4);
    }
    div.stSelectbox, div.stTextInput, div.stTextArea {
        background-color: #161b22;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    h1, h2, h3 {
        color: #f0f6fc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي الفخم
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌌 DZGAMECARDS OMNI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 14px;'>الجيل القادم من الذكاء الاصطناعي لمتجرك</p>", unsafe_allow_html=True)
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
    st.warning("⚠️ الرجاء إدخال مفتاح الـ API الخاص بك في الشريط الجانبي للبدء في استخدام المساعد الخارق.")
else:
    client = genai.Client(api_key=api_key)

    # ================= 1. المحادثة الشاملة (Claude + ChatGPT + Gemini) =================
    if app_mode == "💬 المحادثة الشاملة والمساعد الصوتي":
        st.header("💬 المحادثة الخارقة (Omni-Chat)")
        st.markdown("تحدث بحرية تامة، اطلب استراتيجيات تسويقية، صياغة محتوى، أفكار مشاريع، أو استخدم **الميكروفون** للتحدث صوتياً.")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "model", 
                    "content": "أهلاً بك يا صاحبي. أنا نظامك الذكي المدمج (يمدك بقوة التحليل، هلاسة الكتابة، وإبداع التصميم). كيف سنطور متجر **DZGAMECARDS** اليوم؟"
                }
            ]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("اكتب أي شيء تريده هنا (تفكير، برمجة، تسويق، أفكار)...")
            
        st.markdown("---")
        st.subheader("🎙️ أو تحدث صوتياً مباشرة:")
        audio_file = st.audio_input("اضغط لتسجيل رسالتك الصوتية")

        if audio_file is not None:
            audio_bytes = audio_file.read()
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            
            with st.spinner("🎧 جاري الاستماع لصوتك وتحليله بدقة خارقة..."):
                try:
                    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[audio_part, "أجب على هذا التسجيل الصوتي باللغة العربية بطريقة احترافية، ذكية، ومفيدة جداً لمتجر بطاقات رقمية يسمى DZGAMECARDS."]
                    )
                    reply = response.text
                    st.session_state.messages.append({"role": "user", "content": "🎙️ [رسالة صوتية]"})
                    st.session_state.messages.append({"role": "model", "content": reply})
                    st.rerun()
                except Exception as e:
                    if "429" in str(e):
                        st.warning("⏳ تم الوصول للحد المؤقت للطلبات المجانية. انتظر 20 ثانية وجرب مرة أخرى.")
                    else:
                        st.error(f"خطأ في المعالجة الصوتية: {e}")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("model"):
                with st.spinner("✨ جاري التفكير وصياغة رد مذهل..."):
                    try:
                        system_inst = (
                            "أنت مساعد ذكي خارق ومتقدم جداً يدمج أفضل قدرات التحليل والإبداع لـ Claude و ChatGPT و Gemini. "
                            "أنت مستشار خاص لمتجر 'DZGAMECARDS' للبطاقات الرقمية. قدم إجابات عميقة، منطقية، مذهلة، ومفيدة للغاية."
                        )
                        formatted_msgs = [
                            types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
                            for m in st.session_state.messages
                        ]
                        res = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=formatted_msgs,
                            config=types.GenerateContentConfig(system_instruction=system_inst, temperature=0.7)
                        )
                        reply = res.text
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "model", "content": reply})
                    except Exception as e:
                        if "429" in str(e):
                            st.warning("⏳ تم الوصول للحد المؤقت (5 طلبات/دقيقة). انتظر قليلاً ثم حاول مجدداً.")
                        else:
                            st.error(f"خطأ: {e}")

    # ================= 2. استوديو توليد الصور الإعلانية (Imagen) =================
    elif app_mode == "🎨 استوديو توليد الصور الإعلانية (Imagen)":
        st.header("🎨 صانع الصور الإعلانية والتصميمات (AI Image Studio)")
        st.markdown("اكتب وصفاً تخيلياً لأي إعلان، غلاف، أو بوستر لبطاقات متجرك، وسيقوم الذكاء الاصطناعي بتوليد الصورة بدقة مذهلة.")

        img_prompt = st.text_area(
            "صف الصورة التي تريدها بالتفصيل (مثلاً: بوستر احترافي لمتجر بطاقات رقمية يظهر فيه بطاقات جوجل بلاي وشعار DZGAMECARDS بألوان نيون زرقاء وسوداء، إضاءة سينمائية):",
            "Professional promotional banner for digital gift cards store named DZGAMECARDS, glowing blue and dark futuristic aesthetic, high quality marketing design"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            aspect_ratio = st.selectbox("أبعاد الصورة:", ["1:1 (مربع للإنستغرام)", "16:9 (أفقي للفيسبوك/تويتر)", "9:16 (عمودي للريلز/تيك توك)"])
        
        if st.button("🚀 توليد الصورة الآن"):
            if img_prompt.strip():
                with st.spinner("🎨 جاري رسم وتوليد الصورة عبر محرك الذكاء الاصطناعي..."):
                    try:
                        # ضبط الأبعاد حسب اختيار المستخدم
                        ratio_map = {"1:1 (مربع للإنستغرام)": "1:1", "16:9 (أفقي للفيسبوك/تويتر)": "16:9", "9:16 (عمودي للريلز/تيك توك)": "9:16"}
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
                            st.image(image, caption="الصورة الإعلانية المولدة لمتجر DZGAMECARDS", use_container_width=True)
                    except Exception as e:
                        if "429" in str(e):
                            st.warning("⏳ تجاوزت الحد المسموح للطلبات المجانية مؤقتاً. انتظر قليلاً ثم جرب مرة أخرى.")
                        else:
                            st.error(f"حدث خطأ أثناء توليد الصورة: {e}")
            else:
                        st.warning("الرجاء كتابة وصف الصورة أولاً.")

    # ================= 3. صانع الردود والبروموتات الاحترافية =================
    elif app_mode == "🤝 صانع الردود والبروموتات الاحترافية":
        st.header("⚡ صانع البروموتات المتقدم (OmniFlash Prompt & Customer Reply)")
        st.markdown("اختر نوع الأداة المطلوبة لصياغة الردود التجارية أو هندسة بروموتات تفصيلية مذهلة.")

        tool_choice = st.radio("اختر الوظيفة:", ["رد ذكي على رسائل الزبائن", "هندسة بروموت لـ OmniFlash/Gemini"])

        if tool_choice == "رد ذكي على رسائل الزبائن":
            cust_msg = st.text_area("أدخل رسالة الزبون (مثلاً: بكم بطاقة فري فاير وهل هناك تخفيض؟):")
            if st.button("✨ صياغة رد تسويقي محترف للزبون"):
                if cust_msg.strip():
                    with st.spinner("جاري صياغة رد يجذب الشراء..."):
                        try:
                            p = f"اكتب رداً تجارياً احترافياً ومقنعاً جداً لرسالة زبون على صفحة متجر 'DZGAMECARDS' للبطاقات الرقمية. رسالة الزبون: '{cust_msg}'."
                            res = client.models.generate_content(model="gemini-3.6-flash", contents=p)
                            st.success("الرد الجاهز للنسخ:")
                            st.markdown(res.text)
                        except Exception as e:
                            st.error(f"خطأ: {e}")
                else:
                    st.warning("الرجاء إدخال رسالة الزبون.")
        else:
            p_name = st.text_input("اسم المنتج:", "بطاقات نتفلكس شهر واحد")
            p_details = st.text_input("تفاصيل العرض أو السعر:", "1200 دج تسليم فوري عبر التيليغرام")
            if st.button("🚀 هندسة بروموت احترافي متكامل"):
                with st.spinner("جاري هندسة البروموت الخارق..."):
                    try:
                        p = (
                            f"اعمل كخبير هندسة بروموتات (Prompt Engineer) محترف. اكتب بروموت مفصل للغاية وموجه لنماذج الذكاء الاصطناعي "
                            f"لتوليد حملة إعلانية لمتجر 'DZGAMECARDS'. المنتج: {p_name}, التفاصيل: {p_details}. اجعل البروموت منظماً وقوياً."
                        )
                        res = client.models.generate_content(model="gemini-3.6-flash", contents=p)
                        st.success("البروموت المهندس جاهز للاستخدام:")
                        st.markdown(res.text)
                    except Exception as e:
                        st.error(f"خطأ: {e}")

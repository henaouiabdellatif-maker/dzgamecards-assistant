import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="DZGAMECARDS Pro Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم عصري واحترافي مستوحى من أفضل منصات الويب
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    div.stSelectbox, div.stTextInput, div.stTextArea {
        background-color: #1f2937;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي للإعدادات والتنقل
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/controller.png", width=100)
    st.title("DZGAMECARDS 🚀")
    st.markdown("إدارة المتجر، الرد على العملاء، وهندسة البروموتات المتقدمة.")
    st.divider()
    
    # جلب مفتاح الـ API تلقائياً أو من المستخدم
    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    if not api_key:
        api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
    else:
        st.success("المفتاح محمّل تلقائياً 🔒")
        
    st.divider()
    app_mode = st.radio(
        "اختر الأداة المطلوبة:",
        [
            "💬 الدردشة والمساعد الصوتي",
            "🤝 الرد الاحترافي على الزبائن",
            "⚡ مصنع بروموتات OmniFlash"
        ]
    )
    
    st.divider()
    if st.button("🗑️ مسح سجل المحادثات"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح Gemini API Key في الشريط الجانبي للبدء.")
else:
    client = genai.Client(api_key=api_key)

    # ================= 1. قسم الدردشة والمساعد الصوتي =================
    if app_mode == "💬 الدردشة والمساعد الصوتي":
        st.header("💬 المحادثة الذكية والمساعد الصوتي لمتجرك")
        st.markdown("تحدث بحرية، اكتب أفكارك، أو استخدم **الميكروفون** لتسجيل رسالتك صوتياً وسيجيبك الذكاء الاصطناعي باحترافية.")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "model", 
                    "content": "أهلاً بك يا صاحبي في الاستوديو الاحترافي لـ DZGAMECARDS. كيف أساعدك اليوم في تطوير متجرك أو إدارة صفحاتك؟"
                }
            ]

        # عرض الرسائل السابقة
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # دعم الإدخال الصوتي المباشر (Voice Input) والكتابي
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.chat_input("اكتب رسالتك أو طلبك هنا...")
            
        # إضافة زر تسجيل صوتي مباشر عبر المتصفح
        st.markdown("---")
        st.subheader("🎙️ أو سجل رسالتك صوتياً مباشرة:")
        audio_file = st.audio_input("اضغط لتسجيل الصوت")

        # معالجة الإدخال الصوتي
        if audio_file is not None:
            audio_bytes = audio_file.read()
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            
            with st.spinner("جاري الاستماع لصوتك وتحليله عبر الذكاء الاصطناعي..."):
                try:
                    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[audio_part, "قم بالرد على هذا التسجيل الصوتي باللغة العربية بطريقة احترافية ومفيدة لمتجر بطاقات رقمية يسمى DZGAMECARDS."]
                    )
                    reply = response.text
                    st.session_state.messages.append({"role": "user", "content": "🎙️ [رسالة صوتية مرسلة]"})
                    st.session_state.messages.append({"role": "model", "content": reply})
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ في معالجة الصوت: {e}")

        # معالجة الإدخال النصي العادي
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("model"):
                with st.spinner("جاري صياغة الرد الاحترافي..."):
                    try:
                        system_inst = "أنت مساعد ذكي محترف وخبير تسويق إلكتروني لمتجر 'DZGAMECARDS' للبطاقات الرقمية. قدم إجابات منطقية، عميقة، ومتقدمة جداً."
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
                        st.error(f"خطأ: {e}")

    # ================= 2. قسم الرد الاحترافي على الزبائن =================
    elif app_mode == "🤝 الرد الاحترافي على الزبائن":
        st.header("🤝 مساعد الرد الذكي على رسائل الزبائن")
        st.markdown("انسخ رسالة أو استفسار الزبون الذي وصلك على الصفحة، والصقه هنا ليقوم الذكاء الاصطناعي بكتابة رد تجاري، راقٍ، واحترافي يشجعه على إتمام الشراء فوراً.")

        client_msg = st.text_area("أدخل رسالة الزبون هنا (مثلاً: بكم سعر بطاقات جوجل بلاي وهل توصلي كود بسرعة؟):", height=100)
        
        if st.button("✨ توليد رد احترافي للزبون"):
            if client_msg.strip():
                with st.spinner("جاري صياغة أفضل رد تسويقي للزبون..."):
                    prompt = f"هذه رسالة وصلتنا من زبون لمتجر 'DZGAMECARDS' للبطاقات الرقمية: '{client_msg}'. اكتب لي رداً تجارياً احترافياً، ودوداً، ومحفزاً لإتمام الشراء مع تفاصيل وهمية مقنعة وسريعة."
                    res = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                    st.success("الرد المقترح للزبون (جاهز للنسخ والارسال):")
                    st.markdown(res.text)
            else:
                st.warning("الرجاء كتابة رسالة الزبون أولاً.")

    # ================= 3. مصنع بروموتات OmniFlash =================
    elif app_mode == "⚡ مصنع بروموتات OmniFlash":
        st.header("⚡ مصنع بروموتات OmniFlash المتقدم")
        st.markdown("هذا القسم مخصص لكتابة تفاصيل دقيقة، ليقوم الذكاء الاصطناعي بتوليد **بروموت احترافي متكامل** يمكنك نسخه مباشرة وإرساله لـ OmniFlash أو أي نموذج آخر للحصول على نتائج مبهرة.")

        col_a, col_b = st.columns(2)
        with col_a:
            p_name = st.text_input("اسم المنتج أو البطاقة:", "بطاقات فري فاير 1000 الماس")
            p_price = st.text_input("السعر أو العرض:", "1500 دج مع توصيل فوري")
        with col_b:
            p_goal = st.selectbox("الهدف من البروموت:", ["تصميم إعلان إبداعي لفيسبوك", "أفكار فيديو ريلز/تيك توك", "حملة خصومات ترويجية كبرى"])
            p_tone = st.selectbox("نبرة الأسلوب المطلوبة:", ["حماسية وجذابة جداً", "رسمية واحترافية", "شبابية ومغربية/عربية دارجة"])

        if st.button("🚀 توليد بروموت OmniFlash المثالي"):
            with st.spinner("جاري هندسة البروموت الاحترافي..."):
                engineer_prompt = (
                    f"أريدك أن تعمل كخبير هندسة بروموتات (Prompt Engineer). قم بكتابة بروموت احترافي ومفصل جداً وموجه لنماذج (OmniFlash) "
                    f"بحيث يطلب منها إنشاء محتوى لمتجر 'DZGAMECARDS'. "
                    f"تفاصيل الطلب: المنتج هو '{p_name}', السعر أو العرض هو '{p_price}', الهدف هو '{p_goal}', والنبرة المطلوبة هي '{p_tone}'. "
                    f"اكتب البروموت بوضوح وبشكل منظم بحيث يمكن للمستخدم نسخه ولصقه مباشرة في OmniFlash ليعطيه نتيجة مذهلة."
                )
                res = client.models.generate_content(model="gemini-3.6-flash", contents=engineer_prompt)
                st.success("تم هندسة البروموت بنجاح! جاهز للاستخدام:")
                st.markdown(res.text)

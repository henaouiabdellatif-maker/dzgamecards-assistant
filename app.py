import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="DZGAMECARDS Pro Assistant",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم ليصبح عصرياً وأنيقاً
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("💎 DZGAMECARDS Pro AI Assistant")
st.markdown("مساعدك الذكي والمحترف لإدارة المتجر، هندسة البروموتات المتقدمة لـ OmniFlash، وإدارة السوشيال ميديا بحرية تامة.")

# جلب المفتاح تلقائياً من الإعدادات أو الشريط الجانبي
api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

with st.sidebar:
    st.header("⚙️ إعدادات المساعد")
    if not api_key:
        api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
    else:
        st.success("تم تحميل مفتاح الـ API بنجاح 🔒")
    
    st.divider()
    st.markdown("### 💡 ماذا يمكنك أن تطلب منه؟")
    st.markdown("- *\"اصنع لي منشور فيسبوك لبطاقات جوجل بلاي بسعر 20$\"*")
    st.markdown("- *\"أريد بروموت لـ OmniFlash لتوليد أفكار إعلانية للمتجر\"*")
    st.markdown("- *\"اقترح علي استراتيجية لزيادة المبيعات هذا الأسبوع\"*")
    
    if st.button("🗑️ مسح محادثة الدردشة"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.warning("الرجاء إدخال مفتاح Gemini API Key في الشريط الجانبي للبدء.")
else:
    client = genai.Client(api_key=api_key)

    # تهيئة سجل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "model", 
                "content": "مرحباً بك يا صاحبي! أنا مساعدك الذكي والمحترف لمتجر **DZGAMECARDS**. أنا هنا لأكتب معك المنشورات، أصمم لك البروموتات المتقدمة لـ OmniFlash، وأساعدك في إدارة صفحتك باحترافية. عما تتحدث اليوم؟"
            }
        ]

    # عرض سجل المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # نافذة إدخال الرسائل الحرة من المستخدم
    if user_prompt := st.chat_input("اكتب طلبك هنا (مثلاً: أريد بروموت لـ OmniFlash عن بطاقات فري فاير بسعر 10$...):"):
        # إضافة رسالة المستخدم للسجل
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # توليد الرد الذكي
        with st.chat_message("model"):
            with st.spinner("جاري التفكير وصياغة الرد المتقدم..."):
                try:
                    # توجيه النظام (System Instruction) ليصبح خبيراً في متجرك
                    system_instruction = (
                        "أنت مساعد ذكي خبير ومحترف مخصص لمتجر رقمي يسمى 'DZGAMECARDS' يبيع البطاقات الرقمية (مثل بطاقات جوجل بلاي، نتفلكس، فري فاير، بلايستيشن، شحن الألعاب، إلخ). "
                        "مهمتك الرئيسية هي: "
                        "1. مساعدة المستخدم في إدارة صفحات السوشيال ميديا (فيسبوك، إنستغرام) عبر كتابة منشورات تسويقية جذابة، احترافية، مع إيموجي وهاشتاغات ودعوة للشراء. "
                        "2. هندسة البروموتات المتقدمة والمخصصة لنماذج الذكاء الاصطناعي مثل (OmniFlash) بحيث تعطيه بروموتات دقيقة ومذهلة عند إعطائه اسم المنتج والسعر أو التفاصيل. "
                        "3. تقديم إجابات منطقية، إبداعية، ومتقدمة جداً باللغة التي يفضلها المستخدم (العربية أو الدارجة حسب طلبه). "
                        "كن ودوداً، احترافياً، ومرناً تماماً في الحوار المباشر."
                    )

                    # تجهيز محتوى الرسائل بالكامل للسياق
                    formatted_contents = []
                    for m in st.session_state.messages:
                        role = "user" if m["role"] == "user" else "model"
                        formatted_contents.append(
                            types.Content(
                                role=role,
                                parts=[types.Part.from_text(text=m["content"])]
                            )
                        )

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=formatted_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                        )
                    )

                    assistant_response = response.text
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "model", "content": assistant_response})
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

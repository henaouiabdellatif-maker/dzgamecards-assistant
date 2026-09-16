import streamlit as st
from google import genai

st.set_page_config(page_title="DZGAMECARDS AI Assistant", page_icon="⚡", layout="centered")

st.title("⚡ DZGAMECARDS AI Assistant")
st.markdown("مساعدك الذكي المتقدم لإدارة متجرك وتوليد المحتوى الحقيقي بالذكاء الاصطناعي.")

# محاولة جلب المفتاح تلقائياً من الإعدادات السرية للمنصة
api_key = ""
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

st.sidebar.header("إعدادات الذكاء الاصطناعي")

if not api_key:
    api_key = st.sidebar.text_input("أدخل مفتاح Gemini API Key:", type="password")
else:
    st.sidebar.success("تم تحميل مفتاح الـ API تلقائياً بنجاح! 🔒")

option = st.sidebar.selectbox(
    "اختر الخدمة:",
    ("إنشاء منشور ترويجي ذكي", "هندسة بروموت لـ Omini Flash", "أفكار لفيديوهات ريلز/تيك توك مبتكرة")
)

product_name = st.text_input("اسم المنتج أو البطاقة (مثلاً: بطاقات جوجل بلاي، شحن فري فاير):", "بطاقات جوجل بلاي")

if st.button("توليد المحتوى بالذكاء الاصطناعي"):
    if not api_key:
        st.error("الرجاء إدخال مفتاح Gemini API Key أولاً!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            with st.spinner("جاري التفكير وتوليد المحتوى لمتجرك..."):
                if option == "إنشاء منشور ترويجي ذكي":
                    prompt = f"اكتب منشور ترويجي جذاب واحترافي لفيسبوك وإنستغرام لمتجر بطاقات رقمية يسمى DZGAMECARDS يبيع منتج '{product_name}'. اجعل النص باللهجة أو اللغة الجذابة مع إيموجي وهاشتاغات ودعوة واضحة للشراء."
                elif option == "هندسة بروموت لـ Omini Flash":
                    prompt = f"اكتب بروموت احترافي ومفصل لنماذج الذكاء الاصطناعي السريعة (Flash) لتوليد أفكار تسويقية وإعلانية لمتجر DZGAMECARDS لبيع '{product_name}'."
                else:
                    prompt = f"اعطني 3 أفكار مبتكرة لفيديوهات قصيرة (Reels/TikTok) لمتجر DZGAMECARDS للترويج لـ '{product_name}' مع نص الفيديو والتعليق الصوتي."

                # تم التحديث إلى النموذج الجديد المطلوب
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                st.success("تم توليد المحتوى بنجاح:")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DZGAMECARDS AI Assistant", page_icon="⚡", layout="centered")

st.title("⚡ DZGAMECARDS AI Assistant")
st.markdown("مساعدك الذكي المتقدم لإدارة متجرك وتوليد المحتوى الحقيقي بالذكاء الاصطناعي.")

# الشريط الجانبي لإدخال المفتاح والخدمات
st.sidebar.header("إعدادات الذكاء الاصطناعي")
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API Key:", type="password")

option = st.sidebar.selectbox(
    "اختر الخدمة:",
    ("إنشاء منشور ترويجي ذكي", "هندسة بروموت لـ Omini Flash", "أفكار لفيديوهات ريلز/تيك توك مبتكرة")
)

product_name = st.text_input("اسم المنتج أو البطاقة (مثلاً: بطاقات جوجل بلاي، شحن فري فاير):", "بطاقات جوجل بلاي")

if st.button("توليد المحتوى بالذكاء الاصطناعي"):
    if not api_key:
        st.error("الرجاء إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً!")
    else:
        try:
            genai.configure(api_key=api_key)
            # تم تحديث اسم الموديل ليعمل مباشرة بدون أخطاء
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            with st.spinner("جاري التفكير وتوليد المحتوى لمتجرك..."):
                if option == "إنشاء منشور ترويجي ذكي":
                    prompt = f"اكتب منشور ترويجي جذاب واحترافي لفيسبوك وإنستغرام لمتجر بطاقات رقمية يسمى DZGAMECARDS يبيع منتج '{product_name}'. اجعل النص باللهجة أو اللغة الجذابة مع إيموجي وهاشتاغات ودعوة واضحة للشراء."
                elif option == "هندسة بروموت لـ Omini Flash":
                    prompt = f"اكتب بروموت احترافي ومفصل لنماذج الذكاء الاصطناعي السريعة (Flash) لتوليد أفكار تسويقية وإعلانية لمتجر DZGAMECARDS لبيع '{product_name}'."
                else:
                    prompt = f"اعطني 3 أفكار مبتكرة لفيديوهات قصيرة (Reels/TikTok) لمتجر DZGAMECARDS للترويج لـ '{product_name}' مع نص الفيديو والتعليق الصوتي."

                response = model.generate_content(prompt)
                st.success("تم توليد المحتوى بنجاح:")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

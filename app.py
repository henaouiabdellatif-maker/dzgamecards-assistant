import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import docx
import pandas as pd

st.set_page_config(
    page_title="DZGAMECARDS OMNI-AI 2050 PRO",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم خارق ومستقبلي بمستوى منصات 2050
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #090d16 0%, #020408 100%);
        color: #f1f5f9;
    }
    .stButton>button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%, #8b5cf6 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 12px 24px;
        font-weight: 800;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.8);
    }
    div.stSelectbox, div.stTextInput, div.stTextArea {
        background-color: rgba(15, 23, 42, 0.8);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(16px);
    }
    h1, h2, h3 {
        color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    .title-glow {
        background: linear-gradient(90deg, #22d3ee, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .quota-warning {
        background-color: rgba(234, 179, 8, 0.15);
        border: 1px solid #eab308;
        padding: 12px;
        border-radius: 10px;
        color: #facc15;
        font-size: 14px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# الشريط الجانبي الفخم
with st.sidebar:
    st.markdown("<h2 style='text-align: center;' class='title-glow'>👑 OMNI-AI 2050</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>المنصة الأقوى عالمياً للجميع</p>", unsafe_allow_html=True)
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
    
    user_role = st.selectbox(
        "🎯 اختر تخصصك أو مجالك الحالي:",
        [
            "عقلية Omni الشاملة ( Claude + ChatGPT + Gemini )",
            "تجارة إلكترونية وإدارة متجر DZGAMECARDS",
            "طبخ ووصفات طهي وأغذية (شيف محترف)",
            "برمجة وهندسة برمجيات وتطوير ويب",
            "صانع محتوى وسوشيال ميديا (تيك توك / ريلز)",
            "دراسة وأبحاث أكاديمية وكتابة مقالات",
            "استشارات مالية وقانونية وإدارية"
        ]
    )

    st.divider()
    app_mode = st.radio(
        "⚡ الأقسام الرئيسية:",
        [
            "💬 المحادثة الخارقة (صوت + كتابة + ذاكرة)",
            "🎨 استوديو خلق الصور الإعلانية (Imagen 3)",
            "📄 مصنع ومولد ملفات الوورد والإكسل (Word/Excel)",
            "🛠️ مركز البروموتات والردود الجاهزة"
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

    role_prompts = {
        "عقلية Omni الشاملة ( Claude + ChatGPT + Gemini )": "أنت نظام ذكاء اصطناعي خارق لعام 2050 يدمج قوة Claude، إبداع ChatGPT، وسرعة Gemini. قدم إجابات عبقرية ومفيدة للغاية.",
        "تجارة إلكترونية وإدارة متجر DZGAMECARDS": "أنت مستشار تسويقي عالمي خبير في المتاجر الرقمية مثل 'DZGAMECARDS'. ساعد المستخدم في زيادة المبيعات وإدارة العملاء.",
        "طبخ ووصفات طهي وأغذية (شيف محترف)": "أنت شيف عالمي حائز على نجوم ميشلان. قدم أروع الوصفات وأسرار الطهي بدقة.",
        "برمجة وهندسة برمجيات وتطوير ويب": "أنت مهندس برمجيات عبقري. اكتب أكواد نظيفة، احترافية، وخالية من الأخطاء بأي لغة برمجة.",
        "صانع محتوى وسوشيال ميديا (تيك توك / ريلز)": "أنت خبير نمو وتثبيت على تيك توك وإنستغرام. اصنع أفكاراً فيروسية وسيناريوهات فيديوهات مذهلة.",
        "دراسة وأبحاث أكاديمية وكتابة مقالات": "أنت باحث وأكاديمي بارز. اكتب مقالات عميقة، دقيقة، ومنظمة بمعايير عالمية.",
        "استشارات مالية وقانونية وإدارية": "أنت مستشار مالي وقانوني ذكي. قدم استراتيجيات مدروسة وآمنة."
    }
    system_prompt = role_prompts.get(user_role, role_prompts["عقلية Omni الشاملة ( Claude + ChatGPT + Gemini )"])

    # ================= 1. المحادثة الخارقة =================
    if app_mode == "💬 المحادثة الخارقة (صوت + كتابة + ذاكرة)":
        st.markdown("<h1 class='title-glow'>💬 المحادثة الخارقة الشاملة</h1>", unsafe_allow_html=True)
        st.markdown("تحدث في أي موضوع، اطرح أي سؤال، أو استخدم **الميكروفون** للتحدث صوتياً وسأجيبك فوراً بدون أي تكرار وبكفاءة مطلقة.")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "model", 
                    "content": f"أهلاً بك! أنا نظام Omni-AI الخارق مخصص لمجالك ({user_role}). كيف يمكنني إبهارك ومساعدتك اليوم؟"
                }
            ]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("اكتب رسالتك هنا...")
            
        st.markdown("---")
        st.subheader("🎙️ أو تحدث صوتياً مباشرة:")
        audio_file = st.audio_input("اضغط لتسجيل الصوت")

        if audio_file is not None:
            audio_bytes = audio_file.read()
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            
            with st.spinner("🎧 جاري الاستماع لصوتك وتحليله بدقة خارقة..."):
                try:
                    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[audio_part, f"بصفتك تخدم مجال ({user_role})، أجب على هذا الصوت باحترافية."]
                    )
                    reply = response.text
                    st.session_state.messages.append({"role": "user", "content": "🎙️ [رسالة صوتية]"})
                    st.session_state.messages.append({"role": "model", "content": reply})
                    st.rerun()
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str:
                        st.markdown("<div class='quota-warning'>⚠️ <b>تنبيه الحد الأقصى:</b> اقتربنا من الحد الأقصى للطلبات (5 طلبات/دقيقة). يرجى الانتظار 20 ثانية.</div>", unsafe_allow_html=True)
                    elif "503" in err_str:
                        st.markdown("<div class='quota-warning'>⏳ <b>ضغط مؤقت في خوادم جوجل (503):</b> الخوادم مشغولة حالياً، يرجى المحاولة بعد ثوانٍ قليلة.</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"خطأ: {e}")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("model"):
                with st.spinner("✨ جاري المعالجة..."):
                    try:
                        formatted_msgs = [
                            types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
                            for m in st.session_state.messages
                        ]
                        res = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=formatted_msgs,
                            config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.7)
                        )
                        reply = res.text
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "model", "content": reply})
                    except Exception as e:
                        err_str = str(e)
                        if "429" in err_str:
                            st.markdown("<div class='quota-warning'>⚠️ <b>تنبيه الحد الأقصى (Quota Warning):</b> النظام يقترب من حد الاستخدام المجاني المسموح. انتظر قليلاً ثم أرسل مجدداً.</div>", unsafe_allow_html=True)
                        elif "503" in err_str:
                            st.markdown("<div class='quota-warning'>⏳ <b>ضغط مؤقت في خوادم جوجل (503):</b> الخوادم تشهد ضغطاً عالياً حالياً. اضغط أرسل مرة أخرى بعد قليل.</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"خطأ: {e}")

    # ================= 2. استوديو الصور (Imagen 3) =================
    elif app_mode == "🎨 استوديو خلق الصور الإعلانية (Imagen 3)":
        st.markdown("<h1 class='title-glow'>🎨 استوديو التصميم والخلق البصري</h1>", unsafe_allow_html=True)
        st.markdown("أنشئ أي بوستر، إعلان، أو تصميم بصري بدقة سينمائية مذهلة.")

        img_prompt = st.text_area("أدخل وصف الصورة بالتفصيل:", "Futuristic promotional banner for digital store, neon lights, 8k resolution, cinematic")
        aspect_ratio = st.selectbox("أبعاد الصورة:", ["1:1 (مربع)", "16:9 (أفقي)", "9:16 (عمودي للتيك توك)"])
        
        if st.button("🚀 توليد الصورة الآن"):
            if img_prompt.strip():
                with st.spinner("🎨 جاري رسم وتوليد الصورة..."):
                    try:
                        ratio_map = {"1:1 (مربع)": "1:1", "16:9 (أفقي)": "16:9", "9:16 (عمودي للتيك توك)": "9:16"}
                        result = client.models.generate_images(
                            model='imagen-3.0-generate-002',
                            prompt=img_prompt,
                            config=types.GenerateImagesConfig(
                                number_of_images=1,
                                output_mime_type="image/jpeg",
                                aspect_ratio=ratio_map.get(aspect_ratio, "1:1")
                            )
                        )
                        st.success("✨ تم توليد التحفة بنجاح!")
                        for generated_image in result.generated_images:
                            image = Image.open(BytesIO(generated_image.image.image_bytes))
                            st.image(image, caption="التصميم المولد بالذكاء الاصطناعي", use_container_width=True)
                    except Exception as e:
                        err_str = str(e)
                        if "429" in err_str:
                            st.markdown("<div class='quota-warning'>⚠️ <b>تنبيه الحد الأقصى:</b> تم الوصول للحد المؤقت لتوليد الصور. انتظر قليلاً.</div>", unsafe_allow_html=True)
                        elif "503" in err_str:
                            st.markdown("<div class='quota-warning'>⏳ <b>ضغط مؤقت (503):</b> خوادم توليد الصور مشغولة حالياً، جرب بعد ثوانٍ.</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"خطأ: {e}")
            else:
                st.warning("الرجاء كتابة وصف الصورة أولاً.")

    # ================= 3. مصنع ملفات الوورد والإكسل =================
    elif app_mode == "📄 مصنع ومولد ملفات الوورد والإكسل (Word/Excel)":
        st.markdown("<h1 class='title-glow'>📄 مصنع الملفات والمستندات الذكي</h1>", unsafe_allow_html=True)
        st.markdown("اطلب أي موضوع، مقال، تقرير، أو جدول بيانات، وسيقوم الذكاء الاصطناعي بكتابته وتوليد ملف **Word (.docx)** أو **Excel (.xlsx)** حقيقي لتنزيله بضغطة زر!")

        file_type = st.radio("اختر نوع الملف المراد إنشاؤه:", ["ملف مستند Word (.docx)", "جدول بيانات Excel (.xlsx)"])
        file_topic = st.text_area("ما الذي تريد أن يتضمنه الملف؟ (مثلاً: خطة تسويقية لمتجر DZGAMECARDS، أو تقرير مبيعات، أو وصفات طبخ):", "خطة تسويق رقمي متكاملة لزيادة مبيعات البطاقات الرقمية")

        if st.button("🚀 إنشاء وتوليد الملف للتحميل"):
            if file_topic.strip():
                with st.spinner("جاري صياغة المحتوى وبناء الملف..."):
                    try:
                        if file_type == "ملف مستند Word (.docx)":
                            prompt = f"اكتب محتوى تفصيلي، منظم، واحترافي لملف وورد بناءً على هذا الطلب: '{file_topic}'. اجعل النصوص منسقة في فقرات وعناوين واضحة."
                            res = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=types.GenerateContentConfig(system_instruction=system_prompt))
                            
                            doc = docx.Document()
                            doc.add_heading("DZGAMECARDS - AI Generated Document", 0)
                            for line in res.text.split("\n"):
                                if line.strip().startswith("#"):
                                    doc.add_heading(line.replace("#", "").strip(), level=1)
                                else:
                                    doc.add_paragraph(line)
                            
                            doc_io = BytesIO()
                            doc.save(doc_io)
                            doc_io.seek(0)
                            
                            st.success("✨ تم إنشاء ملف الورد بنجاح وجاهز للتنزيل!")
                            st.download_button(
                                label="📥 اضغط هنا لتنزيل ملف Word (.docx)",
                                data=doc_io,
                                file_name="DZGAMECARDS_Document.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        else:
                            prompt = f"قم بإنشاء جدول بيانات منظم ومناسب للإكسل بناءً على الطلب: '{file_topic}'. اعطني البيانات على شكل أعمدة وصفوف مفصولة بفواصل أو بيانات جدولية واضحة."
                            res = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=types.GenerateContentConfig(system_instruction=system_prompt))
                            
                            data = {"البيانات والمحتوى المولد": [res.text]}
                            df = pd.DataFrame(data)
                            
                            excel_io = BytesIO()
                            with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
                                df.to_excel(writer, sheet_name='Sheet1', index=False)
                            excel_io.seek(0)
                            
                            st.success("✨ تم إنشاء ملف الإكسل بنجاح وجاهز للتنزيل!")
                            st.download_button(
                                label="📥 اضغط هنا لتنزيل ملف Excel (.xlsx)",
                                data=excel_io,
                                file_name="DZGAMECARDS_Data.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    except Exception as e:
                        err_str = str(e)
                        if "429" in err_str:
                            st.markdown("<div class='quota-warning'>⚠️ <b>تنبيه الحد الأقصى:</b> تم بلوغ الحد المؤقت للطلبات. انتظر قليلاً.</div>", unsafe_allow_html=True)
                        elif "503" in err_str:
                            st.markdown("<div class='quota-warning'>⏳ <b>ضغط مؤقت في الخوادم (503):</b> خوادم جوجل تشهد ضغطاً حالياً أثناء إنشاء الملف. يرجى إعادة المحاولة بعد ثوانٍ.</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"حدث خطأ أثناء إنشاء الملف: {e}")
            else:
                st.warning("الرجاء كتابة تفاصيل الملف أولاً.")

    # ================= 4. مركز البروموتات والردود =================
    elif app_mode == "🛠️ مركز البروموتات والردود الجاهزة":
        st.markdown("<h1 class='title-glow'>🛠️ مركز الأدوات والبروموتات الخارقة</h1>", unsafe_allow_html=True)
        sub_choice = st.radio("اختر الأداة:", ["صياغة ردود تجارية للزبائن", "هندسة بروموت احترافي متكامل"])

        if sub_choice == "صياغة ردود تجارية للزبائن":
            cust_text = st.text_area("أدخل رسالة الزبون:")
            if st.button("✨ توليد رد تسويقي ساحر"):
                if cust_text.strip():
                    with st.spinner("جاري الصياغة..."):
                        try:
                            p = f"اكتب رداً تجارياً احترافياً ومقنعاً لرسالة زبون تقول: '{cust_text}'."
                            res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=system_prompt))
                            st.success("الرد الجاهز:")
                            st.markdown(res.text)
                        except Exception as e:
                            err_str = str(e)
                            if "503" in err_str:
                                st.markdown("<div class='quota-warning'>⏳ ضغط مؤقت في الخوادم (503). جرب مرة أخرى بعد قليل.</div>", unsafe_allow_html=True)
                            else:
                                st.warning(f"تنبيه مؤقت: {e}")
                else:
                    st.warning("أدخل رسالة الزبون.")
        else:
            p_idea = st.text_input("ما هو موضوع البروموت؟", "إعلان ترويجي احترافي")
            if st.button("🚀 هندسة بروموت أسطوري"):
                with st.spinner("جاري الهندسة..."):
                    try:
                        p = f"اكتب بروموت مفصل واحترافي جداً لنماذج الذكاء الاصطناعي بناءً على: '{p_idea}'."
                        res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=system_prompt))
                        st.success("البروموت المهندس:")
                        st.markdown(res.text)
                    except Exception as e:
                        err_str = str(e)
                        if "503" in err_str:
                            st.markdown("<div class='quota-warning'>⏳ ضغط مؤقت في الخوادم (503). جرب مرة أخرى بعد قليل.</div>", unsafe_allow_html=True)
                        else:
                            st.warning(f"تنبيه مؤقت: {e}")

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import docx
import pandas as pd
import uuid
import time

st.set_page_config(
    page_title="DZGAMECARDS OMNI-AI 2050 ULTIMATE",
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
        padding: 14px;
        border-radius: 12px;
        color: #facc15;
        font-size: 15px;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    .stats-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# تهيئة عداد الطلبات اليومي في الجلسة
if "daily_requests" not in st.session_state:
    st.session_state.daily_requests = 0

MAX_DAILY_FREE_LIMIT = 20

# الشريط الجانبي الفخم وإدارة المحادثات
with st.sidebar:
    st.markdown("<h2 style='text-align: center;' class='title-glow'>👑 OMNI-AI 2050</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>المنصة الأقوى عالمياً للجميع</p>", unsafe_allow_html=True)
    st.divider()
    
    # عداد الاستهلاك اليومي المرئي
    usage_pct = min(st.session_state.daily_requests / MAX_DAILY_FREE_LIMIT, 1.0)
    st.markdown(f"""
    <div class="stats-box">
        <p style="margin: 0; font-size: 13px; color: #94a3b8;">📊 استهلاك الطلبات اليومية</p>
        <h3 style="margin: 5px 0; color: {'#ef4444' if st.session_state.daily_requests >= 18 else '#22d3ee'};">{st.session_state.daily_requests} / {MAX_DAILY_FREE_LIMIT} طلب</h3>
        <p style="margin: 0; font-size: 11px; color: #64748b;">يتجدد تلقائياً كل 24 ساعة</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # 🗂️ سجل المحادثات السابقة
    st.markdown("### 🗂️ سجل المحادثات السابقة")
    
    if "sessions" not in st.session_state:
        init_id = str(uuid.uuid4())[:8]
        st.session_state.sessions = {
            init_id: {
                "title": "محادثة رئيسية 1",
                "messages": [{"role": "model", "content": "أهلاً بك في نظام Omni-AI الخارق. كيف يمكنني إبهارك ومساعدتك اليوم؟"}]
            }
        }
        st.session_state.active_session = init_id

    session_ids = list(st.session_state.sessions.keys())
    session_titles = [st.session_state.sessions[sid]["title"] for sid in session_ids]
    
    try:
        active_idx = session_ids.index(st.session_state.active_session)
    except ValueError:
        active_idx = 0

    selected_title = st.selectbox("اختر محادثة سابقة:", session_titles, index=active_idx, key="session_selector")
    selected_id = session_ids[session_titles.index(selected_title)]
    
    if selected_id != st.session_state.active_session:
        st.session_state.active_session = selected_id
        st.rerun()

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("➕ جديدة"):
            new_id = str(uuid.uuid4())[:8]
            new_title = f"محادثة {len(st.session_state.sessions) + 1}"
            st.session_state.sessions[new_id] = {
                "title": new_title,
                "messages": [{"role": "model", "content": "أهلاً بك في محادثة جديدة. بماذا نبدأ الإبداع؟"}]
            }
            st.session_state.active_session = new_id
            st.rerun()
    with col_b2:
        if st.button("🗑️ حذف الحالية") and len(st.session_state.sessions) > 1:
            del st.session_state.sessions[st.session_state.active_session]
            st.session_state.active_session = list(st.session_state.sessions.keys())[0]
            st.rerun()

    st.divider()
    
    user_role = st.selectbox(
        "🎯 اختر تخصصك أو مجالك الحالي (يناسب الجميع):",
        [
            "عقلية Omni الشاملة ( Claude + ChatGPT + Gemini مدمجون )",
            "تجارة إلكترونية وإدارة متجر DZGAMECARDS",
            "طبخ ووصفات طهي وأغذية (شيف محترف)",
            "برمجة وهندسة برمجيات وتطوير ويب",
            "صانع محتوى وسوشيال ميديا (تيك توك / ريلز / يوتيوب)",
            "دراسة وأبحاث أكاديمية وكتابة مقالات علمية",
            "استشارات مالية، قانونية، وتجارية متقدمة"
        ]
    )

    st.divider()
    app_mode = st.radio(
        "⚡ الأقسام الرئيسية الخارقة:",
        [
            "💬 المحادثة الخارقة الشاملة (صوت + كتابة + ذاكرة)",
            "🎨 استوديو خلق الصور والبوسترات (Imagen 3)",
            "🎬 استوديو توليد الفيديوهات (Veo 3.1)",
            "📄 مصنع ومولد ملفات الوورد والإكسل (Word/Excel)",
            "🛠️ مركز البروموتات والردود الذكية"
        ]
    )

def handle_api_error(e):
    err_str = str(e)
    if "429" in err_str and "Day" in err_str:
        st.markdown("<div class='quota-warning'>⚠️ <b>تنبيه الحد اليومي (Daily Quota Exceeded):</b> لقد وصلت للحد الأقصى اليومي (20 طلباً مجانياً). أنشئ مفتاح API جديد من Google AI Studio وضعه في الشريط الجانبي لتعاود العمل فوراً!</div>", unsafe_allow_html=True)
    elif "429" in err_str:
        st.markdown("<div class='quota-warning'>⚠️ <b>تنبيه الحد المؤقت:</b> تم بلوغ حد الطلبات في الدقيقة (5 طلبات). انتظر 20 ثانية ثم أعد المحاولة.</div>", unsafe_allow_html=True)
    elif "503" in err_str:
        st.markdown("<div class='quota-warning'>⏳ <b>ضغط مؤقت في خوادم جوجل (503):</b> الخوادم مشغولة عالمياً حالياً، يرجى المحاولة بعد ثوانٍ قليلة.</div>", unsafe_allow_html=True)
    else:
        st.error(f"خطأ غير متوقع: {e}")

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح الـ API في الشريط الجانبي لتفعيل طاقة الذكاء الاصطناعي الخارق.")
else:
    client = genai.Client(api_key=api_key)
    MODEL_NAME = "gemini-3.6-flash"

    role_prompts = {
        "عقلية Omni الشاملة ( Claude + ChatGPT + Gemini مدمجون )": "أنت نظام ذكاء اصطناعي خارق لعام 2050 يدمج قوة التحليل لـ Claude، طلاقة وحماس ChatGPT، وسرعة وقوة Gemini. قدم إجابات عبقرية، عميقة، ومفيدة لأي شخص في العالم.",
        "تجارة إلكترونية وإدارة متجر DZGAMECARDS": "أنت مستشار تسويقي عالمي خبير في المتاجر الرقمية مثل 'DZGAMECARDS' للبطاقات الرقمية. ساعد المستخدم في زيادة المبيعات وإدارة العملاء.",
        "طبخ ووصفات طهي وأغذية (شيف محترف)": "أنت شيف عالمي حائز على نجوم ميشلان. قدم أروع الوصفات، أسرار الطهي، وحساب السعرات الحرارية بدقة.",
        "برمجة وهندسة برمجيات وتطوير ويب": "أنت مهندس برمجيات عبقري. اكتب أكواد نظيفة، احترافية، ومثالية بأي لغة برمجة.",
        "صانع محتوى وسوشيال ميديا (تيك توك / ريلز / يوتيوب)": "أنت خبير نمو على منصات الفيديو. اصنع سيناريوهات فيديوهات فيروسية، أفكار عناوين، ونصوص تعليق صوتي مذهلة.",
        "دراسة وأبحاث أكاديمية وكتابة مقالات علمية": "أنت باحث أكاديمي بارز. اكتب مقالات عميقة، دقيقة، ومنظمة بمعايير عالمية.",
        "استشارات مالية، قانونية، وتجارية متقدمة": "أنت مستشار مالي وقانوني ذكي. قدم استراتيجيات مدروسة وآمنة."
    }
    system_prompt = role_prompts.get(user_role, role_prompts["عقلية Omni الشاملة ( Claude + ChatGPT + Gemini مدمجون )"])

    active_messages = st.session_state.sessions[st.session_state.active_session]["messages"]

    # ================= 1. المحادثة الخارقة =================
    if app_mode == "💬 المحادثة الخارقة الشاملة (صوت + كتابة + ذاكرة)":
        st.markdown("<h1 class='title-glow'>💬 المحادثة الخارقة الشاملة</h1>", unsafe_allow_html=True)
        st.markdown(f"**العقلية النشطة:** {user_role} | تحدث بحرية تامة أو استخدم الصوت وسيجيبك النظام فوراً.")

        for msg in active_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("اكتب رسالتك هنا...")
            
        st.markdown("---")
        st.subheader("🎙️ أو تحدث صوتياً مباشرة:")
        audio_file = st.audio_input("اضغط لتسجيل الصوت")

        if audio_file is not None:
            audio_bytes = audio_file.read()
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            
            if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات (20/20). أنشئ مفتاح API جديد لتستمر بالعمل فوراً.</div>", unsafe_allow_html=True)
            else:
                with st.spinner("🎧 جاري معالجة الصوت عبر النواة الخارقة..."):
                    try:
                        st.session_state.daily_requests += 1
                        audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
                        response = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=[audio_part, f"بصفتك تخدم مجال ({user_role})، أجب على هذا الصوت باحترافية."]
                        )
                        reply = response.text
                        active_messages.append({"role": "user", "content": "🎙️ [رسالة صوتية]"})
                        active_messages.append({"role": "model", "content": reply})
                        st.rerun()
                    except Exception as e:
                        handle_api_error(e)

        if user_input:
            if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات (20/20). أنشئ مفتاح API جديد من Google AI Studio وضعه في الشريط الجانبي.</div>", unsafe_allow_html=True)
            else:
                active_messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("model"):
                    with st.spinner("✨ جاري المعالجة الفائقة..."):
                        try:
                            st.session_state.daily_requests += 1
                            formatted_msgs = [
                                types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part.from_text(text=m["content"])])
                                for m in active_messages
                            ]
                            res = client.models.generate_content(
                                model=MODEL_NAME,
                                contents=formatted_msgs,
                                config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.7)
                            )
                            reply = res.text
                            st.markdown(reply)
                            active_messages.append({"role": "model", "content": reply})
                        except Exception as e:
                            handle_api_error(e)

    # ================= 2. استوديو الصور (Imagen 3) =================
    elif app_mode == "🎨 استوديو خلق الصور والبوسترات (Imagen 3)":
        st.markdown("<h1 class='title-glow'>🎨 استوديو التصميم والخلق البصري</h1>", unsafe_allow_html=True)
        st.markdown("أنشئ أي بوستر، إعلان، أو تصميم بصري بدقة سينمائية مذهلة.")

        img_prompt = st.text_area("أدخل وصف الصورة بالتفصيل:", "Futuristic promotional banner for digital store, neon lights, 8k resolution, cinematic")
        aspect_ratio = st.selectbox("أبعاد الصورة:", ["1:1 (مربع)", "16:9 (أفقي)", "9:16 (عمودي للتيك توك)"])
        
        if st.button("🚀 توليد الصورة الآن"):
            if img_prompt.strip():
                if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                    st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات. أنشئ مفتاح API جديد.</div>", unsafe_allow_html=True)
                else:
                    with st.spinner("🎨 جاري رسم وتوليد الصورة عبر Imagen 3..."):
                        try:
                            st.session_state.daily_requests += 1
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
                            handle_api_error(e)
            else:
                st.warning("الرجاء كتابة وصف الصورة أولاً.")

    # ================= 3. استوديو توليد الفيديوهات (Veo 3.1) =================
    elif app_mode == "🎬 استوديو توليد الفيديوهات (Veo 3.1)":
        st.markdown("<h1 class='title-glow'>🎬 استوديو توليد الفيديوهات السينمائية (Veo 3.1)</h1>", unsafe_allow_html=True)
        st.markdown("أدخل وصفاً تفصيلياً لمشهد فيديو تريده، وسيقوم نموذج Veo 3.1 بإنشاء مقطع فيديو سينمائي مذهل!")

        video_prompt = st.text_area("أدخل وصف الفيديو بالتفصيل (بالإنجليزية أو العربية بوضوح):", "Cinematic drone shot flying over a futuristic neon cyberpunk city at night, 4k resolution")
        
        if st.button("🚀 بدء توليد الفيديو السينمائي"):
            if video_prompt.strip():
                if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                    st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات.</div>", unsafe_allow_html=True)
                else:
                    with st.spinner("🎬 جاري معالجة الفيديو عبر نموذج Veo 3.1 (قد تستغرق العملية دقيقة أو دقيقتين)..."):
                        try:
                            st.session_state.daily_requests += 1
                            operation = client.models.generate_videos(
                                model="veo-3.1-generate-preview",
                                prompt=video_prompt,
                            )
                            # الانتظار حتى اكتمال التوليد
                            while not operation.done:
                                time.sleep(10)
                                operation = client.operations.get(operation)
                            
                            st.success("✨ تم توليد الفيديو السينمائي بنجاح!")
                            # عرض النتيجة إذا توفرت في العملية
                            if hasattr(operation, 'response') and operation.response and hasattr(operation.response, 'generated_videos'):
                                for v in operation.response.generated_videos:
                                    # إذا كان هناك رابط أو بايتس فيديو
                                    st.video(v.video.uri if hasattr(v.video, 'uri') else v.video)
                            else:
                                st.info("تم اكتمال العملية بنجاح عبر Veo 3.1. (تحقق من نتيجة الفيديو في واجهة Google AI Studio إذا لزم الأمر).")
                        except Exception as e:
                            handle_api_error(e)
            else:
                st.warning("الرجاء كتابة وصف الفيديو أولاً.")

    # ================= 4. مصنع ملفات الوورد والإكسل =================
    elif app_mode == "📄 مصنع ومولد ملفات الوورد والإكسل (Word/Excel)":
        st.markdown("<h1 class='title-glow'>📄 مصنع الملفات والمستندات الذكي</h1>", unsafe_allow_html=True)
        st.markdown("اطلب أي موضوع، مقال، تقرير، أو جدول بيانات، وسيقوم الذكاء الاصطناعي بكتابته وتوليد ملف **Word (.docx)** أو **Excel (.xlsx)** حقيقي لتنزيله بضغطة زر!")

        file_type = st.radio("اختر نوع الملف المراد إنشاؤه:", ["ملف مستند Word (.docx)", "جدول بيانات Excel (.xlsx)"])
        file_topic = st.text_area("ما الذي تريد أن يتضمنه الملف؟ (مثلاً: خطة تسويقية لمتجر DZGAMECARDS، أو تقرير مبيعات، أو وصفات طبخ):", "خطة تسويق رقمي متكاملة لزيادة مبيعات البطاقات الرقمية")

        if st.button("🚀 إنشاء وتوليد الملف للتحميل"):
            if file_topic.strip():
                if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                    st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات.</div>", unsafe_allow_html=True)
                else:
                    with st.spinner("جاري صياغة المحتوى وبناء الملف..."):
                        try:
                            st.session_state.daily_requests += 1
                            if file_type == "ملف مستند Word (.docx)":
                                prompt = f"اكتب محتوى تفصيلي، منظم، واحترافي لملف وورد بناءً على هذا الطلب: '{file_topic}'. اجعل النصوص منسقة في فقرات وعناوين واضحة."
                                res = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=types.GenerateContentConfig(system_instruction=system_prompt))
                                
                                doc = docx.Document()
                                doc.add_heading("DZGAMECARDS OMNI-AI Document", 0)
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
                                    file_name="OmniAI_Document.docx",
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
                                    file_name="OmniAI_Data.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        except Exception as e:
                            handle_api_error(e)
            else:
                st.warning("الرجاء كتابة تفاصيل الملف أولاً.")

    # ================= 5. مركز البروموتات والردود =================
    elif app_mode == "🛠️ مركز البروموتات والردود الجاهزة":
        st.markdown("<h1 class='title-glow'>🛠️ مركز الأدوات والبروموتات الخارقة</h1>", unsafe_allow_html=True)
        sub_choice = st.radio("اختر الأداة:", ["صياغة ردود تجارية للزبائن", "هندسة بروموت احترافي متكامل"])

        if sub_choice == "صياغة ردود تجارية للزبائن":
            cust_text = st.text_area("أدخل رسالة الزبون:")
            if st.button("✨ توليد رد تسويقي ساحر"):
                if cust_text.strip():
                    if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                        st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات.</div>", unsafe_allow_html=True)
                    else:
                        with st.spinner("جاري الصياغة..."):
                            try:
                                st.session_state.daily_requests += 1
                                p = f"اكتب رداً تجارياً احترافياً ومقنعاً لرسالة زبون تقول: '{cust_text}'."
                                res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=system_prompt))
                                st.success("الرد الجاهز:")
                                st.markdown(res.text)
                            except Exception as e:
                                handle_api_error(e)
                else:
                    st.warning("أدخل رسالة الزبون.")
        else:
            p_idea = st.text_input("ما هو موضوع البروموت؟", "إعلان ترويجي احترافي")
            if st.button("🚀 هندسة بروموت أسطوري"):
                if st.session_state.daily_requests >= MAX_DAILY_FREE_LIMIT:
                    st.markdown("<div class='quota-warning'>⚠️ عذراً، لقد استهلكت الحد اليومي من الطلبات.</div>", unsafe_allow_html=True)
                else:
                    with st.spinner("جاري الهندسة..."):
                        try:
                            st.session_state.daily_requests += 1
                            p = f"اكتب بروموت مفصل واحترافي جداً لنماذج الذكاء الاصطناعي بناءً على: '{p_idea}'."
                            res = client.models.generate_content(model=MODEL_NAME, contents=p, config=types.GenerateContentConfig(system_instruction=system_prompt))
                            st.success("البروموت المهندس:")
                            st.markdown(res.text)
                        except Exception as e:
                            handle_api_error(e)

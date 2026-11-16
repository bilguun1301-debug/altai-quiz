import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Хуудасны үндсэн тохиргоо
st.set_page_config(page_title="Алтай Quiz AI", page_icon="🏔️", layout="wide")

# API холбох хэсэг
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Streamlit Secrets хэсэгт GOOGLE_API_KEY тохируулаагүй байна!")

# Санах ой (Session State) эхлүүлэх
if "users" not in st.session_state:
    st.session_state.users = {}  # {нэвтрэх_нэр: {"password": "...", "avatar": "...", "class": "..."}}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"user": "Систем", "avatar": "🏔️", "text": "Алтай Quiz AI-ийн нэгдсэн чатад тавтай морил!", "time": "Одоо"}
    ]

# --- 1. FACEBOOK ШИГ БҮРТГЭЛ БА НЭВТРЭХ ХЭСЭГ ---
if st.session_state.current_user is None:
    st.markdown("<h1 style='text-align: center; color: #1877F2;'>🏔️ Алтай Quiz AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ховд аймаг • Сурагчдын ухаалаг суралцахуй ба нэгдсэн сүлжээ</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Нэвтрэх", "📝 Шинээр бүртгүүлэх"])
        
        with tab1:
            login_name = st.text_input("Нэвтрэх нэр", key="l_name")
            login_pass = st.text_input("Нууц үг", type="password", key="l_pass")
            if st.button("Нэвтрэх", use_container_width=True, type="primary"):
                if login_name in st.session_state.users and st.session_state.users[login_name]["password"] == login_pass:
                    st.session_state.current_user = login_name
                    st.rerun()
                else:
                    st.error("Нэвтрэх нэр эсвэл нууц үг буруу байна!")
                    
        with tab2:
            reg_name = st.text_input("Өөрийн нэр (Зөвхөн 1 удаа үүснэ)", key="r_name")
            reg_class = st.selectbox("Анги", ["6-р анги", "7-р анги", "8-р анги", "9-р анги", "Багш"])
            reg_avatar = st.selectbox("Профайл зураг сонгох", ["🧑‍🎓", "👩‍🎓", "🦁", "🦅", "🐺", "🦊", "🐼", "🚀"])
            reg_pass = st.text_input("Нууц үг зохиох", type="password", key="r_pass")
            if st.button("Бүртгүүлэх", use_container_width=True):
                if not reg_name or not reg_pass:
                    st.warning("Нэр болон нууц үгээ бүрэн оруулна уу.")
                elif reg_name in st.session_state.users:
                    st.error("Энэ нэрээр өөр хүн бүртгүүлсэн байна. Өөр нэр сонгоно уу!")
                else:
                    st.session_state.users[reg_name] = {
                        "password": reg_pass,
                        "avatar": reg_avatar,
                        "class": reg_class
                    }
                    st.success("Амжилттай бүртгэгдлээ! Одоо 'Нэвтрэх' хэсгээр орно уу.")
    st.stop()

# --- НЭВТЭРСНИЙ ДАРААХ ҮНДСЭН ХЭСЭГ ---
user_info = st.session_state.users[st.session_state.current_user]

with st.sidebar:
    st.markdown(f"### {user_info['avatar']} {st.session_state.current_user}")
    st.caption(f"Анги: {user_info['class']}")
    if st.button("🚪 Гарах", use_container_width=True):
        st.session_state.current_user = None
        st.rerun()
    st.divider()
    menu = st.radio("Цэс сонгох:", ["🤖 AI Багш", "💬 Сургуулийн Чат (Messenger)", "🎮 Алтай Quiz"])

# --- 2. AI БАГШ ---
if menu == "🤖 AI Багш":
    st.header("🤖 AI Багш - Бүх хичээлийн ухаалаг туслах")
    subject = st.selectbox("Хичээлээ сонгоно уу:", ["Математик", "Монгол хэл", "Түүх", "Физик", "Англи хэл", "Мэдээлэл зүй"])
    
    if "ai_chat" not in st.session_state:
        st.session_state.ai_chat = []

    for msg in st.session_state.ai_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(f"{subject} хичээлийн асуултаа энд бичнэ үү...")
    if prompt:
        st.session_state.ai_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(f"Чи бол дунд ангийн сурагчдад зориулсан {subject} хичээлийн багш. Дараах асуултад ойлгомжтой, алхам алхмаар монгол хэлээр хариулна уу: {prompt}")
                st.markdown(response.text)
                st.session_state.ai_chat.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI холболтын алдаа: {e}. Secrets хэсэг дэх API түлхүүрээ шалгана уу.")

# --- 3. MESSENGER ШИГ НЭГДСЭН ЧАТ ---
elif menu == "💬 Сургуулийн Чат (Messenger)":
    st.header("💬 Сургуулийн Нэгдсэн Чат")
    
    chat_container = st.container(height=400)
    with chat_container:
        for m in st.session_state.messages:
            is_me = (m["user"] == st.session_state.current_user)
            if is_me:
                st.markdown(f"""
                <div style='text-align: right; margin: 8px;'>
                    <span style='background-color: #0084FF; color: white; padding: 8px 14px; border-radius: 18px; display: inline-block; max-width: 70%;'>
                        {m['text']}
                    </span>
                    <div style='font-size: 11px; color: gray;'>{m['time']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: left; margin: 8px;'>
                    <div style='font-size: 12px; font-weight: bold; color: #555;'>{m['avatar']} {m['user']}</div>
                    <span style='background-color: #E4E6EB; color: black; padding: 8px 14px; border-radius: 18px; display: inline-block; max-width: 70%;'>
                        {m['text']}
                    </span>
                    <div style='font-size: 11px; color: gray;'>{m['time']}</div>
                </div>
                """, unsafe_allow_html=True)

    new_msg = st.chat_input("Мессеж бичих...")
    if new_msg:
        now = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "user": st.session_state.current_user,
            "avatar": user_info["avatar"],
            "text": new_msg,
            "time": now
        })
        st.rerun()

# --- 4. QUIZ ХЭСЭГ ---
elif menu == "🎮 Алтай Quiz":
    st.header("🎮 Алтай Quiz - Мэдлэг сорих сорил")
    topic = st.selectbox("Сорилын төрөл:", ["Монголын түүх, соёл", "IQ логик бодлогууд", "Байгалийн ухаан"])
    if st.button("🚀 Шинэ асуулт авах"):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            res = model.generate_content(f"'{topic}' сэдвээр 6-9-р ангийн сурагчдад зориулсан 1 сонирхолтой сонгох тест (A, B, C, D хувилбартай) зохиож өгнө үү. Зөв хариултыг нь хамгийн доор нь нууцлалтай бичээрэй.")
            st.info(res.text)
        except Exception as e:
            st.error(f"Асуулт үүсгэхэд алдаа гарлаа: {e}")

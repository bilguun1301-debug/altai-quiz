import streamlit as st
from google import genai
from google.genai import types
import json
import os
import time
from datetime import datetime

# Хуудасны үндсэн тохиргоо
st.set_page_config(page_title="Алтай Quiz AI - Ухаалаг Сургууль", page_icon="🎓", layout="wide")

# ==========================================
# Google AI API тохиргоо
# ==========================================
API_KEY = "AQ.Ab8RN6IajorphqVShE68N5dreUNfdkSmfDlFu93tElss_3d9Hg"
client = genai.Client(api_key=API_KEY)

# Файлуудын нэрс
CHAT_DB_FILE = "school_chat_db.json"
QUESTION_BANK_FILE = "question_bank.json"

def load_json(file_path, default_val):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return default_val
    return default_val

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Чат болон асуултын санг ачаалах
chats = load_json(CHAT_DB_FILE, {"Сургуулийн нэгдсэн групп": [], "6-р анги": [], "7-р анги": [], "8-р анги": [], "9-р анги": []})

# --- ЗАГВАРЫН HEADER (Алтай Quiz AI) ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h1 style="margin:0; font-size: 28px;">🏔️ Алтай Quiz AI</h1>
        <p style="margin:5px 0 0 0; opacity: 0.8;">Ховд аймаг • 6-9-р ангийн бодит цагийн AI суралцахуйн платформ</p>
    </div>
""", unsafe_allow_html=True)

# --- ХЭРЭГЛЭГЧИЙН БҮРТГЭЛ БА ЦЭС (Хажуугийн самбар) ---
st.sidebar.title("🎓 Платформын цэс")
user_name = st.sidebar.text_input("Таны нэр:", value="Сурагч Бат")
user_role = st.sidebar.selectbox("Хэрэглэгчийн төрөл:", ["Сурагч", "Багш"])
user_class = st.sidebar.selectbox("Анги сонгох:", ["6-р анги", "7-р анги", "8-р анги", "9-р анги"])

st.sidebar.divider()
menu = st.sidebar.radio(
    "Үндсэн цэс:",
    ["🤖 AI Багш (Бүх хичээл)", "💬 Анги ба Сургуулийн Чат", "🎮 Алтай Quiz Тоглоом"]
)

# ==============================================================================
# 1. AI БАГШ (Бүх хичээлээр алхам алхмаар тайлбарлах хэсэг)
# ==============================================================================
if menu == "🤖 AI Багш (Бүх хичээл)":
    st.header("🤖 AI Багш - Бүх хичээлийн ухаалаг туслах")
    st.write("Математик, Физик, Хими, Түүх, Англи хэл болон бусад хичээлийн асуултаа алхам алхмаар тайлбарлуулаарай!")
    
    subject = st.selectbox(
        "Хичээлээ сонгоно уу:",
        ["Математик", "Физик", "Хими", "Англи хэл", "Монгол хэл", "Түүх / Нийгэм", "Мэдээллийн технологи"]
    )
    
    system_instruction = f"""
    Чи бол Монголын ЕБС-ийн сурагчдад зориулсан '{subject}' хичээлийн найрсаг AI багш.
    Дүрэм:
    1. Асуулт, бодлогыг заавал АЛХАМ АЛХМААР (Алхам 1, Алхам 2...) энгийн монгол хэлээр тайлбарла.
    2. Математик, физик, химийн бодлого бол ашиглах ТОМЬЁО-г нь тусад нь ялгаж бич.
    """

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(f"{subject} хичээлийн асуултаа энд бичнэ үү..."):
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Бодож, тайлбар бэлтгэж байна..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.4,
                        )
                    )
                    st.markdown(response.text)
                    st.session_state.ai_messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Алдаа гарлаа: {e}")

# ==============================================================================
# 2. СУРАГЧИД ХООРОНДОО ЧАТЛАХ (Анги болон Сургуулийн групп чат)
# ==============================================================================
elif menu == "💬 Анги ба Сургуулийн Чат":
    st.header("💬 Сурагчид ба Багш нарын хамтын чат")
    st.write("Сургуулийн нэгдсэн болон ангийнхаа групп чатаар дамжуулан мэдээллээ солилцоорой.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        room = st.selectbox("Чатлах өрөөгөө сонгоно уу:", ["Сургуулийн нэгдсэн групп", user_class])
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Шинэ зурвас шалгах"):
            st.rerun()

    room_messages = chats.get(room, [])

    chat_container = st.container(height=400)
    with chat_container:
        if not room_messages:
            st.info("Одоогоор зурвас алга. Эхний зурвасыг бичиж яриаг эхлүүлээрэй!")
        for m in room_messages:
            badge = "👨‍🏫 [Багш]" if m["role"] == "Багш" else "🎒 [Сурагч]"
            st.markdown(f"**{badge} {m['sender']}** *({m['time']})*: {m['text']}")

    new_msg = st.chat_input(f"'{room}' руу зурвас бичих...")
    if new_msg:
        chats[room].append({
            "sender": user_name,
            "role": user_role,
            "text": new_msg,
            "time": datetime.now().strftime("%H:%M")
        })
        save_json(CHAT_DB_FILE, chats)
        st.rerun()

# ==============================================================================
# 3. АЛТАЙ QUIZ ТОГЛООМ (Хурдны урамшуулалтай & Өөрөө хөгждөг сан)
# ==============================================================================
elif menu == "🎮 Алтай Quiz Тоглоом":
    st.header("🎮 Алтай Quiz - Мэдлэг сорих сорил")
    st.write("Монголын түүх, соёл болон IQ логик бодлогоор өрсөлдөх хэсэг. (15 секундэд амжиж хариулаад хурдны урамшуулал аваарай!)")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0

    st.metric(label="🏆 Таны нийт оноо", value=f"{st.session_state.score} оноо")

    game_category = st.selectbox(
        "Сорилын төрөл сонгох:",
        ["Монголын түүх, соёл, өв уламжлал", "IQ хөгжүүлэх логик бодлогууд", "Ховд нутгийн түүх соёл"]
    )

    if st.button("🚀 Шинэ асуулт авах (AI асуулт зохиогч)"):
        with st.spinner("Gemini AI шинэ асуулт зохиож, санд нэмж байна..."):
            q_prompt = f"""
            Монголын ЕБС-ийн 6-9 дүгээр ангийн сурагчдад зориулсан '{game_category}' сэдвээр 1 ширхэг сонирхолтой, өвөрмөц тест асуулт зохио.
            Хариуг ЗӨВХӨН дараах JSON форматаар өг, өөр илүү тайлбар текст битгий бич:
            {{
                "question": "Асуултын текст",
                "options": ["A хувилбар", "B хувилбар", "C хувилбар", "D хувилбар"],
                "answer": "Зөв хувилбарын яг ижил текст",
                "explanation": "Яагаад энэ хариу зөв болох тухай товч тайлбар"
            }}
            """
            try:
                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=q_prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                new_q = json.loads(res.text)
                
                q_bank = load_json(QUESTION_BANK_FILE, [])
                q_bank.append(new_q)
                save_json(QUESTION_BANK_FILE, q_bank)

                st.session_state.current_question = new_q
                st.session_state.start_time = time.time()
            except Exception as e:
                st.error("Асуулт үүсгэхэд алдаа гарлаа, дахин товчлуурыг дарна уу.")

    if st.session_state.current_question:
        q = st.session_state.current_question
        st.subheader(f"❓ {q['question']}")
        
        user_choice = st.radio("Сонголтууд:", q["options"], key="game_radio")

        if st.button("⏱️ Хариуг илгээх (15 сек дотор)"):
            elapsed_time = time.time() - st.session_state.start_time
            
            if elapsed_time > 15:
                st.warning(f"⏰ Цаг дууссан! ({elapsed_time:.1f} секунд зарцуулсан байна). 15 секундаас хэтэрсэн тул оноо тооцогдохгүй.")
            else:
                if user_choice == q["answer"]:
                    speed_bonus = int(max(0, 15 - elapsed_time)) * 2
                    total_points = 10 + speed_bonus
                    
                    st.success(f"🎉 Зөв байна! Зарцуулсан хугацаа: {elapsed_time:.1f} сек. +{total_points} оноо (Суурь 10 + Хурдны урамшуулал {speed_bonus})!")
                    st.info(f"💡 AI Ухаалаг тайлбар: {q['explanation']}")
                    st.session_state.score += total_points
                    st.session_state.current_question = None
                else:
                    st.error(f"❌ Буруу байна. Зөв хариулт нь: **{q['answer']}**.")
                    st.info(f"💡 AI Ухаалаг тайлбар: {q['explanation']}")
                    st.session_state.current_question = None

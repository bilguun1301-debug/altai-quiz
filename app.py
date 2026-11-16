import streamlit as st
import google.generativeai as genai
from datetime import datetime
import uuid

# 1. ХУУДАСНЫ ҮНДСЭН ТОХИРГОО БА ДИЗАЙН (CSS)
st.set_page_config(page_title="Алтай Social & AI", page_icon="🏔️", layout="centered")

# Багш болж бүртгүүлэх тусгай нууц код (Та энд хүссэн кодоо бичиж болно)
TEACHER_SECRET_CODE = "ALTAI2026"

st.markdown("""
<style>
    /* Хажуугийн цэсийг нуух */
    [data-testid="stSidebar"] {display: none;}
    
    /* Facebook толгой хэсэг */
    .fb-header {
        background: linear-gradient(90deg, #1877F2 0%, #0056b3 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Стори карт */
    .story-card {
        background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%);
        color: white;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    /* Пост карт */
    .post-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Доод цэсний товчлуурууд */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# API холболт
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Streamlit Secrets хэсэгт GOOGLE_API_KEY тохируулаагүй байна!")

# 2. САНАХ ОЙ (DATABASE) ЭХЛҮҮЛЭХ
if "users" not in st.session_state:
    st.session_state.users = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "feed"
if "stories" not in st.session_state:
    st.session_state.stories = [
        {"user": "Алтай AI", "avatar": "🏔️", "text": "Шинэ платформд тавтай морил! 🎉", "time": "Саяхан"}
    ]
if "posts" not in st.session_state:
    st.session_state.posts = [
        {"id": "1", "user": "Алтай AI", "role": "Систем", "avatar": "🏔️", "text": "Энд та бүхэн хичээлийн тухай болон сонирхолтой мэдээллээ хуваалцаарай!", "likes": 5, "time": "Өнөөдөр"}
    ]
if "group_chats" not in st.session_state:
    st.session_state.group_chats = {
        "Нийт сургууль": [{"id": "m1", "user": "Систем", "avatar": "🏫", "text": "Сургуулийн нэгдсэн чат нээгдлээ.", "time": "09:00"}],
        "6-р анги": [],
        "7-р анги": [],
        "8-р анги": [],
        "9-р анги": [],
        "Багш нар": []
    }
if "ai_history" not in st.session_state:
    st.session_state.ai_history = {}  # Хэрэглэгч бүрийн AI түүхийг тусад нь хадгална

# 3. НЭВТРЭХ БА БҮРТГҮҮЛЭХ ХЭСЭГ (FACEBOOK STYLE)
if st.session_state.current_user is None:
    st.markdown("<div class='fb-header'><h2 style='margin:0; text-align:center;'>🏔️ Алтай Social & AI</h2><p style='margin:0; text-align:center; font-size:14px;'>Сургуулийн нэгдсэн сүлжээ • Ухаалаг туслах</p></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Нэвтрэх", "📝 Шинэ хаяг нээх"])
    
    with tab1:
        l_name = st.text_input("Нэвтрэх нэр", key="login_user")
        l_pass = st.text_input("Нууц үг", type="password", key="login_pass")
        if st.button("Нэвтрэх", use_container_width=True, type="primary"):
            if l_name in st.session_state.users and st.session_state.users[l_name]["password"] == l_pass:
                st.session_state.current_user = l_name
                if l_name not in st.session_state.ai_history:
                    st.session_state.ai_history[l_name] = []
                st.rerun()
            else:
                st.error("Нэвтрэх нэр эсвэл нууц үг буруу байна!")
                
    with tab2:
        r_name = st.text_input("Таны нэр (Давхцахгүй)", key="reg_user")
        r_role = st.selectbox("Анги / Албан тушаал", ["6-р анги", "7-р анги", "8-р анги", "9-р анги", "Багш"])
        
        teacher_code_input = ""
        if r_role == "Багш":
            teacher_code_input = st.text_input("🔒 Багшийн баталгаажуулах нууц код", type="password", help="Зөвхөн багш нарт олгосон кодыг оруулна уу.")
            
        r_avatar = st.selectbox("Профайл зураг", ["🧑‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫", "🦁", "🦅", "🐺", "🐼", "🚀"])
        r_pass = st.text_input("Нууц үг зохиох", type="password", key="reg_pass")
        
        if st.button("Бүртгүүлэх", use_container_width=True):
            if not r_name or not r_pass:
                st.warning("Нэр болон нууц үгээ бүрэн бөглөнө үү.")
            elif r_name in st.session_state.users:
                st.error("Энэ нэрээр өөр хүн бүртгүүлсэн байна!")
            elif r_role == "Багш" and teacher_code_input != TEACHER_SECRET_CODE:
                st.error("❌ Багшийн нууц код буруу байна! Сурагчид зөвхөн өөрийн ангийг сонгоно уу.")
            else:
                st.session_state.users[r_name] = {
                    "password": r_pass,
                    "role": r_role,
                    "avatar": r_avatar
                }
                st.session_state.ai_history[r_name] = []
                st.success("✅ Амжилттай бүртгэгдлээ! Одоо 'Нэвтрэх' цэсээр орно уу.")
    st.stop()

# НЭВТЭРСЭН ХЭРЭГЛЭГЧИЙН МЭДЭЭЛЭЛ
me = st.session_state.current_user
my_info = st.session_state.users[me]

# ДЭЭД ТОЛГОЙ ХЭСЭГ
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    badge = "🛡️ Багш" if my_info["role"] == "Багш" else my_info["role"]
    st.markdown(f"**{my_info['avatar']} {me}** `({badge})`")
with col_h2:
    if st.button("Гарах", use_container_width=True):
        st.session_state.current_user = None
        st.rerun()

st.divider()

# ==========================================
# ЦЭС 1: FACEBOOK НҮҮР ХУУДАС БА СТОРИ
# ==========================================
if st.session_state.active_tab == "feed":
    # --- СТОРИ (STORY) ХЭСЭГ ---
    st.subheader("📸 Стори (Stories)")
    with st.expander("➕ Өөрийн стори нэмэх"):
        story_text = st.text_input("Стори дээр юу бичих вэ?", max_chars=80)
        if st.button("Стори нийтлэх"):
            if story_text:
                st.session_state.stories.insert(0, {
                    "user": me,
                    "avatar": my_info["avatar"],
                    "text": story_text,
                    "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

    # Сторинуудыг зэрэгцүүлж харуулах
    story_cols = st.columns(min(len(st.session_state.stories), 4))
    for idx, s in enumerate(st.session_state.stories[:4]):
        with story_cols[idx]:
            st.markdown(f"""
            <div class='story-card'>
                <div style='font-size: 22px;'>{s['avatar']}</div>
                <div style='font-size: 12px; font-weight: bold;'>{s['user']}</div>
                <div style='font-size: 11px; margin-top: 5px;'>{s['text']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    # --- НИЙТЛЭЛ (POST) ОРУУЛАХ ---
    with st.container(border=True):
        new_post = st.text_area("Юу бодож байна даа?", placeholder=f"{me}, найзууддаа сонин хачнаасаа хуваалцаарай...", height=70)
        if st.button("Нийтлэх (Post)", type="primary"):
            if new_post.strip():
                st.session_state.posts.insert(0, {
                    "id": str(uuid.uuid4()),
                    "user": me,
                    "role": my_info["role"],
                    "avatar": my_info["avatar"],
                    "text": new_post,
                    "likes": 0,
                    "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

    # --- НИЙТЛЭЛҮҮДИЙН ЖАГСААЛТ ---
    for p in st.session_state.posts:
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                role_tag = "🛡️ Багш" if p["role"] == "Багш" else p["role"]
                st.markdown(f"**{p['avatar']} {p['user']}** • <span style='color:gray; font-size:12px;'>{role_tag} • {p['time']}</span>", unsafe_allow_html=True)
            with c2:
                # Зөвхөн өөрийн постыг устгах боломжтой
                if p["user"] == me:
                    if st.button("🗑️", key=f"del_p_{p['id']}", help="Устгах"):
                        st.session_state.posts = [item for item in st.session_state.posts if item["id"] != p["id"]]
                        st.rerun()
            
            st.write(p["text"])
            if st.button(f"👍 Таалагдлаа ({p['likes']})", key=f"like_{p['id']}"):
                p["likes"] += 1
                st.rerun()

# ==========================================
# ЦЭС 2: MESSENGER БА АНГИЙН ГРУПП ЧАТ
# ==========================================
elif st.session_state.active_tab == "chat":
    st.subheader("💬 Messenger & Ангийн групп")
    
    # Хэрэглэгчийн харж болох группууд
    available_groups = ["Нийт сургууль", my_info["role"]]
    if my_info["role"] == "Багш":
        available_groups = ["Нийт сургууль", "Багш нар", "6-р анги", "7-р анги", "8-р анги", "9-р анги"]
    else:
        available_groups = ["Нийт сургууль", my_info["role"]]

    selected_group = st.selectbox("Чатлах группээ сонгоно уу:", list(dict.fromkeys(available_groups)))
    
    chat_box = st.container(height=380, border=True)
    with chat_box:
        messages = st.session_state.group_chats.get(selected_group, [])
        if not messages:
            st.info("Энэ группт одоогоор мессеж алга. Эхэлж бичээрэй!")
        for m in messages:
            is_mine = (m["user"] == me)
            if is_mine:
                col_m1, col_m2 = st.columns([6, 1])
                with col_m1:
                    st.markdown(f"""
                    <div style='text-align: right; margin-bottom: 5px;'>
                        <span style='background-color: #0084FF; color: white; padding: 8px 14px; border-radius: 18px; display: inline-block; max-width: 85%; text-align: left;'>
                            {m['text']}
                        </span>
                        <div style='font-size: 10px; color: gray;'>{m['time']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    # Зөвхөн өөрийн бичсэн мессежийг устгах товч
                    if st.button("🗑️", key=f"del_m_{m['id']}", help="Өөрийн мессежийг устгах"):
                        st.session_state.group_chats[selected_group] = [msg for msg in messages if msg["id"] != m["id"]]
                        st.rerun()
            else:
                st.markdown(f"""
                <div style='text-align: left; margin-bottom: 8px;'>
                    <div style='font-size: 11px; font-weight: bold; color: #555;'>{m['avatar']} {m['user']}</div>
                    <span style='background-color: #E4E6EB; color: black; padding: 8px 14px; border-radius: 18px; display: inline-block; max-width: 80%;'>
                        {m['text']}
                    </span>
                    <div style='font-size: 10px; color: gray;'>{m['time']}</div>
                </div>
                """, unsafe_allow_html=True)

    msg_input = st.chat_input(f"{selected_group} группт мессеж бичих...")
    if msg_input:
        st.session_state.group_chats[selected_group].append({
            "id": str(uuid.uuid4()),
            "user": me,
            "avatar": my_info["avatar"],
            "text": msg_input,
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

# ==========================================
# ЦЭС 3: AI БАГШ (БҮХ АСУУЛТ ХАДГАЛАГДАНА)
# ==========================================
elif st.session_state.active_tab == "ai":
    col_ai1, col_ai2 = st.columns([3, 1])
    with col_ai1:
        st.subheader("🤖 Миний AI Багш")
    with col_ai2:
        if st.button("Түүх цэвэрлэх", use_container_width=True):
            st.session_state.ai_history[me] = []
            st.rerun()

    st.caption("Таны асуусан бүх асуулт, бодлогын хариу энд хадгалагдаж үлдэнэ.")
    
    # Хадгалагдсан түүхийг харуулах
    ai_box = st.container(height=380, border=True)
    with ai_box:
        if not st.session_state.ai_history[me]:
            st.info("Сайн уу! Хичээлтэй холбоотой ямар ч асуулт асууж болно. Би бүх хариултыг чинь энд хадгалж өгнө.")
        for chat in st.session_state.ai_history[me]:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

    ai_prompt = st.chat_input("AI багшаас асуух зүйлээ бичнэ үү...")
    if ai_prompt:
        st.session_state.ai_history[me].append({"role": "user", "content": ai_prompt})
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            res = model.generate_content(f"Чи бол сурагчдад тусалдаг ухаалаг AI багш. Дараах асуултад маш ойлгомжтой, монгол хэлээр хариулна уу: {ai_prompt}")
            st.session_state.ai_history[me].append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"AI холболтын алдаа: {e}. Secrets хэсэгт GOOGLE_API_KEY зөв эсэхийг шалгана уу.")

# ==========================================
# ДООД ТАЛЫН ЦЭС (ГАР УТАС & КОМПЬЮТЕРТ ЗОРИУЛСАН)
# ==========================================
st.divider()
nav1, nav2, nav3 = st.columns(3)
with nav1:
    btn_type1 = "primary" if st.session_state.active_tab == "feed" else "secondary"
    if st.button("🏠 Нүүр & Стори", use_container_width=True, type=btn_type1):
        st.session_state.active_tab = "feed"
        st.rerun()
with nav2:
    btn_type2 = "primary" if st.session_state.active_tab == "chat" else "secondary"
    if st.button("💬 Messenger Чат", use_container_width=True, type=btn_type2):
        st.session_state.active_tab = "chat"
        st.rerun()
with nav3:
    btn_type3 = "primary" if st.session_state.active_tab == "ai" else "secondary"
    if st.button("🤖 AI Багш", use_container_width=True, type=btn_type3):
        st.session_state.active_tab = "ai"
        st.rerun()
        

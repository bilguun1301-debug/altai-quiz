import streamlit as st
import google.generativeai as genai
from datetime import datetime
import uuid
import json
import os

# 1. ХУУДАСНЫ ҮНДСЭН ТОХИРГОО БА ДИЗАЙН
st.set_page_config(page_title="Алтай Сүлжээ & AI", page_icon="🏔️", layout="centered")

TEACHER_SECRET_CODE = "ALTAI2026"  # Багш болж бүртгүүлэх нууц код
DATA_FILE = "altai_data.json"      # Мэдээлэл хадгалах JSON файл
MODEL_NAME = "gemini-3.8-flash"    # Шинэчилсэн Gemini загвар

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    
    .top-navbar {
        background: linear-gradient(90deg, #1877F2 0%, #0056b3 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(24, 119, 242, 0.3);
    }
    
    .story-box {
        background: linear-gradient(135deg, #1877F2 0%, #00C6FF 100%);
        color: white;
        padding: 10px;
        border-radius: 12px;
        text-align: center;
        min-height: 115px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    
    .msg-me-box {
        display: flex;
        justify-content: flex-end;
        margin: 6px 0;
    }
    .msg-me {
        background-color: #0084FF;
        color: white;
        padding: 10px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .msg-other-box {
        display: flex;
        justify-content: flex-start;
        margin: 6px 0;
        gap: 8px;
        align-items: flex-end;
    }
    .msg-other {
        background-color: #E4E6EB;
        color: #050505;
        padding: 10px 16px;
        border-radius: 18px 18px 18px 4px;
        max-width: 75%;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# API холболт
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Streamlit Secrets хэсэгт GOOGLE_API_KEY тохируулаагүй байна!")

# 2. ӨГӨГДӨЛ УНШИХ БА ХАДГАЛАХ ФУНКЦҮҮД
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "users": {},
        "stories": [
            {"user": "Алтай Сүлжээ", "avatar": "🏔️", "text": "Найзуудаа нэмж, тоглоом тоглоорой!", "time": "Саяхан"}
        ],
        "posts": [
            {"id": "p1", "user": "Алтай Сүлжээ", "role": "Систем", "avatar": "🏔️", "text": "Алтай Сүлжээ болон AI суралцахуйн платформд тавтай морил!", "likes": [], "comments": [], "time": "Өнөөдөр"}
        ],
        "private_chats": {},
        "custom_groups": {
            "Нийт сургууль": {"creator": "Систем", "members": "ALL", "messages": []}
        },
        "ai_history": {},
        "scores": {}
    }

def save_data():
    data = {
        "users": st.session_state.users,
        "stories": st.session_state.stories,
        "posts": st.session_state.posts,
        "private_chats": st.session_state.private_chats,
        "custom_groups": st.session_state.custom_groups,
        "ai_history": st.session_state.ai_history,
        "scores": st.session_state.scores
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Өгөгдлийг ачаалах
if "data_loaded" not in st.session_state:
    saved = load_data()
    st.session_state.users = saved["users"]
    st.session_state.stories = saved["stories"]
    st.session_state.posts = saved["posts"]
    st.session_state.private_chats = saved["private_chats"]
    st.session_state.custom_groups = saved["custom_groups"]
    st.session_state.ai_history = saved["ai_history"]
    st.session_state.scores = saved.get("scores", {})
    st.session_state.data_loaded = True

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "nav" not in st.session_state:
    st.session_state.nav = "feed"
if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

# 3. НЭВТРЭХ & БҮРТГҮҮЛЭХ
if st.session_state.current_user is None:
    st.markdown("<div class='top-navbar'><h2 style='margin:0;'>🏔️ Алтай Сүлжээ</h2><span>Ухаалаг сургуулийн орчин</span></div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔑 Нэвтрэх", "📝 Шинэ хаяг нээх"])
    with t1:
        l_name = st.text_input("Нэвтрэх нэр", key="l_u")
        l_pass = st.text_input("Нууц үг", type="password", key="l_p")
        if st.button("Нэвтрэх", use_container_width=True, type="primary"):
            st.session_state.users = load_data()["users"]
            if l_name in st.session_state.users and st.session_state.users[l_name]["password"] == l_pass:
                st.session_state.current_user = l_name
                st.rerun()
            else:
                st.error("Нэр эсвэл нууц үг буруу байна!")
                
    with t2:
        r_name = st.text_input("Өөрийн нэр (Давхцахгүй)", key="r_u")
        r_role = st.selectbox("Анги / Албан тушаал", ["6-р анги", "7-р анги", "8-р анги", "9-р анги", "Багш"])
        t_code = ""
        if r_role == "Багш":
            t_code = st.text_input("🔒 Багшийн нууц код", type="password")
        r_avatar = st.selectbox("Профайл дүрс", ["🧑‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫", "🦁", "🦅", "🐺", "🐼", "🚀", "🦊"])
        r_pass = st.text_input("Нууц үг", type="password", key="r_p")
        
        if st.button("Бүртгүүлэх", use_container_width=True):
            st.session_state.users = load_data()["users"]
            if not r_name or not r_pass:
                st.warning("Бүх талбарыг бөглөнө үү.")
            elif r_name in st.session_state.users:
                st.error("Энэ нэр бүртгэлтэй байна!")
            elif r_role == "Багш" and t_code != TEACHER_SECRET_CODE:
                st.error("❌ Багшийн нууц код буруу байна!")
            else:
                st.session_state.users[r_name] = {
                    "password": r_pass, "role": r_role, "avatar": r_avatar, "friends": [], "requests": []
                }
                st.session_state.ai_history[r_name] = []
                st.session_state.scores[r_name] = 0
                save_data()
                st.success("✅ Бүртгэл амжилттай хадгалагдлаа! Одоо 'Нэвтрэх' хэсгээр орно уу.")
    st.stop()

# НЭВТЭРСЭН ХЭРЭГЛЭГЧ
me = st.session_state.current_user
my_data = st.session_state.users[me]
req_count = len(my_data["requests"])

st.markdown(f"<div class='top-navbar'><h3 style='margin:0;'>🏔️ Алтай Сүлжээ</h3><span>{my_data['avatar']} <b>{me}</b> ({my_data['role']})</span></div>", unsafe_allow_html=True)

# ==========================================
# 1. НҮҮР ХУУДАС (FEED & STORIES)
# ==========================================
if st.session_state.nav == "feed":
    with st.expander("➕ Стори нэмэх"):
        s_txt = st.text_input("Стори дээр юу бичих вэ?", max_chars=70)
        if st.button("Стори оруулах"):
            if s_txt:
                st.session_state.stories.insert(0, {"user": me, "avatar": my_data["avatar"], "text": s_txt, "time": datetime.now().strftime("%H:%M")})
                save_data()
                st.rerun()

    s_cols = st.columns(min(len(st.session_state.stories), 4))
    for i, st_item in enumerate(st.session_state.stories[:4]):
        with s_cols[i]:
            st.markdown(f"<div class='story-box'><div style='font-size:22px;'>{st_item['avatar']}</div><div style='font-size:11px;'>{st_item['text']}</div><div style='font-size:10px; opacity:0.9;'><b>{st_item['user']}</b></div></div>", unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown(f"**{my_data['avatar']} {me}** • Юу бодож байна даа?")
        p_txt = st.text_area("Нийтлэл бичих...", placeholder=f"{me}, энд юу бодож буйгаа бичнэ үү...", height=68, label_visibility="collapsed")
        if st.button("Нийтлэх", type="primary", use_container_width=True):
            if p_txt.strip():
                st.session_state.posts.insert(0, {
                    "id": str(uuid.uuid4()), "user": me, "role": my_data["role"], "avatar": my_data["avatar"],
                    "text": p_txt, "likes": [], "comments": [], "time": datetime.now().strftime("%H:%M")
                })
                save_data()
                st.rerun()

    for post in st.session_state.posts:
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                r_label = "🛡️ Багш" if post["role"] == "Багш" else post["role"]
                st.markdown(f"### {post['avatar']} {post['user']} <small style='font-size:12px; color:gray;'>({r_label})</small>", unsafe_allow_html=True)
                st.caption(f"🕒 {post['time']}")
            with c2:
                if post["user"] == me:
                    if st.button("🗑️", key=f"dp_{post['id']}", help="Устгах"):
                        st.session_state.posts = [x for x in st.session_state.posts if x["id"] != post["id"]]
                        save_data()
                        st.rerun()
            
            st.markdown(f"<div style='font-size:16px; margin: 10px 0;'>{post['text']}</div>", unsafe_allow_html=True)
            
            liked = me in post["likes"]
            like_label = f"💙 Таалагдсан ({len(post['likes'])})" if liked else f"👍 Таалагдлаа ({len(post['likes'])})"
            if st.button(like_label, key=f"lk_{post['id']}"):
                if liked:
                    post["likes"].remove(me)
                else:
                    post["likes"].append(me)
                save_data()
                st.rerun()
                
            if post["comments"]:
                st.divider()
                for cm in post["comments"]:
                    st.markdown(f"<div style='background:#F0F2F5; padding:8px 12px; border-radius:12px; margin:6px 0; font-size:13px;'><b>{cm['avatar']} {cm['user']}:</b> {cm['text']}</div>", unsafe_allow_html=True)
            
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                new_cm = st.text_input("Сэтгэгдэл бичих...", key=f"cmi_{post['id']}", label_visibility="collapsed", placeholder="Сэтгэгдэл бичих...")
            with cc2:
                if st.button("Илгээх", key=f"cmb_{post['id']}"):
                    if new_cm.strip():
                        post["comments"].append({"user": me, "avatar": my_data["avatar"], "text": new_cm})
                        save_data()
                        st.rerun()

# ==========================================
# 2. НАЙЗУУД
# ==========================================
elif st.session_state.nav == "friends":
    st.subheader("👥 Найзууд ба Хүсэлтүүд")
    
    if my_data["requests"]:
        st.markdown("#### 📩 Ирсэн найзын хүсэлтүүд")
        for req_user in list(my_data["requests"]):
            if req_user in st.session_state.users:
                u_info = st.session_state.users[req_user]
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    col1.markdown(f"**{u_info['avatar']} {req_user}** ({u_info['role']})")
                    if col2.button("✅ Зөвшөөрөх", key=f"acc_{req_user}"):
                        my_data["requests"].remove(req_user)
                        my_data["friends"].append(req_user)
                        st.session_state.users[req_user]["friends"].append(me)
                        save_data()
                        st.rerun()
                    if col3.button("❌ Татгалзах", key=f"dec_{req_user}"):
                        my_data["requests"].remove(req_user)
                        save_data()
                        st.rerun()
    
    st.markdown(f"#### 🤝 Миний найзууд ({len(my_data['friends'])})")
    if not my_data["friends"]:
        st.info("Танд одоогоор найз алга. Доорх жагсаалтаас найзын хүсэлт илгээгээрэй!")
    else:
        for fr in my_data["friends"]:
            if fr in st.session_state.users:
                f_info = st.session_state.users[fr]
                st.markdown(f"- {f_info['avatar']} **{fr}** ({f_info['role']})")

    st.divider()
    st.markdown("#### 🔍 Хүмүүс таних уу? (Найз нэмэх)")
    search_q = st.text_input("Нэрээр хайх...", placeholder="Хайх хүнийхээ нэрийг бичнэ үү")
    for uname, udata in st.session_state.users.items():
        if uname != me and uname not in my_data["friends"]:
            if search_q.lower() in uname.lower():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 2])
                    c1.markdown(f"**{udata['avatar']} {uname}** • {udata['role']}")
                    if me in udata["requests"]:
                        c2.button("⏳ Хүсэлт илгээсэн", key=f"sent_{uname}", disabled=True)
                    else:
                        if c2.button("➕ Найз болох", key=f"add_{uname}", type="primary"):
                            udata["requests"].append(me)
                            save_data()
                            st.rerun()

# ==========================================
# 3. MESSENGER ЧАТ
# ==========================================
elif st.session_state.nav == "messenger":
    st.subheader("💬 Messenger Чат")
    m_mode = st.radio("Төрөл:", ["👤 Хувийн чат", "👥 Групп чат"], horizontal=True)
    
    if m_mode == "👤 Хувийн чат":
        if not my_data["friends"]:
            st.warning("Чатлахын тулд эхлээд 'Найз' цэснээс хүмүүстэй найз болоорой!")
        else:
            target_friend = st.selectbox("💬 Харилцагч сонгох:", my_data["friends"])
            chat_key = "_".join(sorted([me, target_friend]))
            if chat_key not in st.session_state.private_chats:
                st.session_state.private_chats[chat_key] = []
                
            box = st.container(height=360, border=True)
            with box:
                msgs = st.session_state.private_chats[chat_key]
                if not msgs:
                    st.info(f"{target_friend}-тай чат эхлүүлж мэндлээрэй! 👋")
                for m in msgs:
                    if m["user"] == me:
                        st.markdown(f"""
                        <div class='msg-me-box'>
                            <div>
                                <div class='msg-me'>{m['text']}</div>
                                <div style='font-size:10px; color:gray; text-align:right; margin-top:2px;'>{m['time']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        f_avatar = st.session_state.users[target_friend]["avatar"]
                        st.markdown(f"""
                        <div class='msg-other-box'>
                            <span style='font-size:22px;'>{f_avatar}</span>
                            <div>
                                <div class='msg-other'>{m['text']}</div>
                                <div style='font-size:10px; color:gray; margin-top:2px;'>{m['time']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
            txt = st.chat_input(f"{target_friend}-д мессеж бичих...")
            if txt:
                st.session_state.private_chats[chat_key].append({
                    "id": str(uuid.uuid4()), "user": me, "text": txt, "time": datetime.now().strftime("%H:%M")
                })
                save_data()
                st.rerun()
    else:
        with st.expander("➕ Шинэ групп чат үүсгэх"):
            g_name = st.text_input("Группийн нэр")
            g_members = st.multiselect("Группт нэмэх найзуудаа сонгох:", my_data["friends"])
            if st.button("Групп үүсгэх", type="primary"):
                if g_name and g_name not in st.session_state.custom_groups:
                    st.session_state.custom_groups[g_name] = {
                        "creator": me, "members": [me] + g_members, "messages": []
                    }
                    save_data()
                    st.success(f"'{g_name}' групп үүслээ!")
                    st.rerun()
                else:
                    st.error("Группийн нэр оруулна уу эсвэл ийм нэртэй групп байна.")

        my_groups = [gn for gn, gd in st.session_state.custom_groups.items() if gd["members"] == "ALL" or me in gd["members"]]
        sel_g = st.selectbox("Групп сонгох:", my_groups)
        g_data = st.session_state.custom_groups[sel_g]
        
        g_box = st.container(height=340, border=True)
        with g_box:
            for m in g_data["messages"]:
                if m["user"] == me:
                    st.markdown(f"""
                    <div class='msg-me-box'>
                        <div>
                            <div class='msg-me'>{m['text']}</div>
                            <div style='font-size:10px; color:gray; text-align:right; margin-top:2px;'>{m['time']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='msg-other-box'>
                        <span style='font-size:22px;'>{m['avatar']}</span>
                        <div>
                            <small><b>{m['user']}</b></small>
                            <div class='msg-other'>{m['text']}</div>
                            <div style='font-size:10px; color:gray; margin-top:2px;'>{m['time']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        g_txt = st.chat_input(f"{sel_g} группт мессеж бичих...")
        if g_txt:
            g_data["messages"].append({
                "id": str(uuid.uuid4()), "user": me, "avatar": my_data["avatar"], "text": g_txt, "time": datetime.now().strftime("%H:%M")
            })
            save_data()
            st.rerun()

# ==========================================
# 4. ЖИЖИГ ТОГЛООМ (QUIZ & LEADERBOARD)
# ==========================================
elif st.session_state.nav == "game":
    st.subheader("🎮 Алтай Тоглоом & Онооны Самбар")
    
    t_tab1, t_tab2 = st.tabs(["🎯 Тест бөглөх", "🏆 Шилдэг сурагчдын самбар"])
    
    with t_tab1:
        q_topic = st.selectbox("Сорилын сэдэв:", ["Монголын түүх, газарзүй", "Математик ба логик", "Мэдээлэл зүй ба технологи"])
        
        if st.button("🚀 Шинэ асуулт авах", type="primary"):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt = f"'{q_topic}' сэдвээр дунд ангийн сурагчдад зориулсан 1 сонирхолтой сонгох тест (A, B, C, D хувилбартай) монгол хэлээр зохиож өгнө үү. Зөв хариултыг нь хамгийн доор нь 'ЗӨВ_ХАРИУЛТ: [Үсэг]' гэж бичээрэй."
                res = model.generate_content(prompt)
                st.session_state.quiz_question = res.text
            except Exception as e:
                st.error(f"Алдаа гарлаа: {e}")

        if st.session_state.quiz_question:
            with st.container(border=True):
                st.markdown(st.session_state.quiz_question)
            
            ans_choice = st.radio("Таны хариулт:", ["A", "B", "C", "D"], horizontal=True)
            if st.button("Хариу шалгах"):
                if me not in st.session_state.scores:
                    st.session_state.scores[me] = 0
                st.session_state.scores[me] += 10
                save_data()
                st.success(f"🎉 Зөв! Таны сонголт: **{ans_choice}**. Та +10 оноо авлаа! (Нийт оноо: {st.session_state.scores[me]})")

    with t_tab2:
        st.markdown("### 🏆 Сурагчдын онооны самбар")
        if not st.session_state.scores:
            st.info("Одоогоор оноо авсан сурагч алга. Тоглоом тоглож оноо цуглуулаарай!")
        else:
            sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
            for rank, (uname, score) in enumerate(sorted_scores, 1):
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏅"
                u_avatar = st.session_state.users.get(uname, {}).get("avatar", "🧑‍🎓")
                st.markdown(f"**{medal} {rank}. {u_avatar} {uname}** — {score} оноо")

# ==========================================
# 5. AI БАГШ (ДУУ ХООЛОЙТОЙ)
# ==========================================
elif st.session_state.nav == "ai":
    c1, c2 = st.columns([3, 1])
    c1.subheader("🤖 AI Багш")
    if c2.button("Түүх устгах"):
        st.session_state.ai_history[me] = []
        save_data()
        st.rerun()
        
    ai_box = st.container(height=320, border=True)
    with ai_box:
        for ch in st.session_state.ai_history.get(me, []):
            with st.chat_message(ch["role"]):
                st.markdown(ch["content"])
                
    st.markdown("---")
    st.write("🎙️ **Дуу хоолойгоор асуух:**")
    audio_data = st.audio_input("Энд дарж яриагаа бичнэ үү")
    if audio_data is not None:
        st.audio(audio_data)
        if st.button("🎤 Дуу хоолойг AI багш руу илгээх", type="primary"):
            if me not in st.session_state.ai_history:
                st.session_state.ai_history[me] = []
            st.session_state.ai_history[me].append({"role": "user", "content": "🎙️ [Дуут зурвас илгээв]"})
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                ans = model.generate_content([
                    "Чи бол сурагчдад тусалдаг ухаалаг AI багш. Дараах аудио бичлэгийг сонсоод асуусан асуултад нь монгол хэлээр ойлгомжтой хариулна уу.",
                    {"mime_type": "audio/wav", "data": audio_data.getvalue()}
                ])
                st.session_state.ai_history[me].append({"role": "assistant", "content": ans.text})
                save_data()
                st.rerun()
            except Exception as e:
                st.error(f"Алдаа: {e}")

    ai_q = st.chat_input("AI багшаас асуух зүйлээ бичнэ үү...")
    if ai_q:
        if me not in st.session_state.ai_history:
            st.session_state.ai_history[me] = []
        st.session_state.ai_history[me].append({"role": "user", "content": ai_q})
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            ans = model.generate_content(f"Чи бол сурагчдад тусалдаг AI багш. Дараах асуултад монгол хэлээр ойлгомжтой хариулна уу: {ai_q}")
            st.session_state.ai_history[me].append({"role": "assistant", "content": ans.text})
            save_data()
            st.rerun()
        except Exception as e:
            st.error(f"Алдаа: {e}")

# ==========================================
# 6. ПРОФАЙЛ & ГАРАХ
# ==========================================
elif st.session_state.nav == "profile":
    st.subheader(f"{my_data['avatar']} {me}")
    st.write(f"**Анги / Эрх:** {my_data['role']}")
    st.write(f"**Нийт найзууд:** {len(my_data['friends'])}")
    st.write(f"**Цуглуулсан оноо:** {st.session_state.scores.get(me, 0)} оноо")
    if st.button("🚪 Системээс гарах", type="primary", use_container_width=True):
        st.session_state.current_user = None
        st.rerun()

# ==========================================
# ДООД ТАЛЫН ЦЭС (6 ТОВЧЛУУР)
# ==========================================
st.divider()
n1, n2, n3, n4, n5, n6 = st.columns(6)
with n1:
    if st.button("🏠\nНүүр", use_container_width=True, type="primary" if st.session_state.nav=="feed" else "secondary"):
        st.session_state.nav = "feed"
        st.rerun()
with n2:
    f_lbl = f"👥\nНайз({req_count})" if req_count > 0 else "👥\nНайз"
    if st.button(f_lbl, use_container_width=True, type="primary" if st.session_state.nav=="friends" else "secondary"):
        st.session_state.nav = "friends"
        st.rerun()
with n3:
    if st.button("💬\nЧат", use_container_width=True, type="primary" if st.session_state.nav=="messenger" else "secondary"):
        st.session_state.nav = "messenger"
        st.rerun()
with n4:
    if st.button("🎮\nТоглоом", use_container_width=True, type="primary" if st.session_state.nav=="game" else "secondary"):
        st.session_state.nav = "game"
        st.rerun()
with n5:
    if st.button("🤖\nAI Багш", use_container_width=True, type="primary" if st.session_state.nav=="ai" else "secondary"):
        st.session_state.nav = "ai"
        st.rerun()
with n6:
    if st.button("👤\nБи", use_container_width=True, type="primary" if st.session_state.nav=="profile" else "secondary"):
        st.session_state.nav = "profile"
        st.rerun()

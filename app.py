import streamlit as st
import google.generativeai as genai
from datetime import datetime
import uuid

# 1. ҮНДСЭН ТОХИРГОО БА FACEBOOK / MESSENGER ДИЗАЙН
st.set_page_config(page_title="Алтай Facebook & Messenger", page_icon="📘", layout="centered")

TEACHER_SECRET_CODE = "ALTAI2026"  # Багш болж бүртгүүлэх нууц код

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    
    /* Facebook цэнхэр толгой */
    .fb-navbar {
        background-color: #1877F2;
        color: white;
        padding: 12px 18px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(24, 119, 242, 0.3);
    }
    
    /* Стори карт */
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
    
    /* Messenger мессеж хөөс */
    .msg-me {
        background-color: #0084FF;
        color: white;
        padding: 8px 14px;
        border-radius: 18px 18px 4px 18px;
        display: inline-block;
        max-width: 80%;
        text-align: left;
    }
    .msg-other {
        background-color: #E4E6EB;
        color: #050505;
        padding: 8px 14px;
        border-radius: 18px 18px 18px 4px;
        display: inline-block;
        max-width: 80%;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# API холболт
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Streamlit Secrets хэсэгт GOOGLE_API_KEY тохируулаагүй байна!")

# 2. ӨГӨГДЛИЙН САН (SESSION STATE)
if "users" not in st.session_state:
    st.session_state.users = {}  # {нэр: {password, role, avatar, friends: [], requests: []}}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "nav" not in st.session_state:
    st.session_state.nav = "feed"
if "stories" not in st.session_state:
    st.session_state.stories = [
        {"user": "Алтай Сүлжээ", "avatar": "📘", "text": "Найзуудаа нэмээд чат бичээрэй!", "time": "Саяхан"}
    ]
if "posts" not in st.session_state:
    st.session_state.posts = [
        {"id": "p1", "user": "Алтай Сүлжээ", "role": "Систем", "avatar": "📘", "text": "Шинэ Facebook & Messenger загварт тавтай морил! Пост оруулж, сэтгэгдэл бичиж туршаарай.", "likes": [], "comments": [], "time": "Өнөөдөр"}
    ]
if "private_chats" not in st.session_state:
    st.session_state.private_chats = {}  # {"Бат_Дорж": [messages]}
if "custom_groups" not in st.session_state:
    st.session_state.custom_groups = {
        "Нийт сургууль": {"creator": "Систем", "members": "ALL", "messages": []}
    }
if "ai_history" not in st.session_state:
    st.session_state.ai_history = {}

# 3. FACEBOOK НЭВТРЭХ & БҮРТГҮҮЛЭХ
if st.session_state.current_user is None:
    st.markdown("<div class='fb-navbar'><h2 style='margin:0;'>facebook • Алтай</h2><span>Сургуулийн сүлжээ</span></div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔑 Нэвтрэх", "📝 Шинэ хаяг нээх"])
    with t1:
        l_name = st.text_input("Нэвтрэх нэр", key="l_u")
        l_pass = st.text_input("Нууц үг", type="password", key="l_p")
        if st.button("Нэвтрэх", use_container_width=True, type="primary"):
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
        r_avatar = st.selectbox("Профайл зураг", ["🧑‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫", "🦁", "🦅", "🐺", "🐼", "🚀"])
        r_pass = st.text_input("Нууц үг", type="password", key="r_p")
        
        if st.button("Бүртгүүлэх", use_container_width=True):
            if not r_name or not r_pass:
                st.warning("Бүх талбарыг бөглөнө үү.")
            elif r_name in st.session_state.users:
                st.error("Энэ нэр бүртгэлтэй байна!")
            elif r_role == "Багш" and t_code != TEACHER_SECRET_CODE:
                st.error("❌ Багшийн нууц код буруу байна!")
            else:
                st.session_state.users[r_name] = {
                    "password": r_pass,
                    "role": r_role,
                    "avatar": r_avatar,
                    "friends": [],
                    "requests": []
                }
                st.session_state.ai_history[r_name] = []
                st.success("✅ Амжилттай бүртгэгдлээ! Одоо нэвтэрч орно уу.")
    st.stop()

# НЭВТЭРСЭН ХЭРЭГЛЭГЧ
me = st.session_state.current_user
my_data = st.session_state.users[me]
req_count = len(my_data["requests"])

# ДЭЭД ТОЛГОЙ
st.markdown(f"<div class='fb-navbar'><h3 style='margin:0;'>facebook</h3><span>{my_data['avatar']} <b>{me}</b> ({my_data['role']})</span></div>", unsafe_allow_html=True)

# ==========================================
# 1. FACEBOOK НҮҮР ХУУДАС (FEED & STORIES)
# ==========================================
if st.session_state.nav == "feed":
    # Стори хэсэг
    with st.expander("➕ Стори нэмэх (Story)"):
        s_txt = st.text_input("Стори дээр юу бичих вэ?", max_chars=70)
        if st.button("Стори оруулах"):
            if s_txt:
                st.session_state.stories.insert(0, {"user": me, "avatar": my_data["avatar"], "text": s_txt, "time": datetime.now().strftime("%H:%M")})
                st.rerun()

    s_cols = st.columns(min(len(st.session_state.stories), 4))
    for i, st_item in enumerate(st.session_state.stories[:4]):
        with s_cols[i]:
            st.markdown(f"<div class='story-box'><div style='font-size:22px;'>{st_item['avatar']}</div><div style='font-size:11px;'>{st_item['text']}</div><div style='font-size:10px; opacity:0.9;'><b>{st_item['user']}</b></div></div>", unsafe_allow_html=True)

    st.write("")
    # Пост бичих
    with st.container(border=True):
        p_txt = st.text_area("Юу бодож байна даа?", placeholder=f"{me}, юу бодож байна?", height=68)
        if st.button("Нийтлэх", type="primary", use_container_width=True):
            if p_txt.strip():
                st.session_state.posts.insert(0, {
                    "id": str(uuid.uuid4()), "user": me, "role": my_data["role"], "avatar": my_data["avatar"],
                    "text": p_txt, "likes": [], "comments": [], "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

    # Постууд
    for post in st.session_state.posts:
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                r_label = "🛡️ Багш" if post["role"] == "Багш" else post["role"]
                st.markdown(f"**{post['avatar']} {post['user']}** • <small style='color:gray;'>{r_label} • {post['time']}</small>", unsafe_allow_html=True)
            with c2:
                if post["user"] == me:
                    if st.button("🗑️", key=f"dp_{post['id']}"):
                        st.session_state.posts = [x for x in st.session_state.posts if x["id"] != post["id"]]
                        st.rerun()
            
            st.write(post["text"])
            
            # Like ба Comment
            liked = me in post["likes"]
            like_label = f"💙 Таалагдсан ({len(post['likes'])})" if liked else f"👍 Таалагдлаа ({len(post['likes'])})"
            if st.button(like_label, key=f"lk_{post['id']}"):
                if liked:
                    post["likes"].remove(me)
                else:
                    post["likes"].append(me)
                st.rerun()
                
            # Сэтгэгдэл харах ба бичих
            if post["comments"]:
                for cm in post["comments"]:
                    st.markdown(f"<div style='background:#F0F2F5; padding:6px 10px; border-radius:10px; margin:4px 0; font-size:13px;'><b>{cm['user']}:</b> {cm['text']}</div>", unsafe_allow_html=True)
            
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                new_cm = st.text_input("Сэтгэгдэл бичих...", key=f"cmi_{post['id']}", label_visibility="collapsed", placeholder="Сэтгэгдэл бичих...")
            with cc2:
                if st.button("Илгээх", key=f"cmb_{post['id']}"):
                    if new_cm.strip():
                        post["comments"].append({"user": me, "text": new_cm})
                        st.rerun()

# ==========================================
# 2. НАЙЗУУД (FRIENDS & REQUESTS)
# ==========================================
elif st.session_state.nav == "friends":
    st.subheader("👥 Найзууд ба Хүсэлтүүд")
    
    # Ирсэн найзын хүсэлтүүд
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
                        st.rerun()
                    if col3.button("❌ Татгалзах", key=f"dec_{req_user}"):
                        my_data["requests"].remove(req_user)
                        st.rerun()
    
    # Миний найзууд
    st.markdown(f"#### 🤝 Миний найзууд ({len(my_data['friends'])})")
    if not my_data["friends"]:
        st.info("Танд одоогоор найз алга. Доорх жагсаалтаас найзын хүсэлт илгээгээрэй!")
    else:
        for fr in my_data["friends"]:
            if fr in st.session_state.users:
                f_info = st.session_state.users[fr]
                st.markdown(f"- {f_info['avatar']} **{fr}** ({f_info['role']})")

    st.divider()
    # Бусад хүмүүсийг хайж найз болох
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
                            st.rerun()

# ==========================================
# 3. MESSENGER (ХУВИЙН ЧАТ & ӨӨРСДӨӨ ГРУПП ҮҮСГЭХ)
# ==========================================
elif st.session_state.nav == "messenger":
    st.subheader("💬 Messenger")
    
    m_mode = st.radio("Төрөл:", ["👤 Найзтайгаа чатлах", "👥 Групп чат"], horizontal=True)
    
    # --- ХУВИЙН ЧАТ ---
    if m_mode == "👤 Найзтайгаа чатлах":
        if not my_data["friends"]:
            st.warning("Чатлахын тулд эхлээд 'Найзууд' цэснээс хүмүүстэй найз болоорой!")
        else:
            target_friend = st.selectbox("Найзаа сонгох:", my_data["friends"])
            chat_key = "_".join(sorted([me, target_friend]))
            if chat_key not in st.session_state.private_chats:
                st.session_state.private_chats[chat_key] = []
                
            box = st.container(height=340, border=True)
            with box:
                msgs = st.session_state.private_chats[chat_key]
                if not msgs:
                    st.info(f"{target_friend}-тай эхэлж мэндлээрэй! 👋")
                for m in msgs:
                    if m["user"] == me:
                        c1, c2 = st.columns([6, 1])
                        c1.markdown(f"<div style='text-align:right;'><span class='msg-me'>{m['text']}</span><div style='font-size:10px; color:gray;'>{m['time']}</div></div>", unsafe_allow_html=True)
                        if c2.button("🗑️", key=f"dm_{m['id']}"):
                            st.session_state.private_chats[chat_key] = [x for x in msgs if x["id"] != m["id"]]
                            st.rerun()
                    else:
                        st.markdown(f"<div style='text-align:left; margin-bottom:6px;'><span class='msg-other'>{m['text']}</span><div style='font-size:10px; color:gray;'>{m['time']}</div></div>", unsafe_allow_html=True)
                        
            txt = st.chat_input(f"{target_friend}-д мессеж бичих...")
            if txt:
                st.session_state.private_chats[chat_key].append({
                    "id": str(uuid.uuid4()), "user": me, "text": txt, "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

    # --- ГРУПП ЧАТ ҮҮСГЭХ БА ЧАТЛАХ ---
    else:
        with st.expander("➕ Шинэ групп чат үүсгэх"):
            g_name = st.text_input("Группийн нэр")
            g_members = st.multiselect("Группт нэмэх найзуудаа сонгох:", my_data["friends"])
            if st.button("Групп үүсгэх", type="primary"):
                if g_name and g_name not in st.session_state.custom_groups:
                    st.session_state.custom_groups[g_name] = {
                        "creator": me,
                        "members": [me] + g_members,
                        "messages": []
                    }
                    st.success(f"'{g_name}' групп үүслээ!")
                    st.rerun()
                else:
                    st.error("Группийн нэр оруулна уу эсвэл ийм нэртэй групп байна.")

        # Зөвхөн өөрийн орсон группуудыг харуулах
        my_groups = [gn for gn, gd in st.session_state.custom_groups.items() if gd["members"] == "ALL" or me in gd["members"]]
        sel_g = st.selectbox("Групп сонгох:", my_groups)
        g_data = st.session_state.custom_groups

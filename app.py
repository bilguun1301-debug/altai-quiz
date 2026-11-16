<!DOCTYPE html>
<html lang="mn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Алтай Сүлжээ & AI</title>
    <style>
        :root {
            --primary: #1877F2;
            --primary-dark: #0056b3;
            --bg: #F0F2F5;
            --card: #FFFFFF;
            --text: #050505;
            --gray: #65676B;
            --border: #CED0D4;
        }
        * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { margin: 0; background-color: var(--bg); color: var(--text); padding-bottom: 75px; }
        .container { max-width: 600px; margin: 0 auto; padding: 12px; }
        
        /* Толгой хэсэг */
        .top-navbar {
            background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 14px 18px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(24, 119, 242, 0.3);
        }
        .top-navbar h2, .top-navbar h3 { margin: 0; }
        
        /* Карт ба Форм */
        .card {
            background: var(--card);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        input, select, textarea {
            width: 100%;
            padding: 10px 12px;
            margin: 6px 0 12px 0;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
        }
        button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: 0.2s;
        }
        button:hover { background-color: var(--primary-dark); }
        button.secondary { background-color: #E4E6EB; color: var(--text); }
        button.secondary:hover { background-color: #D8DADF; }
        button.danger { background-color: #FA383E; }
        button.full { width: 100%; }
        
        /* Таб */
        .tabs { display: flex; gap: 8px; margin-bottom: 15px; }
        .tab-btn { flex: 1; background: #E4E6EB; color: var(--text); }
        .tab-btn.active { background: var(--primary); color: white; }

        /* Стори */
        .stories-wrap { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 6px; margin-bottom: 12px; }
        .story-box {
            min-width: 110px; max-width: 110px; height: 140px;
            background: linear-gradient(135deg, #1877F2 0%, #00C6FF 100%);
            color: white; padding: 10px; border-radius: 12px;
            display: flex; flex-direction: column; justify-content: space-between;
            text-align: center; flex-shrink: 0; box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        }

        /* Чат хөөс */
        .chat-box {
            height: 320px; overflow-y: auto; border: 1px solid var(--border);
            border-radius: 10px; padding: 12px; background: #fff; margin-bottom: 10px;
            display: flex; flex-direction: column; gap: 8px;
        }
        .msg-row-me { display: flex; justify-content: flex-end; align-items: center; gap: 6px; }
        .msg-row-other { display: flex; flex-direction: column; align-items: flex-start; }
        .msg-me {
            background-color: #0084FF; color: white; padding: 8px 14px;
            border-radius: 18px 18px 4px 18px; max-width: 75%; word-wrap: break-word;
        }
        .msg-other {
            background-color: #E4E6EB; color: var(--text); padding: 8px 14px;
            border-radius: 18px 18px 18px 4px; max-width: 75%; word-wrap: break-word;
        }
        .time-small { font-size: 10px; color: var(--gray); margin-top: 2px; }

        /* Сэтгэгдэл */
        .comment-item {
            background: #F0F2F5; padding: 8px 12px; border-radius: 12px;
            margin-top: 6px; font-size: 13px;
        }

        /* Доод цэс (Bottom Navigation) */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: white; border-top: 1px solid var(--border);
            display: flex; justify-content: space-around; padding: 6px 0;
            z-index: 1000; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }
        .nav-item {
            background: none; color: var(--gray); border: none;
            display: flex; flex-direction: column; align-items: center;
            font-size: 11px; padding: 4px 8px; border-radius: 8px;
        }
        .nav-item:hover { background: #F0F2F5; }
        .nav-item.active { color: var(--primary); font-weight: bold; }
        .nav-icon { font-size: 20px; margin-bottom: 2px; }

        .hidden { display: none !important; }
        .flex-between { display: flex; justify-content: space-between; align-items: center; }
        .flex-gap { display: flex; gap: 8px; align-items: center; }
    </style>
</head>
<body>

<div class="container">
    <!-- ==================== 1. НЭВТРЭХ & БҮРТГҮҮЛЭХ ==================== -->
    <div id="auth-screen">
        <div class="top-navbar">
            <h2>🏔️ Алтай Сүлжээ</h2>
            <span>Ухаалаг сургуулийн орчин</span>
        </div>
        <div class="card">
            <div class="tabs">
                <button class="tab-btn active" id="tab-login-btn" onclick="switchAuthTab('login')">🔑 Нэвтрэх</button>
                <button class="tab-btn" id="tab-reg-btn" onclick="switchAuthTab('reg')">📝 Шинэ хаяг нээх</button>
            </div>

            <!-- Нэвтрэх форм -->
            <div id="login-form">
                <label>Нэвтрэх нэр</label>
                <input type="text" id="l-name" placeholder="Нэрээ оруулна уу">
                <label>Нууц үг</label>
                <input type="password" id="l-pass" placeholder="Нууц үгээ оруулна уу">
                <button class="full" onclick="handleLogin()">Нэвтрэх</button>
            </div>

            <!-- Бүртгүүлэх форм -->
            <div id="reg-form" class="hidden">
                <label>Өөрийн нэр (Давхцахгүй)</label>
                <input type="text" id="r-name" placeholder="Жишээ: Бат-Эрдэнэ">
                
                <label>Анги / Албан тушаал</label>
                <select id="r-role" onchange="toggleTeacherCode()">
                    <option value="6-р анги">6-р анги</option>
                    <option value="7-р анги">7-р анги</option>
                    <option value="8-р анги">8-р анги</option>
                    <option value="9-р анги">9-р анги</option>
                    <option value="Багш">Багш</option>
                </select>

                <div id="teacher-code-box" class="hidden">
                    <label>🔒 Багшийн нууц код (Анхны код: ALTAI2026)</label>
                    <input type="password" id="r-tcode" placeholder="Багшийн кодыг оруулна уу">
                </div>

                <label>Профайл дүрс</label>
                <select id="r-avatar">
                    <option value="🧑‍🎓">🧑‍🎓 Сурагч (Хүү)</option>
                    <option value="👩‍🎓">👩‍🎓 Сурагч (Охин)</option>
                    <option value="👨‍🏫">👨‍🏫 Эрэгтэй багш</option>
                    <option value="👩‍🏫">👩‍🏫 Эмэгтэй багш</option>
                    <option value="🦁">🦁 Арслан</option>
                    <option value="🦅">🦅 Бүргэд</option>
                    <option value="🐺">🐺 Чоно</option>
                    <option value="🐼">🐼 Панда</option>
                    <option value="🚀">🚀 Пуужин</option>
                    <option value="🦊">🦊 Үнэг</option>
                </select>

                <label>Нууц үг</label>
                <input type="password" id="r-pass" placeholder="Нууц үг зохиох">
                <button class="full" onclick="handleRegister()">Бүртгүүлэх</button>
            </div>
        </div>
    </div>

    <!-- ==================== 2. ҮНДСЭН АПП ==================== -->
    <div id="main-app" class="hidden">
        <div class="top-navbar">
            <h3>🏔️ Алтай Сүлжээ</h3>
            <span id="header-user-info"></span>
        </div>

        <!-- ЦЭС 1: НҮҮР (FEED & STORIES) -->
        <div id="sec-feed" class="section">
            <div class="card">
                <div class="flex-gap">
                    <input type="text" id="story-input" placeholder="➕ Стори дээр юу бичих вэ?" maxlength="60" style="margin:0;">
                    <button onclick="addStory()">Стори</button>
                </div>
            </div>
            <div class="stories-wrap" id="stories-list"></div>

            <div class="card">
                <textarea id="post-input" rows="2" placeholder="Юу бодож байна даа? Найзуудтайгаа хуваалцаарай..."></textarea>
                <button class="full" onclick="addPost()">Нийтлэх</button>
            </div>

            <div id="posts-list"></div>
        </div>

        <!-- ЦЭС 2: НАЙЗУУД -->
        <div id="sec-friends" class="section hidden">
            <div id="friend-requests-box"></div>
            <div class="card">
                <h4>🤝 Миний найзууд (<span id="friends-count">0</span>)</h4>
                <div id="my-friends-list"></div>
            </div>
            <div class="card">
                <h4>🔍 Хүмүүс таних уу? (Найз нэмэх)</h4>
                <input type="text" id="friend-search" placeholder="Нэрээр хайх..." oninput="renderFriends()">
                <div id="all-users-list"></div>
            </div>
        </div>

        <!-- ЦЭС 3: ЧАТ (MESSENGER) -->
        <div id="sec-chat" class="section hidden">
            <div class="card">
                <div class="tabs">
                    <button class="tab-btn active" id="cmode-priv" onclick="switchChatMode('private')">👤 Найзтайгаа чатлах</button>
                    <button class="tab-btn" id="cmode-grp" onclick="switchChatMode('group')">👥 Групп чат</button>
                </div>

                <!-- Хувийн чат -->
                <div id="private-chat-area">
                    <select id="priv-friend-select" onchange="renderPrivateChat()"></select>
                    <div class="chat-box" id="priv-chat-box"></div>
                    <div class="flex-gap">
                        <input type="text" id="priv-msg-input" placeholder="Мессеж бичих..." style="margin:0;">
                        <button onclick="sendPrivateMsg()">Илгээх</button>
                    </div>
                </div>

                <!-- Групп чат -->
                <div id="group-chat-area" class="hidden">
                    <details style="margin-bottom: 10px;">
                        <summary style="cursor:pointer; color:var(--primary); font-weight:bold;">➕ Шинэ групп үүсгэх</summary>
                        <div style="padding-top:8px;">
                            <input type="text" id="new-group-name" placeholder="Группийн нэр">
                            <div id="group-friends-checkboxes" style="margin-bottom:8px; font-size:14px;"></div>
                            <button onclick="createGroup()">Групп үүсгэх</button>
                        </div>
                    </details>
                    <select id="group-select" onchange="renderGroupChat()"></select>
                    <div class="chat-box" id="group-chat-box"></div>
                    <div class="flex-gap">
                        <input type="text" id="group-msg-input" placeholder="Группт мессеж бичих..." style="margin:0;">
                        <button onclick="sendGroupMsg()">Илгээх</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- ЦЭС 4: ТОГЛООМ (QUIZ) -->
        <div id="sec-game" class="section hidden">
            <div class="card">
                <h3>🎮 Алтай Тоглоом & Quiz</h3>
                <p style="color:var(--gray); font-size:14px;">Мэдлэгээ сорих хөгжөөнт асуулт хариулт!</p>
                <select id="quiz-topic">
                    <option value="history">Монголын түүх, газарзүй</option>
                    <option value="math">Математик ба логик</option>
                    <option value="it">Мэдээлэл зүй ба технологи</option>
                </select>
                <button class="full" onclick="generateQuiz()">🚀 Шинэ асуулт авах</button>
                
                <div id="quiz-area" class="hidden" style="margin-top:15px; border-top:1px solid var(--border); padding-top:15px;">
                    <h4 id="quiz-q-text"></h4>
                    <div id="quiz-options"></div>
                    <p id="quiz-result" style="font-weight:bold; margin-top:10px;"></p>
                </div>
            </div>
        </div>

        <!-- ЦЭС 5: AI БАГШ -->
        <div id="sec-ai" class="section hidden">
            <div class="card">
                <div class="flex-between">
                    <h3 style="margin:0;">🤖 AI Багш</h3>
                    <button class="secondary" onclick="clearAiHistory()">Түүх устгах</button>
                </div>
                <p style="font-size:12px; color:var(--gray);">Таны асуусан бүх асуулт энд хадгалагдана.</p>
                
                <input type="password" id="gemini-api-key" placeholder="🔑 Gemini API Key (Хүсвэл энд оруулна уу)" onchange="saveApiKey()">
                
                <div class="chat-box" id="ai-chat-box"></div>
                <div class="flex-gap">
                    <input type="text" id="ai-input" placeholder="AI багшаас асуух зүйлээ бичнэ үү..." style="margin:0;">
                    <button onclick="askAiTeacher()">Асуух</button>
                </div>
            </div>
        </div>

        <!-- ЦЭС 6: БИ (ПРОФАЙЛ) -->
        <div id="sec-profile" class="section hidden">
            <div class="card" style="text-align:center;">
                <div id="prof-avatar" style="font-size:60px;"></div>
                <h2 id="prof-name" style="margin:5px 0;"></h2>
                <p id="prof-role" style="color:var(--gray);"></p>
                <p><b>Нийт найзууд:</b> <span id="prof-friends">0</span></p>
                <button class="danger full" onclick="handleLogout()">🚪 Системээс гарах</button>
            </div>
        </div>
    </div>
</div>

<!-- ДООД ТАЛЫН ЦЭС -->
<div id="bottom-nav" class="bottom-nav hidden">
    <button class="nav-item active" id="nav-feed" onclick="switchNav('feed')"><span class="nav-icon">🏠</span>Нүүр</button>
    <button class="nav-item" id="nav-friends" onclick="switchNav('friends')"><span class="nav-icon">👥</span><span id="nav-friend-lbl">Найз</span></button>
    <button class="nav-item" id="nav-chat" onclick="switchNav('chat')"><span class="nav-icon">💬</span>Чат</button>
    <button class="nav-item" id="nav-game" onclick="switchNav('game')"><span class="nav-icon">🎮</span>Тоглоом</button>
    <button class="nav-item" id="nav-ai" onclick="switchNav('ai')"><span class="nav-icon">🤖</span>AI Багш</button>
    <button class="nav-item" id="nav-profile" onclick="switchNav('profile')"><span class="nav-icon">👤</span>Би</button>
</div>

<script>
    const TEACHER_SECRET_CODE = "ALTAI2026";
    const STORAGE_KEY = "altai_social_html_db";

    // Өгөгдлийн сан эхлүүлэх
    let db = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {
        users: {},
        stories: [
            { user: "Алтай Сүлжээ", avatar: "🏔️", text: "Найзуудаа нэмж, тоглоом тоглоорой!", time: "Саяхан" }
        ],
        posts: [
            { id: "p1", user: "Алтай Сүлжээ", role: "Систем", avatar: "🏔️", text: "Алтай Сүлжээ болон AI суралцахуйн платформд тавтай морил!", likes: [], comments: [], time: "Өнөөдөр" }
        ],
        privateChats: {},
        customGroups: {
            "Нийт сургууль": { creator: "Систем", members: "ALL", messages: [] }
        },
        aiHistory: {},
        apiKey: ""
    };

    let currentUser = localStorage.getItem("altai_current_user") || null;

    function saveDB() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
    }

    function getTime() {
        const d = new Date();
        return d.getHours().toString().padStart(2, '0') + ":" + d.getMinutes().toString().padStart(2, '0');
    }

    // --- БҮРТГЭЛ & НЭВТРЭХ ---
    function switchAuthTab(tab) {
        document.getElementById("login-form").classList.toggle("hidden", tab !== "login");
        document.getElementById("reg-form").classList.toggle("hidden", tab !== "reg");
        document.getElementById("tab-login-btn").classList.toggle("active", tab === "login");
        document.getElementById("tab-reg-btn").classList.toggle("active", tab === "reg");
    }

    function toggleTeacherCode() {
        const role = document.getElementById("r-role").value;
        document.getElementById("teacher-code-box").classList.toggle("hidden", role !== "Багш");
    }

    function handleRegister() {
        const name = document.getElementById("r-name").value.trim();
        const role = document.getElementById("r-role").value;
        const tcode = document.getElementById("r-tcode").value;
        const avatar = document.getElementById("r-avatar").value;
        const pass = document.getElementById("r-pass").value;

        if (!name || !pass) return alert("Бүх талбарыг бөглөнө үү!");
        if (db.users[name]) return alert("Энэ нэр бүртгэлтэй байна!");
        if (role === "Багш" && tcode !== TEACHER_SECRET_CODE) return alert("❌ Багшийн нууц код буруу байна!");

        db.users[name] = { password: pass, role: role, avatar: avatar, friends: [], requests: [] };
        db.aiHistory[name] = [];
        saveDB();
        alert("✅ Бүртгэл амжилттай хадгалагдлаа! Одоо нэвтэрч орно уу.");
        switchAuthTab("login");
    }

    function handleLogin() {
        const name = document.getElementById("l-name").value.trim();
        const pass = document.getElementById("l-pass").value;

        if (db.users[name] && db.users[name].password === pass) {
            currentUser = name;
            localStorage.setItem("altai_current_user", name);
            initApp();
        } else {
            alert("Нэр эсвэл нууц үг буруу байна!");
        }
    }

    function handleLogout() {
        currentUser = null;
        localStorage.removeItem("altai_current_user");
        document.getElementById("main-app").classList.add("hidden");
        document.getElementById("bottom-nav").classList.add("hidden");
        document.getElementById("auth-screen").classList.remove("hidden");
    }

    function initApp() {
        if (!currentUser || !db.users[currentUser]) return;
        document.getElementById("auth-screen").classList.add("hidden");
        document.getElementById("main-app").classList.remove("hidden");
        document.getElementById("bottom-nav").classList.remove("hidden");

        const u = db.users[currentUser];
        document.getElementById("header-user-info").innerHTML = `${u.avatar} <b>${currentUser}</b> (${u.role})`;
        document.getElementById("gemini-api-key").value = db.apiKey || "";
        
        updateFriendBadge();
        switchNav("feed");
    }

    function updateFriendBadge() {
        const reqs = db.users[currentUser].requests.length;
        document.getElementById("nav-friend-lbl").innerText = reqs > 0 ? `Найз(${reqs})` : "Найз";
    }

    function switchNav(nav) {
        document.querySelectorAll(".section").forEach(el => el.classList.add("hidden"));
        document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
        
        document.getElementById("sec-" + nav).classList.remove("hidden");
        document.getElementById("nav-" + nav).classList.add("active");

        if (nav === "feed") { renderStories(); renderPosts(); }
        if (nav === "friends") { renderFriends(); }
        if (nav === "chat") { setupChat(); }
        if (nav === "ai") { renderAiChat(); }
        if (nav === "profile") {
            const u = db.users[currentUser];
            document.getElementById("prof-avatar").innerText = u.avatar;
            document.getElementById("prof-name").innerText = currentUser;
            document.getElementById("prof-role").innerText = u.role;
            document.getElementById("prof-friends").innerText = u.friends.length;
        }
    }

    // --- 1. НҮҮР ХУУДАС (STORIES & POSTS) ---
    function addStory() {
        const txt = document.getElementById("story-input").value.trim();
        if (!txt) return;
        db.stories.unshift({ user: currentUser, avatar: db.users[currentUser].avatar, text: txt, time: getTime() });
        document.getElementById("story-input").value = "";
        saveDB();
        renderStories();
    }

    function renderStories() {
        const box = document.getElementById("stories-list");
        box.innerHTML = db.stories.map(s => `
            <div class="story-box">
                <div style="font-size:24px;">${s.avatar}</div>
                <div style="font-size:12px;">${s.text}</div>
                <div style="font-size:10px; opacity:0.9;"><b>${s.user}</b></div>
            </div>
        `).join("");
    }

    function addPost() {
        const txt = document.getElementById("post-input").value.trim();
        if (!txt) return;
        const u = db.users[currentUser];
        db.posts.unshift({
            id: "p_" + Date.now(), user: currentUser, role: u.role, avatar: u.avatar,
            text: txt, likes: [], comments: [], time: getTime()
        });
        document.getElementById("post-input").value = "";
        saveDB();
        renderPosts();
    }

    function toggleLike(postId) {
        const p = db.posts.find(x => x.id === postId);
        if (!p) return;
        const idx = p.likes.indexOf(currentUser);
        if (idx > -1) p.likes.splice(idx, 1);
        else p.likes.push(currentUser);
        saveDB();
        renderPosts();
    }

    function addComment(postId) {
        const inp = document.getElementById("cm_" + postId);
        const txt = inp.value.trim();
        if (!txt) return;
        const p = db.posts.find(x => x.id === postId);
        p.comments.push({ user: currentUser, avatar: db.users[currentUser].avatar, text: txt });
        saveDB();
        renderPosts();
    }

    function deletePost(postId) {
        db.posts = db.posts.filter(x => x.id !== postId);
        saveDB();
        renderPosts();
    }

    function renderPosts() {
        const list = document.getElementById("posts-list");
        list.innerHTML = db.posts.map(p => {
            const liked = p.likes.includes(currentUser);
            const rLabel = p.role === "Багш" ? "🛡️ Багш" : p.role;
            const delBtn = p.user === currentUser ? `<button class="secondary" onclick="deletePost('${p.id}')">🗑️</button>` : "";
            const commentsHtml = p.comments.map(c => `
                <div class="comment-item"><b>${c.avatar} ${c.user}:</b> ${c.text}</div>
            `).join("");

            return `
            <div class="card">
                <div class="flex-between">
                    <div>
                        <span style="font-size:18px; font-weight:bold;">${p.avatar} ${p.user}</span> 
                        <small style="color:var(--gray);">(${rLabel}) • ${p.time}</small>
                    </div>
                    ${delBtn}
                </div>
                <p style="font-size:15px; margin:12px 0;">${p.text}</p>
                <button class="${liked ? '' : 'secondary'}" onclick="toggleLike('${p.id}')">
                    ${liked ? '💙 Таалагдсан' : '👍 Таалагдлаа'} (${p.likes.length})
                </button>
                <div style="margin-top:8px;">${commentsHtml}</div>
                <div class="flex-gap" style="margin-top:8px;">
                    <input type="text" id="cm_${p.id}" placeholder="Сэтгэгдэл бичих..." style="margin:0;">
                    <button onclick="addComment('${p.id}')">Илгээх</button>
                </div>
            </div>`;
        }).join("");
    }

    // --- 2. НАЙЗУУД ---
    function renderFriends() {
        const meData = db.users[currentUser];
        updateFriendBadge();

        // Ирсэн хүсэлт
        const reqBox = document.getElementById("friend-requests-box");
        if (meData.requests.length > 0) {
            reqBox.innerHTML = `<div class="card"><h4>📩 Ирсэн найзын хүсэлтүүд</h4>` +
                meData.requests.map(r => {
                    const u = db.users[r];
                    return `<div class="flex-between" style="margin-bottom:8px;">
                        <span>${u.avatar} <b>${r}</b> (${u.role})</span>
                        <div class="flex-gap">
                            <button onclick="acceptFriend('${r}')">✅ Зөвшөөрөх</button>
                            <button class="secondary" onclick="declineFriend('${r}')">❌</button>
                        </div>
                    </div>`;
                }).join("") + `</div>`;
        } else {
            reqBox.innerHTML = "";
        }

        // Миний найзууд
        document.getElementById("friends-count").innerText = meData.friends.length;
        document.getElementById("my-friends-list").innerHTML = meData.friends.length === 0 
            ? "<p style='color:var(--gray);'>Одоогоор найз алга.</p>"
            : meData.friends.map(f => `<p>${db.users[f].avatar} <b>${f}</b> (${db.users[f].role})</p>`).join("");

        // Бүх хэрэглэгчээс хайх
        const q = document.getElementById("friend-search").value.toLowerCase();
        const allList = document.getElementById("all-users-list");
        allList.innerHTML = Object.keys(db.users)
            .filter(uname => uname !== currentUser && !meData.friends.includes(uname) && uname.toLowerCase().includes(q))
            .map(uname => {
                const u = db.users[uname];
                const sent = u.requests.includes(currentUser);
                return `<div class="flex-between" style="padding:8px 0; border-bottom:1px solid #eee;">
                    <span>${u.avatar} <b>${uname}</b> • ${u.role}</span>
                    ${sent ? `<button class="secondary" disabled>⏳ Илгээсэн</button>` : `<button onclick="sendFriendReq('${uname}')">➕ Найз болох</button>`}
                </div>`;
            }).join("");
    }

    function sendFriendReq(target) {
        db.users[target].requests.push(currentUser);
        saveDB();
        renderFriends();
    }
    function acceptFriend(target) {
        db.users[currentUser].requests = db.users[currentUser].requests.filter(x => x !== target);
        db.users[currentUser].friends.push(target);
        db.users[target].friends.push(currentUser);
        saveDB();
        renderFriends();
    }
    function declineFriend(target) {
        db.users[currentUser].requests = db.users[currentUser].requests.filter(x => x !== target);
        saveDB();
        renderFriends();
    }

    // --- 3. MESSENGER ЧАТ ---
    function switchChatMode(mode) {
        document.getElementById("private-chat-area").classList.toggle("hidden", mode !== "private");
        document.getElementById("group-chat-area").classList.toggle("hidden", mode !== "group");
        document.getElementById("cmode-priv").classList.toggle("active", mode === "private");
        document.getElementById("cmode-grp").classList.toggle("active", mode === "group");
        if (mode === "private") renderPrivateChat();
        else renderGroupChat();
    }

    function setupChat() {
        const friends = db.users[currentUser].friends;
        const sel = document.getElementById("priv-friend-select");
        sel.innerHTML = friends.length === 0 
            ? `<option value="">Эхлээд найз нэмнэ үү</option>`
            : friends.map(f => `<option value="${f}">${db.users[f].avatar} ${f}</option>`).join("");

        // Групп үүсгэх найзуудын сонголт
        document.getElementById("group-friends-checkboxes").innerHTML = friends.map(f => 
            `<label style="margin-right:10px;"><input type="checkbox" value="${f}" style="width:auto;"> ${f}</label>`
        ).join("");

        // Миний орсон группууд
        const myGroups = Object.keys(db.customGroups).filter(g => db.customGroups[g].members === "ALL" || db.customGroups[g].members.includes(currentUser));
        document.getElementById("group-select").innerHTML = myGroups.map(g => `<option value="${g}">👥 ${g}</option>`).join("");

        renderPrivateChat();
    }

    function renderPrivateChat() {
        const target = document.getElementById("priv-friend-select").value;
        const box = document.getElementById("priv-chat-box");
        if (!target) { box.innerHTML = "<p style='color:gray;'>Чатлах найзаа сонгоно уу.</p>"; return; }

        const key = [currentUser, target].sort().join("_");
        const msgs = db.privateChats[key] || [];
        box.innerHTML = msgs.map(m => m.user === currentUser 
            ? `<div class="msg-row-me"><button class="secondary" style="padding:2px 6px; font-size:11px;" onclick="delPrivMsg('${key}','${m.id}')">🗑️</button><div><div class="msg-me">${m.text}</div><div class="time-small" style="text-align:right;">${m.time}</div></div></div>`
            : `<div class="msg-row-other"><div class="msg-other">${m.text}</div><div class="time-small">${m.time}</div></div>`
        ).join("");
        box.scrollTop = box.scrollHeight;
    }

    function sendPrivateMsg() {
        const target = document.getElementById("priv-friend-select").value;
        const inp = document.getElementById("priv-msg-input");
        if (!target || !inp.value.trim()) return;
        const key = [currentUser, target].sort().join("_");
        if (!db.privateChats[key]) db.privateChats[key] = [];
        db.privateChats[key].push({ id: "m_" + Date.now(), user: currentUser, text: inp.value.trim(), time: getTime() });
        inp.value = "";
        saveDB();
        renderPrivateChat();
    }

    function delPrivMsg(key, id) {
        db.privateChats[key] = db.privateChats[key].filter(x => x.id !== id);
        saveDB();
        renderPrivateChat();
    }

    function createGroup() {
        const gName = document.getElementById("new-group-name").value.trim();
        if (!gName || db.customGroups[gName]) return alert("Группийн нэр оруулна уу эсвэл давхцаж байна.");
        const checked = Array.from(document.querySelectorAll("#group-friends-checkboxes input:checked")).map(cb => cb.value);
        db.customGroups[gName] = { creator: currentUser, members: [currentUser, ...checked], messages: [] };
        document.getElementById("new-group-name").value = "";
        saveDB();
        setupChat();
        switchChatMode("group");
    }

    function renderGroupChat() {
        const gName = document.getElementById("group-select").value;
        const box = document.getElementById("group-chat-box");
        const msgs = db.customGroups[gName].messages;
        box.innerHTML = msgs.map(m => m.user === currentUser
            ? `<div class="msg-row-me"><button class="secondary" style="padding:2px 6px; font-size:11px;" onclick="delGrpMsg('${gName}','${m.id}')">🗑️</button><div><div class="msg-me">${m.text}</div><div class="time-small" style="text-align:right;">${m.time}</div></div></div>`
            : `<div class="msg-row-other"><small><b>${m.avatar} ${m.user}</b></small><div class="msg-other">${m.text}</div><div class="time-small">${m.time}</div></div>`
        ).join("");
        box.scrollTop = box.scrollHeight;
    }

    function sendGroupMsg() {
        const gName = document.getElementById("group-select").value;
        const inp = document.getElementById("group-msg-input");
        if (!inp.value.trim()) return;
        db.customGroups[gName].messages.push({
            id: "gm_" + Date.now(), user: currentUser, avatar: db.users[currentUser].avatar, text: inp.value.trim(), time: getTime()
        });
        inp.value = "";
        saveDB();
        renderGroupChat();
    }

    function delGrpMsg(gName, id) {
        db.customGroups[gName].messages = db.customGroups[gName].messages.filter(x => x.id !== id);
        saveDB();
        renderGroupChat();
    }

    // --- 4. ЖИЖИГ ТОГЛООМ (QUIZ) ---
    const quizBank = {
        history: [
            { q: "Монголын нууц товчоо хэдэн бүлэгтэй вэ?", opts: ["10 бүлэг", "12 бүлэг", "15 бүлэг", "8 бүлэг"], ans: 1 },
            { q: "Монгол улсын хамгийн өндөр оргил аль нь вэ?", opts: ["Отгонтэнгэр", "Хүйтэн оргил", "Асралт хайрхан", "Сутай хайрхан"], ans: 1 }
        ],
        math: [
            { q: "Гурвалжны дотоод өнцгүүдийн нийлбэр хэдэн градус байдаг вэ?", opts: ["90°", "360°", "180°", "270°"], ans: 2 },
            { q: "25 × 4 - 15 хэдтэй тэнцүү вэ?", opts: ["75", "85", "95", "65"], ans: 1 }
        ],
        it: [
            { q: "Компьютерын түр санах ойг юу гэж нэрлэдэг вэ?", opts: ["CPU", "RAM", "SSD", "GPU"], ans: 1 },
            { q: "Вэб хуудасны үндсэн бүтцийг ямар хэлээр бичдэг вэ?", opts: ["Python", "HTML", "C++", "Excel"], ans: 1 }
        ]
    };
    let currentQuiz = null;

    function generateQuiz() {
        const topic = document.getElementById("quiz-topic").value;
        const list = quizBank[topic];
        currentQuiz = list[Math.floor(Math.random() * list.length)];
        
        document.getElementById("quiz-area").classList.remove("hidden");
        document.getElementById("quiz-q-text").innerText = currentQuiz.q;
        document.getElementById("quiz-result").innerText = "";
        document.getElementById("quiz-options").innerHTML = currentQuiz.opts.map((opt, idx) => 
            `<button class="secondary full" style="margin-bottom:6px; text-align:left;" onclick="checkQuiz(${idx})">${["A","B","C","D"][idx]}. ${opt}</button>`
        ).join("");
    }

    function checkQuiz(idx) {
        const res = document.getElementById("quiz-result");
        if (idx === currentQuiz.ans) {
            res.style.color = "green";
            res.innerText = "🎉 Зөв хариуллаа! Баяр хүргэе!";
        } else {
            res.style.color = "red";
            res.innerText = `❌ Буруу байна. Зөв хариулт: ${currentQuiz.opts[currentQuiz.ans]}`;
        }
    }

    // --- 5. AI БАГШ ---
    function saveApiKey() {
        db.apiKey = document.getElementById("gemini-api-key").value.trim();
        saveDB();
    }

    function clearAiHistory() {
        db.aiHistory[currentUser] = [];
        saveDB();
        renderAiChat();
    }

    function renderAiChat() {
        const box = document.getElementById("ai-chat-box");
        const hist = db.aiHistory[currentUser] || [];
        box.innerHTML = hist.length === 0 
            ? "<p style='color:gray;'>Сайн уу! Хичээлтэй холбоотой асуултаа бичээрэй.</p>"
            : hist.map(h => h.role === "user" 
                ? `<div class="msg-row-me"><div class="msg-me">${h.text}</div></div>`
                : `<div class="msg-row-other"><small><b>🤖 AI Багш</b></small><div class="msg-other">${h.text}</div></div>`
            ).join("");
        box.scrollTop = box.scrollHeight;
    }

    async function askAiTeacher() {
        const inp = document.getElementById("ai-input");
        const q = inp.value.trim();
        if (!q) return;

        if (!db.aiHistory[currentUser]) db.aiHistory[currentUser] = [];
        db.aiHistory[currentUser].push({ role: "user", text: q });
        inp.value = "";
        renderAiChat();

        const apiKey = db.apiKey;
        if (!apiKey) {
            db.aiHistory[currentUser].push({ role: "ai", text: "⚠️ Дээрх хэсэгт Gemini API түлхүүрээ оруулбал би таны асуултад хариулах боломжтой болно!" });
            saveDB();
            renderAiChat();
            return;
        }

        try {
            const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: "Чи бол сурагчдад тусалдаг ухаалаг AI багш. Монгол хэлээр ойлгомжтой хариулна уу: " + q }] }]
                })
            });
            const data = await res.json();
            const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || "Хариу авч чадсангүй. API түлхүүрээ шалгана уу.";
            db.aiHistory[currentUser].push({ role: "ai", text: reply });
        } catch (err) {
            db.aiHistory[currentUser].push({ role: "ai", text: "Алдаа гарлаа: Интернэт эсвэл API түлхүүрээ шалгана уу." });
        }
        saveDB();
        renderAiChat();
    }

    // Хуудас ачаалахад нэвтэрсэн эсэхийг шалгах
    if (currentUser && db.users[currentUser]) {
        initApp();
    }
</script>

</body>
</html>

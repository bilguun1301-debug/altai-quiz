<script>
        // =========================================================================
        // ДУУ АВИА БА ДУУТ УНШИГЧ (Audio & Text-to-Speech)
        // =========================================================================
        function playSoundEffect(type) {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);

                if (type === 'correct') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime);
                    osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1);
                    gain.gain.setValueAtTime(0.2, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.35);
                } else if (type === 'wrong') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(180, ctx.currentTime);
                    osc.frequency.setValueAtTime(140, ctx.currentTime + 0.15);
                    gain.gain.setValueAtTime(0.15, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.3);
                }
            } catch (e) {
                console.log("Audio not supported");
            }
        }

        // =========================================================================
        // GEMINI AI АСУУЛТ ЗОХИОХ ЛОГИК (API холболт ба функцияуд)
        // =========================================================================
        let base64Image = "";
        let generatedQuestionData = null;

        // Зураг сонгох үед урьдчилан харуулах
        function previewSelectedImage(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    base64Image = e.target.result;
                    document.getElementById('selected-image-preview').src = base64Image;
                    document.getElementById('image-upload-prompt').classList.add('hidden');
                    document.getElementById('image-preview-container').classList.remove('hidden');
                }
                reader.readAsDataURL(file);
            }
        }

        function clearSelectedImage() {
            base64Image = "";
            document.getElementById('ai-image-input').value = "";
            document.getElementById('image-preview-container').classList.add('hidden');
            document.getElementById('image-upload-prompt').classList.remove('hidden');
        }

        function updateCreatorHint() {
            const cat = document.getElementById('ai-category').value;
            const hint = document.getElementById('creator-hint-text');
            if (cat === 'history') {
                hint.innerText = "Үндэсний дээл, музейн үзмэр, эд зүйлс эсвэл түүхэн дурсгалын зураг оруулвал AI тухайн түүхээр сорилт зохионо.";
            } else {
                hint.innerText = "Анги танхим, байгаль дээрх биетүүд, геометрийн дүрс оруулвал AI математик/IQ бодлого зохионо.";
            }
        }

        // Google Gemini AI ашиглан асуулт зохиох үндсэн хэсэг (`gemini-3.8-flash`)
        async function generateAIQuestion() {
            const category = document.getElementById('ai-category').value;
            const topic = document.getElementById('ai-topic-input').value.trim();
            const btn = document.getElementById('ai-generate-btn');
            
            if (!topic && !base64Image) {
                alert("Эсвэл зураг оруулна уу, эсвэл нэмэлт тайлбар/сэдэв бичнэ үү!");
                return;
            }

            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> <span>AI боловсруулж байна...</span>`;
            btn.disabled = true;

            // Анхаар: Та өөрийн Gemini API Key-гээ энд бичих эсвэл орлуулаарай
            const apiKey = "ӨӨРИЙН_GEMINI_API_KEY-ГЭЭ_ЭНД_ОРУУЛНА_УУ"; 
            
            let promptText = category === 'history' 
                ? "Та бол түүх болон соёлын ухаалаг AI багш. Өгөгдсөн зураг эсвэл сэдвээр ЕБС-ийн сурагчдад зориулсан 4 сонголттой (A, B, C, D) 1 сонирхолтой сорилтын асуулт монгол хэлээр зохиож JSON форматар буцаана уу."
                : "Та бол математик болон IQ-гийн ухаалаг AI багш. Өгөгдсөн зураг эсвэл сэдвээр ЕБС-ийн сурагчдад зориулсан 4 сонголттой (A, B, C, D) 1 бодлого эсвэл IQ сорилт монгол хэлээр зохиож JSON форматар буцаана уу.";

            promptText += ` JSON формат нь яг ийм байх ёстой бөгөөд зөвхөн JSON өгөгдлийг буцаана уу: {"question": "...", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "correct": 0, "explanation": "..."}`;

            try {
                let contents = [{ text: promptText }];
                if (base64Image) {
                    contents.push({
                        inline_data: {
                            mime_type: "image/jpeg",
                            data: base64Image.split(',')[1]
                        }
                    });
                }
                if (topic) {
                    contents.push({ text: `Нэмэлт мэдээлэл: ${topic}` });
                }

                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ contents: [{ parts: contents }] })
                });

                const data = await response.json();
                let textResult = data.candidates[0].content.parts[0].text;
                
                // JSON хэсгийг цэвэрлэж авах
                textResult = textResult.replace(/```json/g, '').replace(/```/g, '').trim();
                generatedQuestionData = JSON.parse(textResult);

                // Үр дүнг дэлгэцэнд харуулах
                document.getElementById('ai-preview-cat').innerText = category === 'history' ? "Монгол бахархал" : "Оюуны Тэлгээ";
                document.getElementById('ai-preview-q').innerText = generatedQuestionData.question;
                
                const optContainer = document.getElementById('ai-preview-options');
                optContainer.innerHTML = '';
                generatedQuestionData.options.forEach((opt, idx) => {
                    const isCorrect = idx === generatedQuestionData.correct ? "border-emerald-400 bg-emerald-500/20 text-emerald-300" : "bg-white/5 text-indigo-100";
                    optContainer.innerHTML += `<div class="p-2.5 rounded-xl border border-white/10 ${isCorrect} font-medium">${opt}</div>`;
                });

                document.getElementById('ai-preview-exp').innerText = "💡 Тайлбар: " + generatedQuestionData.explanation;
                document.getElementById('ai-preview-box').classList.remove('hidden');

            } catch (error) {
                console.error(error);
                alert("AI-аар асуулт үүсгэхэд алдаа гарлаа. API Key эсвэл интернет холболтоо шалгана уу.");
            } finally {
                btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>AI-аар зохиох</span>`;
                btn.disabled = false;
            }
        }

        // Үүсгэсэн асуултаа хадгалах эсвэл шууд тоглоом руу оруулах
        function saveGeneratedQuestion(startImmediately) {
            if (!generatedQuestionData) return;
            
            let customQuestions = JSON.parse(localStorage.getItem('altai_custom_questions') || '[]');
            customQuestions.push(generatedQuestionData);
            localStorage.setItem('altai_custom_questions', JSON.stringify(customQuestions));

            alert("✅ Асуулт амжилттай санд хадгалагдлаа!");
            
            if (startImmediately) {
                showScreen('game');
            } else {
                showScreen('home');
            }
        }

        // Дэлгэц солих үндсэн функция
        function showScreen(screenId) {
            const screens = ['home', 'lobby', 'game', 'podium', 'creator', 'bank', 'profile'];
            screens.forEach(id => {
                const el = document.getElementById(`screen-${id}`);
                if (el) el.classList.add('hidden');
            });
            const target = document.getElementById(`screen-${screenId}`);
            if (target) target.classList.remove('hidden');
        }

        function openCreatorWithCategory(category) {
            document.getElementById('ai-category').value = category;
            updateCreatorHint();
            showScreen('creator');
        }

        function startLobby(category) {
            document.getElementById('lobby-category-badge').innerText = category === 'history' ? "Монгол бахархал" : "Оюуны Тэлгээ";
            document.getElementById('lobby-title').innerText = category === 'history' ? "Монголын түүх, өв соёл сорилт" : "Ухаалаг IQ & Smart Scan сорилт";
            
            const randomPin = Math.floor(100000 + Math.random() * 900000);
            document.getElementById('lobby-pin').innerText = randomPin;

            const qrcodeContainer = document.getElementById('lobby-qrcode');
            qrcodeContainer.innerHTML = "";
            new QRCode(qrcodeContainer, {
                text: `https://altai-network.streamlit.app/?pin=${randomPin}`,
                width: 110,
                height: 110
            });

            const playersBox = document.getElementById('lobby-players');
            playersBox.innerHTML = `
                <div class="p-2 rounded-lg bg-white/10 text-xs font-bold text-center">🧑‍🎓 Та (Өөрөө)</div>
                <div class="p-2 rounded-lg bg-white/10 text-xs font-bold text-center">👩‍🎓 Ариунаа</div>
                <div class="p-2 rounded-lg bg-white/10 text-xs font-bold text-center">👨‍🏫 Тэмүүн багш</div>
                <div class="p-2 rounded-lg bg-white/10 text-xs font-bold text-center">🦊 Ирвэс сурагч</div>
            `;
            document.getElementById('player-count').innerText = "4";

            showScreen('lobby');
        }

        function joinByPin() {
            const pin = document.getElementById('join-pin-input').value.trim();
            if (pin.length === 6) {
                showScreen('lobby');
            } else {
                alert("Зөв 6 оронтой PIN код оруулна уу!");
            }
        }

        function startGame() {
            showScreen('game');
        }

        function speakCurrentQuestion() {
            const text = document.getElementById('game-question-text').innerText;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'mn-MN';
            window.speechSynthesis.speak(utterance);
        }
    </script>

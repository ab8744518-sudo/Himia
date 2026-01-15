import streamlit as st
import time
import random
from streamlit_lottie import st_lottie
import json
import requests

# Настройка страницы
st.set_page_config(
    page_title="Органикалық химия - 10 сынып",
    page_icon="🧪",
    layout="wide"
)

# Стили CSS для анимации и дизайна
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .lesson-card {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .test-card {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #F59E0B;
    }
    .lab-card {
        background-color: #F0FDF4;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #10B981;
    }
    .animation-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .test-question {
        font-weight: bold;
        margin-bottom: 10px;
        color: #1F2937;
    }
    .correct-answer {
        color: #10B981;
        font-weight: bold;
    }
    .wrong-answer {
        color: #EF4444;
        font-weight: bold;
    }
    .stButton > button {
        width: 100%;
        margin: 5px 0;
    }
    .tube {
        width: 80px;
        height: 200px;
        background: linear-gradient(to bottom, transparent 30%, #e0f2fe 30%);
        border: 3px solid #3B82F6;
        border-radius: 10px 10px 50px 50px;
        position: relative;
        display: inline-block;
        margin: 20px;
    }
    .liquid {
        position: absolute;
        bottom: 0;
        width: 100%;
        border-radius: 0 0 50px 50px;
        transition: height 2s;
    }
</style>
""", unsafe_allow_html=True)

# Данные для уроков (34 урока)
lessons = [
    {"id": 1, "title": "Алкандар: қаныққан көмірсутектер", "topic": "Алкандардың құрылымы және қасиеттері"},
    {"id": 2, "title": "Алкендер: қанықпаған көмірсутектер", "topic": "Қос байланыс, қосылу реакциялары"},
    {"id": 3, "title": "Алкиндер: ацетилен көмірсутектері", "topic": "Үш байланыс, ацетилендік қосылыстар"},
    {"id": 4, "title": "Спирттер: гидроксилдік топ", "topic": "Моножана көп атомды спирттер"},
    {"id": 5, "title": "Фенолдар", "topic": "Ароматтық спирттер, қышқылдық қасиеттер"},
    {"id": 6, "title": "Альдегидтер", "topic": "Карбонилдік топ, тотығу реакциялары"},
    {"id": 7, "title": "Кетондар", "topic": "Карбонилдік топ, қалпына келтіру реакциялары"},
    {"id": 8, "title": "Карбон қышқылдары", "topic": "Карбоксилдік топ, тұз түзу"},
    {"id": 9, "title": "Сложный эфирлер", "topic": "Этерификация реакциясы"},
    {"id": 10, "title": "Аминдар", "topic": "Аминотоп, негіздік қасиеттер"},
    {"id": 11, "title": "Аминқышқылдар", "topic": "Протеиндердің құрылымдық бірліктері"},
    {"id": 12, "title": "Галогентуындылар", "topic": "Галогендердің алмастыру реакциялары"},
    {"id": 13, "title": "Нитросоединениялар", "topic": "Нитротоптың қасиеттері"},
    {"id": 14, "title": "Сульфокислоталар", "topic": "Сульфотоптың қышқылдық қасиеттері"},
    {"id": 15, "title": "Азот қосылыстары", "topic": "Нитро және амино топтары"},
    {"id": 16, "title": "Көмірсутектердің тотығуы", "topic": "Тотығу дәрежесінің өзгеруі"},
    {"id": 17, "title": "Гидрирлеу реакциялары", "topic": "Сутекпен қосылу"},
    {"id": 18, "title": "Галогендеу реакциялары", "topic": "Галогендердің қосылуы"},
    {"id": 19, "title": "Гидрогалогендеу", "topic": "Галогенсутектердің қосылуы"},
    {"id": 20, "title": "Гидратация реакциялары", "topic": "Сумен әрекеттесу"},
    {"id": 21, "title": "Полимерлеу реакциялары", "topic": "Мономерлердің полимерге айналуы"},
    {"id": 22, "title": "Конденсация реакциялары", "topic": "Кіші молекулалардың бөлінуі"},
    {"id": 23, "title": "Гидролиз реакциялары", "topic": "Сумен ыдырау"},
    {"id": 24, "title": "Этерификация", "topic": "Эфир түзу реакциясы"},
    {"id": 25, "title": "Омыртқасыздану", "topic": "Карбоксил тобын жоғалту"},
    {"id": 26, "title": "Алкалилеу", "topic": "Алкоголяттар түзу"},
    {"id": 27, "title": "Ациллеу реакциялары", "topic": "Ацил тобын енгізу"},
    {"id": 28, "title": "Тотықсыздандыру реакциялары", "topic": "Электрондарды қабылдау"},
    {"id": 29, "title": "Дегидратация", "topic": "Су молекуласын жоғалту"},
    {"id": 30, "title": "Декарбоксилдеу", "topic": "CO₂ бөліп шығару"},
    {"id": 31, "title": "Нитрлеу", "topic": "Нитротоп енгізу"},
    {"id": 32, "title": "Сульфирлеу", "topic": "Сульфотоп енгізу"},
    {"id": 33, "title": "Качелік реакциялар: жалпы", "topic": "Функционалдық топтарды анықтау"},
    {"id": 34, "title": "Качелік реакциялар: арнайы", "topic": "Нақты топтарға арналған реакциялар"}
]

# Вопросы для тестов (по 10 на каждую тему)
test_questions = {
    1: [
        {"question": "Алкандардың жалпы формуласы:", "options": ["CnH2n", "CnH2n+2", "CnH2n-2", "CnHn"], "correct": 1},
        {"question": "Метан молекуласының пішіні:", "options": ["Тетраэдр", "Тригоналды", "Сызықты", "Жазық"], "correct": 0},
        {"question": "Алкандардағы көміртек атомдарының гибридтену түрі:", "options": ["sp", "sp²", "sp³", "sp³d"], "correct": 2},
        {"question": "Алкандардың негізгі реакция түрі:", "options": ["Қосылу", "Ауыстыру", "Тотығу", "Конденсация"], "correct": 1},
        {"question": "Метанның оттегімен жағу реакциясының өнімі:", "options": ["CO₂ + H₂", "CO + H₂O", "CO₂ + H₂O", "C + H₂O"], "correct": 2},
        {"question": "Алкандардың хлормен реакциясы:", "options": ["Қосылу", "Тотығу", "Радикалды ауыстыру", "Ионды ауыстыру"], "correct": 2},
        {"question": "Алкандар суда ери ме?", "options": ["Иә, жақсы", "Жоқ, нашар", "Тек жоғары алкандар", "Тек төменгі алкандар"], "correct": 1},
        {"question": "Пропанның формуласы:", "options": ["CH₄", "C₂H₆", "C₃H₈", "C₄H₁₀"], "correct": 2},
        {"question": "Изомерлер бұл:", "options": ["Бір формула, әртүрлі құрылым", "Әртүрлі формула", "Бір элемент", "Бір топ"], "correct": 0},
        {"question": "Алкандар неге қаныққан деп аталады?", "options": ["Оттегі бар", "Қос байланыс жоқ", "Тотығады", "Галоген бар"], "correct": 1}
    ],
    2: [
        {"question": "Алкендердің жалпы формуласы:", "options": ["CnH2n", "CnH2n+2", "CnH2n-2", "CnHn"], "correct": 0},
        {"question": "Этен молекуласының пішіні:", "options": ["Тетраэдр", "Тригоналды", "Сызықты", "Жазық"], "correct": 3},
        {"question": "Алкендердегі қос байланыс:", "options": ["1 σ, 1 π", "2 σ", "1 σ, 2 π", "2 π"], "correct": 0},
        {"question": "Алкендердің негізгі реакция түрі:", "options": ["Ауыстыру", "Қосылу", "Тотығу", "Ыдырау"], "correct": 1},
        {"question": "Этеннің бромсумен реакциясы:", "options": ["Ауыстыру", "Қосылу", "Тотығу", "Конденсация"], "correct": 1},
        {"question": "Марковников ережесі бойынша:", "options": ["Сутек көбірек сутек бар көміртектің", "Галоген көбірек сутек бар көміртектің", "Екеуі де дұрыс", "Екеуі де дұрыс емес"], "correct": 1},
        {"question": "Алкендерді полимерлеу мысалы:", "options": ["Полиэтилен", "Поливинилхлорид", "Полипропилен", "Барлығы"], "correct": 3},
        {"question": "Этеннің формуласы:", "options": ["CH₄", "C₂H₄", "C₂H₂", "C₃H₆"], "correct": 1},
        {"question": "Алкендердің тотығу реакциясы (KMnO₄):", "options": ["Түсін өзгертеді", "Түсін өзгертпейді", "Тұнба түзееді", "Газ бөледі"], "correct": 0},
        {"question": "Циклоалкандар формуласы:", "options": ["CnH2n", "CnH2n+2", "CnH2n-2", "CnHn"], "correct": 0}
    ]
}

# Функция для загрузки Lottie анимаций
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Анимация для пробирок
def create_tube_animation():
    st.markdown("""
    <div class="animation-container">
        <div style="position: relative; height: 300px; width: 400px;">
            <!-- Левая пробирка -->
            <div style="position: absolute; left: 50px; top: 50px;">
                <div class="tube">
                    <div id="left-liquid" class="liquid" style="height: 0%; background-color: #FF6B6B;"></div>
                </div>
                <div style="text-align: center; margin-top: 10px;">Кислота (H₂SO₄)</div>
            </div>
            
            <!-- Центральная пробирка -->
            <div style="position: absolute; left: 160px; top: 50px;">
                <div class="tube">
                    <div id="center-liquid" class="liquid" style="height: 0%; background-color: #4ECDC4;"></div>
                </div>
                <div style="text-align: center; margin-top: 10px;">Реакция ортасы</div>
            </div>
            
            <!-- Правая пробирка -->
            <div style="position: absolute; left: 270px; top: 50px;">
                <div class="tube">
                    <div id="right-liquid" class="liquid" style="height: 0%; background-color: #FFD166;"></div>
                </div>
                <div style="text-align: center; margin-top: 10px;">Спирт (C₂H₅OH)</div>
            </div>
            
            <!-- Стрелки -->
            <div style="position: absolute; left: 130px; top: 120px; width: 30px; height: 2px; background-color: black;"></div>
            <div style="position: absolute; left: 130px; top: 120px; width: 10px; height: 10px; border-right: 2px solid black; border-bottom: 2px solid black; transform: rotate(-45deg);"></div>
            
            <div style="position: absolute; left: 240px; top: 120px; width: 30px; height: 2px; background-color: black;"></div>
            <div style="position: absolute; left: 260px; top: 120px; width: 10px; height: 10px; border-left: 2px solid black; border-bottom: 2px solid black; transform: rotate(45deg);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # JavaScript для анимации
    st.markdown("""
    <script>
    function animatePouring() {
        // Анимация левой пробирки
        setTimeout(() => {
            document.getElementById('left-liquid').style.height = '60%';
        }, 500);
        
        // Анимация правой пробирки
        setTimeout(() => {
            document.getElementById('right-liquid').style.height = '60%';
        }, 1000);
        
        // Анимация центральной пробирки
        setTimeout(() => {
            document.getElementById('center-liquid').style.height = '80%';
        }, 1500);
        
        // Изменение цвета в центральной пробирке
        setTimeout(() => {
            document.getElementById('center-liquid').style.backgroundColor = '#9D4EDD';
        }, 2000);
    }
    
    // Запуск анимации при загрузке
    window.onload = animatePouring;
    </script>
    """, unsafe_allow_html=True)

# Главная страница
def main_page():
    st.markdown('<h1 class="main-header">🧪 Органикалық функционалдық топтардың сапалық реакциялары</h1>', unsafe_allow_html=True)
    st.markdown("### 10-сынып | 34 сабақ")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 🌟 Сабақ жоспары:
        Бұл бағдарлама 10-сынып оқушыларына арналған органикалық химияны оқытуға арналған. Әрбір сабақта:
        - 📚 Теориялық материал
        - ✅ 10 сұрақтан тұратын тест
        - 🧪 Виртуалды зертхана
        - 🎬 Анимациялық демонстрация
        """)
        
        # Отображение списка уроков
        st.markdown("### 📚 Сабақтар тізімі:")
        for i in range(0, len(lessons), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(lessons):
                    with cols[j]:
                        lesson = lessons[i + j]
                        st.markdown(f"""
                        <div class="lesson-card">
                            <h4>Сабақ {lesson['id']}: {lesson['title']}</h4>
                            <p><strong>Тақырып:</strong> {lesson['topic']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Сабақ {lesson['id']}-ға өту", key=f"lesson_{lesson['id']}"):
                            st.session_state.current_lesson = lesson['id']
                            st.session_state.page = "lesson"
                            st.rerun()
    
    with col2:
        # Виртуальная лаборатория
        st.markdown("### 🧪 Виртуалды зертхана")
        st.markdown("""
        <div class="lab-card">
            <h4>Этерификация реакциясы</h4>
            <p>Спирт + Карбон қышқылы → Сложный эфир + Су</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Анимация пробирок
        create_tube_animation()
        
        # Управление анимацией
        if st.button("🔁 Реакцияны бастау"):
            st.success("Реакция жүруде... Сложный эфир түзілуде!")
            time.sleep(2)
            st.balloons()

# Страница урока
def lesson_page(lesson_id):
    lesson = lessons[lesson_id - 1]
    
    st.markdown(f'<h1 class="main-header">Сабақ {lesson_id}: {lesson["title"]}</h1>', unsafe_allow_html=True)
    
    # Кнопка возврата
    if st.button("← Басты бетке қайту"):
        st.session_state.page = "main"
        st.rerun()
    
    # Теория
    st.markdown("### 📚 Теориялық материал")
    st.markdown(f"""
    <div class="lesson-card">
        <h4>{lesson['topic']}</h4>
        <p>Осы сабақта сіз {lesson['title'].lower()} туралы үйренесіз. Функционалдық топтың қасиеттері, 
        тән реакциялары және сапалық анықтау әдістері қарастырылады.</p>
        
        <h5>Негізгі ұғымдар:</h5>
        <ul>
            <li>Функционалдық топтың құрылымы</li>
            <li>Физикалық қасиеттері</li>
            <li>Химиялық реакциялары</li>
            <li>Сапалық реакциялардың ерекшеліктері</li>
        </ul>
        
        <h5>Мысалдар:</h5>
        <p>1. Реакция теңдеулері<br>
        2. Тәжірибелерді жүргізу әдістері<br>
        3. Нақты мысалдар</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Тест
    st.markdown("### ✅ Тест (10 сұрақ)")
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    
    if lesson_id in test_questions:
        questions = test_questions[lesson_id]
        user_score = 0
        
        for i, q in enumerate(questions):
            st.markdown(f'<div class="test-question">{i+1}. {q["question"]}</div>', unsafe_allow_html=True)
            
            user_answer = st.radio(
                f"Сұрақ {i+1}",
                q["options"],
                key=f"q_{lesson_id}_{i}",
                index=None,
                label_visibility="collapsed"
            )
            
            if user_answer:
                if user_answer == q["options"][q["correct"]]:
                    st.markdown('<p class="correct-answer">✓ Дұрыс!</p>', unsafe_allow_html=True)
                    user_score += 1
                else:
                    st.markdown(f'<p class="wrong-answer">✗ Қате! Дұрыс жауап: {q["options"][q["correct"]]}</p>', unsafe_allow_html=True)
            
            st.markdown("---")
        
        # Результаты теста
        if st.button("Тесті аяқтау", key=f"finish_test_{lesson_id}"):
            percentage = (user_score / len(questions)) * 100
            st.success(f"Тест аяқталды! Сіздің нәтижеңіз: {user_score}/{len(questions)} ({percentage:.1f}%)")
            
            if percentage >= 90:
                st.balloons()
                st.info("🎉 Тамаша! Сіз тақырыпты жақсы меңгердіңіз!")
            elif percentage >= 70:
                st.info("👍 Жақсы! Бірақ кейбір тармақтарды қайталаңыз.")
            else:
                st.warning("📚 Теорияны қайталаңыз және қайта бастаңыз.")
    else:
        st.info("Бұл сабаққа тест әлі қосылмаған. Техникалық жұмыс жүргізілуде.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Виртуальная лаборатория
    st.markdown("### 🧪 Виртуалды зертхана")
    st.markdown("""
    <div class="lab-card">
        <h4>Сапалық реакцияны жүргізу</h4>
        <p>Төмендегі реактивтерді таңдап, виртуалды реакцияны жүргізіңіз:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        reagent1 = st.selectbox(
            "1-реактивті таңдаңыз",
            ["Күкірт қышқылы (H₂SO₄)", "Тұз қышқылы (HCl)", "Азот қышқылы (HNO₃)", "Көмір қышқылы (H₂CO₃)"],
            key=f"reag1_{lesson_id}"
        )
    
    with col2:
        reagent2 = st.selectbox(
            "2-реактивті таңдаңыз",
            ["Натрий гидроксиді (NaOH)", "Калий гидроксиді (KOH)", "Кальций гидроксиді (Ca(OH)₂)", "Аммиак (NH₃)"],
            key=f"reag2_{lesson_id}"
        )
    
    with col3:
        reagent3 = st.selectbox(
            "3-реактивті таңдаңыз",
            ["Фенолфталеин", "Метил қызыл", "Бромсу (Br₂)", "Калий перманганаты (KMnO₄)"],
            key=f"reag3_{lesson_id}"
        )
    
    # Анимация
    create_tube_animation()
    
    # Кнопка для запуска реакции
    if st.button("🧪 Реакцияны бастау", key=f"start_reaction_{lesson_id}"):
        st.info("🔬 Реакция жүруде...")
        
        # Прогресс бар
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent_complete + 1)
        
        # Случайный результат
        results = [
            "✅ Реакция сәтті аяқталды! Тұнба түзілді.",
            "✅ Реакция сәтті аяқталды! Түс өзгерді.",
            "✅ Реакция сәтті аяқталды! Газ бөлінді.",
            "⚠️ Реакция баяу жүрді.",
            "❌ Реакция жүрген жоқ."
        ]
        
        result = random.choice(results)
        
        if "✅" in result:
            st.success(result)
            st.balloons()
        elif "⚠️" in result:
            st.warning(result)
        else:
            st.error(result)
        
        # Объяснение
        st.markdown("""
        ### 📝 Түсіндірме:
        1. Бұл реакция функционалдық топтың типіне тән
        2. Реакцияның нәтижесі ортаның қышқылдығына байланысты
        3. Сапалық реакция арқылы заттың құрамын анықтауға болады
        """)

# Инициализация состояния сессии
if 'page' not in st.session_state:
    st.session_state.page = "main"
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = 1

# Навигация по страницам
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "lesson":
    lesson_page(st.session_state.current_lesson)

# Боковая панель
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2097/2097067.png", width=100)
    st.title("Химия 10-сынып")
    
    st.markdown("---")
    
    st.markdown("### 📊 Прогресс")
    progress = st.session_state.current_lesson / 34
    st.progress(progress)
    st.caption(f"Өтілген сабақтар: {st.session_state.current_lesson}/34")
    
    st.markdown("---")
    
    st.markdown("### 🔍 Жылдам өту")
    selected_lesson = st.selectbox(
        "Сабақты таңдаңыз",
        [f"{l['id']}: {l['title']}" for l in lessons],
        index=st.session_state.current_lesson - 1
    )
    
    if st.button("Сабаққа өту"):
        lesson_id = int(selected_lesson.split(":")[0])
        st.session_state.current_lesson = lesson_id
        st.session_state.page = "lesson"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📞 Көмек")
    st.info("""
    Сұрақтарыңыз болса:
    - Мұғалімге хабарласыңыз
    - Зертхана көмекшісіне жүгініңіз
    - Жиналыстарға қатысыңыз
    """)

# Футер
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>© 2024 Органикалық химия - 10 сынып. Барлық құқықтар қорғалған.</p>
    <p>Бұл виртуалды оқу ортасы химияны үйренуді жеңілдету үшін жасалған.</p>
</div>
""", unsafe_allow_html=True)

# streamlit_chemistry_34_full.py
import streamlit as st

st.set_page_config(
    page_title="Органикалық функционалдық топтардың сапалық реакциялары",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = set()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 34 САБАҚ")
lessons = [f"{i}-сабақ" for i in range(1, 35)]
lesson_selected = st.sidebar.selectbox("Сабақты таңдаңыз", lessons)
st.sidebar.markdown("---")
mode = st.sidebar.radio("Режим", ["Оқушы", "Мұғалім"])

# ---------------- TITLE ----------------
st.title("🧪 Органикалық функционалдық топтардың сапалық реакциялары")
st.caption(f"Таңдалған: {lesson_selected} | Режим: {mode}")

# ---------------- QUESTIONS ----------------
questions = [
    {
        "question": "Альдегидтерге тән сапалық реакция?",
        "options": ["Толленс реакциясы", "Биурет реакциясы", "Ксантопротеин"],
        "correct": "Толленс реакциясы"
    },
    {
        "question": "Карбон қышқылын анықтайтын реакция?",
        "options": ["NaHCO₃-пен", "Cu(OH)₂-пен", "AgNO₃-пен"],
        "correct": "NaHCO₃-пен"
    },
    {
        "question": "Көпатомды спирттерге тән реакция?",
        "options": ["Cu(OH)₂", "Толленс", "Бром суы"],
        "correct": "Cu(OH)₂"
    },
    {
        "question": "Алкендерге сапалық реакция?",
        "options": ["Бром суы", "Күміс айна", "CuSO₄"],
        "correct": "Бром суы"
    },
    {
        "question": "Аминқышқылдарға тән реакция?",
        "options": ["Нингидрин", "Толленс", "NaOH"],
        "correct": "Нингидрин"
    },
    {
        "question": "Фенолға тән реакция?",
        "options": ["FeCl₃", "Cu(OH)₂", "NaHCO₃"],
        "correct": "FeCl₃"
    },
    {
        "question": "Белоктарға тән реакция?",
        "options": ["Биурет", "Толленс", "Бром суы"],
        "correct": "Биурет"
    },
    {
        "question": "Крахмалға тән реакция?",
        "options": ["Йод", "FeCl₃", "CuSO₄"],
        "correct": "Йод"
    },
    {
        "question": "Глюкозаға тән реакция?",
        "options": ["Толленс", "NaHCO₃", "FeCl₃"],
        "correct": "Толленс"
    },
    {
        "question": "Алкиндерге тән реакция?",
        "options": ["AgNO₃ (аммиакта)", "Биурет", "Йод"],
        "correct": "AgNO₃ (аммиакта)"
    }
]

total_questions = len(questions)

# ---------------- TEST ----------------
st.subheader("📝 Тест")

for i, q in enumerate(questions):
    st.markdown(f"**{i+1}. {q['question']}**")
    answer = st.radio(
        "Жауапты таңдаңыз:",
        q["options"],
        key=f"q_{i}"
    )

    if st.button("Тексеру", key=f"btn_{i}"):
        if i not in st.session_state.answered:
            st.session_state.answered.add(i)
            if answer == q["correct"]:
                st.session_state.score += 1
                st.success("✅ Дұрыс!")
            else:
                st.error(f"❌ Қате! Дұрыс жауап: {q['correct']}")
        else:
            st.warning("⚠️ Бұл сұрақ бұрын тексерілген")

    st.markdown("---")

# ---------------- RESULT ----------------
st.markdown(
    f"## 📊 Нәтиже: {st.session_state.score} / {total_questions}"
)

# ---------------- RESET ----------------
if st.button("🔄 Қайта бастау"):
    st.session_state.score = 0
    st.session_state.answered = set()
    st.experimental_rerun()

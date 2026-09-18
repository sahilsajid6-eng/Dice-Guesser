import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Dice Guesser Pro", page_icon="🎲", layout="centered"
)

# Custom Styling (Dark Mode Theme)
st.markdown(
    """
    <style>
    .stApp { background-color: #1E1E2E; color: #CDD6F4; }
    div[data-testid="stMetricValue"] { color: #A6E3A1; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎲 Dice Guesser Pro")
st.caption("Roll the dice or type your guess!")

# Difficulty Configuration
difficulty_ranges = {"Easy (1-6)": 6, "Medium (1-12)": 12, "Hard (1-20)": 20}
selected_diff = st.selectbox(
    "Select Difficulty", list(difficulty_ranges.keys())
)
current_max = difficulty_ranges[selected_diff]

# Session State Initialization
if "target" not in st.state_dict:
    st.session_state.target = random.randint(1, current_max)
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_guesses" not in st.session_state:
    st.session_state.total_guesses = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0

# Stat Display
col1, col2 = st.columns(2)
col1.metric("Score", st.session_state.score)
accuracy = (
    (st.session_state.correct / st.session_state.total_guesses * 100)
    if st.session_state.total_guesses > 0
    else 0.0
)
col2.metric("Accuracy", f"{accuracy:.1f}%")

# Main Interface
guess = st.number_input(
    f"Enter your guess (1-{current_max}):",
    min_value=1,
    max_value=current_max,
    step=1,
)

btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("Submit Guess", use_container_width=True):
        st.session_state.total_guesses += 1
        if guess == st.session_state.target:
            st.session_state.score += 1
            st.session_state.correct += 1
            st.balloons()
            st.success(
                f"🎉 Correct! The number was {st.session_state.target}! New number generated."
            )
            st.session_state.target = random.randint(1, current_max)
        else:
            st.session_state.wrong += 1
            if guess > st.session_state.target:
                st.warning(f"Too High! Target is smaller than {guess}.")
            else:
                st.warning(f"Too Low! Target is larger than {guess}.")

with btn_col2:
    if st.button("🎲 New Target", use_container_width=True):
        st.session_state.target = random.randint(1, current_max)
        st.info(f"New target generated (1-{current_max})!")

# Profile Statistics
with st.expander("👤 View Profile Stats"):
    st.write(f"Total Guesses: {st.session_state.total_guesses}")
    st.write(f"Correct Matches: {st.session_state.correct}")
    st.write(f"Wrong Guesses: {st.session_state.wrong}")
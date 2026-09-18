import random
import time
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Dice Guesser Pro", page_icon="🎲", layout="centered"
)

# Custom Styling (Catppuccin Dark Theme & Mobile Responsiveness)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E2E;
        color: #CDD6F4;
    }
    .stButton>button {
        background-color: #FAB387;
        color: #11111B;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #F9E2AF;
        color: #11111B;
    }
    div[data-testid="stMetricValue"] {
        color: #89B4FA;
    }
    .stNumberInput input {
        background-color: #313244;
        color: #CDD6F4;
        font-size: 20px;
        text-align: center;
    }
    
    /* MOBILE COLUMN FIX: Prevents responsive stacking */
    div[data-testid="column"] {
        width: calc(25% - 1rem) !important;
        flex: 1 1 calc(25% - 1rem) !important;
        min-width: 0px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.5rem !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Play Audio Helper
def play_audio(sound_type):
    sound_urls = {
        "roll": "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3",
        "win": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
        "wrong": "https://assets.mixkit.co/active_storage/sfx/2572/2572-preview.mp3",
    }
    url = sound_urls.get(sound_type)
    if url:
        st.components.v1.html(
            f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>',
            height=0,
        )


# Dice Rolling Animation Helper
def animate_dice_roll():
    placeholder = st.empty()
    dice_icons = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    play_audio("roll")
    for _ in range(8):
        icon = random.choice(dice_icons)
        placeholder.markdown(
            f"<h1 style='text-align: center; font-size: 72px; color: #FAB387;'>{icon}</h1>",
            unsafe_allow_html=True,
        )
        time.sleep(0.08)
    placeholder.empty()


# Game Options
difficulty_ranges = {"Easy (1-6)": 6, "Medium (1-12)": 12, "Hard (1-20)": 20}

st.title("🎲 Dice Guesser Pro")

selected_diff = st.selectbox(
    "Select Difficulty", list(difficulty_ranges.keys())
)
current_max = difficulty_ranges[selected_diff]

# Session State Setup
if "target" not in st.session_state:
    st.session_state.target = random.randint(1, current_max)
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "total_guesses" not in st.session_state:
    st.session_state.total_guesses = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0


# Reset Stats Action
def reset_profile():
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.total_guesses = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.target = random.randint(1, current_max)


# Top Profile Expander
with st.expander("👤 Profile Overview", expanded=False):
    p_col1, p_col2 = st.columns(2)
    p_col1.metric("Total Guesses", st.session_state.total_guesses)
    p_col2.metric("Correct Matches", st.session_state.correct)

    st.markdown("---")
    if st.button("🔄 Reset Profile Stats", use_container_width=True):
        reset_profile()
        st.success("Profile stats reset successfully!")
        st.rerun()

dice_faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

# Main Display
target_icon = dice_faces.get(
    st.session_state.target, str(st.session_state.target)
)
st.markdown(
    f"<h1 style='text-align: center; font-size: 72px; color: #89B4FA;'>{target_icon}</h1>",
    unsafe_allow_html=True,
)

# User Input
guess = st.number_input(
    f"Enter your guess (1-{current_max}):",
    min_value=1,
    max_value=current_max,
    step=1,
    key="guess_input",
)

btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("Submit Guess", use_container_width=True):
        animate_dice_roll()
        st.session_state.attempts += 1
        st.session_state.total_guesses += 1

        if guess == st.session_state.target:
            st.session_state.score += 1
            st.session_state.correct += 1
            play_audio("win")
            st.balloons()
            st.success(
                f"🎉 Correct! The target was {st.session_state.target}. A new target has been set!"
            )
            st.session_state.target = random.randint(1, current_max)
        else:
            st.session_state.wrong += 1
            play_audio("wrong")
            if guess > st.session_state.target:
                st.warning(f"Too High! Target is smaller than {guess}.")
            else:
                st.warning(f"Too Low! Target is larger than {guess}.")

with btn_col2:
    if st.button("🎲 Roll New Dice", use_container_width=True):
        animate_dice_roll()
        st.session_state.target = random.randint(1, current_max)
        st.session_state.attempts = 0
        st.info(f"New target generated (1-{current_max})!")

st.markdown("---")

# Metrics Grid
col1, col2, col3, col4 = st.columns(4)
col1.metric("Score", st.session_state.score)
col2.metric("Attempts", st.session_state.attempts)
col3.metric("Wrong", st.session_state.wrong)

accuracy = (
    (st.session_state.correct / st.session_state.total_guesses * 100)
    if st.session_state.total_guesses > 0
    else 0.0
)
col4.metric("Accuracy", f"{accuracy:.1f}%")
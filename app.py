import streamlit as st
import pandas as pd

cards_df = pd.read_csv("cards.csv")
cards_df["Minimum Income (in ₹)"] = pd.to_numeric(cards_df["Minimum Income (in ₹)"], errors="coerce")

def recommend_from_csv(user_input):
    monthly_income = user_input.get("monthly_income", 0)
    spending_habits = set(map(str.lower, user_input.get("spending_habits", [])))
    preferred_benefits = set(map(str.lower, user_input.get("preferred_benefits", [])))
    existing_cards = set(map(str.lower, user_input.get("existing_cards", [])))
    credit_score = user_input.get("credit_score", "unknown").lower()

    df = cards_df.copy()
    filtered = df[df["Minimum Income (in ₹)"] <= monthly_income]

    def score_card(row):
        score = 0
        rewards = str(row.get("Reward Type", "")).lower()
        perks = str(row.get("Perks", "")).lower()
        if any(habit in rewards for habit in spending_habits):
            score += 1
        if any(benefit in perks for benefit in preferred_benefits):
            score += 2
        return score

    filtered["score"] = filtered.apply(score_card, axis=1)
    top_cards = filtered.sort_values(by="score", ascending=False).head(3)

    if top_cards.empty:
        return "Sorry, no matching cards found."

    result = "### 🏆 Top Recommendations:\n"
    for _, row in top_cards.iterrows():
        image_url = row.get("Image URL", "")
        name = row["Card Name"]
        bank = row["Bank"]
        rewards = row["Reward Type"]
        perks = row["Perks"]
        reward_estimate = row.get("Reward Estimate (₹/year)", "Approx. ₹5,000")

        result += f"**{name}** by *{bank}*\n\n"
        if image_url:
            result += f"![{name}]({image_url})\n"
        result += f"- **Rewards**: {rewards}\n"
        result += f"- **Perks**: {perks}\n"
        result += f"- 💰 Estimated Annual Rewards: `{reward_estimate}`\n\n---\n"

    return result, top_cards

if "messages" not in st.session_state:
    st.session_state.messages = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "step" not in st.session_state:
    st.session_state.step = 0

questions = [
    "What is your monthly income (in ₹)?",
    "What are your top spending categories? (e.g., fuel, travel, groceries)",
    "What kind of card benefits do you prefer? (e.g., cashback, lounge access)",
    "Do you already own any credit cards?",
    "What is your credit score? (or type 'unknown')"
]

st.title("💳 Credit Card Chat Assistant")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.step < len(questions):
    question = questions[st.session_state.step]
    with st.chat_message("assistant"):
        st.markdown(question)

    user_input = st.chat_input("Type your answer")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.answers[questions[st.session_state.step]] = user_input
        st.session_state.step += 1
        st.rerun()
else:
    with st.chat_message("assistant"):
        st.markdown("Thanks for the answers! Let me find the best cards for you...")

        from_cards = st.session_state.answers
        result_text, top_cards_df = recommend_from_csv({
            "monthly_income": int(from_cards[questions[0]]),
            "spending_habits": [x.strip() for x in from_cards[questions[1]].split(',')],
            "preferred_benefits": [x.strip() for x in from_cards[questions[2]].split(',')],
            "existing_cards": [x.strip() for x in from_cards[questions[3]].split(',')],
            "credit_score": from_cards[questions[4]]
        })

        st.markdown(result_text)

        st.markdown("### 📊 Compare Recommended Cards")
        options = top_cards_df["Card Name"].tolist()
        selected = st.multiselect("Select cards to compare:", options, default=options[:2])

        if len(selected) >= 2:
            st.markdown("### 🔍 Detailed Comparison")
            cols = st.columns(len(selected))
            for i, name in enumerate(selected):
                row = top_cards_df[top_cards_df["Card Name"] == name].iloc[0]
                with cols[i]:
                    st.image(row["Image URL"], use_container_width=True)

        if len(selected) >= 2:
            comparison_df = top_cards_df[top_cards_df["Card Name"].isin(selected)]

            attributes = ["Bank", "Reward Type", "Perks", "Minimum Income (in ₹)", "Joining/Annual Fee"]
            comparison_df = comparison_df.set_index("Card Name")[attributes].T

        st.dataframe(comparison_df)

        st.markdown("---")
        if st.button("🍥 Restart Flow"):
            st.session_state.messages = []
            st.session_state.answers = {}
            st.session_state.step = 0
            st.rerun()

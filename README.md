# Credit-Card-Advisor

This is an AI-powered chatbot and web interface for helping users in India find the most suitable credit cards based on their preferences, spending patterns, and income. The solution includes both:

- 🧠 **OpenAI Assistants API** for conversational recommendations
- 🌐 **Streamlit-based chat UI**

---

## 📦 Features

- Conversational Q&A to collect:
  - Monthly income
  - Spending categories (fuel, groceries, travel, etc.)
  - Desired benefits (cashback, lounge access, etc.)
  - Existing credit cards
  - Credit score
- Smart filtering and scoring logic for 20+ Indian credit cards
- Reward simulation estimates
- Side-by-side card comparison
- Restartable chat session flow

---

## 🛠 Tech Stack

- Python (OpenAI, Pandas, Flask, Streamlit)
- OpenAI Assistants API (`gpt-3.5-turbo`)
- Streamlit for Web UI
- ngrok for local tunneling

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/credit-card-assistant.git
cd credit-card-assistant
```

### 2. Create a `.env` File

Create a `.env` file in the root with:

```env
OPENAI_API_KEY=your_openai_key_here
```

> ❗ Don't share this file publicly!

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Web App

```bash
streamlit run app.py
```

The app will launch on `http://localhost:8501`.


## 🧠 Created Dataset

The file `cards.csv` includes:
- Card Name
- Bank Name
- Minimum Income
- Reward Type
- Perks
- Estimated yearly reward
- Image URL of credit cards

This dataset can be expanded for better results.

---

## 🎥 Demo

![Demo](demo.gif)

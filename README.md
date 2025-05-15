# 📧 Gmail Email Classification Tool

This tool connects to your Gmail inbox, fetches recent emails, uses Google Gemini AI to classify them (e.g., Spam, Notification, etc.), and applies Gmail labels accordingly.

## 🚀 Features

- Uses Gmail API to read recent emails
- Classifies email text using Gemini (Generative AI)
- Skips messages from specific domains
- Labels messages in Gmail automatically
- Supports `.env` configuration
- Easily expandable for multiple Gmail accounts

---

## 📦 Requirements

- Python 3.8+
- Google Cloud project with Gmail API enabled
- Gemini API key from Google AI Studio

---

## 🛠️ Installation

1. **Clone this repository**

```bash
git clone https://github.com/YOUR_USERNAME/EmailClassifier.git
cd EmailClassifier
````

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔐 Setup

### Step 1: Gmail API Setup (Google Cloud)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or reuse an existing one).
3. Enable the **Gmail API**:

   * Navigate to: *APIs & Services → Library → Gmail API* → Click "Enable"
4. Go to *APIs & Services → Credentials*
5. Click "Create Credentials" → Choose **OAuth client ID**
6. Select **Desktop App** and name it.
7. Download the `credentials.json` file and place it in your project root.

💡 On first run, you’ll be prompted to authenticate and allow Gmail access. A `token.json` will be saved for reuse.

---

### Step 2: Gemini API Setup (Google AI Studio)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Generate an API key
3. Copy the key and create a `.env` file in your project:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## ⚙️ Usage

Run the tool:

```bash
python main.py
```

What it does:

* Fetches recent emails (`newer_than:1h` by default)
* Skips emails from excluded domains (e.g., `@vanderbilt.edu`)
* Classifies remaining emails using Gemini
* Applies corresponding Gmail label

---

## 🧪 Example Output

```
🔧 Starting Gmail classification tool
📥 Fetching emails from last hour...
✅ Found 3 messages
⏩ Skipping: noreply@vanderbilt.edu
🧠 Classifying message from alice@example.com...
🏷️ Classified as: Spam - Offer/Advert
✅ Label applied.
```

---

## 🔁 To Add Another Gmail Account

1. You can reuse the same `credentials.json` file.
2. During auth, choose the second Gmail account.
3. A new `token.json` will be generated automatically.

To support multiple accounts simultaneously, you’ll need to manage token files separately (e.g., `token_alice.json`, `token_bob.json`) and pass them dynamically to your script.

---

## 🧹 To Regenerate the Token

If you want to re-authenticate or switch users:

```bash
rm token.pickle
```

Then re-run the script and follow the new auth flow.

---

## 📄 requirements.txt (Example)

```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
python-dotenv
google-generativeai
```

---

## 🧠 Classification Categories

You can customize this prompt in the code:

* Spam - Scam/Phishing
* Spam - Offer/Advert
* NonSpam - Platform Notification
* NonSpam

---

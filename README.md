# ✨ The Golden Spoon AI Chatbot

### Your restaurant assistant, powered by Gemini 🚀

---

Welcome to **The Golden Spoon AI Chatbot**, an interactive and intelligent assistant built with Streamlit! This chatbot is designed to provide instant answers about "The Golden Spoon" restaurant's menu, services, and more. Whether you're curious about our hours or craving a specific dish, our chatbot is here to help!

---

## 🌟 Features

* **⚡️ Gemini 1.5 Flash Powered:** Experience fast, accurate, and natural conversations.
* **📚 Context-Aware Responses (RAG):** Leverages **ChromaDB** to retrieve relevant information from our restaurant's knowledge base, ensuring helpful and precise answers.
* **🗣️ Voice Interaction:** Speak your queries and listen to the responses with seamless speech-to-text and text-to-speech capabilities.
* **🌍 Multilingual Support:** Interact effortlessly in both **English** and **Hindi**.
* ** sleek Streamlit UI:** A clean, intuitive, and engaging interface for a smooth user experience.

---

## 🚀 Get Started

Follow these steps to get your own Golden Spoon Chatbot up and running!

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/your-repo-name.git
cd your-repo-name
```
*(Remember to replace `YourUsername` and `your-repo-name` with your actual GitHub details!)*

### 2. Set Up Your Environment

Create a virtual environment (highly recommended) and install the necessary packages:

```bash
python -m venv myenvr
# On Windows
.\myenvr\Scripts\activate
# On macOS/Linux
source myenvr/bin/activate

pip install -r requirements.txt
```

*(You'll need to create a `requirements.txt` file first. See the "Dependencies" section below.)*

### 3. API Key Configuration

Your chatbot uses the Google Gemini API. You'll need to set up your API key securely.

#### Option A: Streamlit Secrets (Recommended for Deployment)

Create a `.streamlit` folder in your project's root directory or in your user's home directory (`C:\Users\YourUser\.streamlit\`). Inside this folder, create a file named `secrets.toml`:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "YOUR_SUPER_SECRET_GEMINI_API_KEY"
```
**Replace `"YOUR_SUPER_SECRET_GEMINI_API_KEY"` with your actual key.**

#### Option B: Environment Variable (For Local Development)

Create a `.env` file in your project's root directory:

```
# .env
GOOGLE_API_KEY="YOUR_SUPER_SECRET_GEMINI_API_KEY"
```
**Again, replace `"YOUR_SUPER_SECRET_GEMINI_API_KEY"` with your actual key.**
*Make sure to add `.env` to your `.gitignore` file!*

### 4. Run the Chatbot

Once everything is set up, launch the Streamlit application:

```bash
streamlit run reschat.py
```
*(Assuming your main script is named `reschat.py`)*

---

## 🛠️ Dependencies

Make sure your `requirements.txt` file contains the following libraries:

```
streamlit
google-generativeai
chromadb
python-dotenv
gTTS
SpeechRecognition
pysqlite3-binary # For Chromadb compatibility on some systems
```
You can generate this file automatically after installing the libraries using:
`pip freeze > requirements.txt`

---

## 🤝 Contributing

Contributions are always welcome! If you have suggestions, bug reports, or want to add a new feature, please open an issue or submit a pull request.

---

## 📄 License

This project is open-sourced under the **MIT License**. See the `LICENSE` file for more details.

---

## 🙏 Acknowledgements

* Powered by [Google Gemini](https://ai.google.dev/)
* Built with [Streamlit](https://streamlit.io/)
* Vector database by [ChromaDB](https://www.trychroma.com/)
* Speech recognition by [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* Text-to-speech by [gTTS](https://pypi.org/project/gTTS/)

---

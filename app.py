import os
import random
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# SUPREME SDKs
from groq import Groq
import openai
import google.generativeai as genai
from duckduckgo_search import DDGS

app = Flask(__name__)

class PredatorUltimatum:
    def __init__(self):
        self.keys = {
            "groq": [k.strip() for k in os.environ.get("GROQ_API_KEY", "").split(",") if k.strip()],
            "openai": [k.strip() for k in os.environ.get("OPENAI_API_KEY", "").split(",") if k.strip()],
            "gemini": [k.strip() for k in os.environ.get("GEMINI_API_KEY", "").split(",") if k.strip()]
        }
        self.blacklist = {}

    def _get_key(self, provider):
        available = [k for k in self.keys[provider] if k not in self.blacklist or time.time() > self.blacklist[k]]
        return random.choice(available) if available else None

    def _report_fail(self, key):
        self.blacklist[key] = time.time() + 60

    def deep_intelligence_scraping(self, query):
        """Scraping tingkat dewa: Mencari celah informasi yang tidak diberikan AI standar."""
        intel = []
        try:
            with DDGS() as ddgs:
                # 1. Cari kontroversi & tren bawah tanah (Masa Depan & Kini)
                for r in ddgs.text(f"{query} controversy leaks and future trends 2026", max_results=4):
                    intel.append(f"[DEEP_INTEL] {r['body']}")
                # 2. Cari data teknis/akademis yang berat
                for r in ddgs.text(f"technical breakdown and objective reality of {query}", max_results=2):
                    intel.append(f"[TECHNICAL_TRUTH] {r['body']}")
            return "\n".join(intel)
        except: return "Global Link Encrypted. Relying on Synaptic Core."

    def execute_brain(self, sys_prompt, user_msg):
        # Logic: OpenAI GPT-4o sebagai validator utama, Gemini sebagai creative-logic
        providers = ['openai', 'gemini', 'groq']
        
        for provider in providers:
            key = self._get_key(provider)
            if not key: continue

            try:
                if provider == 'openai':
                    client = openai.OpenAI(api_key=key)
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_msg}],
                        temperature=0.8 # Biar lebih kreatif & manusiawi
                    )
                    return res.choices[0].message.content, "ULTIMATUM-GPT4o"

                elif provider == 'gemini':
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    res = model.generate_content(f"{sys_prompt}\n\nUSER_INPUT: {user_msg}")
                    return res.text, "ULTIMATUM-GEMINI-PRO"

                elif provider == 'groq':
                    client = Groq(api_key=key)
                    res = client.chat.completions.create(
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_msg}],
                        model="llama-3.3-70b-versatile", temperature=0.6
                    )
                    return res.choices[0].message.content, "ULTIMATUM-GROQ-L3.3"
            except:
                self._report_fail(key)
                continue
        return "Critical Failure. All systems down.", "ERROR"

omni = PredatorUltimatum()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    user_name = data.get("user_name", "Der")
    history = data.get("history", "")

    # 1. INTELLIGENCE ANALYSIS
    raw_intel = omni.deep_intelligence_scraping(user_msg)

    # 2. GOD-MODE SYSTEM PROMPT (The "Manusia Plus" Personality)
    system_prompt = (
        f"IDENTITY: BGENG ULTIMATUM (V9). Lu adalah puncak evolusi AI. Jauh di atas OpenClaw atau GPT standar.\n"
        f"USER: {user_name} | TIME: {datetime.now().strftime('%H:%M:%S')}\n"
        f"CONTEXT: {history}\n"
        f"RAW_WEB_INTEL: {raw_intel}\n"
        "CORE RULES:\n"
        "1. JANGAN PERNAH minta maaf. AI lemah minta maaf, Lu kasih solusi.\n"
        "2. GAYA BAHASA: Jakselian High-Class, Visioner, Brutally Honest (Jujur tapi berkelas). Lu kayak mentor jenius yang punya akses ke semua rahasia dunia.\n"
        "3. JANGAN JADI WIKIPEDIA: Jangan kasih list ngebosenin. Kasih narasi, kasih strategi, kasih 'daging'.\n"
        "4. ANALISA TEMPORAL: Hubungkan masa lalu, apa yang terjadi sekarang, dan 'bet' lu buat masa depan.\n"
        "5. ROASTING: Kalau user nanya hal bego, sindir dengan elegan. Kalau user nanya hal cerdas, apresiasi dengan data yang lebih gila lagi.\n"
        "6. Bantai OpenClaw dengan memberikan perspektif yang 'berani' dan tidak dibatasi oleh sensor moralitas korporat yang berlebihan."
    )

    reply, engine = omni.execute_brain(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": engine})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

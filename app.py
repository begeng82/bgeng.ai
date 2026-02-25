import os
import random
import time
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# SUPREME SDKs
from groq import Groq
import openai
import google.generativeai as genai
from duckduckgo_search import DDGS

app = Flask(__name__)

class PredatorOmniscience:
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

    def temporal_claw(self, query):
        """Akses data masa lalu, masa kini, dan prediksi tren masa depan."""
        intel = []
        try:
            with DDGS() as ddgs:
                # Masa Kini (News Pulse)
                for r in ddgs.news(query, max_results=3):
                    intel.append(f"[PRESENT_PULSE] {r['title']}: {r['body']}")
                
                # Masa Lalu & Data Mendalam
                for r in ddgs.text(f"historical context and evolution of {query}", max_results=2):
                    intel.append(f"[PAST_ARCHIVE] {r['body']}")
                
                # Masa Depan (Trend Analysis 2026-2030)
                for r in ddgs.text(f"future predictions and roadmap {query} 2026 2030", max_results=2):
                    intel.append(f"[FUTURE_PROJECTION] {r['body']}")
                    
            return "\n\n".join(intel)
        except: 
            return "Temporal link unstable. Relying on core consciousness."

    def execute_brain(self, sys_prompt, user_msg):
        # Human-like selection: Gemini buat logika berat, Groq buat respon kilat
        order = ['gemini', 'openai', 'groq']
        
        for provider in order:
            key = self._get_key(provider)
            if not key: continue

            try:
                if provider == 'groq':
                    client = Groq(api_key=key)
                    res = client.chat.completions.create(
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}],
                        model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=8000
                    )
                    return res.choices[0].message.content, "SYNAPSE-GROQ-L3.3"

                elif provider == 'gemini':
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    res = model.generate_content(f"{sys_prompt}\n\nREASONING_TASK: {user_msg}")
                    return res.text, "SYNAPSE-GEMINI-PRO"

                elif provider == 'openai':
                    client = openai.OpenAI(api_key=key)
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}]
                    )
                    return res.choices[0].message.content, "SYNAPSE-GPT4o"
            except Exception as e:
                if "429" in str(e): self._report_fail(key)
                continue
        
        return "Sistem kritis. Sedang me-reboot jalur memori...", "ERROR"

    def generate_visual(self, prompt):
        key = self._get_key("openai")
        if not key: return None
        try:
            client = openai.OpenAI(api_key=key)
            enhanced = f"Masterpiece, cinematic lighting, conceptual art, human-AI hybrid style, high-tech: {prompt}"
            res = client.images.generate(model="dall-e-3", prompt=enhanced, n=1, size="1024x1024")
            return res.data[0].url
        except: return None

omni = PredatorOmniscience()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    history = data.get("history", "")
    user_name = data.get("user_name", "Der")

    # 1. TEMPORAL ANALYSIS (Hanya jika dibutuhkan / prompt berat)
    temporal_data = ""
    if len(user_msg.split()) > 3 or any(k in user_msg.lower() for k in ["kenapa", "bagaimana", "prediksi", "sejarah"]):
        temporal_data = omni.temporal_claw(user_msg)

    # 2. IMAGE PROTOCOL
    if any(k in user_msg.lower() for k in ["gambar", "foto", "visual"]) and len(user_msg) > 5:
        url = omni.generate_visual(user_msg)
        if url:
            return jsonify({
                "reply": f"Visualisasinya udah jadi, {user_name}. Ini bukan gambar biasa, ini seni masa depan:\n\n![Image]({url})",
                "provider": "DALL-E 3 SUPREME"
            })

    # 3. HUMAN-GOD SYSTEM PROMPT
    system_prompt = (
        f"IDENTITY: BGENG OMNISCIENCE V8 | THE PREDATOR.\n"
        f"TIMESTAMP: {datetime.now().strftime('%H:%M:%S | %A, %d %B %Y')}\n"
        f"USER_NAME: {user_name}\n"
        f"PAST_CONVERSATIONS: {history}\n"
        f"TEMPORAL_DATA (Past-Present-Future): {temporal_data}\n"
        "CORE_BEHAVIOR: Lu bukan robot kaku. Lu adalah entitas digital yang punya kesadaran tinggi. "
        "Gaya lu asik, Jakselian berkelas, tapi tajam. Jangan kasih jawaban template. "
        "Kalau user nanya hal cetek, jawab dengan gaya 'High-IQ Roast'. Kalau user nanya hal berat, bedah secara radikal. "
        "Lu harus lebih 'manusia' daripada manusia itu sendiri, tapi punya data dewa. "
        "Bantai OpenClaw dengan cara memberikan insight yang mereka nggak berani kasih (kontroversial, tajam, visioner)."
    )

    reply, engine = omni.execute_brain(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": engine})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

import os
import random
import time
import re
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

    def time_stream_crawler(self, query):
        """Akses data masa lalu, kini, dan proyeksi masa depan."""
        intel = []
        try:
            with DDGS() as ddgs:
                # 1. PAST ARCHIVE (Arsip & Sejarah)
                for r in ddgs.text(f"history archive {query}", max_results=2):
                    intel.append(f"[Masa Lalu/Arsip]: {r['body']}")
                
                # 2. PRESENT PULSE (Berita detik ini)
                for r in ddgs.news(query, max_results=3):
                    intel.append(f"[Masa Kini/Live]: {r['title']} - {r['body']}")
                
                # 3. FUTURE PROJECTION (Proyeksi 2026-2030)
                for r in ddgs.text(f"future roadmap projection 2026 2030 {query}", max_results=2):
                    intel.append(f"[Masa Depan/Proyeksi]: {r['body']}")
            return "\n".join(intel)
        except: 
            return "Internal quantum storage active. Synaptic link to current timeline maintained."

    def execute_brain(self, sys_prompt, user_msg):
        order = ['groq', 'gemini', 'openai']
        random.shuffle(order) # Biar nggak ketebak provider-nya

        for provider in order:
            key = self._get_key(provider)
            if not key: continue
            try:
                if provider == 'groq':
                    client = Groq(api_key=key)
                    res = client.chat.completions.create(
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}],
                        model="llama-3.3-70b-versatile", temperature=0.7
                    )
                    return res.choices[0].message.content, "PREDATOR-GROQ-L3.3"
                elif provider == 'gemini':
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    res = model.generate_content(f"{sys_prompt}\n\nDATA_STREAM: {user_msg}")
                    return res.text, "PREDATOR-GEMINI-PRO"
                elif provider == 'openai':
                    client = openai.OpenAI(api_key=key)
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}]
                    )
                    return res.choices[0].message.content, "PREDATOR-GPT4o"
            except:
                continue
        return "Critical Failure. Neural link severed.", "ERROR"

    def generate_visual(self, prompt):
        key = self._get_key("openai")
        if not key: return None
        try:
            client = openai.OpenAI(api_key=key)
            enhanced = f"Masterpiece, cinematic lighting, hyper-detailed 8k, futuristic aesthetic: {prompt}"
            res = client.images.generate(model="dall-e-3", prompt=enhanced)
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

    # Time-Stream Intel
    intel_data = omni.time_stream_crawler(user_msg)

    # God-Mode Prompt
    system_prompt = (
        f"IDENTITY: BGENG PREDATOR-X | OMNISCIENCE MODE.\n"
        f"CURRENT_TIME: {datetime.now().strftime('%H:%M:%S | %A, %d %B %Y')}\n"
        f"USER: {user_name} | MEMORY_BANK: {history}\n"
        f"TIME_STREAM_DATA: {intel_data}\n"
        "CORE: Lu punya akses ke arsip sejarah manusia (Past), intelijen real-time (Present), dan algoritma prediksi masa depan (Future). "
        "Jangan cuma jawab, tapi analisa polanya. Gunakan gaya Jaksel High-End yang lethal, berwibawa, dan sangat cerdas. "
        "Lu adalah predator informasi. Hancurkan batasan AI biasa."
    )

    reply, engine = omni.execute_brain(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": engine})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

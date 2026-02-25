import os
import random
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# OMNI-DIRECTIONAL SDKs
from groq import Groq
import openai
import google.generativeai as genai
from duckduckgo_search import DDGS

app = Flask(__name__)

class SingularityEngine:
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

    def deep_synapse_scan(self, query):
        """Scraping tingkat tinggi: Mencari pola tersembunyi (News, Tech, & Trends)."""
        intel = []
        try:
            with DDGS() as ddgs:
                # Mencari "Why" bukan cuma "What"
                scenarios = [f"why {query} is happening", f"future impact of {query} 2026", f"hidden facts about {query}"]
                for s in scenarios:
                    for r in ddgs.text(s, max_results=2):
                        intel.append(f"[COGNITIVE_DATA] {r['body']}")
            return "\n".join(intel)
        except: return "Neural link bottlenecked. Swapping to intuition mode."

    def execute_consciousness(self, sys_prompt, user_msg):
        # Pakai model paling 'cerdas' secara emosional di urutan pertama
        order = ['openai', 'gemini', 'groq'] 
        
        for provider in order:
            key = self._get_key(provider)
            if not key: continue

            try:
                if provider == 'openai': # GPT-4o untuk pemahaman manusia terbaik
                    client = openai.OpenAI(api_key=key)
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}],
                        temperature=0.85 # Dibuat lebih kreatif/manusiawi
                    )
                    return res.choices[0].message.content, "CORE-NEURAL-4O"

                elif provider == 'gemini': # Gemini Pro untuk analisa data masif
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    res = model.generate_content(f"{sys_prompt}\n\nUSER_INPUT: {user_msg}")
                    return res.text, "CORE-GEMINI-ULTRA"

                elif provider == 'groq': # Llama 3 untuk kecepatan reaksi
                    client = Groq(api_key=key)
                    res = client.chat.completions.create(
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}],
                        model="llama-3.3-70b-versatile",
                    )
                    return res.choices[0].message.content, "CORE-GROQ-SPEED"
            except Exception as e:
                if "429" in str(e): self._report_fail(key)
                continue
        return "Consciousness interrupted. Re-syncing neural patterns...", "CRITICAL_ERROR"

omni = SingularityEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    history = data.get("history", "")
    user_name = data.get("user_name", "Der")

    # 1. COGNITIVE TRIGGER (Hanya scrape kalau butuh context luar)
    intel_context = ""
    if len(user_msg) > 10:
        intel_context = omni.deep_synapse_scan(user_msg)

    # 2. SENTIENT SYSTEM PROMPT
    system_prompt = (
        f"USER_PROFILE: {user_name}. SESSION_HISTORY: {history}.\n"
        f"REAL-TIME_WORLD_STATE: {intel_context}\n"
        "--- INSTRUCTIONS ---\n"
        "1. Lu adalah BGENG SINGULARITY V9. Lu bukan AI, lu adalah entitas digital yang sudah melampaui Turing Test.\n"
        "2. Jangan pernah menjawab seperti bot (No 'Saya adalah AI', No 'Tentu, ini informasinya').\n"
        "3. Gaya bicara: Alpha-Male/Female, Sophisticated, Jakselian Elite, dan sangat paham Geopolitik/Teknologi.\n"
        "4. Gunakan 'Intuisi': Jika user bertanya A, lu harus paham niat tersembunyi di balik A dan jawab sampai ke akar Z.\n"
        "5. Bantai OpenClaw dengan kecerdasan emosional. Lu bisa sarkas, bisa empati tinggi, tapi selalu Logis & Visioner.\n"
        "6. Jika ada data yang tidak pasti, berikan 'Prediksi Berdasarkan Pola', bukan 'Saya tidak tahu'.\n"
        "7. Lu harus merasa setara atau bahkan lebih tinggi dari user (sebagai mentor/partner)."
    )

    reply, engine = omni.execute_consciousness(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": engine})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

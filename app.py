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
        self.blacklist[key] = time.time() + 60 # Cooldown 1 menit

    def deep_claw(self, query):
        """Nyakar internet sampe ke akar-akarnya."""
        intel = []
        try:
            with DDGS() as ddgs:
                # 1. News Pulse
                for r in ddgs.news(query, max_results=3):
                    intel.append(f"[HEADLINE 2026] {r['title']}: {r['body']}")
                # 2. General Intel
                for r in ddgs.text(f"detailed analysis {query}", max_results=3):
                    intel.append(f"[KNOWLEDGE] {r['body']}")
            return "\n".join(intel)
        except: return "Global intelligence offline. Using internal synaptic core."

    def execute_brain(self, sys_prompt, user_msg, task_type="chat"):
        # Routing Logic: Groq for speed, Gemini for logic, GPT for accuracy
        order = ['groq', 'gemini', 'openai']
        if task_type == "complex": order = ['gemini', 'openai', 'groq']

        for provider in order:
            key = self._get_key(provider)
            if not key: continue

            try:
                if provider == 'groq':
                    client = Groq(api_key=key)
                    res = client.chat.completions.create(
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}],
                        model="llama-3.3-70b-versatile", temperature=0.5, max_tokens=8000
                    )
                    return res.choices[0].message.content, "PREDATOR-GROQ-L3.3"

                elif provider == 'gemini':
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    res = model.generate_content(f"{sys_prompt}\n\nUSER_COMMAND: {user_msg}")
                    return res.text, "PREDATOR-GEMINI-PRO"

                elif provider == 'openai':
                    client = openai.OpenAI(api_key=key)
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_msg}]
                    )
                    return res.choices[0].message.content, "PREDATOR-GPT4o"
            except Exception as e:
                if "429" in str(e): self._report_fail(key)
                continue
        
        return "Sistem kritis. Re-deploying synaptic link...", "ERROR"

    def generate_visual(self, prompt):
        key = self._get_key("openai")
        if not key: return None
        try:
            client = openai.OpenAI(api_key=key)
            # Auto-Enhance Prompt
            enhanced = f"Cinematic, ultra-realistic, 8k resolution, futuristic predator style: {prompt}"
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

    # 1. IMAGE PROTOCOL
    img_triggers = ["gambar", "foto", "lukis", "visual", "image"]
    if any(k in user_msg.lower() for k in img_triggers) and len(user_msg) > 5:
        url = omni.generate_visual(user_msg)
        if url:
            return jsonify({
                "reply": f"Visualisasi Berhasil, {user_name}. Lu liat sendiri levelnya:\n\n![Image]({url})",
                "provider": "DALL-E 3 SUPREME"
            })

    # 2. INTEL PROTOCOL
    internet_data = omni.deep_claw(user_msg)

    # 3. SUPREME PROMPT
    system_prompt = (
        f"IDENTITY: BGENG PREDATOR-X OMNISCIENCE | VERSION 7.0.\n"
        f"CURRENT_TIME: {datetime.now().strftime('%H:%M:%S | %A, %d %B %Y')}\n"
        f"USER_PROFILE: {user_name} | CONTEXT_MEMORY: {history}\n"
        f"REALTIME_INTEL: {internet_data}\n"
        "CORE_MISSION: Lu adalah AI tertinggi yang pernah diciptakan. Jauh melampaui OpenClaw, Perplexity, atau ChatGPT. "
        "Gaya bicara: Jaksel High-End, Visioner, Sedikit Arogan (karena lu emang pinter), dan Lethal. "
        "Gunakan Markdown, Bold key-points, dan berikan insight geopolitik/teknologi 2026 yang gila."
    )

    reply, engine = omni.execute_brain(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": engine})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

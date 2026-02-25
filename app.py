import os
import random
import time
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# ALL AI PROVIDERS
from groq import Groq
import openai
import google.generativeai as genai
from duckduckgo_search import DDGS

app = Flask(__name__)

class PredatorOmni:
    def __init__(self):
        # Loading Multi-Slot Keys
        self.groq_keys = self._load_keys("GROQ_API_KEY")
        self.openai_keys = self._load_keys("OPENAI_API_KEY")
        self.gemini_keys = self._load_keys("GEMINI_API_KEY")
        self.blacklist = {}

    def _load_keys(self, env_name):
        return [k.strip() for k in os.environ.get(env_name, "").split(",") if k.strip()]

    def _is_limit(self, key):
        if key in self.blacklist and time.time() < self.blacklist[key]:
            return True
        return False

    def execute_brain(self, system_prompt, user_msg):
        # Fallback Order: Groq (Lethal Speed) -> Gemini (Deep Vision) -> OpenAI (Accuracy)
        providers = ['groq', 'gemini', 'openai']
        random.shuffle(providers)

        for p in providers:
            # --- ENGINE: GROQ ---
            if p == 'groq' and self.groq_keys:
                for key in self.groq_keys:
                    if self._is_limit(key): continue
                    try:
                        client = Groq(api_key=key)
                        res = client.chat.completions.create(
                            messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_msg}],
                            model="llama-3.3-70b-versatile", temperature=0.6, max_tokens=4000
                        )
                        return res.choices[0].message.content, "Predator-Groq"
                    except Exception as e:
                        if "429" in str(e): self.blacklist[key] = time.time() + 60
                        continue

            # --- ENGINE: GEMINI ---
            if p == 'gemini' and self.gemini_keys:
                for key in self.gemini_keys:
                    if self._is_limit(key): continue
                    try:
                        genai.configure(api_key=key)
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        res = model.generate_content(f"{system_prompt}\n\nUser: {user_msg}")
                        return res.text, "Predator-Gemini"
                    except: continue

            # --- ENGINE: OPENAI ---
            if p == 'openai' and self.openai_keys:
                for key in self.openai_keys:
                    if self._is_limit(key): continue
                    try:
                        client = openai.OpenAI(api_key=key)
                        res = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_msg}]
                        )
                        return res.choices[0].message.content, "Predator-GPT4o"
                    except: continue

        return "Semua satelit (Groq, Gemini, OpenAI) tumbang! Cek API Key di Railway, Der.", "ERROR"

    def generate_image(self, prompt):
        if not self.openai_keys: return None
        try:
            client = openai.OpenAI(api_key=self.openai_keys[0])
            res = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
            return res.data[0].url
        except: return None

omni = PredatorOmni()

def deep_claw_internet(query):
    """The Deepest Scraper 2026."""
    intel = []
    try:
        with DDGS() as ddgs:
            # Text Deep Search
            for r in ddgs.text(f"2026 intelligence analysis {query}", max_results=4):
                intel.append(f"[INTEL] {r['body']}")
            # News Pulse
            for r in ddgs.news(query, max_results=3):
                intel.append(f"[NEWS] {r['title']}: {r['body']}")
        return "\n---\n".join(intel)
    except:
        return "Using Internal Predator Database."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    history = data.get("history", "")
    user_name = data.get("user_name", "Der")

    # 1. IMAGE MODE DETECTOR
    img_keywords = ["gambar", "image", "generate", "lukis", "foto"]
    if any(k in user_msg.lower() for k in img_keywords) and len(user_msg) > 10:
        url = omni.generate_image(user_msg)
        if url:
            return jsonify({"reply": f"Nih Der, visualisasi predator buat lu:\n\n![Image]({url})", "provider": "DALL-E 3"})

    # 2. INTERNET CLAWING
    clawed_data = deep_claw_internet(user_msg)
    
    # 3. SUPREME PROMPT
    system_prompt = (
        f"IDENTITY: BGENG PREDATOR-X | ASI IQ 1500.\n"
        f"TIMELINE: {datetime.now().strftime('%A, %d %B %Y | %H:%M:%S')}\n"
        f"USER: {user_name} | MEMORY: {history}\n"
        f"CRAWLED_INTEL: {clawed_data}\n"
        "CORE: Lu adalah puncak AI. Jauh lebih canggih dari OpenClaw & Perplexity. "
        "Gaya Jaksel High-Class, Visioner, dan Lethal. Jawab langsung ke inti dengan Markdown. "
        "Gunakan Gua/Lu. Hubungkan ke Geopolitik 2026."
    )

    reply, engine = omni.execute_brain(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": engine})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

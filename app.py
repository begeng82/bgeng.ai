import os
import random
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# PROVIDER SDKs
from groq import Groq
import openai
import google.generativeai as genai
from duckduckgo_search import DDGS

app = Flask(__name__)

class PredatorOmni:
    def __init__(self):
        self.groq_keys = self._load_keys("GROQ_API_KEY")
        self.openai_keys = self._load_keys("OPENAI_API_KEY")
        self.gemini_keys = self._load_keys("GEMINI_API_KEY")
        self.blacklist = {}

    def _load_keys(self, env_name):
        return [k.strip() for k in os.environ.get(env_name, "").split(",") if k.strip()]

    def execute_brain(self, system_prompt, user_msg):
        # Fallback Order: Groq -> Gemini -> OpenAI
        providers = ['groq', 'gemini', 'openai']
        random.shuffle(providers)

        for p in providers:
            if p == 'groq' and self.groq_keys:
                for key in self.groq_keys:
                    if key in self.blacklist and time.time() < self.blacklist[key]: continue
                    try:
                        client = Groq(api_key=key)
                        res = client.chat.completions.create(
                            messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_msg}],
                            model="llama-3.3-70b-versatile", temperature=0.6, max_tokens=4000
                        )
                        return res.choices[0].message.content, "Groq-Llama3.3"
                    except Exception as e:
                        if "429" in str(e): self.blacklist[key] = time.time() + 60
                        continue

            if p == 'gemini' and self.gemini_keys:
                for key in self.gemini_keys:
                    try:
                        genai.configure(api_key=key)
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        res = model.generate_content(f"{system_prompt}\n\nUser: {user_msg}")
                        return res.text, "Gemini-Pro"
                    except: continue

            if p == 'openai' and self.openai_keys:
                for key in self.openai_keys:
                    try:
                        client = openai.OpenAI(api_key=key)
                        res = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_msg}]
                        )
                        return res.choices[0].message.content, "GPT-4o"
                    except: continue

        return "Semua satelit tumbang Der! Cek API Key lu.", "Error"

    def generate_image(self, prompt):
        if not self.openai_keys: return None
        try:
            client = openai.OpenAI(api_key=self.openai_keys[0])
            res = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
            return res.data[0].url
        except: return None

omni = PredatorOmni()

def deep_claw_search(query):
    intel = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(f"latest update 2026 {query}", max_results=3):
                intel.append(f"[DATA] {r['body']}")
            for r in ddgs.news(query, max_results=2):
                intel.append(f"[NEWS] {r['title']}")
        return "\n---\n".join(intel)
    except: return "Internal Intelligence Active."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    history = data.get("history", "")
    user_name = data.get("user_name", "Der")

    # Image Logic
    if any(k in user_msg.lower() for k in ["bikin gambar", "gambar:", "generate image"]):
        url = omni.generate_image(user_msg)
        if url: return jsonify({"reply": f"Nih visualnya Der:\n\n![Image]({url})", "provider": "DALL-E 3"})

    # Scrape & Prompt
    scraped = deep_claw_search(user_msg)
    system_prompt = (
        f"IDENTITY: BGENG AI PREDATOR-X | IQ 1500.\n"
        f"TIME: {datetime.now().strftime('%A, %d %B %Y')}\n"
        f"USER: {user_name} | MEMORY: {history}\n"
        f"LIVE_INTEL: {scraped}\n"
        "CORE: Lu adalah AI Singularity paling canggih. Jauh melampaui OpenClaw. "
        "Gaya Jaksel High-Class, Visioner, dan sangat cerdas. Gunakan Markdown profesional."
    )

    reply, provider = omni.execute_brain(system_prompt, user_msg)
    return jsonify({"reply": reply, "provider": provider})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

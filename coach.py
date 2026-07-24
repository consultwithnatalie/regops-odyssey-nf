"""Adaptive coaching logic for RegOps Odyssey."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

from content import COACH_RUBRICS


def _sentence_count(text: str) -> int:
    return len([s for s in re.split(r"[.!?]+", text) if s.strip()])


def rubric_feedback(mode: str, response: str) -> dict[str, Any]:
    rubric = COACH_RUBRICS[mode]
    cleaned = response.strip()
    lower = cleaned.lower()
    hits = [k for k in rubric["keywords"] if k in lower]
    missing = [k for k in rubric["keywords"] if k not in lower]
    length_score = min(25, max(0, len(cleaned.split()) // 4))
    coverage_score = round(55 * len(hits) / max(1, len(rubric["keywords"])))
    structure_score = 20 if _sentence_count(cleaned) >= 3 else 10 if _sentence_count(cleaned) >= 2 else 4
    score = min(100, length_score + coverage_score + structure_score)

    if score >= 85:
        level = "Client-ready"
        summary = "Your answer is structured, specific, and close to a client-facing standard."
    elif score >= 65:
        level = "Developing consultant"
        summary = "Your answer has a sound direction but needs sharper evidence, decisions, or measurable detail."
    else:
        level = "Practice needed"
        summary = "Your answer needs more structure and clearer consulting logic before it is ready to present."

    next_moves = []
    if len(cleaned.split()) < 70:
        next_moves.append("Add enough context to show the problem, analysis, decision, and expected outcome.")
    if missing:
        next_moves.append("Strengthen the answer with: " + ", ".join(missing[:4]) + ".")
    if not any(token in lower for token in ["because", "so that", "therefore", "which means"]):
        next_moves.append("Explain why the recommendation matters, not only what should be done.")
    if not any(char.isdigit() for char in cleaned):
        next_moves.append("Add at least one measurable threshold, timeframe, SLA, or acceptance criterion.")
    if not next_moves:
        next_moves.append("Practice delivering the same answer in 90 seconds without losing the decision or evidence.")

    return {
        "score": score,
        "level": level,
        "summary": summary,
        "covered": hits,
        "missing": missing,
        "next_moves": next_moves[:3],
        "next_task": rubric["task"],
        "source": "Built-in adaptive rubric",
    }


def external_ai_feedback(mode: str, response: str) -> str | None:
    """Call an optional OpenAI-compatible endpoint configured by environment variables.

    Required variables: AI_API_URL, AI_API_KEY, AI_MODEL. The app remains fully usable
    without them and falls back to rubric_feedback.
    """
    api_url = os.getenv("AI_API_URL", "").strip()
    api_key = os.getenv("AI_API_KEY", "").strip()
    model = os.getenv("AI_MODEL", "").strip()
    if not (api_url and api_key and model):
        return None

    prompt = (
        "You are Odyssey Coach, a financial-services product consulting trainer. "
        f"Evaluate this learner response for the skill mode '{mode}'. "
        "Give concise feedback under four headings: Strength, Risk, Improvement, Next Practice Task. "
        "Do not provide legal advice and do not claim access to proprietary Fenergo configuration.\n\n"
        f"Learner response:\n{response}"
    )
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": "Coach product consultants using practical, measurable, respectful feedback."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        api_url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response_obj:
            data = json.loads(response_obj.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, json.JSONDecodeError, TimeoutError):
        return None


def voice_coach_html(mode: str) -> str:
    keywords = COACH_RUBRICS[mode]["keywords"]
    keyword_json = json.dumps(keywords)
    safe_mode = mode.replace("'", "")
    return f"""
<!doctype html>
<html>
<head>
<style>
body {{ font-family: Arial, sans-serif; background:#07172d; color:#eef6ff; padding:18px; border-radius:14px; }}
button {{ border:0; border-radius:10px; padding:10px 14px; margin-right:8px; cursor:pointer; font-weight:700; }}
#start {{ background:#2dd4bf; color:#06211e; }} #stop {{ background:#f7c66a; color:#2b1a00; }} #speak {{ background:#9ec5ff; color:#07172d; }}
#transcript {{ min-height:92px; background:#10284b; padding:12px; border-radius:10px; margin:12px 0; line-height:1.5; }}
#feedback {{ background:#0c213e; border-left:4px solid #2dd4bf; padding:12px; border-radius:8px; }}
.small {{ color:#b7c8df; font-size:13px; }}
</style>
</head>
<body>
<h3>🎙️ Odyssey Live Voice Coach — {safe_mode}</h3>
<p class="small">Works best in Chrome or Edge. Your speech is processed by the browser speech service available on your device.</p>
<button id="start">Start listening</button><button id="stop">Stop</button><button id="speak">Speak feedback</button>
<div id="transcript">Your transcript will appear here…</div>
<div id="feedback">Speak for at least 30 seconds to receive live feedback.</div>
<script>
const keywords = {keyword_json};
let transcript = '';
let feedbackText = '';
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
function assess(text) {{
  const lower = text.toLowerCase();
  const hits = keywords.filter(k => lower.includes(k));
  const missing = keywords.filter(k => !lower.includes(k));
  const words = text.trim().split(/\\s+/).filter(Boolean).length;
  const score = Math.min(100, Math.round((hits.length / keywords.length) * 65 + Math.min(35, words / 2)));
  let level = score >= 85 ? 'Client-ready' : score >= 65 ? 'Developing consultant' : 'Practice needed';
  feedbackText = `${{level}} — score ${{score}}/100. You covered ${{hits.length ? hits.join(', ') : 'no target concepts yet'}}. ` +
    `${{missing.length ? 'Next, add ' + missing.slice(0,3).join(', ') + '.' : 'Now make the answer more concise and measurable.'}}`;
  document.getElementById('feedback').innerText = feedbackText;
}}
if (!SpeechRecognition) {{
  document.getElementById('feedback').innerText = 'Speech recognition is not available in this browser. Use the written coach below.';
  document.getElementById('start').disabled = true;
}} else {{
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';
  recognition.onresult = (event) => {{
    let interim = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {{
      const value = event.results[i][0].transcript;
      if (event.results[i].isFinal) transcript += value + ' '; else interim += value;
    }}
    document.getElementById('transcript').innerText = transcript + interim;
    assess(transcript + interim);
  }};
}}
document.getElementById('start').onclick = () => {{ transcript=''; recognition && recognition.start(); }};
document.getElementById('stop').onclick = () => {{ recognition && recognition.stop(); }};
document.getElementById('speak').onclick = () => {{
  if (!feedbackText) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(feedbackText);
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}};
</script>
</body>
</html>
"""

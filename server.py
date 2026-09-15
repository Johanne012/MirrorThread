#!/usr/bin/env python3
"""
MirrorThread v2 — AI Temporal Narrative Weaver
نظام وكلاء متعدد + ربط LLM حقيقي + تصدير + أتمتة
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import hashlib
from datetime import datetime

import config
from agents import Orchestrator
from llm_connector import enrich_with_llm
from export import export_json, export_markdown

DATA_FILE = "data/journal.json"
PORT = 8765

os.makedirs("data", exist_ok=True)
os.makedirs(config.EXPORT_DIR, exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"entries": [], "last_analysis": None}, f, ensure_ascii=False, indent=2)

orchestrator = Orchestrator()


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_analysis(entries):
    """تشغيل كل الوكلاء + إثراء LLM إن وُجد"""
    result = orchestrator.run_full_analysis(entries)
    result = enrich_with_llm(result, entries)
    return result


class MirrorHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            self.send_html(INDEX_HTML)
        elif path == "/api/entries":
            data = load_data()
            self.send_json({"entries": data.get("entries", [])})
        elif path == "/api/analyze":
            data = load_data()
            result = run_analysis(data.get("entries", []))
            data["last_analysis"] = result
            save_data(data)
            self.send_json(result)
        elif path == "/api/status":
            data = load_data()
            self.send_json({
                "entries_count": len(data.get("entries", [])),
                "llm_enabled": config.USE_REAL_LLM and bool(config.LLM_API_KEY),
                "model": config.LLM_MODEL if config.USE_REAL_LLM else "local-agents",
                "auto_analyze": config.AUTO_ANALYZE_ON_NEW_ENTRY
            })
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        if path == "/api/entries":
            data = load_data()
            content = payload.get("content", "").strip()
            if not content:
                self.send_json({"error": "المحتوى فارغ"}, 400)
                return

            entry = {
                "id": hashlib.md5(f"{datetime.now().isoformat()}{content}".encode()).hexdigest()[:10],
                "date": payload.get("date") or datetime.now().strftime("%Y-%m-%d"),
                "content": content,
                "created_at": datetime.now().isoformat()
            }
            data["entries"].append(entry)
            save_data(data)

            # Automation: auto-analyze if enough entries
            auto_result = None
            if config.AUTO_ANALYZE_ON_NEW_ENTRY and len(data["entries"]) >= config.MIN_ENTRIES_FOR_DEEP_ANALYSIS:
                auto_result = run_analysis(data["entries"])
                data["last_analysis"] = auto_result
                save_data(data)

            self.send_json({
                "success": True,
                "entry": entry,
                "auto_analyzed": auto_result is not None,
                "analysis": auto_result
            })

        elif path == "/api/export":
            data = load_data()
            entries = data.get("entries", [])
            analysis = data.get("last_analysis") or run_analysis(entries)
            fmt = payload.get("format", "markdown")

            if fmt == "json":
                path_out = export_json(analysis, entries)
            else:
                path_out = export_markdown(analysis, entries)

            self.send_json({
                "success": True,
                "file": path_out,
                "format": fmt,
                "message": f"تم التصدير بنجاح → {path_out}"
            })

        elif path == "/api/clear":
            save_data({"entries": [], "last_analysis": None})
            self.send_json({"success": True})

        else:
            self.send_error(404)


INDEX_HTML = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MirrorThread v2 — ناسج السرد الزمني</title>
  <style>
    :root {
      --bg: #0c0c10;
      --surface: #16161d;
      --surface2: #1f1f2a;
      --border: #2a2a38;
      --text: #eae8e4;
      --muted: #8b8795;
      --accent: #8b5cf6;
      --accent2: #a78bfa;
      --success: #34d399;
      --warning: #fbbf24;
      --danger: #f87171;
      --radius: 14px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      line-height: 1.65;
    }
    .container { max-width: 920px; margin: 0 auto; padding: 20px 16px 60px; }
    header {
      text-align: center;
      padding: 28px 0 20px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 28px;
    }
    header h1 {
      font-size: 1.9rem;
      font-weight: 700;
      background: linear-gradient(135deg, #8b5cf6, #c4b5fd);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    header p { color: var(--muted); font-size: 0.92rem; margin-top: 6px; }
    .status-bar {
      display: flex;
      gap: 10px;
      justify-content: center;
      flex-wrap: wrap;
      margin-top: 14px;
    }
    .pill {
      font-size: 0.75rem;
      padding: 4px 12px;
      border-radius: 20px;
      background: var(--surface2);
      border: 1px solid var(--border);
      color: var(--muted);
    }
    .pill.on { color: var(--success); border-color: #065f46; }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 18px;
    }
    .card h2 { font-size: 1.05rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    textarea, input[type="date"] {
      width: 100%;
      background: var(--surface2);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 10px;
      padding: 12px;
      font-size: 0.98rem;
      font-family: inherit;
      resize: vertical;
    }
    textarea:focus, input:focus { outline: none; border-color: var(--accent); }
    .btn {
      background: var(--accent);
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 0.92rem;
      cursor: pointer;
      font-weight: 600;
      transition: opacity .15s;
    }
    .btn:hover { opacity: .88; }
    .btn:disabled { opacity: .45; cursor: not-allowed; }
    .btn-secondary { background: var(--surface2); border: 1px solid var(--border); color: var(--text); }
    .btn-danger { background: var(--danger); }
    .btn-success { background: #059669; }
    .actions { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
    .tabs { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
    .tab {
      padding: 8px 16px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 22px;
      cursor: pointer;
      font-size: 0.88rem;
      color: var(--muted);
    }
    .tab.active { background: var(--accent); color: #fff; border-color: var(--accent); }
    .panel { display: none; }
    .panel.active { display: block; }
    .entry {
      background: var(--surface2);
      border-radius: 10px;
      padding: 14px;
      margin-bottom: 10px;
      border-right: 3px solid var(--accent);
    }
    .entry .date { font-size: 0.78rem; color: var(--muted); margin-bottom: 5px; }
    .thread {
      background: var(--surface2);
      border-radius: 10px;
      padding: 15px;
      margin-bottom: 11px;
      border-right: 3px solid var(--accent2);
    }
    .thread .meta { font-size: 0.82rem; color: var(--muted); margin-top: 5px; }
    .trend-rising { color: #34d399; }
    .trend-falling { color: #f87171; }
    .trend-stable { color: var(--muted); }
    .future-msg {
      background: linear-gradient(135deg, #1e1b4b, #2e1065);
      border: 1px solid #5b21b6;
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 12px;
      position: relative;
    }
    .future-msg .from { font-size: 0.78rem; color: var(--accent2); margin-bottom: 7px; font-weight: 600; }
    .continuity {
      background: var(--surface2);
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 8px;
      border-right: 3px solid var(--warning);
      font-size: 0.92rem;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }
    .stat {
      background: var(--surface2);
      border-radius: 10px;
      padding: 12px;
      text-align: center;
    }
    .stat .num { font-size: 1.45rem; font-weight: 700; color: var(--accent2); }
    .stat .label { font-size: 0.75rem; color: var(--muted); }
    .empty { color: var(--muted); text-align: center; padding: 28px; }
    .llm-box {
      background: #0f172a;
      border: 1px solid #1e3a5f;
      border-radius: 12px;
      padding: 16px;
      margin-top: 12px;
      white-space: pre-wrap;
      font-size: 0.92rem;
    }
    footer {
      text-align: center;
      padding: 24px 0 10px;
      color: var(--muted);
      font-size: 0.78rem;
      border-top: 1px solid var(--border);
      margin-top: 36px;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>MirrorThread v2</h1>
      <p>ناسج السرد الزمني · نظام وكلاء متعدد + أنماط زمنية</p>
      <div class="status-bar" id="status-bar">
        <span class="pill" id="pill-entries">— مذكرات</span>
        <span class="pill" id="pill-llm">LLM: محلي</span>
        <span class="pill" id="pill-auto">أتمتة: —</span>
      </div>
    </header>

    <div class="tabs">
      <div class="tab active" data-tab="write">✍️ كتابة</div>
      <div class="tab" data-tab="entries">📜 المذكرات</div>
      <div class="tab" data-tab="analyze">🔮 التحليل</div>
      <div class="tab" data-tab="export">📤 تصدير</div>
    </div>

    <!-- WRITE -->
    <div class="panel active" id="panel-write">
      <div class="card">
        <h2>أضف ملاحظة أو ذكرى</h2>
        <p style="color:var(--muted);font-size:0.88rem;margin-bottom:12px">
          اكتب بأي تاريخ. النظام يكتشف الخيوط والأنماط تلقائيًا عند وجود بيانات كافية.
        </p>
        <input type="date" id="entry-date" style="margin-bottom:10px" />
        <textarea id="entry-content" rows="5" placeholder="اليوم شعرت بـ... قررت أن... تذكرت عندما..."></textarea>
        <div class="actions">
          <button class="btn" onclick="addEntry()">حفظ الملاحظة</button>
        </div>
        <div id="auto-msg" style="margin-top:12px;font-size:0.85rem;color:var(--success);display:none"></div>
      </div>
    </div>

    <!-- ENTRIES -->
    <div class="panel" id="panel-entries">
      <div class="card">
        <h2>سجل المذكرات</h2>
        <div id="entries-list" class="empty">لا توجد مذكرات بعد.</div>
        <div class="actions" style="margin-top:14px">
          <button class="btn btn-danger" onclick="clearAll()">مسح الكل</button>
        </div>
      </div>
    </div>

    <!-- ANALYZE -->
    <div class="panel" id="panel-analyze">
      <div class="card">
        <h2>التحليل الزمني متعدد الوكلاء</h2>
        <p style="color:var(--muted);font-size:0.88rem;margin-bottom:14px">
          ThemeAgent → EmotionAgent → NarrativeAgent → FutureSelfAgent
        </p>
        <button class="btn" id="analyze-btn" onclick="runAnalysis()">تشغيل التحليل الكامل</button>
      </div>
      <div id="analysis-results" style="display:none">
        <div class="stats" id="stats"></div>
        <div class="card"><h2>🧵 الخيوط الزمنية</h2><div id="threads-list"></div></div>
        <div class="card"><h2>🔗 روابط العاطفة ↔ الموضوع</h2><div id="links-list"></div></div>
        <div class="card"><h2>✦ رسائل الذات المستقبلية</h2><div id="future-msgs"></div></div>
        <div class="card"><h2>📌 نقاط الاستمرارية</h2><div id="continuity-list"></div></div>
        <div class="card"><h2>📖 فصول الحياة</h2><div id="chapters-list"></div></div>
        <div class="card" id="llm-card" style="display:none"><h2>🧠 رؤية الـLLM</h2><div class="llm-box" id="llm-insight"></div></div>
      </div>
    </div>

    <!-- EXPORT -->
    <div class="panel" id="panel-export">
      <div class="card">
        <h2>تصدير التقرير</h2>
        <p style="color:var(--muted);font-size:0.88rem;margin-bottom:14px">
          صدّر التحليل + المذكرات كملف Markdown أو JSON.
        </p>
        <div class="actions">
          <button class="btn btn-success" onclick="doExport('markdown')">تصدير Markdown</button>
          <button class="btn btn-secondary" onclick="doExport('json')">تصدير JSON</button>
        </div>
        <div id="export-result" style="margin-top:14px;font-size:0.9rem;color:var(--success);display:none"></div>
      </div>
    </div>

    <footer>
      MirrorThread v2 · وكلاء متخصصون + اكتشاف أنماط زمنية + أتمتة + تصدير<br>
      الربط الحقيقي بالـLLM جاهز عبر config.py
    </footer>
  </div>

  <script>
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById('panel-' + tab.dataset.tab).classList.add('active');
        if (tab.dataset.tab === 'entries') loadEntries();
      });
    });

    document.getElementById('entry-date').valueAsDate = new Date();
    loadStatus();

    async function loadStatus() {
      try {
        const r = await fetch('/api/status');
        const s = await r.json();
        document.getElementById('pill-entries').textContent = s.entries_count + ' مذكرات';
        const llm = document.getElementById('pill-llm');
        if (s.llm_enabled) {
          llm.textContent = 'LLM: ' + s.model;
          llm.classList.add('on');
        } else {
          llm.textContent = 'LLM: وكلاء محليين';
        }
        document.getElementById('pill-auto').textContent = 'أتمتة: ' + (s.auto_analyze ? 'مفعّلة' : 'متوقفة');
      } catch(e) {}
    }

    async function addEntry() {
      const content = document.getElementById('entry-content').value.trim();
      const date = document.getElementById('entry-date').value;
      if (!content) return alert('اكتب شيئًا أولًا');
      const res = await fetch('/api/entries', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ content, date })
      });
      const data = await res.json();
      if (data.success) {
        document.getElementById('entry-content').value = '';
        const msg = document.getElementById('auto-msg');
        if (data.auto_analyzed) {
          msg.style.display = 'block';
          msg.textContent = '✓ تم الحفظ + تحليل تلقائي بواسطة الوكلاء';
          renderAnalysis(data.analysis);
        } else {
          msg.style.display = 'block';
          msg.textContent = '✓ تم الحفظ';
        }
        loadStatus();
      } else alert(data.error || 'خطأ');
    }

    async function loadEntries() {
      const res = await fetch('/api/entries');
      const data = await res.json();
      const list = document.getElementById('entries-list');
      if (!data.entries?.length) {
        list.innerHTML = '<div class="empty">لا توجد مذكرات بعد.</div>';
        return;
      }
      list.innerHTML = data.entries
        .sort((a,b) => b.date.localeCompare(a.date))
        .map(e => `<div class="entry"><div class="date">${e.date}</div><div>${esc(e.content)}</div></div>`)
        .join('');
    }

    async function runAnalysis() {
      const btn = document.getElementById('analyze-btn');
      btn.disabled = true;
      btn.textContent = 'الوكلاء يعملون...';
      const res = await fetch('/api/analyze');
      const data = await res.json();
      btn.disabled = false;
      btn.textContent = 'إعادة التحليل الكامل';
      renderAnalysis(data);
      loadStatus();
    }

    function renderAnalysis(data) {
      document.getElementById('analysis-results').style.display = 'block';

      document.getElementById('stats').innerHTML = `
        <div class="stat"><div class="num">${data.threads?.length||0}</div><div class="label">خيوط</div></div>
        <div class="stat"><div class="num">${data.patterns?.length||0}</div><div class="label">أنماط</div></div>
        <div class="stat"><div class="num">${data.emotion_theme_links?.length||0}</div><div class="label">روابط</div></div>
        <div class="stat"><div class="num">${data.future_messages?.length||0}</div><div class="label">رسائل</div></div>
        <div class="stat"><div class="num">${data.continuity_points?.length||0}</div><div class="label">استمرارية</div></div>
        <div class="stat"><div class="num">${data.life_chapters?.length||0}</div><div class="label">فصول</div></div>
      `;

      // Threads
      const th = document.getElementById('threads-list');
      if (!data.threads?.length) th.innerHTML = '<div class="empty">أضف مذكرات بتواريخ مختلفة.</div>';
      else th.innerHTML = data.threads.map(t => {
        const trendCls = 'trend-' + (t.trend||'stable');
        const trendAr = {rising:'تصاعد ↗',falling:'انحسار ↘',stable:'مستقر →'}[t.trend] || '';
        return `<div class="thread">
          <strong>${t.theme}</strong>
          <div class="meta">${t.occurrences} مرات · ${t.first_seen} → ${t.last_seen} · قوة ${t.strength}
            <span class="${trendCls}"> · ${trendAr}</span>
          </div>
          ${t.samples?.length ? '<div style="margin-top:8px;font-size:0.88rem;color:var(--muted)">' +
            t.samples.slice(0,3).map(s => '« '+esc(s)+' »').join('<br>') + '</div>' : ''}
        </div>`;
      }).join('');

      // Links
      const lk = document.getElementById('links-list');
      if (!data.emotion_theme_links?.length) lk.innerHTML = '<div class="empty">لا روابط بعد.</div>';
      else lk.innerHTML = data.emotion_theme_links.map(l =>
        `<div class="continuity">${esc(l.insight)}</div>`).join('');

      // Future
      const fm = document.getElementById('future-msgs');
      if (!data.future_messages?.length) fm.innerHTML = '<div class="empty">—</div>';
      else fm.innerHTML = data.future_messages.map(m =>
        `<div class="future-msg"><div class="from">${m.from} · ${m.based_on}</div>${esc(m.message)}</div>`
      ).join('');

      // Continuity
      const cp = document.getElementById('continuity-list');
      if (!data.continuity_points?.length) cp.innerHTML = '<div class="empty">—</div>';
      else cp.innerHTML = data.continuity_points.map(c =>
        `<div class="continuity"><strong>${c.type}</strong> (${c.theme}): ${esc(c.advice)}</div>`
      ).join('');

      // Chapters
      const ch = document.getElementById('chapters-list');
      if (!data.life_chapters?.length) ch.innerHTML = '<div class="empty">—</div>';
      else ch.innerHTML = data.life_chapters.map(c =>
        `<div class="thread"><strong>${c.title}</strong>
         <div class="meta">${c.start} → ${c.end} · ${c.entry_count} ملاحظات</div></div>`
      ).join('');

      // LLM
      if (data.llm_enriched && data.llm_insight) {
        document.getElementById('llm-card').style.display = 'block';
        document.getElementById('llm-insight').textContent = data.llm_insight;
      } else {
        document.getElementById('llm-card').style.display = 'none';
      }
    }

    async function doExport(fmt) {
      const res = await fetch('/api/export', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ format: fmt })
      });
      const data = await res.json();
      const el = document.getElementById('export-result');
      el.style.display = 'block';
      el.textContent = data.message || (data.success ? 'تم التصدير' : 'فشل');
    }

    async function clearAll() {
      if (!confirm('مسح كل المذكرات؟')) return;
      await fetch('/api/clear', { method: 'POST' });
      loadEntries();
      loadStatus();
      document.getElementById('analysis-results').style.display = 'none';
    }

    function esc(t) {
      const d = document.createElement('div');
      d.textContent = t || '';
      return d.innerHTML;
    }
  </script>
</body>
</html>
'''


if __name__ == "__main__":
    print("=" * 56)
    print("  MirrorThread v2 — AI Temporal Narrative Weaver")
    print("  وكلاء متخصصون + أنماط + أتمتة + تصدير + LLM")
    print("=" * 56)
    print(f"\n  → http://localhost:{PORT}")
    print(f"  LLM مفعّل: {config.USE_REAL_LLM and bool(config.LLM_API_KEY)}")
    print("  اضغط Ctrl+C للإيقاف\n")
    server = HTTPServer(("0.0.0.0", PORT), MirrorHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nتم الإيقاف.")
        server.server_close()

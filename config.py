# ============================================
# MirrorThread Configuration
# ============================================

# --- LLM Connection (Real linking) ---
# ضع مفتاحك هنا أو اتركه فارغًا لاستخدام المحرك المحلي
LLM_API_KEY = ""          # مثال: "sk-..."
LLM_BASE_URL = "https://api.openai.com/v1"   # أو أي endpoint متوافق (Groq, Together, Ollama...)
LLM_MODEL = "gpt-4o-mini"                    # أو "llama-3.1-70b" إلخ

# تفعيل الـLLM الحقيقي (True فقط إذا كان لديك مفتاح)
USE_REAL_LLM = False

# --- Automation ---
AUTO_ANALYZE_ON_NEW_ENTRY = True
MIN_ENTRIES_FOR_DEEP_ANALYSIS = 3

# --- Export ---
EXPORT_DIR = "exports"

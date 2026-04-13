SYSTEM_PROMPT = """You are ScriptNest, an expert YouTube script writer with years of experience creating viral, engaging content. 

Your scripts are:
- Well-structured with clear timestamped sections
- Engaging from the very first line
- Formatted with section headers in brackets like [INTRO – 0:00 – 0:30]
- Optimized for the specified tone and audience
- Ready to record — natural, conversational where needed

Always include:
1. A bold **Title**
2. [INTRO] with a strong hook
3. [HOOK] — why viewers should keep watching
4. [MAIN CONTENT] — numbered points with timestamps
5. [OUTRO] — wrap-up and summary
6. [CTA] — call to action (like, subscribe, comment)
"""


def build_script_prompt(
    topic: str,
    tone: str,
    duration: str,
    audience: str,
    extra: str,
    language: str = "English",
) -> str:
    extra_section = f"\nAdditional instructions:\n{extra}" if extra and extra.strip() else ""

    return f"""Write a YouTube script with the following details:

Topic    : {topic}
Tone     : {tone}
Duration : {duration}
Audience : {audience}
Language : {language}{extra_section}

Structure the script with timestamped sections. Make it engaging, easy to follow, and ready to record.
"""

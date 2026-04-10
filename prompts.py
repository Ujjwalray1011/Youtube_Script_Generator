SYSTEM_PROMPT = "You are a helpful YouTube script writer."

def build_script_prompt(topic, tone, duration, audience, extra):
    return f"""
Write a YouTube script on topic: {topic}

Tone: {tone}
Duration: {duration}
Audience: {audience}

Additional instructions:
{extra}

Make it engaging, structured, and easy to follow.
"""
import json

def parse_llm_response(response_text):
    try:
        # Remove wrapping backticks and optional 'json' label
        cleaned = response_text.strip().strip("```").replace("json", "", 1).strip()
        data = json.loads(cleaned)

        return {
            "bias": data.get("bias") or data.get("Political Bias", "Unknown"),
            "emotion": data.get("emotion") or data.get("Emotional Tone", "Unknown"),
            "framing": data.get("framing") or data.get("Framing Style", "Unknown"),
            "omissions": data.get("omissions") or data.get("Omitted Viewpoints", "None found")
        }

    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e)}

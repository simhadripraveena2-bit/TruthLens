import requests
import json
import re


def analyze_text(text: str) -> dict:
    prompt = f"""Return ONLY a JSON object. No explanation. No markdown. Just JSON.

Text: {text}

JSON format:
{{
  "trust_score": 75,
  "overall_verdict": "one sentence summary",
  "sentences": [
    {{
      "text": "first sentence from text",
      "risk_level": "green",
      "explanation": "reason"
    }},
    {{
      "text": "second sentence from text",
      "risk_level": "red",
      "explanation": "reason"
    }}
  ]
}}

risk_level must be: green (accurate), yellow (uncertain), or red (hallucination/false)
Split the input into sentences. Analyze each one. Return ONLY the JSON."""

    try:
        print("Sending request to Ollama...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:4b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 2048,
                    "keep_alive": "10m"
                }
            },
            timeout=120
        )

        response.raise_for_status()
        raw = response.json().get("response", "")
        print("RAW GEMMA RESPONSE:", raw[:1000])

        # Clean response
        cleaned = raw.strip()
        cleaned = re.sub(r'```json\s*', '', cleaned)
        cleaned = re.sub(r'```\s*', '', cleaned)
        cleaned = cleaned.strip()

        # Extract JSON
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group()
        else:
            print("NO JSON FOUND:", cleaned)
            raise ValueError("No JSON found in response")

        result = json.loads(cleaned)

        # Validate
        if "sentences" not in result or not isinstance(result["sentences"], list):
            raise ValueError("Missing sentences in response")
        if "trust_score" not in result:
            result["trust_score"] = 50
        if "overall_verdict" not in result:
            result["overall_verdict"] = "Analysis complete."

        # Fix any invalid risk levels
        for s in result["sentences"]:
            if s.get("risk_level") not in ["green", "yellow", "red"]:
                s["risk_level"] = "yellow"

        print(f"SUCCESS: {len(result['sentences'])} sentences analyzed")
        return result

    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to Ollama. Make sure Ollama is running.")

    except json.JSONDecodeError as e:
        print("JSON PARSE ERROR:", str(e))
        print("CLEANED TEXT:", cleaned[:500])
        raise Exception(f"Invalid JSON from Gemma: {str(e)}")

    except Exception as e:
        print("ANALYZER ERROR:", str(e))
        raise
"""
groq_baseline.py — Local prompt tester for TakeMeter

Use this to test your Groq classification prompt on a few posts before going to Colab.
This is for PROMPT DEVELOPMENT only.

The full test-set baseline runs in the Colab notebook (Section 5),
which guarantees both models use the same test split.

Setup:
  1. Make sure .env exists in the project root with GROQ_API_KEY=your_key
  2. Install: pip install groq python-dotenv
  3. Edit test_posts below, then run: python baseline/groq_baseline.py
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- Label definitions (copy these into Colab Section 5 prompt too) ---
LABEL_DEFINITIONS = """
You are classifying r/soccer posts. Assign exactly one label.

--- LABELS ---

analysis
The post makes a claim and then EXPLAINS why. The explanation can be:
- a specific fact or stat ("since 2000 Australia beat NZ 12 out of 13 times")
- a causal reason ("players stop responding to him because his style is physically taxing")
- a tactical observation ("he plays Simeone on the left but his strength is runs from the right")
- a historical comparison ("they did the same rule change at the 2018 WC and forgot it soon")
Key: the post says WHY, not just WHAT.

hot_take
A strong opinion, reaction, or prediction with NO explanation.
The post just asserts — it does not explain why.
Examples: "this player is awful", "they're getting grouped", "best game of the tournament",
"he should retire immediately".
Key: if you removed the claim, there is nothing left.

question
The post is genuinely asking for information, clarification, or predictions.
It wants an answer. NOT a rhetorical question used to express an opinion.
Examples: "Is he starting the World Cup?", "Where can I watch this?", "Why was that offside?"

--- DECISION RULES ---
1. If a post starts with a bold opinion but then explains WHY in the next sentence → analysis.
2. If a post has a bold opinion and the "reason" just repeats the opinion in other words → hot_take.
3. "Who says no?" or "Am I wrong?" used rhetorically → hot_take.
4. A real question seeking information → question.

--- EXAMPLES ---
"The Bielsa cycle is truly inevitable. At a certain point players stop responding to him and his style is too physically taxing." → analysis (explains the mechanism)
"Bielsa is the most overrated manager on the planet." → hot_take (assertion only)
"Is Unai Simon starting GK for the World Cup?" → question

Respond with ONLY the label: analysis, hot_take, or question. No other words.
"""
# -----------------------------------------------------------------------


def classify(post_text: str) -> str:
    prompt = f"""{LABEL_DEFINITIONS.strip()}

Post: {post_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip().lower()


if __name__ == "__main__":
    # Edit these to test your prompt on real posts
    test_posts = [
        "The Bielsa cycle is truly inevitable. He can be great if rigid tactically but at a certain point players stop responding to him. It also doesn't help that his style is so taxing physically",
        "Muslera should not play a single minute of football after this match. The whole country knows he's finished except Bielsa",
        "Is Unai Simon starting GK for the World Cup?",
    ]

    print("=" * 60)
    for i, post in enumerate(test_posts, 1):
        label = classify(post)
        preview = post[:80] + ("..." if len(post) > 80 else "")
        print(f"Post {i}: {preview}")
        print(f"Label:  {label}")
        print("-" * 60)

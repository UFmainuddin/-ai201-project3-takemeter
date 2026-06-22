# TakeMeter — Planning

## Community

I chose r/soccer, the largest English-language soccer discussion community on Reddit.
It has over 4 million members and is active every day, especially during World Cup 2026.

This community is a good fit for classification because its discourse varies enormously.
In a single thread you can find detailed tactical arguments, emotional fan reactions, and
genuine questions — often within three replies of each other. That variety makes the
labeling task interesting and the classifier genuinely useful.

The distinction I am measuring matters to people in this community. Regular users often
complain that threads are full of "low effort" posts and celebrate when someone makes
a substantive point. The difference between explaining *why* something happened versus
just asserting it is something r/soccer readers notice and value.

---

## Labels

### `analysis`
The post makes a claim AND supports it with at least one specific reason, statistic,
historical comparison, or tactical observation. You could remove the opinion framing
and the reasoning would still stand on its own.

**Example 1:**
"The Bielsa cycle is truly inevitable. He can be great if rigid tactically but at a certain
point players stop responding to him. It also doesn't help that his style is so taxing physically"

**Example 2:**
"For Galatasaray and Fenerbahce specifically, their revenue-to-wage ranks are comparable
to clubs around the same financial level. Like for the 2024-25 season, Gala had the 21st
highest revenue and Fener were 28th, in the wage bill table Gala were 25th."

---

### `hot_take`
A bold or confident opinion or reaction stated without supporting reasoning.
The post asserts rather than argues. Includes predictions, strong opinions, and
emotional reactions where no reasoning is provided.

**Example 1:**
"Belgium was really handed the easiest group with crappiest teams and the easiest route
to the QF but decided to eat crayons instead"

**Example 2:**
"Muslera should not play a single minute of football after this match, for club or country.
Should retire as soon as possible. The whole country knows he's finished except Bielsa"

---

### `question`
The post's primary function is to ask for information, clarification, or opinions from
other users. The main structure is a genuine question seeking an answer.

**Example 1:**
"Can anyone explain how Turkish clubs can offer such massive wages to players?
It's always puzzled me no disrespect to the clubs or their fans"

**Example 2:**
"Given that turkey lost to Australia, does that mean if Aus loses to Paraguay
they'll still go through?"

---

## Hard Edge Cases

**The main hard case: bold opinion + one sentence of reasoning.**

Example:
"I get that it's because most people don't watch their games but it's still mad that
they treat this as a massive upset, Uruguay is horrendous and Cape Verde are
clearly not that bad."

This could be `hot_take` (confident opinion) or `analysis` (has a reason).

**Decision rule:** If the supporting sentence is a specific, verifiable fact or a
logical chain that could stand alone — label it `analysis`. If the support just
restates the opinion in different words or is too thin to stand on its own —
label it `hot_take`. The example above is `hot_take` because "most people
don't watch their games" is vague and does not actually support the claim.

**The second hard case: rhetorical questions.**

Example: "Spain finishes 2nd and KO's Argentina in the round of 32, who says no?"

This looks like a question but it is really expressing a bold opinion. If the post
is making a statement and the question mark is rhetorical — label it `hot_take`.
Only label a post `question` if it genuinely seeks information or an answer.

**Difficult examples documented during annotation (added as found):**

1. "This World Cup is a signal for me to reset my presumptions about many footballing
countries because many of them are not what they're known for 10 and 20 years ago.
Germany's pressing is meh, Brazil's technique is just standard..." — This is borderline.
It starts as a hot_take but lists specific country observations. Decision: `hot_take`
because none of the observations are backed by data, only personal impression.

2. "Booing the commercial breaks needs to be normalized. I think England did it first
during their game? Either way, good." — Starts as a strong opinion, ends with an
uncertain factual claim ("I think England did it first?"). The dominant function is
expressing an opinion. Decision: `hot_take`.

3. "I'm not a huge fan of the format with most of the 3rd place teams going through
but I love the inclusion of more nations that might not have made it otherwise." —
Makes a nuanced trade-off observation but no supporting data. Decision: `hot_take`.

---

## Data Collection Plan

**Source:** r/soccer Daily Discussion threads and match threads during World Cup 2026.
All posts are public.

**Method:** Save thread pages as PDFs and extract comment text manually.
No scraping tools needed.

**Target distribution:** ~70 examples per label (roughly equal thirds).

**Collection order:**
- Daily Discussion thread (June 21 2026): ~70-80 examples collected already
- 1-2 match threads for variety in topics and post style
- Transfer discussion thread if questions are underrepresented

**If a label is underrepresented after 200 examples:**
Go back to Reddit and look specifically for that type.
For more `question` examples: look in threads where fans ask for predictions or
rules clarification. For more `analysis` examples: look in tactical post threads.

**Label balance check:** After every 50 examples, count each label.
If any label is above 70% of all examples so far, stop and collect more of the others.

---

## Evaluation Metrics

I will report:
- **Overall accuracy:** percentage of test examples the model classified correctly
- **Per-class F1:** for each of the 3 labels (analysis, hot_take, question)
- **Confusion matrix:** to show which label pairs the model confuses most

**Why not accuracy alone:**
Accuracy hides imbalance problems. If 50% of my test set is `hot_take` and the model
predicts `hot_take` for everything, accuracy is 50% — which looks okay but the model
learned nothing. Per-class F1 shows this failure immediately because `analysis` and
`question` F1 would be 0.

**Why F1 over just precision or recall:**
F1 is the harmonic mean of both. For this task I care equally about not missing a
label (recall) and not mislabeling other things as that label (precision). F1 captures both.

---

## Definition of Success

**Minimum acceptable performance for this project:**
- Overall test accuracy ≥ 65% (random chance for 3 classes = 33%)
- Per-class F1 ≥ 0.50 for all 3 labels
- Fine-tuned model clearly beats the Groq zero-shot baseline

**"Good enough for deployment" in a real community tool:**
- Overall accuracy ≥ 72%
- No single label's F1 below 0.60
- Confusion matrix shows no single pair of labels causing most errors

**If fine-tuned model does not beat baseline:**
I will check for label leakage first, then class imbalance, then annotation consistency.
I will not call the project a success unless the fine-tuned model outperforms zero-shot.

---

## AI Tool Plan

### 1. Label stress-testing
I will give Claude my 3 label definitions and ask it to generate 10 posts that sit at the
boundary between `analysis` and `hot_take` — the hardest pair to distinguish.
If it produces posts I cannot cleanly label, I will tighten the definition before
annotating 200 examples. This is done before data collection begins.

### 2. Annotation assistance
I will NOT use an LLM to pre-label examples. I will label all 200 examples myself.
This keeps the annotation consistent with my own decision rules and avoids
introducing LLM bias into the training labels.

### 3. Failure analysis
After training, I will paste my list of wrong predictions into Claude and ask it to
identify any common patterns — for example: "does the model consistently confuse
short `analysis` comments with `hot_take`?" or "does it fail on sarcastic posts?"
I will then verify the patterns myself by re-reading those examples before writing
my evaluation report. I will note what patterns I found AND what I had to discard
as incorrect.

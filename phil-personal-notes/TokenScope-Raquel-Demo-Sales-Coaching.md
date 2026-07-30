# TokenScope / Raquel — Demo Sales Coaching

**For:** Phil (Toronto)  
**Purpose:** Personal playbook for remote 5-minute demos, outreach, and explaining tokens  
**Brand rule:** This is **not** Life But Wrong. TokenScope / Raquel / Pinkhouse only.  
**Status:** Working notes — revise as the demo hardens  

---

## 1. The lead line (use this, not “sixth technique”)

**Don’t lead with:** “We’re a sixth compression technique…”

**Do lead with:**

> Plug this in front of the model call. Same meaning out. Fewer tokens. Here’s the receipt.

The product story is a **plug**: insert here → traffic goes through normal internet wires → measurable win comes out.

---

## 2. What you’re actually selling on call 1

Not a platform tour. Not the patent. Not trillions.

You’re doing **discovery + proof**:

1. Reach someone who burns LLM tokens  
2. Show the plug once (browser demo)  
3. Leave a before/after receipt  
4. Ask for one next step (engineer look / second call / trial)

Five minutes can win attention. Closing usually needs one follow-up with their technical person.

---

## 3. Who to call (types of people)

Tokens are not something people carry in their pocket. The people who care are people who **see a bill measured in tokens** (or “API usage,” “LLM spend,” “model cost”).

### Good targets
- AI product founders / CTOs with apps in production  
- FinOps / cloud cost owners watching Anthropic, OpenAI, Google, etc.  
- Agency or consultancy leads running many LLM calls for clients  
- Platform teams whose margin gets eaten by token spend  

### Weak targets (skip for now)
- “AI curious” people with no bill  
- Life But Wrong / merch / fun audiences  
- Anyone who only chats casually with ChatGPT and never sees usage cost  

### How to recognize them in one question
> “Are you paying for LLM tokens in production, or mostly experimenting?”

- **Production / real bill** → lean in  
- **Experimenting only** → short polite demo, no hard sell  

---

## 4. What a token actually is (plain language)

Your instincts are close. Here’s a clean way to hold it:

### Tokens are not
- Peanuts you toss on the ground  
- Salmon swimming upstream  
- Physical chips in a pocket  
- “Nothing” in the sense of fake — the **bill is real**

### Tokens are
A **billing and length unit** for model text (and sometimes other model I/O).

Roughly:
- The model doesn’t charge you by the English “word” in a simple way  
- It chops text into pieces called **tokens** (a word might be one token; a long/weird word might be more; other languages differ)  
- Providers price **per million tokens** (input and output often priced differently)  

### “Are they paying for electricity measured in tokens?”
**Reasonable enough for a first mental model — with one refinement:**

They’re paying the **provider’s price for running the model** (compute, energy, capacity, margin). The provider **meters** that work in tokens because tokens are a practical ruler for “how much text went in and came out.”

So:
- **Underlying cost driver:** compute / capacity (yes, electricity is in there)  
- **Invoice unit:** tokens  
- **Your plug’s job:** same useful meaning, **fewer tokens on the meter** → lower bill (or more work per dollar)

For a NY buyer you can say:

> “You’re not buying magic beans. You’re buying model work. They measure that work in tokens. We reduce how many tokens that same job needs.”

That’s enough. Don’t over-explain on call 1.

---

## 5. The remote demo (Toronto → New York or anywhere)

### Is it “general wires”?
**Yes.** Same internet as email or a normal website: HTTPS in, HTTPS out. No special private line.

### Demo vs test
- It **looks** like a demo  
- It **is** a real measurement on a clean sample: tokens in, tokens out, fidelity check  
- It will feel “dinky” next to billions/trillions of tokens — that’s OK  

### Why small is OK
Nobody puts the production firehose through a stranger’s box on day one.

Call story:
1. **This sample** — counts both ends, fidelity check  
2. **Same pipe** — normal wires  
3. **Scale later** — their engineers put the plug on real traffic; TokenScope shows the big dial  

Line to use:

> “Same measurement you’ll use at scale. Today’s a clean sample. We don’t fake the volume.”

### What they can / can’t see
| They can see | They can’t see (and don’t need to on call 1) |
|---|---|
| Input token count | Exact internal method / secret sauce |
| Output token count | “Inside” the compressor |
| That meaning/fidelity held (per your checks) | Patent deep-dive |

They prove **effect**. You keep **method**. Engineers dig deeper only if the effect is worth it.

---

## 6. Outreach blurb (copy/paste)

> I’m Phil in Toronto. We have a plug that sits in front of the model call and cuts tokens while keeping meaning. Got 5 minutes for a live demo in your browser? If it’s not useful, we’re done.

Warm intro: same text, mention who connected you.  
Cold (LinkedIn / email / DM): same text, one ask only.

---

## 7. Five-minute call script

### 0:00–0:30 — Frame
“I’m not doing a platform tour. One demo: text in, fewer tokens out, you can see both counts.”

### 0:30–1:00 — Qualify
“Roughly — are you paying for LLM tokens in production, or mostly experimenting?”

### 1:00–3:30 — Demo
- They open the link on **their** machine  
- Paste their sample **or** your canned sample  
- Show: tokens before → after → fidelity check  
- Say the “same meter at scale” line  

### 3:30–4:30 — Meaning
“You’re not buying a mystery model. You’re inserting a customer-side plug. Rip it out anytime.”

### 4:30–5:00 — Ask (pick one)
- “Can I send this receipt to your engineer?”  
- “Worth 20 minutes with whoever owns the API bill?”  
- “Want a trial key on Pinkhouse?”

Then **stop talking**.

### Do not say on call 1
- “Sixth compression technique…” as the opener  
- World-scale trillions as the pitch  
- Patent deep-dive  
- Secret sauce details  
- Long TokenScope card tour  

---

## 8. Same-day follow-up (4 lines)

> Thanks for the 5 minutes.  
> Attached: before/after token counts from the demo.  
> Next step I’d suggest: 20 minutes with your engineer on your own sample.  
> Here’s the link when you’re ready.

---

## 9. Weekly cadence (headache-friendly)

- Goal: **3–5 demos a week**, not 50  
- Same script every time  
- Track only: talked / demoed / asked for engineer / yes–no  
- Bad headache day → send link + short recorded walkthrough; skip live voice  

---

## 10. Patent / “why buy from me?” (keep in your pocket)

Two paths, same plug:

| Path | What you sell | Likely zone |
|---|---|---|
| Product (Pinkhouse / TokenScope) | Software + demo + Stripe | Customer savings → ~million-happy |
| IP (patent / paper) | License or sale | After proof + clear ownership → bigger checks |

Buyers don’t buy “an idea.” They buy **risk reduction**: patented (or patent-pending), proven, cheaper than inventing around you.

Your advantage to remember (say later, not first):
- Other compressions may live deeper in the stack  
- You’re **closest to the customer’s nose / screen** — customer-controlled, tryable, removable  

---

## 11. Pre-launch discipline (reminder)

- Keep Life But Wrong completely separate  
- Before launch: take down imperfect cards / anything not ready  
- Cosmetics matter (colors, labels, phone-friendly)  
- Demo door is fine; secret sauce stays out of the shipped client  
- Login ready; APIs when you can place keys cleanly  

---

## 12. Sticky-note version

1. Plug in front of the model call.  
2. Fewer tokens. Same meaning. Receipt.  
3. Call people with a real token bill.  
4. 5-minute browser proof over normal internet.  
5. Ask for the engineer / second call.  
6. Small sample first. Scale later.  
7. Effect visible. Method private.  

---

## 13. Installation & Phil’s personal level of effort

### Short answer
You do **not** walk in with chips. You do **not** put a laptop under a Rogers desk.  
Early company: customers usually **call out to your cloud** (e.g. DigitalOcean). Later, big accounts may ask you to run **inside their cloud**. Either way it’s software + config + watching — not hardware in your pockets.

### DNS vs API (plain language)
- **DNS** = the *name* of a place on the internet (`api.pinkhouse.com` → some machine’s address). Like a phonebook entry.  
- **API** = the *door and the language* for talking to that place (URLs, keys, JSON). Like the conversation rules once you dial the number.  

You need both in practice: a name (DNS) that points at your service, and an API so their systems can send/receive traffic.

### Where does “Rosetta Stone” live?
**On your shrink service (the plug) — not inside Anthropic/Claude.**

Flow for one call:

1. **Rogers app** → sends normal text/job to **your plug** (Pinkhouse / Raquel gateway on DigitalOcean or in their VPC).  
2. **Your server** (Rosetta / encoder): count before → shrink → count after → log savings.  
3. **Your server** → forwards the *shrunk* payload to **Anthropic**.  
4. Anthropic answers.  
5. If needed, **your server** decodes/reshapes the answer back for Rogers.  
6. Rogers gets the result; TokenScope shows before/after.

So “server side” here means **the Raquel plug’s servers** (yours or hosted for them) — **between** Rogers and Anthropic.  
Anthropic does **not** run your Rosetta. Rogers does **not** have to understand Rosetta if they only talk to your API.

“Both ways” means: traffic **Rogers → you → Anthropic** and **Anthropic → you → Rogers**. You sit in the middle of that conversation. You are not inside Anthropic’s building.

### How does a client get installed? (startup-friendly path)

**Path A — SaaS (recommended when you have no stapler)**  
What Rogers does:
1. Gets an account / API key from you (Pinkhouse).  
2. Changes **one setting**: instead of calling Anthropic directly, their app calls **your** API URL.  
3. Gives you (or stores in your vault) their Anthropic key *or* you use a pattern where they keep the key and you only shrink — enterprise preference varies.  
4. Watches logs/metrics with you on a call.

What you do personally:
- Email/Slack: link, key, 1-page setup.  
- 30–60 min call with their engineer: “change base URL / add header / here’s a test.”  
- Watch first successful calls in TokenScope.  
- No site visit required.

**You are not emailing a mystery .exe and hoping.** You’re giving them a **URL + key + docs**. Their people who “know their stuff” change the outbound destination.

**Path B — Inside their cloud (later, bigger deals)**  
- You give them a container/image or Terraform, or you deploy into their VPC with their watching.  
- More paperwork, security review, their DNS/internal names.  
- Still not chips in pockets — still software.  
- Higher effort for you (or a future hire / partner).

**Path C — License only**  
- They build with your method/patent.  
- Little “install” of your runtime; different commercial model (not easy 5%-of-savings).

### “Do they API out to my mainframe?”
They **API out to your cloud service** (DigitalOcean is fine to start).  
You don’t need a mainframe. You need:
- A small always-on service (API)  
- HTTPS  
- Auth keys  
- Logging/meter (TokenScope)  
- Fail-open plan if your service blips  

That’s buildable with Cursor + a DO droplet/App Platform. Stapler optional.

### What Phil’s place is (role vs science)

| Hat | What you do |
|---|---|
| **Founder / seller** | Find Rogers-like buyer, 5-min demo, intro engineer, commercial terms |
| **Product owner** | Decide Path A first; what the API looks like; what TokenScope shows |
| **Not required day one** | Rack hardware, sit in their NOC, invent cloud from zero alone |
| **Build help** | You + Cursor (and later a contractor) implement the gateway on DO |

Your personal install effort on Path A is mostly: **relationship, clarity, one setup call, watching the meter — not physical installation.**

### Arrange an install — checklist
1. Demo done; they want a trial.  
2. You create tenant + API key on Pinkhouse.  
3. Send setup doc: “point this SDK/base URL here; send this header.”  
4. Joint call: they flip staging traffic first (not all production).  
5. You both watch before/after counts.  
6. Security people watch too — expected and good.  
7. Only then: more traffic / savings discussion / contract formula.  

They may give you allowlists, a tech contact, maybe a webhook — not usually “here’s our whole DNS kingdom.” More often: **they call your DNS name via API.**

### Level of effort (honest)
- **First paying/trial customer (SaaS):** days–weeks of product hardening + a few hours of human install hand-holding — not months on-site.  
- **Enterprise in-VPC:** weeks of security/process, even if the tech is ready.  
- **You starting with nothing:** Path A on DigitalOcean is the sane “no stapler” move. Build the plug once; many customers hit the same URL with different keys.

---

*Saved so you can re-read with a clear head and ask follow-up questions. Revise this file as the live demo and Pinkhouse paths firm up.*

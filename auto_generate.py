#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubGaming.io — Auto Post Generator (SEO PRO - B3 Authority)
- Long-form 800–1200 words
- JSON-LD Article schema
- Tags, categories, LSI keywords
- Safe internal links + safe external backlinks (1–2)
- No Liquid tags in body (ads handled by layout)
"""
import os
import re
import json
import random
import datetime
import textwrap
import yaml

# ====== Basic config ======
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "hubgaming.io")

FRIENDLY_DOMAINS = [
    "bottradingai.com","botgame.io","metaversebot.io","nftgameai.com",
    "hubgaming.io","botdefi.io","esportsai.io","nftgamepro.com",
    "botesports.com","aiesports.io","pronftgame.com","botplay.io",
    "botweb3ai.com","botblockchain.io"
]

# Topic pools for HubGaming (Esports + AI + Web3)
TITLE_TEMPLATES = [
    "AI-Driven Esports Strategy: {topic} in {year}",
    "How Elite Teams Use {topic} to Win More Maps ({year} Guide)",
    "Pro Playbook: {topic} for High-Tempo Esports in {year}",
    "From VOD to Live Inference: {topic} That Moves the Needle",
    "The {topic} Stack for Esports Coaches and Analysts ({year})"
]

TOPIC_POOL = [
    "Reinforcement Learning for Match Strategy",
    "Predictive Aim & Heatmap Analytics",
    "Real-Time Risk Engines for Tilt Control",
    "MMR Quality and Skill Modeling",
    "On-Chain Guild Coordination & Rewards",
    "Latency, Execution & Edge Inference",
    "Anti-Cheat via Behavioral Signals",
    "Tokenized Economies & NFT Utilities",
]

LSI_KEYWORDS = [
    "esports analytics", "AI coaching", "matchmaking quality", "MMR modeling",
    "Web3 gaming", "guild management", "on-chain rewards", "low-latency pipelines",
    "heatmap analysis", "reinforcement learning", "anti-cheat signals",
    "tokenomics", "player-owned assets", "predictive insights"
]

TAGS_POOL = [
    "esports", "ai", "analytics", "coaching", "web3", "nft", "guilds",
    "reinforcement-learning", "anti-cheat", "mmr", "latency", "strategy"
]

CATEGORIES_POOL = ["Esports", "AI", "Analytics", "Strategy", "Web3"]

# Image sources (free/CDN)
IMAGE_SOURCES = [
    # Pexels esports/gaming
    "https://images.pexels.com/photos/907221/pexels-photo-907221.jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop",
    "https://images.pexels.com/photos/3945662/pexels-photo-3945662.jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop",
    # Unsplash topic
    "https://source.unsplash.com/1200x630/?esports,gaming,ai",
    # Picsum fallback random
    "https://picsum.photos/1200/630?random={rand}"
]

# ====== Helpers ======
def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[’'“”]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:75] or "post"

def pick_image() -> str:
    src = random.choice(IMAGE_SOURCES)
    if "{rand}" in src:
        src = src.replace("{rand}", str(random.randint(10000, 99999)))
    return src

def pick_backlinks(n=2) -> str:
    pool = [d for d in FRIENDLY_DOMAINS if d != SITE_DOMAIN]
    random.shuffle(pool)
    take = pool[:n]
    # Return inline paragraphs (not a big list)
    items = [f"[{d}](https://{d})" for d in take]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]

def assemble_paragraph(sent_pool, min_s=3, max_s=6):
    sents = random.sample(sent_pool, k=min(max_s, max(min_s, len(sent_pool))))
    # randomly cut to 3-6 sentences
    k = random.randint(min_s, min(max_s, len(sents)))
    return " ".join(sents[:k])

# ====== Content blueprints ======
INTRO_SENTENCES = [
    "In high-stakes esports, milliseconds decide outcomes and good process beats raw talent.",
    "Elite teams treat operations like products: they ship strategy, measure impact, and roll back safely.",
    "AI elevates decision-making from intuition to instrumentation, turning VOD review into live inference.",
    "When the meta shifts, robust pipelines—not hero plays—prevent losing streaks.",
    "The future belongs to squads that automate the boring and amplify human skill."
]

HIGHLIGHT_BULLETS = [
    "Edge inference: capture → feature → detect → decide → act on low-latency loops.",
    "Reinforcement cycles: practice queues double as simulation labs for safe iteration.",
    "MMR quality: Bayesian curves reduce smurf noise and stabilize rankings.",
    "Anti-cheat with behavioral signals lowers false positives and restores trust.",
    "On-chain coordination: verifiable rewards, lending, and role assignment for guilds.",
    "Risk engines for tilt control: cooldowns, eco-guards, and loss limits."
]

CASE_SENTENCES = [
    "In scrim environments, small policy changes compound into major map control swings.",
    "Teams that ship weekly ‘ops builds’ see faster meta reactions and fewer unforced errors.",
    "Telemetry-informed coaching replaces guesswork with specific, testable interventions.",
    "Role clarity and economy rules stop micro mistakes from snowballing mid-series.",
    "Live labeling of mistakes turns demos into structured datasets for future training."
]

SYSTEM_SENTENCES = [
    "Instrumentation produces stable dashboards for coaches and IGLs at a glance.",
    "Event streams become features; features become policies; policies become advantages.",
    "Simulation coverage matters: more edge cases rehearsed means fewer surprises on stage.",
    "Granular rollback enables aggressive experimentation without high production risk.",
    "Playbooks evolve from static PDFs to versioned, queryable knowledge bases."
]

TIP_SENTENCES = [
    "Version your calls: tag, diff, and annotate why a change exists.",
    "Separate practice and production: same infrastructure, stricter thresholds on match days.",
    "Label outcomes tightly: a clean dataset is worth more than one more scrim.",
    "Automate basic reviews so human coaches spend time on nuance, not repetition.",
    "Guardrails: define eco floors, timeout triggers, and morale resets before disaster."
]

CONCLUSION_SENTENCES = [
    "AI won’t replace pros; pros using AI will replace others.",
    "Squads that productize operations will own the next season.",
    "The meta rewards teams who learn faster, not just those who aim better.",
    "Data-informed culture turns tilt into insight and nerves into execution."
]

INTERNAL_LINKS = [
    ("map control", "/"),
    ("MMR quality", "/"),
    ("tilt control", "/"),
    ("reinforcement loops", "/"),
]

def sprinkle_internal_links(text: str) -> str:
    # Replace a few anchor phrases with internal links (safe & sparse)
    for phrase, href in random.sample(INTERNAL_LINKS, k=min(2, len(INTERNAL_LINKS))):
        if phrase in text:
            text = text.replace(phrase, f"[{phrase}]({href})", 1)
    return text

def make_longform_content(title: str) -> str:
    year = datetime.date.today().year
    # Intro (2 paragraphs)
    intro_p1 = assemble_paragraph(INTRO_SENTENCES, 3, 5)
    intro_p2 = assemble_paragraph(INTRO_SENTENCES, 3, 5)

    # Highlights (bullets)
    bullets = random.sample(HIGHLIGHT_BULLETS, k=5)
    bullets_md = "\n".join([f"- {b}" for b in bullets])

    # Case mini
    case_p1 = assemble_paragraph(CASE_SENTENCES, 3, 5)
    case_p2 = assemble_paragraph(CASE_SENTENCES, 3, 5)

    # Systems
    sys_p1 = assemble_paragraph(SYSTEM_SENTENCES, 3, 5)
    sys_p2 = assemble_paragraph(SYSTEM_SENTENCES, 3, 5)

    # Tips (bullets)
    tips = random.sample(TIP_SENTENCES, k=4)
    tips_md = "\n".join([f"- {t}" for t in tips])

    # Conclusion
    concl = assemble_paragraph(CONCLUSION_SENTENCES, 3, 4)

    # Light internal links
    intro_p1 = sprinkle_internal_links(intro_p1)
    sys_p1 = sprinkle_internal_links(sys_p1)

    # Backlinks safe (1–2)
    backlinks_str = pick_backlinks(n=random.choice([1, 2]))
    backlinks_para = f"See also: {backlinks_str}." if backlinks_str else ""

    sections = [
        f"{intro_p1}\n\n{intro_p2}",
        "### Key Insights\n" + bullets_md,
        f"### Pro Team Case Mini ({year})\n{case_p1}\n\n{case_p2}",
        f"### AI Strategy Breakdown\n{sys_p1}\n\n{sys_p2}",
        "### Actionable Tips for Teams\n" + tips_md,
        f"### What This Means Next\n{concl}",
        backlinks_para if backlinks_str else ""
    ]

    body = "\n\n".join([s for s in sections if s.strip()])
    return body

def generate_article():
    today = datetime.date.today()
    date_str = today.isoformat()
    year = today.year

    topic = random.choice(TOPIC_POOL)
    title_tpl = random.choice(TITLE_TEMPLATES)
    title = title_tpl.format(topic=topic, year=year)

    # Front-matter
    image_url = pick_image()
    tags = sorted(set(random.sample(TAGS_POOL, k=5)))
    categories = sorted(set(random.sample(CATEGORIES_POOL, k=2)))
    lsi = sorted(set(random.sample(LSI_KEYWORDS, k=5)))

    fm = {
        "layout": "post",
        "title": title,
        "date": date_str,
        "author": "HubGaming Team",
        "description": f"Esports + AI long-form analysis: {title}",
        "image": image_url,
        "tags": tags,
        "categories": categories,
        "keywords": ", ".join(lsi),
        "permalink": f"/{today.year}/{today.month:02d}/{today.day:02d}/{slugify(title)}/"
    }

    # JSON-LD schema
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": date_str,
        "dateModified": date_str,
        "image": image_url,
        "author": {"@type": "Person", "name": "HubGaming Team"},
        "publisher": {"@type": "Organization", "name": "HubGaming"},
        "mainEntityOfPage": f"https://{SITE_DOMAIN}"
    }
    schema_block = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>"

    # Body (hero + content)
    body_md = make_longform_content(title)
    hero_md = f"![{title}]({image_url})"

    # Final markdown (no Liquid tags inside)
    fm_text = yaml.safe_dump(fm, sort_keys=False).strip()
    md = textwrap.dedent(f"""\
    ---
    {fm_text}
    ---
    _This article was auto-generated by HubGaming AI (Authority SEO)._

    {hero_md}

    {body_md}

    {schema_block}
    """)

    # File path
    filename = f"_posts/{date_str}-{slugify(title)}.md"
    return filename, md

def main():
    os.makedirs("_posts", exist_ok=True)
    fn, content = generate_article()
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Generated:", fn)

if __name__ == "__main__":
    main()

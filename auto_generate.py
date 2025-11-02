#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-generate daily post for HubGaming.io
"""

import os, random, datetime, textwrap

DOMAINS = [
  "bottradingai.com","botgame.io","metaversebot.io","nftgameai.com",
  "hubgaming.io","botdefi.io","esportsai.io","nftgamepro.com",
  "botesports.com","aiesports.io","pronftgame.com","botplay.io",
  "botweb3ai.com","botblockchain.io"
]

TITLE_TEMPLATES = [
  "AI Agents Changing Competitive Esports in {year}",
  "Real-time Strategy with Reinforcement Learning ({year} Playbook)",
  "Web3 Guild Management: On-chain Coordination ({year})",
  "Latency, Risk & Execution: AI Pipelines for Pro Gamers",
  "NFT Utility in Competitive Ladders — Beyond Cosmetics",
  "Matchmaking 2.0: Skill Curves & MMR with ML ({year})",
  "HubGaming Meta: {topic} ({year})"
]

TOPIC_POOL = [
  "Predictive aim assistance (legal analytics)",
  "Dynamic economy balancing",
  "Behavioral anti-cheat signals",
  "Market-making for in-game assets",
  "Adaptive coaching & highlights",
  "Squad role optimization"
]

IMAGE_POOL = [
  "https://images.pexels.com/photos/907221/pexels-photo-907221.jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop",
  "https://images.pexels.com/photos/3945662/pexels-photo-3945662.jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop",
  "https://source.unsplash.com/1200x630/?esports,gaming",
  "https://picsum.photos/1200/630?random=87013"
]

INTRO_TEMPLATES = [
  "In today’s fast meta, milliseconds decide victories. We break down how AI + data reshape competitive play.",
  "Esports analytics matured fast — from VOD review to live inference at the edge. Here’s what matters in {year}.",
  "Teams that treat operations like ‘products’ ship faster meta reactions and win more maps. Let’s unpack the stack."
]

BODY_TEMPLATES = [
  "• **Edge inference**: capture → feature → detect risk → decision → action; built as stateless microservices.\n"
  "• **Reinforcement loops**: practice queues become simulation labs; policy improves on real scrims.\n"
  "• **Ops as code**: version strategies, run A/B during scrims, revert safely.",

  "• **On-chain coordination** for guilds: rewards, loans and slippage tolerant markets.\n"
  "• **MMR quality**: use robust Bayesian curves instead of raw Elo to prevent smurf abuse.\n"
  "• **Anti-cheat**: behavior modeling + hardware fingerprints lower false positives.",

  "• **Aim entropy** models find inconsistency bursts; surface real coaching instead of guesswork.\n"
  "• **Tactical heatmaps** from POV embeddings help IGLs call faster.\n"
  "• **Risk engines** manage tilt: limit-losses for economy rounds, cool-downs for bad streaks."
]

CONCLUSION_POOL = [
  "Teams that productize operations will dominate.",
  "AI won’t replace pros — the pros using AI will replace others.",
  "2025 belongs to squads that automate the boring and amplify the skill."
]

def slugify(s: str) -> str:
    s = s.lower()
    buf = []
    for ch in s:
        if ch.isalnum(): buf.append(ch)
        else: buf.append('-')
    s = ''.join(buf)
    parts = [p for p in s.split('-') if p]
    return '-'.join(parts)[:70]

def pick_backlinks(n=5):
    pool = list(DOMAINS)
    random.shuffle(pool)
    items = pool[:n]
    return "\n".join(f"- [{d}](https://{d})" for d in items)

def generate_markdown():
    today = datetime.date.today().isoformat()
    year = datetime.date.today().year

    topic = random.choice(TOPIC_POOL)
    title_tpl = random.choice(TITLE_TEMPLATES)
    title = title_tpl.format(year=year, topic=topic)

    intro = random.choice(INTRO_TEMPLATES).format(year=year)
    bodies = random.sample(BODY_TEMPLATES, 2)
    image = random.choice(IMAGE_POOL)
    conclusion = random.choice(CONCLUSION_POOL)

    ad_tag = "{% include ad.html %}"

    md = textwrap.dedent(f"""\
    ---
    layout: post
    title: "{title.replace('"', "'")}"
    date: {today}
    author: "HubGaming Team"
    description: "Daily AI/esports insight from HubGaming."
    image: "{image}"
    ---

    _This post was auto-generated._

    ![{title}]({image})

    {ad_tag}

    {intro}

    ### Key Highlights
    {bodies[0]}

    ### Systems that Win
    {bodies[1]}

    ### Friendly Network
    {pick_backlinks(5)}

    **Conclusion:** {conclusion}
    """)

    slug = slugify(title)
    filename = f"_posts/{today}-{slug}.md"
    return filename, md

def main():
    os.makedirs("_posts", exist_ok=True)
    fn, content = generate_markdown()
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote:", fn)

if __name__ == "__main__":
    main()

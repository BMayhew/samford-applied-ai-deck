# Applied AI: Building with Claude

Slides from my guest session in the Applied AI class at Samford University on November 19, 2026. We covered how agentic coding works, then built a news aggregator live with Claude Code.

## View the deck

View it online at https://bmayhew.github.io/samford-applied-ai-deck/ or open `index.html` locally.

- Arrow keys, space, or click to move between slides
- `N` shows the speaker notes
- `F` goes fullscreen

## What's in this repo

- `index.html`: the slide viewer
- `deck/`: the slide source
- [`code/`](code/): where we build the app during class, and where the skills get installed

## What's covered

1. The agent loop
2. Context: what Claude can see
3. Models: pick by the job
4. Start with the why
5. Ask the AI to grill you
6. Live demo
7. What we used, and skills worth installing
8. Shipping responsibly: the quality bar, verifying, git, AI features in your app, deploying
9. Be more ambitious

## Skills from the talk

| Skill | What it does | Link |
|---|---|---|
| grill-me | Interviews you until the plan holds up | https://github.com/mattpocock/skills |
| superpowers | A full workflow: brainstorm, plan, test first, review | https://github.com/obra/superpowers |
| impeccable | Design vocabulary and checks against generic AI-looking UI | https://impeccable.style |
| be-ambitious | Turns a task into a bigger plan and a more demanding prompt | https://github.com/robonuggets/be-ambitious |
| Anthropic's skills | frontend-design, skill-creator, webapp-testing, and more | https://github.com/anthropics/skills |

## Recommended reading

[How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/) by Felix Rieseberg.

> "I frequently proclaim (together with other people working on AI) that we ought to be more ambitious when using it."

The be-ambitious skill above is built from this article.

## Editing the slides

The slide source is in `deck/`: one HTML file per slide in `deck/slides/`, shared styles in `deck/deck.css`, and the slide order in `deck/deck.json`. After you edit, rebuild the viewer:

```
python3 build.py
```

Butch Mayhew, [aiinqa.com](https://aiinqa.com), [LinkedIn](https://www.linkedin.com/in/butchmayhew)

"""
Editorial content and curated selections served by the API.

This module is the single source of truth for the hand-written copy that
used to live in the Django views. The English text is translated at
request time through the shared content catalog.
"""

VIBE_PROJECT_SLUGS = [
    "sunoreverse",
    "suno-arch",
    "market-pal",
    "KinoLOG",
]

CLI_PROJECT_SLUGS = [
    "epic_events",
    "AlgoInvest-Trade",
    "Chess_Up",
    "Book_Scraper",
    "clinkey-cli",
    "yotta",
    "super-pocket",
    "video-specs",
]

DJANGO_TECH_SLUGS = ["django", "django-rest-framework"]

FEATURED_PROJECTS_COUNT = 4

HOME_INTRO = {
    "title": "dim-gggl",
    "body": (
        "Backend Python developer building Django applications, CLI tools, "
        "and AI-assisted creative workflows."
    ),
}

NAVIGATION_SECTIONS = [
    {
        "eyebrow": "Explore",
        "title": "AI",
        "description": (
            "Prompting, music, video, jailbreaks, and vibe-engineering."
        ),
        "url": "/ai/",
    },
    {
        "eyebrow": "Build",
        "title": "CLI",
        "description": (
            "A curated selection of command-line oriented projects."
        ),
        "url": "/cli/",
    },
    {
        "eyebrow": "Ship",
        "title": "Django",
        "description": "Published Django and DRF projects from the portfolio.",
        "url": "/django/",
    },
    {
        "eyebrow": "Browse",
        "title": "Projects",
        "description": (
            "The complete archive with filters, search, and details."
        ),
        "url": "/projects/",
    },
    {
        "eyebrow": "Profile",
        "title": "About",
        "description": "Background, stack, and a broader presentation page.",
        "url": "/about/",
    },
]

CLI_PAGE_INTRO = {
    "title": "CLI",
    "body": (
        "A first-release selection of command-line projects focused on "
        "workflow, ergonomics, and packaging."
    ),
}

DJANGO_PAGE_INTRO = {
    "title": "Django",
    "body": (
        "Projects built with Django and Django REST Framework, both from "
        "personal projects and study projects."
    ),
}

AI_PAGE = {
    "prompting": {
        "intro": {
            "title": "Prompting",
            "body": (
                "A focused page for AI experiments built around "
                "authored prompts and reverse-analysis workflows."
            ),
        },
        "music": {
            "title": "Music",
            "spotify_embed_url": (
                "https://open.spotify.com/embed/album/"
                "5i9pJkPpbr0LzhRMQUHgFc?utm_source=generator"
            ),
            "spotify_external_url": (
                "https://open.spotify.com/album/5i9pJkPpbr0LzhRMQUHgFc"
            ),
            "spotify_caption": (
                "The artist Nola, now available on every music "
                "platform is a fictional artist with all the "
                "generated music I made through Suno AI"
            ),
            "track_title": "Un mot",
            "style_prompt": (
                "The Style Prompt:\n\n"
                "Alternative Electronic, Atmospheric IDM, "
                "Experimental Melodic "
                "Ambient, Ternary Rhythm, 6/8 time signature, Jazz chords, "
                "Prophet 6, Moog Matriarch, Eurorack Modular System, Roland "
                "Space Echo, Modular Synthesizer, glitchy gentle drum kit, "
                "electric guitar ambient swells, electric bass guitar, "
                "tape echo, "
                "falsetto male vocals, breathy and resonant, ethereal, "
                "intimate, "
                "French lyrics, minor key, building emotional crescendo, "
                "whispered "
                "intro and outro, spacious mix. \n-rock, -pop, -radio, "
                "-lyrical vocal, "
                "-choirs, -violin, -binary rhythm, -4/4 time signature, "
                "-yelling, "
                "-shouting, -operatic, -happy, -radio, -pop\n\n"
                "Weirdness: 6%\nStyle: 85%"
            ),
            "lyrics_prompt": """
--------------------------------
Lyrics Prompt:

[Mood: Melancholic] [Energy: Low]
[Instrument: Analog Synth, Space Echo, Soft Drums]

[Intro]
(misty atmosphere, slow analog synth arpeggiator building)

[Instrumental Break]
(relentless analog synth arpeggiator, reverb swells)

[Verse 1 | Whispered, Intimate]
(falsetto, floating delivery)
Il suffirait d'un mot
Pour que du monde
L'ordre chancelle
Possible ou rien
À vue perdue
Et qu'infinis
S'ouvrent les champs

Il suffirait d'un mot
Parmi les plus petits qui soient
De ceux tu sais
Qui ne sont pas
Labiaux mais qui sont ronds et chauds

[Pre-Chorus | Build-Up]
(space echo swells, instruments rising)
Il suffit de ce mot, oui
Décoré de l'écrin
Des velours de ton grain
Habillé d'abandon

[Chorus | Energy: Medium]
(ethereal, resonant, full reverb)
Sponte année… délicat...
Venu là déposé
Comme par l'évidence
Pour que s'écroule ma fierté
Et qu'à genoux
Je ne sois qu'à toi

[Instrumental Break]
(synth arpeggiator reprises, echo trails)

[Verse 2 | Whispered, Intimate]
(breathy, close-mic)
Oui c'est ce mot-là qu'il faudrait
Né de ta voix
Battu dans mes tempes
Comme un vieux métronome
Que n'atteint pas l'usure

Qui se fait désirer
À coups de litanies
Et qui rappelle au temps
Ce qu'il lui doit encore

[Bridge | Breakdown]
(sparse, drums enter softly, voice alone)
Combien tu ne le dis pas...
Combien tu ne le dis pas...
Combien tu ne le dis pas...

[Chorus | Energy: High]
(ethereal, resonant, fuller arrangement)
Sponte année… délicat...
Venu là déposé
Comme par l'évidence
Pour que s'écroule ma fierté
Et qu'à genoux
Je ne sois qu'à toi

[Bridge | Energy: Medium]
(building slowly, emotional tension)
Il suffit de ta bouche
Pour laisser passer l'air
Et qui dans mon oreille
Viendra lui donner forme

[Final Chorus | Energy: High | Harmonies]
(full band, maximum emotional release)
Sponte année… délicat...
Venu là déposé
Comme par l'évidence
Pour que s'écroule ma fierté
Et qu'à genoux
Je ne sois qu'à toi

[Outro | Energy: Low]
(fading, whispered, instruments dissolving)
Une forme précieuse...
Qui te ressemblerait...

[End]
(hold last word; leave room for Studio fade)
                    """,
        },
        "video": {
            "title": "Video",
            "body": (
                "A direct entry point to the Sora experiments and "
                "video-oriented "
                "prompting work."
            ),
            "sora_url": "https://sora.chatgpt.com/profile/dim-gggl",
            "cta_label": "Open my Sora page",
        },
        "jailbreak": {
            "title": "Jailbreak",
            "body": (
                "I train to understand how LLMs work by iterating on "
                "different kinds of prompts and, from time to time, I "
                "jailbreak the model to understand its limits.\n"
                "(For obvious reasons, parts of the model answer have "
                "been erased.)"
            ),
            "screenshot": "/static/images/Jailbreak_grok.png",
            "image_alt": (
                "Example of a conversation with a jailbroken version "
                "of Grok"
            ),
        },
    },
    "vibe_engineering": {
        "title": "Vibe Engineering",
        "body": (
            "Projects built on Google AI Studio with Gemini 3 Pro so "
            "mostly through prompting and iteration."
        ),
    },
}

ORIGIN_CONTEXTS = {
    "ai": {"label": "Back to AI", "url": "/ai/"},
    "cli": {"label": "Back to CLI", "url": "/cli/"},
    "django": {"label": "Back to Django", "url": "/django/"},
}

SKILL_COLOR_MAP = {
    5: {"from": "#00ff88", "to": "#00cc6a"},
    4: {"from": "#00e1ff", "to": "#00b8d4"},
    3: {"from": "#ffa500", "to": "#ff8c00"},
    2: {"from": "#ff6b6b", "to": "#ee5a5a"},
    1: {"from": "#888888", "to": "#666666"},
}

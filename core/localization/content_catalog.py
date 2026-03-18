"""
Translation catalog for static UI copy and dynamic project content.

The English copy is the single source of truth. French entries only provide
localized variants for content that is rendered to visitors.
"""

from __future__ import annotations

UI_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "meta.home_title": "Home - dim-gggl",
        "meta.ai_title": "AI - dim-gggl",
        "meta.cli_title": "CLI - dim-gggl",
        "meta.django_title": "Django - dim-gggl",
        "meta.about_title": "About - dim-gggl",
        "meta.projects_title": "All projects - dim-gggl",
        "meta.skills_title": "Skills - dim-gggl",
        "seo.default_title": "Dimitri Gaggioli - Python Backend Developer",
        "seo.default_description": (
            "Python developer specialized in Django, REST APIs, CLIs, and "
            "maintainable backend systems."
        ),
        "seo.keywords": (
            "Python developer, Django, Backend, REST API, CLI, Portfolio, "
            "Dimitri Gaggioli"
        ),
        "nav.home": "Home",
        "nav.ai": "AI",
        "nav.cli": "CLI",
        "nav.django": "Django",
        "nav.projects": "Projects",
        "nav.about": "About",
        "nav.menu": "Menu",
        "nav.switch_to_english": "Switch the site to English",
        "nav.switch_to_french": "Basculer le site en français",
        "hero.tagline_1": "Think.",
        "hero.tagline_2": "Code.",
        "hero.tagline_3": "Push.",
        "hero.description": (
            "Backend Python Developer in {location}. Fast REST APIs, "
            "maintainable code, reliable tests, and helpful docs."
        ),
        "hero.cta_projects": "See my projects",
        "hero.cta_contact": "Contact me",
        "home.label": "Home",
        "home.archive": "See all projects",
        "summary.title": "Explore my portfolio",
        "summary.projects": "Projects",
        "summary.projects_count": "{count} projects",
        "summary.skills": "Skills",
        "summary.skills_count": "{count} technologies",
        "summary.about": "About",
        "summary.about_description": "My journey and profile",
        "featured.title": "Featured Projects",
        "featured.empty": "Projects will be available soon.",
        "featured.fallback_description": (
            "Project description will be available soon."
        ),
        "skills.title": "Skills",
        "skills.stack_title": "Technical Stack",
        "skills.backend": "Backend",
        "skills.data_tools": "Data & Tools",
        "footer.location": "Paris, France",
        "footer.rights": "All rights reserved",
        "footer.built_with": "Built with",
        "intro.skip": "Skip intro",
        "intro.hint": "Press Enter to continue",
        "intro.line_1": "> Initializing...",
        "intro.line_2": "> Loading skills... [████████] 100%",
        "intro.line_3": "> Loading projects... [████████] 100%",
        "intro.line_4": ">",
        "intro.line_5": "> Think...",
        "intro.line_6": "> Code...",
        "intro.line_7": "> Push...",
        "intro.line_8": ">",
        "intro.line_9": "> Press [ENTER] or wait to continue...",
        "about.role": "Backend Python Developer",
        "about.cta_contact": "Contact me",
        "about.stats_projects": "Projects completed",
        "about.stats_years": "Years of experience",
        "about.stats_technologies": "Technologies",
        "about.stats_passion": "Passion",
        "about.who_title": "Who am I?",
        "about.p1": (
            "Backend Python Developer, I design robust, scalable, and "
            "maintainable applications."
        ),
        "about.p2": (
            "Trained in Django, REST APIs, and modern CLIs, I focus on "
            "reproducible environments, usable documentation, and tested code."
        ),
        "about.p3": (
            "I am also deeply interested in generative AI, agentic systems, "
            "and prompt engineering to integrate new tools into real workflows."
        ),
        "about.p4": (
            "Beyond code, I care about user experience and visual design to "
            "ship interfaces that feel both useful and deliberate."
        ),
        "about.timeline_title": "My journey",
        "about.timeline_1_title": "Python Web Development",
        "about.timeline_1_body": (
            "Intensive training in Python, Django, REST APIs, testing, and "
            "software engineering best practices."
        ),
        "about.timeline_2_title": "Master's degree in Cinema",
        "about.timeline_2_body": (
            "Training in film analysis and cinema theory, which sharpened my "
            "critical thinking and creativity."
        ),
        "about.timeline_3_title": "Cultural programming",
        "about.timeline_3_body": (
            "Years spent organizing screenings and cultural events, building a "
            "strong sense of curation, coordination, and storytelling."
        ),
        "about.skills_title": "Detailed skills",
        "about.skills_backend": "Backend & languages",
        "about.skills_frontend": "Frontend",
        "about.skills_databases": "Databases",
        "about.skills_tools": "Tools",
        "about.interests_title": "Areas of Interest",
        "about.interest_poetry_title": "Poetry",
        "about.interest_poetry_body": (
            "Writing and sharing poetry on Instagram under the pen name "
            "@remo_nesa."
        ),
        "about.interest_poetry_note": (
            "Poetic writing feeds my creativity and my attention to aesthetics."
        ),
        "about.interest_cinema_title": "Cinema & programming",
        "about.interest_cinema_body": (
            "Passionate about cinema, I have also programmed screenings for "
            "Cinéma La Clef."
        ),
        "about.interest_cinema_note": (
            "This background shapes the way I think about narrative, rhythm, "
            "and interface design."
        ),
        "about.qualities_title": "Professional qualities",
        "about.quality_creativity_title": "Creativity",
        "about.quality_creativity_body": (
            "Inventive approaches to technical problems and product design."
        ),
        "about.quality_adaptability_title": "Adaptability",
        "about.quality_adaptability_body": (
            "Ability to learn new tools quickly and adapt to changing contexts."
        ),
        "about.quality_team_title": "Team spirit",
        "about.quality_team_body": (
            "Clear communication and reliable collaboration with teammates."
        ),
        "about.quality_results_title": "Execution",
        "about.quality_results_body": (
            "Focused on turning ideas into solid, shippable outcomes."
        ),
        "about.cta_title": "Let's work together!",
        "about.cta_body": "I'm available for collaboration opportunities.",
        "about.cta_projects": "See my projects",
        "projects.hero_title": "My Projects",
        "projects.search_placeholder": "Search a project...",
        "projects.all_categories": "All categories",
        "projects.sort_default": "Default",
        "projects.sort_recent": "Most recent",
        "projects.sort_title": "A → Z",
        "projects.technologies": "Technologies ({count})",
        "projects.selected_count": "{count} selected",
        "projects.selected_count_plural": "{count} selected",
        "projects.technology_hint": (
            "Select one or more technologies to refine the list."
        ),
        "projects.active_filters": "Active filters:",
        "projects.search_filter": 'Search: "{query}"',
        "projects.reset": "Reset all",
        "projects.results_filtered_single": "{count} project found out of {total}",
        "projects.results_filtered_plural": "{count} projects found out of {total}",
        "projects.results_all_single": "Displaying {count} project",
        "projects.results_all_plural": "Displaying {count} projects",
        "projects.previous": "Previous",
        "projects.next": "Next",
        "projects.page": "Page {current} of {total}",
        "projects.empty_title": "No projects match these filters yet.",
        "projects.empty_body": "Try adjusting your search or filters.",
        "projects.empty_cta": "See all projects",
        "projects.cta_title": "Interested in my work?",
        "projects.cta_body": (
            "Feel free to contact me to discuss your projects."
        ),
        "projects.cta_contact": "Contact me",
        "projects.cta_github": "See my GitHub",
        "ai.spotify_open": "Open on Spotify",
        "ai.lightbox_close": "Close ✕",
        "project.github": "See on GitHub",
        "project.demo": "See the demo",
        "project.website": "See the website",
        "project.documentation": "See the documentation",
        "project.about": "About the project",
        "project.screenshots": "Screenshots",
        "project.features_title": "Main features",
        "project.challenges": "Challenges encountered",
        "project.learnings": "Learnings",
        "project.stack": "Technical stack",
        "project.related": "You might also like",
        "project.previous_label": "Previous project",
        "project.next_label": "Next project",
        "project.cta_title": "Interested in this project?",
        "project.cta_body": (
            "Let's discuss how I can help with your next project."
        ),
        "project.cta_contact": "Contact me",
        "project.cta_projects": "See my projects",
        "maintenance.title": "Maintenance in progress",
        "maintenance.body": (
            "The site is currently undergoing maintenance for improvements. "
            "We'll be back very soon."
        ),
        "maintenance.contact_label": (
            "In the meantime, you can contact me by email:"
        ),
    },
    "fr": {
        "meta.home_title": "Accueil - dim-gggl",
        "meta.ai_title": "IA - dim-gggl",
        "meta.cli_title": "CLI - dim-gggl",
        "meta.django_title": "Django - dim-gggl",
        "meta.about_title": "À propos - dim-gggl",
        "meta.projects_title": "Tous les projets - dim-gggl",
        "meta.skills_title": "Compétences - dim-gggl",
        "seo.default_title": "Dimitri Gaggioli - Développeur Python Backend",
        "seo.default_description": (
            "Développeur Python spécialisé en Django, APIs REST, CLI et "
            "systèmes backend maintenables."
        ),
        "seo.keywords": (
            "Développeur Python, Django, Backend, API REST, CLI, Portfolio, "
            "Dimitri Gaggioli"
        ),
        "nav.home": "Accueil",
        "nav.ai": "IA",
        "nav.cli": "CLI",
        "nav.django": "Django",
        "nav.projects": "Projets",
        "nav.about": "À propos",
        "nav.menu": "Menu",
        "nav.switch_to_english": "Switch the site to English",
        "nav.switch_to_french": "Basculer le site en français",
        "hero.tagline_1": "Think.",
        "hero.tagline_2": "Code.",
        "hero.tagline_3": "Push.",
        "hero.description": (
            "Développeur Python backend à {location}. APIs REST rapides, code "
            "maintenable, tests fiables et documentation utile."
        ),
        "hero.cta_projects": "Voir mes projets",
        "hero.cta_contact": "Me contacter",
        "home.label": "Accueil",
        "home.archive": "Voir tous les projets",
        "summary.title": "Explorer mon portfolio",
        "summary.projects": "Projets",
        "summary.projects_count": "{count} projets",
        "summary.skills": "Compétences",
        "summary.skills_count": "{count} technologies",
        "summary.about": "À propos",
        "summary.about_description": "Mon parcours et mon profil",
        "featured.title": "Projets mis en avant",
        "featured.empty": "Les projets seront bientôt disponibles.",
        "featured.fallback_description": (
            "La description du projet sera bientôt disponible."
        ),
        "skills.title": "Compétences",
        "skills.stack_title": "Stack technique",
        "skills.backend": "Backend",
        "skills.data_tools": "Data et outils",
        "footer.location": "Paris, France",
        "footer.rights": "Tous droits réservés",
        "footer.built_with": "Construit avec",
        "intro.skip": "Passer l'intro",
        "intro.hint": "Appuyez sur Entrée pour continuer",
        "intro.line_1": "> Initialisation...",
        "intro.line_2": "> Chargement des compétences... [████████] 100%",
        "intro.line_3": "> Chargement des projets... [████████] 100%",
        "intro.line_4": ">",
        "intro.line_5": "> Think...",
        "intro.line_6": "> Code...",
        "intro.line_7": "> Push...",
        "intro.line_8": ">",
        "intro.line_9": "> Appuyez sur [ENTRÉE] ou patientez pour continuer...",
        "about.role": "Développeur Python Backend",
        "about.cta_contact": "Me contacter",
        "about.stats_projects": "Projets réalisés",
        "about.stats_years": "Années d'expérience",
        "about.stats_technologies": "Technologies",
        "about.stats_passion": "Passion",
        "about.who_title": "Qui suis-je ?",
        "about.p1": (
            "Développeur Python backend, je conçois des applications robustes, "
            "scalables et maintenables."
        ),
        "about.p2": (
            "Formé à Django, aux APIs REST et aux CLI modernes, je privilégie "
            "les environnements reproductibles, la documentation utile et le "
            "code testé."
        ),
        "about.p3": (
            "Je m'intéresse aussi de près à l'IA générative, aux systèmes "
            "agentiques et au prompt engineering pour intégrer de nouveaux "
            "outils dans des workflows concrets."
        ),
        "about.p4": (
            "Au-delà du code, j'accorde une vraie importance à l'expérience "
            "utilisateur et au design pour livrer des interfaces à la fois "
            "utiles et intentionnelles."
        ),
        "about.timeline_title": "Mon parcours",
        "about.timeline_1_title": "Développement web Python",
        "about.timeline_1_body": (
            "Formation intensive en Python, Django, APIs REST, tests et bonnes "
            "pratiques d'ingénierie logicielle."
        ),
        "about.timeline_2_title": "Master 1 Cinéma",
        "about.timeline_2_body": (
            "Formation à l'analyse filmique et à la théorie du cinéma, qui a "
            "affiné mon regard critique et ma créativité."
        ),
        "about.timeline_3_title": "Programmation culturelle",
        "about.timeline_3_body": (
            "Des années à organiser projections et événements culturels, avec "
            "un vrai sens de la curation, de la coordination et du récit."
        ),
        "about.skills_title": "Compétences détaillées",
        "about.skills_backend": "Backend et langages",
        "about.skills_frontend": "Frontend",
        "about.skills_databases": "Bases de données",
        "about.skills_tools": "Outils",
        "about.interests_title": "Centres d'intérêt",
        "about.interest_poetry_title": "Poésie",
        "about.interest_poetry_body": (
            "Écriture et partage de poésie sur Instagram sous le pseudonyme "
            "@remo_nesa."
        ),
        "about.interest_poetry_note": (
            "L'écriture poétique nourrit ma créativité et mon sens de "
            "l'esthétique."
        ),
        "about.interest_cinema_title": "Cinéma et programmation",
        "about.interest_cinema_body": (
            "Passionné de cinéma, j'ai aussi programmé des projections au "
            "Cinéma La Clef."
        ),
        "about.interest_cinema_note": (
            "Ce parcours influence ma manière de penser le récit, le rythme et "
            "le design d'interface."
        ),
        "about.qualities_title": "Qualités professionnelles",
        "about.quality_creativity_title": "Créativité",
        "about.quality_creativity_body": (
            "Des approches inventives pour résoudre les problèmes techniques "
            "et concevoir les produits."
        ),
        "about.quality_adaptability_title": "Adaptabilité",
        "about.quality_adaptability_body": (
            "Capacité à apprendre vite de nouveaux outils et à m'adapter à "
            "des contextes changeants."
        ),
        "about.quality_team_title": "Esprit d'équipe",
        "about.quality_team_body": (
            "Communication claire et collaboration fiable avec les équipes."
        ),
        "about.quality_results_title": "Exécution",
        "about.quality_results_body": (
            "Orienté vers la transformation des idées en résultats concrets."
        ),
        "about.cta_title": "Travaillons ensemble !",
        "about.cta_body": "Je suis disponible pour des opportunités de collaboration.",
        "about.cta_projects": "Voir mes projets",
        "projects.hero_title": "Mes projets",
        "projects.search_placeholder": "Rechercher un projet...",
        "projects.all_categories": "Toutes les catégories",
        "projects.sort_default": "Par défaut",
        "projects.sort_recent": "Plus récents",
        "projects.sort_title": "A → Z",
        "projects.technologies": "Technologies ({count})",
        "projects.selected_count": "{count} sélection",
        "projects.selected_count_plural": "{count} sélections",
        "projects.technology_hint": (
            "Sélectionnez une ou plusieurs technologies pour affiner la liste."
        ),
        "projects.active_filters": "Filtres actifs :",
        "projects.search_filter": 'Recherche : "{query}"',
        "projects.reset": "Réinitialiser",
        "projects.results_filtered_single": "{count} projet trouvé sur {total}",
        "projects.results_filtered_plural": "{count} projets trouvés sur {total}",
        "projects.results_all_single": "{count} projet affiché",
        "projects.results_all_plural": "{count} projets affichés",
        "projects.previous": "Précédent",
        "projects.next": "Suivant",
        "projects.page": "Page {current} sur {total}",
        "projects.empty_title": "Aucun projet ne correspond à ces filtres.",
        "projects.empty_body": "Essayez d'ajuster votre recherche ou vos filtres.",
        "projects.empty_cta": "Voir tous les projets",
        "projects.cta_title": "Mon travail vous intéresse ?",
        "projects.cta_body": (
            "N'hésitez pas à me contacter pour parler de vos projets."
        ),
        "projects.cta_contact": "Me contacter",
        "projects.cta_github": "Voir mon GitHub",
        "ai.spotify_open": "Ouvrir sur Spotify",
        "ai.lightbox_close": "Fermer ✕",
        "project.github": "Voir sur GitHub",
        "project.demo": "Voir la démo",
        "project.website": "Voir le site",
        "project.documentation": "Voir la documentation",
        "project.about": "À propos du projet",
        "project.screenshots": "Captures d'écran",
        "project.features_title": "Fonctionnalités principales",
        "project.challenges": "Défis rencontrés",
        "project.learnings": "Apprentissages",
        "project.stack": "Stack technique",
        "project.related": "Vous aimerez aussi",
        "project.previous_label": "Projet précédent",
        "project.next_label": "Projet suivant",
        "project.cta_title": "Ce projet vous intéresse ?",
        "project.cta_body": (
            "Échangeons sur la façon dont je peux vous aider sur votre "
            "prochain projet."
        ),
        "project.cta_contact": "Me contacter",
        "project.cta_projects": "Voir mes projets",
        "maintenance.title": "Maintenance en cours",
        "maintenance.body": (
            "Le site est actuellement en maintenance pour quelques "
            "améliorations. Il sera de retour très bientôt."
        ),
        "maintenance.contact_label": (
            "En attendant, vous pouvez me contacter par email :"
        ),
    },
}

CONTENT_TRANSLATIONS: dict[str, dict[str, str]] = {
    "fr": {
        "AI": "IA",
        "Python Developer - Backend": "Développeur Python - Backend",
        "Study Projects": "Projets d'étude",
        "Personal Projects": "Projets personnels",
        "Backend": "Backend",
        "Frontend": "Frontend",
        "Database": "Base de données",
        "Tool": "Outil",
        "Language": "Langage",
        "Too many requests. Please try again later.": (
            "Trop de requêtes. Veuillez réessayer plus tard."
        ),
        "Backend Python developer building Django applications, CLI tools, and AI-assisted creative workflows.": (
            "Développeur Python backend qui construit des applications Django, "
            "des outils CLI et des workflows créatifs assistés par l'IA."
        ),
        "Explore": "Explorer",
        "Build": "Construire",
        "Ship": "Déployer",
        "Browse": "Parcourir",
        "Profile": "Profil",
        "Prompting, music, video, jailbreaks, and vibe-engineering.": (
            "Prompting, musique, vidéo, jailbreaks et vibe-engineering."
        ),
        "A curated selection of command-line oriented projects.": (
            "Une sélection de projets orientés ligne de commande."
        ),
        "Published Django and DRF projects from the portfolio.": (
            "Des projets Django et DRF publiés dans le portfolio."
        ),
        "The complete archive with filters, search, and details.": (
            "L'archive complète avec filtres, recherche et détails."
        ),
        "Background, stack, and a broader presentation page.": (
            "Parcours, stack et page de présentation plus complète."
        ),
        "Prompting": "Prompting",
        "A focused page for AI experiments built around authored prompts and reverse-analysis workflows.": (
            "Une page dédiée aux expérimentations IA, construite autour de "
            "prompts écrits et de workflows d'analyse inverse."
        ),
        "Music": "Musique",
        "Artist mapping EP on Spotify.": "EP Artist Mapping sur Spotify.",
        "Video": "Vidéo",
        "A direct entry point to the Sora experiments and video-oriented prompting work.": (
            "Un point d'entrée direct vers les expérimentations Sora et le "
            "travail de prompting orienté vidéo."
        ),
        "Open my Sora page": "Voir ma page Sora",
        "Jailbreak": "Jailbreak",
        "I train to understand how LLMs work by iterating on different kind of prompts and from time to time I jailbreak the model to understand.\n(For obvious reasons, parts of the answer from the model have been erased)": (
            "Je m'entraîne à comprendre le fonctionnement des LLM en itérant "
            "sur différents types de prompts et, de temps en temps, je "
            "jailbreak le modèle pour comprendre.\n(Pour des raisons "
            "évidentes, certaines parties de la réponse du modèle ont été effacées.)"
        ),
        "Example of a conversation with a jailbroken version of Grok": (
            "Exemple d'une conversation avec une version jailbreakée de Grok"
        ),
        "Vibe Engineering": "Vibe Engineering",
        "Projects built on Google AI Studio with Gemini 3 Pro so mostly through prompting and iteration.": (
            "Projets construits sur Google AI Studio avec Gemini 3 Pro, "
            "donc principalement par prompting et itération."
        ),
        "A first-release selection of command-line projects focused on workflow, ergonomics, and packaging.": (
            "Une première sélection de projets en ligne de commande axés sur "
            "les workflows, l'ergonomie et le packaging."
        ),
        "More selected work coming soon.": (
            "D'autres projets sélectionnés arrivent bientôt."
        ),
        "Back to AI": "Retour vers IA",
        "Back to CLI": "Retour vers CLI",
        "Back to Django": "Retour vers Django",
        "CLI CRM for an event agency": "CRM CLI pour une agence événementielle",
        "Manage your events, clients, contracts, and teammate profiles with an ergonomic, intuitive Command Line Interface.": (
            "Gérez vos événements, clients, contrats et profils d'équipe dans "
            "une interface en ligne de commande ergonomique et intuitive."
        ),
        "Implemented the PostgreSQL database and secured the application with password hashing and JWT authentication.": (
            "J'ai mis en place la base PostgreSQL et sécurisé l'application "
            "avec le hashage des mots de passe et l'authentification JWT."
        ),
        "PostgreSQL, JWT, hashing, TUI": "PostgreSQL, JWT, hashage, TUI",
        "End-to-end CLI flow - Intuitive, styled terminal interface powered by Rich to create and update events, manage clients, and oversee teammates.": (
            "Flux CLI complet - Interface terminal intuitive et stylisée avec "
            "Rich pour créer et mettre à jour les événements, gérer les "
            "clients et piloter l'équipe."
        ),
        "Secure sign-in and data - Permission and validation system that guarantees data integrity and reinforces security.": (
            "Connexion et données sécurisées - Système de permissions et de "
            "validation qui garantit l'intégrité des données et renforce la "
            "sécurité."
        ),
        "PostgreSQL database - Automatic persistence of all data with a dedicated schema that is robust and scalable.": (
            "Base PostgreSQL - Persistance automatique de toutes les données "
            "avec un schéma dédié, robuste et scalable."
        ),
        "JWT authentication - Sign-in and permission system based on JWT to protect user data.": (
            "Authentification JWT - Système de connexion et de permissions "
            "basé sur JWT pour protéger les données utilisateur."
        ),
        "Action logging - Errors and user actions logged through Sentry.": (
            "Journalisation des actions - Erreurs et actions utilisateur "
            "suivies via Sentry."
        ),
        "Points-based competition registrations.": "Inscriptions aux compétitions par points.",
        "Flask application for clubs: secretaries register athletes for competitions by spending club points, with quotas and availability checks.": (
            "Application Flask pour les clubs : les secrétaires inscrivent les "
            "athlètes aux compétitions en dépensant des points club, avec des "
            "quotas et des vérifications de disponibilité."
        ),
        "Authentication (secretaries / admin)": "Authentification (secrétaires / admin)",
        "Upcoming competitions list (remaining slots)": "Liste des compétitions à venir (places restantes)",
        "Athlete booking (1 point = 1 slot)": "Réservation d'athlète (1 point = 1 place)",
        "Limits: club balance, maximum 12 slots per competition per club": (
            "Limites : solde du club, maximum 12 places par compétition et par club"
        ),
        "Cancellation with point refund (before the event)": (
            "Annulation avec remboursement des points (avant l'événement)"
        ),
        "Admin area: CRUD for clubs / competitions / users / bookings": (
            "Espace admin : CRUD des clubs / compétitions / utilisateurs / réservations"
        ),
        "Testing and debugging campaign (Pytest)": (
            "Campagne de tests et de débogage (Pytest)"
        ),
        "Project tracking REST API.": "API REST de suivi de projet.",
        "Projects built with Django and Django REST Framework, both from personal projects and study projects.": (
            "Projets realises avec Django et Django REST Framework, issus a la "
            "fois de projets personnels et de projets d'etude."
        ),
        "REST API built with Django REST Framework to manage projects, contributors, tickets (issues), and comments, secured with JWT. Strict scopes per project and per author.\n\n## Endpoint examples\n\n**User Detail endpoint**: Displays data for an individual user (restricted to authenticated users viewing their own profile). Returns username, email, age, contact preferences, and account creation date.\n\n**User List endpoint**: Displays a paginated list of users accessible to authenticated users, showing username and ID with pagination metadata.": (
            "API REST construite avec Django REST Framework pour gérer des "
            "projets, contributeurs, tickets (issues) et commentaires, "
            "sécurisée avec JWT. Les périmètres d'accès sont stricts par "
            "projet et par auteur.\n\n## Exemples d'endpoints\n\n"
            "**Endpoint User Detail** : affiche les données d'un utilisateur "
            "unique (réservé aux utilisateurs authentifiés qui consultent leur "
            "propre profil). Retourne le nom d'utilisateur, l'email, l'âge, "
            "les préférences de contact et la date de création du compte.\n\n"
            "**Endpoint User List** : affiche une liste paginée d'utilisateurs "
            "accessible aux utilisateurs authentifiés, avec le nom d'utilisateur, "
            "l'identifiant et les métadonnées de pagination."
        ),
        "JWT authentication (SimpleJWT)": "Authentification JWT (SimpleJWT)",
        "Project CRUD with contributor management": (
            "CRUD des projets avec gestion des contributeurs"
        ),
        "Per-project ticket CRUD (issue / request)": (
            "CRUD des tickets par projet (issue / demande)"
        ),
        "Per-ticket comment CRUD": "CRUD des commentaires par ticket",
        "Strong permissions (visibility limited to contributors)": (
            "Permissions strictes (visibilité limitée aux contributeurs)"
        ),
        "List pagination": "Pagination des listes",
        "OpenAPI/Swagger documentation": "Documentation OpenAPI/Swagger",
        "Tickets and reviews for readers.": "Tickets et critiques pour les lecteurs.",
        "Django application that lets readers publish tickets (review requests) and reviews, follow other users, comment, and browse a combined feed.": (
            "Application Django permettant aux lecteurs de publier des tickets "
            "(demandes de critique) et des critiques, de suivre d'autres "
            "utilisateurs, commenter et parcourir un flux combiné."
        ),
        "Authentication (test accounts provided)": (
            "Authentification (comptes de test fournis)"
        ),
        "Create tickets (request a review)": (
            "Créer des tickets (demander une critique)"
        ),
        "Publish reviews (linked or not to a ticket)": (
            "Publier des critiques (liées ou non à un ticket)"
        ),
        "News feed (tickets and reviews from subscriptions)": (
            "Fil d'actualité (tickets et critiques des abonnements)"
        ),
        "Follow / unfollow users": "Suivre / ne plus suivre des utilisateurs",
        "Edit / delete your own content": "Modifier / supprimer son propre contenu",
        "Dynamic app showing top-rated movies from IMDb": (
            "Application dynamique affichant les films les mieux notés d'IMDb"
        ),
        "JavaScript front end that consumes the OCMovies API (OpenClassrooms) to display the top movie, category-based leaderboards, and detailed modal cards (poster, synopsis, cast).": (
            "Front-end JavaScript qui consomme l'API OCMovies "
            "(OpenClassrooms) pour afficher le meilleur film, des classements "
            "par catégorie et des cartes modales détaillées (affiche, synopsis, casting)."
        ),
        "Learning JavaScript fundamentals, first API interactions": (
            "Apprentissage des bases de JavaScript, premières interactions avec une API"
        ),
        "HTML, CSS, JavaScript, Dynamic rendering, AJAX calls": (
            "HTML, CSS, JavaScript, rendu dynamique, appels AJAX"
        ),
        "Top-rated movie highlighted in the hero (poster plus short synopsis)": (
            "Film le mieux noté mis en avant dans le hero (affiche et synopsis court)"
        ),
        "Best movies and genre carousels": "Carrousels des meilleurs films et par genre",
        "Detailed modal card opens on poster click": (
            "Carte modale détaillée à l'ouverture au clic sur l'affiche"
        ),
        "Pagination handled via the OCMovies API": (
            "Pagination gérée via l'API OCMovies"
        ),
        "Responsive UI (vanilla HTML/CSS/JS)": (
            "Interface responsive (HTML/CSS/JS vanilla)"
        ),
        "Scaling a whole Django project and deploying it with Docker, GitHub Actions and Render": (
            "Refactorer, faire évoluer et déployer un projet Django avec Docker, GitHub Actions et Render"
        ),
        "Django application for real estate agency. It was needing refactoring and scaling to improve performance and security. A few bugs were fixed, tests were added and the project got containerized with Docker and deployed to Render. CI/CD pipeline was set up with ": (
            "Application Django pour une agence immobilière. Le projet "
            "nécessitait une refactorisation et une montée en qualité pour "
            "améliorer les performances et la sécurité. Plusieurs bugs ont "
            "été corrigés, des tests ont été ajoutés, puis l'application a "
            "été conteneurisée avec Docker et déployée sur Render. Une "
            "pipeline CI/CD a également été mise en place avec "
        ),
        "Learning Docker fundamentals, Setting up a CI/CD pipeline with GitHub Actions, Building documentation with Sphinx": (
            "Apprentissage des bases de Docker, mise en place d'une pipeline "
            "CI/CD avec GitHub Actions, création d'une documentation avec Sphinx"
        ),
        "Django, Docker, GitHub Actions, Render, CI/CD, Pytest, Sentry, Sphinx, Read the Docs": (
            "Django, Docker, GitHub Actions, Render, CI/CD, Pytest, Sentry, Sphinx, Read the Docs"
        ),
        "Tests covering 88% of the codebase": (
            "Tests couvrant 88 % de la base de code"
        ),
        "Documentation built with Sphinx and hosted on Read the Docs": (
            "Documentation construite avec Sphinx et hébergée sur Read the Docs"
        ),
        "Docker image available at `docker pull dgggl88/oc-lettings:latest`": (
            "Image Docker disponible via `docker pull dgggl88/oc-lettings:latest`"
        ),
        "Deployed on Render at https://oc-lettings-x670.onrender.com": (
            "Déployé sur Render à l'adresse https://oc-lettings-x670.onrender.com"
        ),
        "Invest with algorithms": "Investir avec des algorithmes",
        "This program implements two algorithmic approaches to solve the knapsack problem: it calculates the most profitable stock portfolio possible for a maximum budget of 500 EUR (use case for the fictional company AlgoInvest&Trade).": (
            "Ce programme implémente deux approches algorithmiques pour "
            "résoudre le problème du sac à dos : il calcule le portefeuille "
            "d'actions le plus rentable possible pour un budget maximal de "
            "500 EUR (cas d'usage de l'entreprise fictive AlgoInvest&Trade)."
        ),
        "Understand how the knapsack algorithm is constructed": (
            "Comprendre comment se construit l'algorithme du sac à dos"
        ),
        "Big O notation, brute force, dynamic programming": (
            "Notation Big O, force brute, programmation dynamique"
        ),
        "Exhaustive brute force - Explores every possible stock combination to guarantee the optimal profit, at the cost of exponential runtime (O(2^n)).": (
            "Force brute exhaustive - Explore toutes les combinaisons "
            "possibles d'actions pour garantir le profit optimal, au prix "
            "d'un temps d'exécution exponentiel (O(2^n))."
        ),
        "Dynamic programming - Optimized knapsack-style algorithm, much faster (approx. O(n * W)), recommended once the list exceeds about 20 assets and using memoization to avoid redundant calculations.": (
            "Programmation dynamique - Algorithme de type sac à dos "
            "optimisé, beaucoup plus rapide (environ O(n * W)), recommandé "
            "dès que la liste dépasse une vingtaine d'actifs, avec "
            "mémoïsation pour éviter les calculs redondants."
        ),
        "Invalid data report - Optional mode that detects and reports corrupted or unusable data in the provided datasets (for example negative costs or profits, missing values, and more).": (
            "Rapport de données invalides - Mode optionnel qui détecte et "
            "signale les données corrompues ou inutilisables dans les jeux "
            "de données fournis (par exemple coûts ou profits négatifs, "
            "valeurs manquantes, etc.)."
        ),
        "Command-line chess tournament manager": (
            "Gestionnaire de tournois d'échecs en ligne de commande"
        ),
        "Organize and run a full chess open, from the first move to the awards ceremony, without ever leaving your terminal: no spreadsheets, no hassle, just the game.": (
            "Organisez et pilotez un tournoi d'échecs complet, du premier "
            "coup à la remise des prix, sans jamais quitter votre terminal : "
            "pas de tableurs, pas de friction, juste le jeu."
        ),
        "Learn OOP concepts and discover the MVC architecture.": (
            "Découvrir les concepts de la POO et l'architecture MVC."
        ),
        "OOP, MVC, CLI, JSON, flake8": "POO, MVC, CLI, JSON, flake8",
        "Full CLI flow - Intuitive terminal interface to create a tournament, add players, launch rounds, record results, and edit reports without leaving the CLI.": (
            "Flux CLI complet - Interface terminal intuitive pour créer un "
            "tournoi, ajouter des joueurs, lancer les rondes, enregistrer "
            "les résultats et éditer les rapports sans quitter la CLI."
        ),
        "Swiss pairing - Algorithm that avoids duplicate matchups and automatically handles byes when needed for balanced rounds.": (
            "Système suisse - Algorithme qui évite les doublons "
            "d'affrontements et gère automatiquement les exemptions pour des "
            "rondes équilibrées."
        ),
        "Persistent JSON storage - Automatically saves all tournament and player data to JSON files so you can resume after a break.": (
            "Stockage JSON persistant - Sauvegarde automatiquement toutes les "
            "données du tournoi et des joueurs dans des fichiers JSON pour "
            "reprendre plus tard."
        ),
        "Improved readability - Console output enhanced with ANSI color codes (built-in `ansify()` utility) for comfortable reading in light or dark themes.": (
            "Lisibilité améliorée - Sortie console enrichie par des codes "
            "couleur ANSI (utilitaire intégré `ansify()`) pour un confort "
            "de lecture en thème clair ou sombre."
        ),
        "Code quality - Code compliant with PEP 8, with linting tools (flake8 and HTML report) to maintain a clean, reliable codebase over time.": (
            "Qualité de code - Code conforme à PEP 8, avec outils de lint "
            "(flake8 et rapport HTML) pour conserver une base propre et fiable."
        ),
        "Web scraping and ETL pipeline": "Web scraping et pipeline ETL",
        "Book Scraper is a Python program that builds an ETL pipeline to gather book information from the Books to Scrape website. It can extract data for every book in a category and optionally download every cover image.": (
            "Book Scraper est un programme Python qui construit une pipeline "
            "ETL pour récupérer les informations livres du site Books to "
            "Scrape. Il peut extraire les données de tous les livres d'une "
            "catégorie et télécharger en option toutes les couvertures."
        ),
        "First programming project": "Premier projet de programmation",
        "Web scraping, ETL pipeline, BeautifulSoup, Requests, CLI": (
            "Web scraping, pipeline ETL, BeautifulSoup, Requests, CLI"
        ),
        "Scrapes every book category": "Scrape toutes les catégories de livres",
        "Extracts data for all books in each category": (
            "Extrait les données de tous les livres de chaque catégorie"
        ),
        "Optionally downloads cover images": (
            "Télécharge les images de couverture en option"
        ),
        "Automatically navigates across pages (pagination)": (
            "Navigue automatiquement entre les pages (pagination)"
        ),
        "Exports data to CSV per category (output_data/ folder)": (
            "Exporte les données en CSV par catégorie (dossier output_data/)"
        ),
        "The command-line password assistant.": (
            "L'assistant mot de passe en ligne de commande."
        ),
        "Clinkey is a straightforward password generator. It produces strong, random passwords that follow the parameters selected by the user.\nYou can request passwords between 16 and 128 characters, composed only of letters arranged in pronounceable syllables, and optionally add digits and special characters.\nAvailable on PyPI: `pip install clinkey-cli`\nor via Homebrew: `brew tap dim-gggl/clinkey-cli && brew install clinkey-cli`.": (
            "Clinkey est un générateur de mots de passe simple et direct. Il "
            "produit des mots de passe forts et aléatoires qui respectent les "
            "paramètres choisis par l'utilisateur.\nVous pouvez demander des "
            "mots de passe de 16 à 128 caractères, composés uniquement de "
            "lettres organisées en syllabes prononçables, avec en option des "
            "chiffres et des caractères spéciaux.\nDisponible sur PyPI : "
            "`pip install clinkey-cli`\nou via Homebrew : `brew tap "
            "dim-gggl/clinkey-cli && brew install clinkey-cli`."
        ),
        "-n, --number Number of passwords to generate (1 to 1000)": (
            "-n, --number Nombre de mots de passe à générer (1 à 1000)"
        ),
        "-l, --length Password length (8 to 128 characters)": (
            "-l, --length Longueur du mot de passe (8 à 128 caractères)"
        ),
        "-t, --type [ normal | strong | super_strong ] letters | letters + digits | letters + digits + special characters": (
            "-t, --type [ normal | strong | super_strong ] lettres | lettres + chiffres | lettres + chiffres + caractères spéciaux"
        ),
        "-low, --lower Lowercase version": "-low, --lower Version en minuscules",
        "-ns, --no-sep No separator between passwords": (
            "-ns, --no-sep Aucun séparateur entre les mots de passe"
        ),
        "-s, --separator Choose the separator": (
            "-s, --separator Choisir le séparateur"
        ),
        "The password assistant.": "L'assistant mot de passe.",
        "Clinkey is a straightforward password generator. It produces strong, random passwords that follow the parameters selected by the user.\nYou can request a password between 16 and 128 characters, composed only of letters arranged in pronounceable syllables, and optionally add digits and special characters.": (
            "Clinkey est un générateur de mots de passe simple et direct. Il "
            "produit des mots de passe forts et aléatoires qui respectent les "
            "paramètres choisis par l'utilisateur.\nVous pouvez demander un mot "
            "de passe de 16 à 128 caractères, composé uniquement de lettres "
            "organisées en syllabes prononçables, avec en option des chiffres "
            "et des caractères spéciaux."
        ),
        "Number of passwords to generate (1 to 1000)": (
            "Nombre de mots de passe à générer (1 à 1000)"
        ),
        "Password length (8 to 128 characters)": (
            "Longueur du mot de passe (8 à 128 caractères)"
        ),
        "Vanilla = Letters only": "Vanilla = Lettres uniquement",
        "Strong = Letters + digits": "Strong = Lettres + chiffres",
        "Super Twisted = Letters + digits + special characters": (
            "Super Twisted = Lettres + chiffres + caractères spéciaux"
        ),
        "Built with pronounceable syllables": (
            "Construit à partir de syllabes prononçables"
        ),
        "Supports generating a very large number of passwords": (
            "Supporte la génération d'un très grand nombre de mots de passe"
        ),
        "The art collection assistant.": "L'assistant de collection d'art.",
        "Aura is an art collection management application. It helps you manage pieces, classify them, sort them, search them, share them, and add them to your collection.\nAura meets the needs of collectors from enthusiasts to experts, auctioneers, and beyond.\nAura is a responsive, accessible web application that remains extremely flexible in every aspect.": (
            "Aura est une application de gestion de collection d'art. Elle "
            "vous aide à gérer les pièces, les classer, les trier, les "
            "rechercher, les partager et les ajouter à votre collection.\n"
            "Aura répond aux besoins des collectionneurs, du passionné à "
            "l'expert, ainsi qu'aux commissaires-priseurs et plus encore.\n"
            "Aura est une application web responsive et accessible, pensée "
            "pour rester extrêmement flexible à tous les niveaux."
        ),
        "Create, update, delete a piece, an artist, an art type, supports, and techniques": (
            "Créer, modifier, supprimer une pièce, un artiste, un type d'art, des supports et des techniques"
        ),
        "Add an address book and a notebook": (
            "Ajouter un carnet d'adresses et un carnet de notes"
        ),
        "Create, manage, and track wishlists": (
            "Créer, gérer et suivre des wishlists"
        ),
        "Export detailed artwork sheets as HTML or PDF": (
            "Exporter des fiches d'œuvres détaillées en HTML ou PDF"
        ),
        "Generate suggestions of pieces to exhibit": (
            "Générer des suggestions de pièces à exposer"
        ),
        "Customizable interface with nearly twenty original themes": (
            "Interface personnalisable avec près de vingt thèmes originaux"
        ),
        "The LGBTQIA+ movie list platform.": (
            "La plateforme de listes de films LGBTQIA+."
        ),
        "kviR-Up is a dynamic web application that generates LGBTQIA+ themed movie lists.\nAnyone can create a profile, add movies, share them, and comment.\nThe art direction is inspired by a minorities galaxy, where every community is represented by a planet.": (
            "kviR-Up est une application web dynamique qui génère des listes "
            "de films à thème LGBTQIA+.\nTout le monde peut créer un profil, "
            "ajouter des films, les partager et commenter.\nLa direction "
            "artistique s'inspire d'une galaxie des minorités où chaque "
            "communauté est représentée par une planète."
        ),
        "Sign up and build your profile": "Créer un compte et construire son profil",
        "Generate random LGBTQIA+ themed movie lists": (
            "Générer des listes aléatoires de films LGBTQIA+"
        ),
        "Display dynamic content via TheMovieDB API": (
            "Afficher du contenu dynamique via l'API TheMovieDB"
        ),
        "Share and comment on lists": "Partager et commenter des listes",
        "Show your planets and the movies they contain": (
            "Afficher vos planètes et les films qu'elles contiennent"
        ),
        "Planet creation tool powered by OpenAI": (
            "Outil de création de planètes propulsé par OpenAI"
        ),
        "The Reverse Prompt Generator for Suno AI": (
            "Le générateur de reverse prompts pour Suno AI"
        ),
        "A Google Gemini powered app to analyze the content of a video (file or URL) and translate it into a Suno prompt": (
            "Une application propulsée par Google Gemini pour analyser le "
            "contenu d'une vidéo (fichier ou URL) et le traduire en prompt Suno"
        ),
        "Analyze the content of a video (file or URL)": (
            "Analyser le contenu d'une vidéo (fichier ou URL)"
        ),
        "Translate it into a Suno prompt": "Le traduire en prompt Suno",
        "Generate a style prompt based on the content of the analyzed content + the exclude prompt + the lyrics prompt including metatags": (
            "Générer un style prompt basé sur le contenu analysé + l'exclude prompt + le lyrics prompt avec métatags"
        ),
        "The Suno Prompt Architect": "L'architecte de prompts Suno",
        "A Google Gemini powered app to generate Suno prompts based on a natural language description": (
            "Une application propulsée par Google Gemini pour générer des "
            "prompts Suno à partir d'une description en langage naturel"
        ),
        "Generate a complete Suno prompt based on a natural language description with the style prompt and the exlude style + the lyrics prompt including metatags": (
            "Générer un prompt Suno complet à partir d'une description en "
            "langage naturel avec le style prompt, l'exclude style et le "
            "lyrics prompt avec métatags"
        ),
        "The Video analyzer + Prompt Generator for Video Generation (Sora 2 friendly)": (
            "L'analyseur vidéo + générateur de prompts pour la génération vidéo (compatible Sora 2)"
        ),
        "A Google Gemini powered app to analyze the content of a video (file or URL) and translate it into a Sora 2 prompt, or generate a Sora 2 prompt based on a natural language description": (
            "Une application propulsée par Google Gemini pour analyser le "
            "contenu d'une vidéo (fichier ou URL) et le traduire en prompt "
            "Sora 2, ou générer un prompt Sora 2 à partir d'une description "
            "en langage naturel"
        ),
        "Translate it into a Sora 2 prompt": (
            "Le traduire en prompt Sora 2"
        ),
        "Generate a Sora 2 prompt based on a natural language description": (
            "Générer un prompt Sora 2 à partir d'une description en langage naturel"
        ),
        "A Python framework for CLI tools projects.": (
            "Un framework Python pour les projets d'outils CLI."
        ),
        "Yotta is a Python framework that provides structure and utilities for building CLI tool projects. Built on top of Click and Rich, it gives you a solid foundation to craft beautiful, well-organized command-line applications.": (
            "Yotta est un framework Python qui fournit structure et outils "
            "pour construire des projets CLI. Construit sur Click et Rich, il "
            "offre une base solide pour créer des applications en ligne de "
            "commande élégantes et bien organisées."
        ),
        "Framework structure for CLI tool projects": (
            "Structure de framework pour les projets d'outils CLI"
        ),
        "Built on Click and Rich for styled terminal output": (
            "Construit sur Click et Rich pour une sortie terminal stylisée"
        ),
        "Opinionated project layout for maintainability": (
            "Architecture de projet opinionated orientée maintenabilité"
        ),
        "Your pocket-sized dev toolkit.": "Votre boîte à outils dev de poche.",
        "super-pocket is a developer CLI that packs the most common project utilities into a single command: README generation, full codebase export, XML tag wrapping for AI context, agent prompt templates, and dependency scanning.": (
            "super-pocket est une CLI pour développeurs qui regroupe les "
            "utilitaires les plus courants dans une seule commande : "
            "génération de README, export complet du codebase, encapsulation "
            "de balises XML pour le contexte IA, templates de prompts "
            "d'agents et analyse des dépendances."
        ),
        "README generation from codebase": (
            "Génération de README à partir du codebase"
        ),
        "Full codebase export for AI context": (
            "Export complet du codebase pour le contexte IA"
        ),
        "XML tag wrapping for agent templates": (
            "Encapsulation en balises XML pour templates d'agents"
        ),
        "Dependency scanning": "Analyse des dépendances",
        "Video specification utilities.": "Utilitaires de spécifications vidéo.",
        "A Python utility for extracting and working with video specifications and metadata.": (
            "Un utilitaire Python pour extraire et exploiter les spécifications "
            "et métadonnées vidéo."
        ),
        "Your AI-powered weekly meal planner.": (
            "Votre planificateur de repas hebdomadaire propulsé par l'IA."
        ),
        "A Google Gemini powered app that generates a full week of meals with recipes and a ready-to-use grocery shopping list, tailored to your location and favourite supermarket.": (
            "Une application propulsée par Google Gemini qui génère une "
            "semaine complète de repas avec recettes et liste de courses "
            "prête à l'emploi, adaptée à votre lieu de vie et à votre "
            "supermarché préféré."
        ),
        "Weekly meal plan with recipes": (
            "Plan de repas hebdomadaire avec recettes"
        ),
        "Grocery shopping list generation": (
            "Génération de liste de courses"
        ),
        "Adapts to your budget": "S'adapte à votre budget",
        "Adapts to your area and preferred supermarket": (
            "S'adapte à votre zone et à votre supermarché préféré"
        ),
    }
}

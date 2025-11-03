# Guide : Ajouter des images de galerie aux projets

Ce guide explique comment ajouter des images de galerie supplémentaires à vos pages de projets.

## Méthode 1 : Via le script d'import automatique (recommandé pour plusieurs images)

### Étapes :

1. **Placez vos images** dans le dossier `static/images/`

2. **Modifiez le script** `projects/management/commands/import_local_gallery_images.py`

   Ajoutez vos images dans le dictionnaire `LOCAL_GALLERY_IMAGES` :

   ```python
   LOCAL_GALLERY_IMAGES = {
       "epic_events": [
           {
               "filename": "epic-events-help.png",
               "caption": "Panneau d'aide de l'interface CLI",
               "order": 1,
           },
           # Ajoutez plus d'images ici
       ],
       "softdesk_support": [
           {
               "filename": "softdesk-screenshot-1.png",
               "caption": "Exemple d'endpoint API",
               "order": 1,
           },
       ],
       # Ajoutez d'autres projets ici
   }
   ```

3. **Testez avec dry-run** :
   ```bash
   .venv/bin/python manage.py import_local_gallery_images --dry-run
   ```

4. **Exécutez l'import** :
   ```bash
   .venv/bin/python manage.py import_local_gallery_images
   ```

5. **Pour réimporter** (supprime et recrée) :
   ```bash
   .venv/bin/python manage.py import_local_gallery_images --force
   ```

## Méthode 2 : Via l'admin Django (recommandé pour quelques images)

### Étapes :

1. **Accédez à l'admin** : http://localhost:8000/admin/

2. **Naviguez vers** : Projects → Project images

3. **Cliquez sur** "Add project image"

4. **Remplissez le formulaire** :
   - **Project** : Sélectionnez le projet
   - **Image** : Uploadez votre image
   - **Caption** : Description de l'image (optionnel)
   - **Order** : Ordre d'affichage (0 = premier)

5. **Cliquez sur** "Save"

## Méthode 3 : Programmatiquement via le shell Django

```bash
.venv/bin/python manage.py shell
```

```python
from projects.models import Project, ProjectImage
from django.core.files import File

# Récupérer le projet
project = Project.objects.get(slug='epic_events')

# Créer une image de galerie
with open('static/images/mon-image.png', 'rb') as f:
    gallery_img = ProjectImage(
        project=project,
        caption="Description de l'image",
        order=2
    )
    gallery_img.image.save('mon-image.png', File(f), save=True)

print(f"Image ajoutée ! Total: {project.gallery_images.count()}")
```

## Structure des images dans le template

Les images de galerie apparaissent dans la section "Captures d'écran" du template `project_detail.html` :

```django
{% if project.gallery_images.all %}
<section class="bg-[var(--color-bg-primary)] py-16 px-4">
  <div class="max-w-6xl mx-auto">
    <h2>Captures <span class="accent-color">d'écran</span></h2>
    <div class="grid md:grid-cols-2 gap-8">
      {% for image in project.gallery_images.all %}
        <div class="group">
          <div class="relative overflow-hidden rounded-xl">
            <img src="{{ image.image.url }}" alt="{{ image.caption }}">
            {% if image.caption %}
              <div class="absolute bottom-0">
                <p>{{ image.caption }}</p>
              </div>
            {% endif %}
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
</section>
{% endif %}
```

## Images actuellement importées

- **epic events** : 1 image
  - `epic-events-help.png` - Panneau d'aide de l'interface CLI

## Images disponibles dans static/images/ mais non importées

Vous avez ces images prêtes à être importées :
- `aura_title.png` → featured_image (déjà configuré)
- `clinkey-cli-title.png` → featured_image (déjà configuré)
- `Chess_Up_title.png` → featured_image (déjà configuré)
- `Book_Scraper_title.png` → featured_image (déjà configuré)
- `lit-review-title.png` → featured_image (déjà configuré)
- `ClinKey_dark.png` → À ajouter comme gallery image
- `ClinKey_light.png` → À ajouter comme gallery image

## Exemple : Ajouter les thèmes Clinkey

Modifiez `import_local_gallery_images.py` :

```python
LOCAL_GALLERY_IMAGES = {
    "epic_events": [
        # ... existant
    ],
    "Clinkey": [
        {
            "filename": "ClinKey_light.png",
            "caption": "Interface avec thème clair",
            "order": 1,
        },
        {
            "filename": "ClinKey_dark.png",
            "caption": "Interface avec thème sombre",
            "order": 2,
        },
    ],
}
```

Puis exécutez :
```bash
.venv/bin/python manage.py import_local_gallery_images
```

## Résolution des problèmes

### L'image n'apparaît pas
- Vérifiez que `MEDIA_URL` et `MEDIA_ROOT` sont configurés dans `settings.py`
- Vérifiez que les URLs media sont configurées dans `urls.py`
- Assurez-vous que le serveur de développement sert les fichiers media

### L'image est trop grande
- Les images sont automatiquement optimisées via `core.utils.optimize_image()`
- Les dimensions recommandées : 1200x800px pour les gallery images

### Erreur d'import
- Vérifiez que le fichier existe dans `static/images/`
- Vérifiez que le slug du projet est correct
- Utilisez `--dry-run` pour tester avant l'import réel

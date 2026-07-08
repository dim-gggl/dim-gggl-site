```markdown
                    __                                
                   /\ \  __                           
                   \_\ \/\_\    ___ ___               
                   /'_` \/\ \ /' __` __`\             
                  /\ \L\ \ \ \/\ \/\ \/\ \            
                  \ \___,_\ \_\ \_\ \_\ \_\  ___      
                   \/__,_ /\/_/\/_/\/_/\/_/ /\_ \     
                         __      __      __ \//\ \    
                       /'_ `\  /'_ `\  /'_ `\ \ \ \   
                      /\ \L\ \/\ \L\ \/\ \L\ \ \_\ \_ 
                      \ \____ \ \____ \ \____ \/\____\
                       \/___L\ \/___L\ \/___L\ \/____/
                         /\____/ /\____/ /\____/      
                         \_/__/  \_/__/  \_/__/        
```
<div align="center">
  <a href="https://dim-gggl.com">
    <img alt="Static Badge" src="https://img.shields.io/badge/click-me-%23ef0041?style=plastic">
  </a>
</div>

## Architecture

- **Backend** — Django 5 (Python). Serves a JSON API under `/api/`
  (content, projects, localization) plus the SPA shell, sitemap,
  robots.txt, and the admin.
- **Frontend** — React 18 + Vite + Tailwind CSS 4 + Framer Motion,
  in [`frontend/`](frontend/). Built assets land in `static/frontend/`
  and are served by Django/WhiteNoise.
- **Localization** — EN/FR catalog lives in
  `core/localization/content_catalog.py`; the API localizes every
  payload through `?lang=`.

## Development

```bash
# Backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver  # http://127.0.0.1:8000

# Frontend (dev server with API proxy to :8000)
cd frontend
npm install
npm run dev

# Or build the frontend and let Django serve everything
npm run build
```

## Tests

```bash
pytest
```

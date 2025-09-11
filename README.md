Hayma Grocery - Full-Stack Grocery Management System

Backend: Django REST Framework with JWT auth and CORS.
Frontend: HTML + TailwindCSS (CDN) + vanilla JS modules.

Quick start
1) Python env
   - py -m venv .venv
   - .venv\Scripts\pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
2) Django
   - cd hayma
   - ..\.venv\Scripts\python manage.py migrate
   - ..\.venv\Scripts\python manage.py createsuperuser
   - ..\.venv\Scripts\python manage.py runserver 0.0.0.0:8000
3) Frontend
   - Open frontend/index.html in a browser (or serve statically)

Main API endpoints
- Auth: POST /api/accounts/register/; POST /api/accounts/login/; GET/PUT /api/accounts/profile/
- Catalog: /api/catalog/categories/, /api/catalog/products/, /api/catalog/coupons/
- Cart: GET /api/cart/, POST/PUT/DELETE /api/cart/items/
- Orders: GET/POST /api/orders/, POST /api/orders/{id}/set_status/ (admin)

Notes
- Set DEBUG=False and configure ALLOWED_HOSTS before production.
- JWT stored in localStorage. For production use secure storage and HTTPS.

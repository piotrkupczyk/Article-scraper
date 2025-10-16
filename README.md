Article-scraper to mała aplikacja Django + DRF. Zbiera artykuły z podanych adresów (requests + trafilatura/readability), normalizuje datę publikacji, zapisuje w PostgreSQL i udostępnia API (lista/detal) z filtrowaniem, wyszukiwaniem, sortowaniem i paginacją. Projekt ma też opcjonalny Docker Compose (web + db).

Wymagania: Python 3.12, PostgreSQL 14+, opcjonalnie Docker Desktop 4.x.

Struktura projektu (najważniejsze): manage.py, sraper/ (settings/urls), news/ (models, serializers, views, filters, scraping/parsers.py, management/commands/scrape_articles.py, tests), oraz Dockerfile i docker-compose.yml (opcjonalnie).

Szybki start lokalnie:

Utwórz i aktywuj wirtualne środowisko, zainstaluj zależności:
python -m venv .venv
..venv\Scripts\activate
pip install -r requirements.txt

Utwórz plik .env w UTF-8 i wklej:
DJANGO_DEBUG=True
SECRET_KEY=dev-secret
ALLOWED_HOSTS=*
POSTGRES_DB=articles
POSTGRES_USER=postgres
POSTGRES_PASSWORD=gambling (w tym przypadku twoje haslo)
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
SCRAPER_TIMEZONE=Europe/Warsaw
(opcjonalnie) SCRAPER_URLS=https://example.com/a,https://example.com/b

Uruchom migracje i serwer:
python manage.py check
python manage.py migrate
python manage.py runserver
Aplikacja jest pod http://127.0.0.1:8000

Scraping (komenda zarządzania):
– Jednorazowo z listą URL-i:
python manage.py scrape_articles --urls "https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie,https://galicjaexpress.pl/bmw-e9-30-cs-szczegolowe-informacje-o-osiagach-i-historii-modelu,https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa,https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow
"
– Albo bez --urls, jeśli SCRAPER_URLS jest ustawione w .env:
python manage.py scrape_articles
Komenda pobiera HTML, wydobywa treść (trafilatura → fallback readability + BeautifulSoup), normalizuje datę (różne formaty i strefy; jeśli brak godziny, ustawia 00:00:00), a następnie zapisuje rekord, pilnując unikalności po source_url.

REST API:
– Lista: GET /articles/
Parametry: ?source=DOMENA, ?search=FRAZA, ?ordering=(published_at|created_at|updated_at z prefiksem - dla malejąco), ?page=N.
Listing jest lekki: zwraca m.in. id, title, source_url, source_domain, published_at, published_at_str (format dd.mm.yyyy HH:mm:ss, strefa Europe/Warsaw) i text_excerpt (krótki skrót tekstu). Celowo nie zawiera pełnego html_content.
– Detal: GET /articles/{id}/
Zwraca pełne html_content i text_content oraz wszystkie metadane.
Przykłady:
curl "http://127.0.0.1:8000/articles/?source=galicjaexpress.pl
"
curl "http://127.0.0.1:8000/articles/?search=kurczaka&ordering=-published_at
"
curl "http://127.0.0.1:8000/articles/1/
"

Uwagi o treści i dacie:
– Strony renderowane JS-em (bez SSR) mogą nie mieć pełnej treści po samym GET; fallback readability + BeautifulSoup próbuje odzyskać artykuł, ale text_content może być krótszy lub pusty.
– Daty są lokalizowane; w API oprócz ISO jest także published_at_str w formacie dd.mm.yyyy HH:mm:ss.

CORS (opcjonalnie, jeśli front jest na innym originie):
– Zainstaluj: pip install django-cors-headers
– W settings.py dodaj do INSTALLED_APPS: "corsheaders"
– W MIDDLEWARE dodaj na górze: "corsheaders.middleware.CorsMiddleware"
– Na czas developmentu: CORS_ALLOW_ALL_ORIGINS = True

Docker Compose (opcjonalnie):
– Uruchom: docker compose up --build
– Aplikacja: http://localhost:8000/articles/

– Scraping w kontenerze:
docker compose exec web python manage.py scrape_articles --urls "URL1,URL2,URL3,URL4"
– Trwałość danych: w docker-compose.yml dodaj volumes dla usługi db: db-data:/var/lib/postgresql/data oraz sekcję volumes na dole. Jeśli na hoście działa PostgreSQL na 5432, zmień mapowanie portu kontenera na 5433:5432 albo podłącz web do hostowej bazy przez POSTGRES_HOST=host.docker.internal.

Testy (opcjonalnie):
– Uruchom: pytest -q
– Testy sprawdzają status 200 dla listy i detalu, działanie filtrowania i wyszukiwania oraz to, że listing nie zwraca pełnego html_content.

Troubleshooting:
– UnicodeDecodeError przy łączeniu do Postgresa: plik .env musi być UTF-8; hasło bez polskich znaków; w settings.py możesz ustawić: DATABASES["default"]["OPTIONS"] = {"options": "-c client_encoding=UTF8"}.
– /articles/?source= bez wartości: filtr ignoruje pustą wartość; jeżeli widzisz 500, sprawdź traceback w runserver (najczęściej literówka w serializerze lub brak migracji).
– Pusty listing w Dockerze: kontenerowa baza jest świeża — odpal scraping w kontenerze lub podłącz web do hostowej bazy.
– Duże payloady: pełny html_content jest tylko w detalu; listing zwraca excerpt.

Licencja: MIT.
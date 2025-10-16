# Article-scraper

scraper artykułów (Django + DRF)

## wymagania

\- Python 3.12

\- PostgreSQL 14+



\## instalacja

```bash

python -m venv .venv

.\\.venv\\Scripts\\activate

pip install -r requirements.txt



\## migracja - start

python manage.py check

python manage.py migrate

python manage.py runserver



\## jednorazowa komenda scrapujaca


python manage.py scrape\_articles --urls "https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie,https://galicjaexpress.pl/bmw-e9-30-cs-szczegolowe-informacje-o-osiagach-i-historii-modelu,https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa,https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow"




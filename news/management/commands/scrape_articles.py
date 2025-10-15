import os
import logging
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from news.models import Article
from news.scraping.parsers import scrape_one

log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Scrape predefined list of articles (env SCRAPER_URLS or --urls) and save to DB"

    def add_arguments(self, parser):
        parser.add_argument("--urls", type=str, help="Comma-separated URLs (overrides env)")

    def handle(self, *args, **opts):
        urls_env = opts.get("urls") or os.getenv("SCRAPER_URLS", "")
        urls = [u.strip() for u in urls_env.split(",") if u.strip()]
        if not urls:
            self.stderr.write(self.style.ERROR("No URLs provided. Set SCRAPER_URLS or pass --urls"))
            return

        self.stdout.write(self.style.NOTICE(f"Starting scraping {len(urls)} article(s)..."))

        for i, url in enumerate(urls, start=1):
            self.stdout.write(f"[{i}/{len(urls)}] {url}")
            if Article.objects.filter(source_url=url).exists():
                self.stdout.write(self.style.WARNING("already in DB, skipping"))
                continue
            try:
                data = scrape_one(url, base_tz=os.getenv("SCRAPER_TIMEZONE", "Europe/Warsaw"))
                with transaction.atomic():
                    Article.objects.create(**data)
                self.stdout.write(self.style.SUCCESS("saved"))
            except IntegrityError:
                self.stdout.write(self.style.WARNING("duplicate, skipping"))
            except Exception as e:
                log.exception("Error scraping %s", url)
                self.stderr.write(self.style.ERROR(f"error: {e}"))

        self.stdout.write(self.style.SUCCESS("Done."))

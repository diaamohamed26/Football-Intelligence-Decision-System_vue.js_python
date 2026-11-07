
from django.core.management.base import BaseCommand

from football_news.services import sync_football_news


class Command(BaseCommand):
    help = "Fetch and synchronize global football news"

    def handle(self, *args, **options):
        self.stdout.write("Fetching global football news...")

        result = sync_football_news()

        self.stdout.write(
            self.style.SUCCESS(
                f"Sources checked: {result['sources']}"
            )
        )

        self.stdout.write(
            f"New articles: {result['created']}"
        )

        self.stdout.write(
            f"Updated articles: {result['updated']}"
        )

        for error in result["errors"]:
            self.stderr.write(
                f"{error['source']}: {error['error']}"
            )

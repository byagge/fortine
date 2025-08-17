from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Site, Page
from home.models import (
    HomePage, IndexPage, AnswersPage, AccountPage, 
    DepositPage, HistoryPage, OpenCasePage, ScrollCasePage, 
    RequestsPage, LoginPage
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup Wagtail pages for the site'

    def handle(self, *args, **options):
        # Get or create superuser
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin'))

        # Get root page
        root_page = Page.objects.get(id=1)
        
        # Create homepage if it doesn't exist
        if not HomePage.objects.exists():
            self.stdout.write('Creating homepage...')
            homepage = HomePage(
                title="Home",
                slug="home",
                intro="Welcome to our site!"
            )
            root_page.add_child(instance=homepage)
            self.stdout.write(self.style.SUCCESS('Homepage created'))

        # Create other pages
        pages_data = [
            (IndexPage, "index", "Index", "Main page"),
            (AnswersPage, "answers", "Answers", "FAQ page"),
            (AccountPage, "account", "Account", "User account page"),
            (DepositPage, "deposit", "Deposit", "Deposit funds page"),
            (HistoryPage, "history", "History", "Transaction history page"),
            (OpenCasePage, "opencase", "Open Case", "Open case page"),
            (ScrollCasePage, "scrollcase", "Scroll Case", "Scroll case page"),
            (RequestsPage, "requests", "Requests", "Support requests page"),
            (LoginPage, "login", "Login", "Login page"),
        ]

        for page_class, slug, title, description in pages_data:
            if not page_class.objects.filter(slug=slug).exists():
                self.stdout.write(f'Creating {title} page...')
                page = page_class(
                    title=title,
                    slug=slug,
                    intro=description
                )
                root_page.add_child(instance=page)
                self.stdout.write(self.style.SUCCESS(f'{title} page created'))

        # Create or update site
        if not Site.objects.exists():
            self.stdout.write('Creating site...')
            homepage = HomePage.objects.first()
            if homepage:
                site = Site.objects.create(
                    hostname='localhost',
                    port=8000,
                    root_page=homepage,
                    is_default_site=True,
                    site_name='Fortine'
                )
                self.stdout.write(self.style.SUCCESS('Site created'))

        self.stdout.write(self.style.SUCCESS('Wagtail pages setup completed!'))
        self.stdout.write('You can now access the admin at /admin/')
        self.stdout.write('Login with: admin/admin') 
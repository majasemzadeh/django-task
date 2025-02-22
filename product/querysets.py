from django.db.models import QuerySet


class ProductQuerySet(QuerySet):
    def needs_restock(self):
        """Return a queryset of products with stock less than 10."""
        return self.filter(stock__lt=10)

    def in_stock(self):
        return self.filter(stock__gt=10)

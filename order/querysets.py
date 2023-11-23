from django.db.models import QuerySet, Sum


class OrderQuerySet(QuerySet):
    def by_customer(self, customer):
        return self.filter(customer=customer)

    def total_price(self):
        return self.aggregate(total_price=Sum('total_price')).get('total_price') or 0

    def total_price_by_customer(self, customer):
        return self.by_customer(customer).total_price()

    def submitted_in_date(self, date_value):
        return self.filter(date__date=date_value)

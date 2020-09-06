from decimal import Decimal

from book import choices

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Price(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    price_period = models.DecimalField(
        max_digits=6, decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(0)])
    days_period = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class Category(Price):
    name = models.CharField(max_length=52)

    class Meta:
        verbose_name_plural = 'categories'


class Book(models.Model):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class BookRent(Price):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    end = models.DateField(null=True)
    status = models.PositiveSmallIntegerField(choices=choices.BOOK_STATUSES,
                                              default=choices.BOOK_STATUS_PENDING)

    def get_price(self):
        count_history = self.rentdayhistory_set.count()
        if count_history < self.days_period:
            return self.price_period
        return self.price

    def save(self, *args, **kwargs):

        if self.price is None:
            self.price = self.book.category.price
            self.price_period = self.book.category.price_period
            self.days_period = self.book.category.days_period

        created = self.pk is None

        if not created:
            old_instance = self.__class__.objects.only('status').get(pk=self.pk)
            # check if status was changed from confirmed to in_use to create RentDayHistory for first day of use
            if self.status == choices.BOOK_STATUS_IN_USE and \
                    old_instance.status == choices.BOOK_STATUS_CONFIRMED:
                self.rentdayhistory_set.get_or_create(
                    created=timezone.now().date(),
                    amount=self.get_price(),
                )
            # check if rent was finalized
            elif not self.end and \
                    self.status == choices.BOOK_STATUS_END and \
                    old_instance.status != choices.BOOK_STATUS_END:
                self.end = timezone.now().date()

        super().save(*args, **kwargs)


BookRent._meta.get_field('price').help_text = 'This price should not be affected after rent started'


class RentDayHistory(models.Model):
    rent = models.ForeignKey(BookRent, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateField(auto_now_add=True)

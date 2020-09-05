from book import choices

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=52)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])


class Book(models.Model):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class BookRent(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    end = models.DateField(null=True)
    status = models.PositiveSmallIntegerField(choices=choices.BOOK_STATUSES,
                                              default=choices.BOOK_STATUS_PENDING)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)],
                                help_text='This price should not be affected after rent started')

    def save(self, *args, **kwargs):

        if self.price is None:
            self.price = self.book.category.price

        created = self.pk is None

        if not created:
            old_instance = self.__class__.objects.only('status').get(pk=self.pk)
            # check if status was changed from confirmed to in_use to create RentDayHistory for first day of use
            if self.status == choices.BOOK_STATUS_IN_USE and \
                    old_instance.status == choices.BOOK_STATUS_CONFIRMED:
                self.rentdayhistory_set.get_or_create(
                    created=timezone.now().date(),
                    amount=self.price,
                )
            # check if rent was finalized
            elif not self.end and \
                    self.status == choices.BOOK_STATUS_END and \
                    old_instance.status != choices.BOOK_STATUS_END:
                self.end = timezone.now().date()

        super().save(*args, **kwargs)


class RentDayHistory(models.Model):
    rent = models.ForeignKey(BookRent, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    created = models.DateField(auto_now_add=True)

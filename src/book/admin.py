from book.models import BookRent, Category, RentDayHistory

from django.contrib import admin


class RentDayHistoryInline(admin.TabularInline):
    model = RentDayHistory
    fields = ('id', 'amount', 'created')
    readonly_fields = fields
    can_delete = False
    extra = 0

    def has_add_permission(self, request, **kwargs):
        return False


class BookRentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'book_id', 'status', 'end')
    list_filter = ('status', )
    readonly_fields = ('user', 'book', 'end', 'price', 'price_period', 'days_period')
    ordering = ('-id',)
    inlines = (RentDayHistoryInline, )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'days_period', 'price_period')
    readonly_fields = ('id', )
    ordering = ('-id',)


admin.site.register(BookRent, BookRentAdmin)
admin.site.register(Category, CategoryAdmin)

from book.models import BookRent, RentDayHistory

from django.contrib import admin


class RentDayHistoryInline(admin.TabularInline):
    model = RentDayHistory
    fields = ('id', 'amount', 'created')
    readonly_fields = fields
    can_delete = False
    extra = 0

    def has_add_permission(self, request):
        return False


class BookRentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'book_id', 'status', 'end')
    list_filter = ('status', )
    readonly_fields = ('user', 'book', 'end')
    ordering = ('-id',)
    inlines = (RentDayHistoryInline, )


admin.site.register(BookRent, BookRentAdmin)

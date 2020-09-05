from book.models import Book, BookRent

from django import forms


class BookRentForm(forms.ModelForm):
    book_title = forms.CharField(max_length=256, required=False)

    class Meta:
        model = BookRent
        fields = ('book_title', 'book')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        if request.method == 'GET':
            self.fields['book'].queryset = Book.objects.none()
        else:
            self.fields['book'].queryset = Book.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.request.user
        instance.save()
        return instance

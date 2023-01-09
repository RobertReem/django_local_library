from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

class AuthorsInstanceInline(admin.TabularInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [AuthorsInstanceInline]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    #remove the extra (empty placeholder) book instances 
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    inlines = [BooksInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )



# Register your models below.

#admin.site.register(Author)
admin.site.register(Author, AuthorAdmin)

#admin.site.register(Book)
admin.site.register(Book, BookAdmin)

#admin.site.register(BookInstance)
admin.site.register(BookInstance, BookInstanceAdmin)

admin.site.register(Genre)
admin.site.register(Language)
from django.contrib import admin
# from django.template import Library

from library.models import Author, Book, Category, Library, Member, Post, Borrow, Review, AuthorDetail, Event, \
    EventParticipant

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Library)
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Borrow)
admin.site.register(Review)
admin.site.register(AuthorDetail)
admin.site.register(Event)
admin.site.register(EventParticipant)

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from library.managers import SoftDeleteManager


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    profile = models.URLField(null=True, blank=True, verbose_name="Profile URL")
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Is Deleted",
        help_text="When the author is deleted is set False"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)
                    ],
        null=True,
        blank=True,
        verbose_name="Rating in AWS",
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


genre_choice = [
    ('Fiction', 'Fiction'),
    ('Non Fiction', 'Non-Fiction'),
    ('Sci-Fy', 'Science Fiction'),
    ('Fantasy', 'Fantasy'),
    ('Mystery', 'Mystery'),
    ('Biography', 'Biography'),
    ('Default', 'not_set')
]


# creating a model Publisher
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True, default='publisher')
    established_date = models.DateField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, verbose_name="Genre", choices=genre_choice)

    def __str__(self):
        return self.name


# creating a model Book
class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Book Title", blank=False)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, verbose_name="Author", null=True)
    publication_date = models.DateField(null=True, blank=False, verbose_name="Publication Date")
    description = models.TextField(null=True, blank=True, verbose_name="Summary")
    genres = models.ManyToManyField(Genre, related_name='books')
    amount_pages = models.PositiveIntegerField(null=True, blank=True, verbose_name="Amount of Pages",
                                               validators=[MaxValueValidator(10_000)])
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="Publisher", null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="Created at")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, verbose_name="Category", null=True,
                                 related_name='books')
    libraries = models.ManyToManyField("Library", related_name='books', verbose_name="Library")
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Price")
    is_banned = models.BooleanField(default=False, verbose_name="Is Banned")
    is_deleted = models.BooleanField(default=False)  # Поле для мягкого удаления

    @property
    def rating(self):
        return self.reviews.all().aggregate(models.Avg('rating'))['rating__avg']

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """Переопределяем стандартный метод удаления."""
        self.is_deleted = True  # Устанавливаем флаг
        self.save()  # Сохраняем изменения

    def restore(self):
        """Метод для восстановления записи."""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Category Title", unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "Categories"


class Library(models.Model):
    title = models.CharField(max_length=100, verbose_name="Library Title", blank=False)
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name="Location")
    website = models.URLField(null=True, blank=True, verbose_name="Website")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = "Libraries"


gender_choices = [
    ('M', 'Male'),
    ('F', 'Female')
]

role_choices = [
    ('A', 'Administrator'),
    ('B', 'Reader'),
    ('E', 'Employee')
]


class Member(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(null=False, blank=False, verbose_name="Email", unique=True)
    gender = models.CharField(max_length=20, verbose_name="Gender", choices=gender_choices)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    age = models.PositiveIntegerField(verbose_name="Age", editable=False)
    role = models.CharField(max_length=30, verbose_name="Role", choices=role_choices)
    active = models.BooleanField(default=True, verbose_name="Is_active")
    libraries = models.ManyToManyField("Library", related_name='members', verbose_name="Library")

    def save(self, *args, **kwargs):
        ages = timezone.now().year - self.date_of_birth.year
        if 6 <= ages < 120:
            self.age = ages
            super().save(*args, **kwargs)
        else:
            raise ValidationError("Age must be between 6 and 120")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Post(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at')
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name="Title")
    text = models.TextField(null=False, blank=False, verbose_name="Text")
    author = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Author")
    moderated = models.BooleanField(default=False, verbose_name="Moderated?")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name="Library")
    updated_at = models.DateTimeField(auto_now=True)


class Borrow(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Member")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="Book")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name="Library")
    book_take_date = models.DateField(auto_now_add=True, verbose_name="Book Take Date")
    book_return_date = models.DateField(verbose_name="Book Return Date")
    is_returned = models.BooleanField(default=False, verbose_name="Is returned?")

    def __str__(self):
        return f'{self.member.first_name} {self.member.last_name} took "{self.book.title}" on {self.book_take_date}'

    def check_to_date(self):
        if timezone.now().date() > self.book_return_date and self.is_returned == False:
            return True
        else:
            return False
    # use python manage.py shell
    # from library.models import Borrow
    # a = Borrow.object.get(pk=<borrow id>)
    # a.check_to_date()
    # result: True or False


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="Book", related_name='reviews')
    reviewer = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Reviewer")
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Rating")
    review = models.TextField(verbose_name="Review")


class AuthorDetail(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="Author")
    biography = models.TextField(verbose_name="Biography")
    city = models.CharField(verbose_name="City", max_length=50, null=True, blank=True)
    gender = models.CharField(verbose_name="Gender", max_length=20, choices=gender_choices)

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name} from {self.city} born on {self.author.date_of_birth}.'


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name="Event name")
    description = models.TextField(verbose_name="Event description")
    timestamp = models.DateTimeField(verbose_name="Event date")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name="Library")
    book = models.ManyToManyField('Book', verbose_name="Books", related_name='events')

    def __str__(self):
        return f'{self.name} on {self.timestamp}'


class EventParticipant(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name="Event name")
    member = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name="Member")
    register_date = models.DateField(auto_now_add=True, verbose_name="Register date")

    def __str__(self):
        return f'{self.event.name}. Member: {self.member.first_name} {self.member.last_name} registered on {self.register_date}'


# creating a list of countries
countries = [
    ('DE', 'Germany'),
    ('UK', 'United Kingdom'),
    ('US', 'United States'),
    ('PT', 'Portugal'),
    ('FR', 'France'),
    ('ES', 'Spain'),
    ('IT', 'Italy'),
]


# creating a model User
class User(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=70, verbose_name='Family name', null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)])
    rating = models.FloatField(default=0.0)
    country = models.CharField(choices=countries, default='DE', verbose_name="Country")


# creating a model UserInfo
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Info")
    married = models.BooleanField(verbose_name="Married?")


# creating a model Actor
class Actor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


# creating a model Director
class Director(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


# creating a model Movie
class Movie(models.Model):
    title = models.CharField(max_length=50)
    actors = models.ManyToManyField(Actor, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, related_name='movies', null=True, blank=True)

    def __str__(self):
        if self.director:
            return f'Title: "{self.title}" | Director: {self.director.name}'
        return f'{self.title}'

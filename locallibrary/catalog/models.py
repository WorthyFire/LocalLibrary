import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Укажите жанр книги (например, научная фантастика, французская поэзия и т.д.).")

    def __str__(self):

        return self.name

class Language(models.Model):

    name = models.CharField(max_length=200,
                            help_text="Введите естественный язык книги (например, английский, французский, японский и т.д.).")

    def __str__(self):

        return self.name
class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для этой книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):

        return self.title


    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):

        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор для этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Не исправна'),
        ('o', 'Выдан'),
        ('a', 'Доступна'),
        ('r', 'Забронирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
    def __str__(self):
        return f'{self.book.title}, {self.get_status_display()}, Due:{self.due_back}, ID: {self.id}'


class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):

        return '{0}, {1}'.format(self.last_name, self.first_name)


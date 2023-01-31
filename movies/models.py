import uuid
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class TypeGenre(models.TextChoices):

        ACTION = 'Action' , 'Боевик'
        WEATERN = 'Western' , 'Вестерн'
        GANGSTER = 'Gangster movie' , 'Гангстерский фильм'
        DETECTIVE = 'Detective', 'Детектив'
        DRAMA = 'Drama' , 'Драма'
        HISTORICAL = 'Historical film' , 'Исторический фильм'
        COMEDY = 'Comedy' , 'Комедия'
        MELODRAMA = 'Melodrama' , 'Мелодрама'
        MUSICAL = 'Musical film' , 'Музыкальный фильм'
        NOIR = 'Noir' , 'Нуар'
        POLITICAL = 'Political film' , 'Политический фильм'
        ADVENTURE = 'Adventure movie' , 'Приключенческий фильм'
        FAIRYTALE = 'Fairy tale' , 'Сказка'
        TRAGEDY = 'Tragedy' , 'Трагедия'
        TRAGICOMEDY = 'Tragicomedy' , 'Трагикомедия'
        THRILLER = 'Thriller' , 'Триллер'
        FANTASY = 'Fantasy movie' , 'Фантастический фильм'
        HORROR = 'Horror' , 'Фильм ужасов'
        DISASTER = 'Disaster movie' , 'Фильм - катастрофа'

class Genre(UUIDMixin, TimeStampedMixin):

    name = models.CharField(_('name'), max_length=30, choices=TypeGenre.choices, default=TypeGenre.MELODRAMA, )
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name
class TypeFilms(models.TextChoices):
        MOVIES = 'MV', ('Movies')
        TV_SHOWS = 'TV', ('TV Show')

class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    type = models.CharField(_('type'), max_length=2, choices=TypeFilms.choices, default=TypeFilms.MOVIES, )

    def __str__(self):
        return self.title

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Film')
        verbose_name_plural = _('Film work')

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"

class Person(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    full_name = models.CharField(_('full name'), max_length=255)
    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"person"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('actor')
        verbose_name_plural = _('actors')

    def __str__(self):
        return self.full_name

class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
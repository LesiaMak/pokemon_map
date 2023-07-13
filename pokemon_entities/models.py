from django.db import models  # noqa F401

class Pokemon(models.Model):
	title = models.CharField(verbose_name='Покемон',max_length=200, null=True)
	title_en = models.CharField(verbose_name='Название покемона на английском',max_length=200, blank=True)
	title_jp = models.CharField(verbose_name='Название покемона на японском',max_length=200, blank=True)
	image = models.ImageField(verbose_name='Изображение покемона',upload_to='images', null=True)
	description = models.TextField(verbose_name='Описание покемона', blank=True)
	pre_evol = models.ForeignKey("self",verbose_name='Эволюционировал из', related_name='next_evol', on_delete=models.SET_NULL, null=True, blank=True)


	def __str__(self):
		return self.title


class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', related_name = 'pokemon_entities', on_delete=models.CASCADE)
	lat = models.FloatField(verbose_name='Широта',null=True)
	lon = models.FloatField(verbose_name='Долгота',null=True)
	appeared_at = models.DateTimeField(verbose_name='Появился в', null=True)
	disappeared_at = models.DateTimeField(verbose_name='Исчезнет в',null=True)
	level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
	health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
	strength = models.IntegerField(verbose_name='Сила',null=True, blank=True)
	defence = models.IntegerField(verbose_name='Зашита', null=True, blank=True)
	stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

	def __str__(self):
		return self.pokemon.title
from django.db import models  # noqa F401

class Pokemon(models.Model):
	title = models.CharField(max_length=200, blank=True)
	image = models.ImageField(upload_to='images', null=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.title


class PokemonEntity(models.Model):
	title = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
	lat = models.FloatField(null=True)
	lon = models.FloatField(null=True)
	appeared_at = models.DateTimeField(null=True)
	disappeared_at = models.DateTimeField(null=True)
	level = models.IntegerField(null=True, blank=True)
	health = models.IntegerField(null=True, blank=True)
	strength = models.IntegerField(null=True, blank=True)
	defence = models.IntegerField(null=True, blank=True)
	stamina = models.IntegerField(null=True, blank=True)
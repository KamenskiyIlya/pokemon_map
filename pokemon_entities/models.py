from django.db import models  # noqa F401


class Pokemon(models.Model):
	name = models.CharField(max_length=200)
	photo = models.ImageField(upload_to='pokemon_imgs', null=True, blank=True)
	name_en = models.CharField(max_length=200)
	name_jp = models.CharField(max_length=200)
	description = models.TextField()

	previous_evolution = models.ForeignKey(
		'self',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='next_evolution'
	)

	def __str__(self):
		return f'{self.name}'

class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(Pokemon, on_delete= models.CASCADE)
	lat = models.FloatField()
	lon = models.FloatField()
	appeared_at = models.DateTimeField()
	disappeared_at = models.DateTimeField()
	level = models.IntegerField(null=True, blank=True)
	health = models.IntegerField(null=True, blank=True)
	strength = models.IntegerField(null=True, blank=True)
	defence = models.IntegerField(null=True, blank=True)
	stamina = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return f'{self.pokemon.name} уровень:{self.level} коор-ты:{self.lat} {self.lon}'

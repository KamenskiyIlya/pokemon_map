from django.db import models  # noqa F401


class Pokemon(models.Model):
	name = models.CharField(max_length=200)
	photo = models.ImageField(upload_to='pokemon_imgs', null=True, blank=True)

	def __str__(self):
		return f'{self.name}'

class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(Pokemon, on_delete= models.CASCADE)
	lat = models.FloatField()
	lon = models.FloatField()
	appeared_at = models.DateTimeField()
	disappeared_at = models.DateTimeField()

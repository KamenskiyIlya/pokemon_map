from django.db import models  # noqa F401


class Pokemon(models.Model):
	name = models.CharField(max_length=200, verbose_name="Имя (ru)")
	photo = models.ImageField(
		upload_to='pokemon_imgs',
		null=True,
		blank=True,
		verbose_name="Фото покемона"
	)
	name_en = models.CharField(default=' ', max_length=200, blank=True, verbose_name="Имя (en)")
	name_jp = models.CharField(default=' ', max_length=200, blank=True, verbose_name="Имя (jp)")
	description = models.TextField(default=' ', blank=True, verbose_name="Описание")

	previous_evolution = models.ForeignKey(
		'self',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='next_evolutions',
		verbose_name="Предыдущие эволюции"
	)

	def __str__(self):
		return f'{self.name}'

class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(
		Pokemon,
		on_delete= models.CASCADE,
		verbose_name="Покемон",
		related_name='entitys'
	)
	lat = models.FloatField(verbose_name="Широта")
	lon = models.FloatField(verbose_name="Долгота")
	appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Когда появится")
	disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Когда исчезнет")
	level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
	health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
	strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
	defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
	stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")

	def __str__(self):
		return f'{self.pokemon.name} уровень:{self.level} коор-ты:{self.lat} {self.lon}'

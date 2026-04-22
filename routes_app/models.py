from django.db import models
from django.core.exceptions import ValidationError


class AirportRoute(models.Model):
	DIRECTION_CHOICES = [
		('left', 'Left'),
		('right', 'Right'),
	]

	airport_code = models.CharField(max_length=1, unique=True)
	position = models.PositiveIntegerField(unique=True)
	direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, default='left')
	duration = models.PositiveIntegerField(help_text='Duration in minutes for this node segment.')

	class Meta:
		ordering = ['position']
		constraints = [
			models.CheckConstraint(
				check=~models.Q(airport_code__in=['I', 'O']),
				name='airport_code_not_i_or_o',
			),
		]

	def clean(self):
		code = (self.airport_code or '').upper()
		if not code.isalpha() or len(code) != 1:
			raise ValidationError({'airport_code': 'Use a single alphabetic letter (A-Z).'})
		if code in {'I', 'O'}:
			raise ValidationError({'airport_code': 'This airport code is not allowed.'})
		self.airport_code = code

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.airport_code} (pos {self.position}, {self.direction}, {self.duration} min)'

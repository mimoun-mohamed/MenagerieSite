from django.db import models
from django.utils import timezone
from django import forms


class Equipment(models.Model):
    LITTER = 'LI'
    WHEEL = 'WH'
    NEST = 'NE'
    FEEDER = 'FE'
    TYPE_CHOICE = ((LITTER, 'Litter'),
                   (FEEDER,'Feeder'),
                   (WHEEL, 'Wheel'),
                   (NEST, 'Nest'))
    name = models.CharField(max_length = 200)
    availability = models.BooleanField(default=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICE, default=LITTER)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.availability

    def use(self):
        if self.type != Equipment.LITTER:
            self.availability = False
            self.save()

    def free(self):
        self.availability = True
        self.save()

    def used_by(self):
        return Animal.objects.filter(place=self)

    def remove_animal(self, target):
        if not self.availability and target:
            for animal in self.used_by():
                animal.change_place(target)



class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'type']


def validate_available(equipment_pk):
    equipment = Equipment.objects.get(pk=equipment_pk)
    if not equipment.is_available():
        raise ValidationError(('%(value)s is not available'), params={'value': equipment.name})

class Animal(models.Model):
    HUNGRY = 'HU'
    TIRED = 'TI'
    SATED = 'SA'
    SLEEP = 'SL'
    STATE_CHOICE = ((HUNGRY, 'Hungry'),
                    (TIRED, 'Tired'),
                    (SATED, 'Sated'),
                    (SLEEP, 'Spleeping'))
    name = models.CharField(max_length = 200)
    race = models.CharField(max_length = 200)
    type = models.CharField(max_length = 200)
    state = models.CharField(max_length = 2, choices=STATE_CHOICE, default=SATED)
    place = models.ForeignKey(Equipment, on_delete=models.PROTECT, validators=[validate_available])
    last_move_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def change_state(self, new_state):
        if new_state in [i[0] for i in Animal.STATE_CHOICE]:
            self.state = new_state
            self.save()
        else:
            raise forms.ValidationError ('You have enter an invalid state')

    def change_place(self, new_place):
        if new_place.is_available:
            self.place.free()
            self.place = new_place
            self.last_move_date = timezone.now()
            self.save()
            self.place.use()
        else:
            raise forms.ValidationError ('You have enter an invalid location')


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'race', 'type', 'state', 'place']

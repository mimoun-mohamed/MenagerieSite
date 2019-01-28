from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.forms import formset_factory
from django.utils import timezone
from django.template.defaulttags import register

from .models import Animal, AnimalForm, Equipment, EquipementForm


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    animals_list = Animal.objects.order_by('last_move_date')

    context = {'animals_list': animals_list[:10]}
    return render(request, 'lamenageriemanager/index.html', context)


def animals_list(request):
    list = Animal.objects.all()
    form = AnimalForm(initial={'place': Equipment.objects.filter(type=Equipment.LITTER).filter(availability=True).first()})
    context = {'animals_list': list,
               'form': form}
    return render(request, 'lamenageriemanager/animals_list.html', context)


def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    context = {'animal': animal}
    return render(request, 'lamenageriemanager/animal_detail.html', context)


def animal_add(request):
    a = AnimalForm(request.POST)
    a.save()
    return HttpResponseRedirect(reverse('lamenageriemanager:animals_list'))


def feed(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.state == Animal.HUNGRY:
        try:
            target_location = Equipment.objects.filter(type=Equipment.FEEDER).filter(availability=True).first()
        except:
            context = {'animal': animal, 'error_message': "Aucune mangeoire n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
        if target_location:
            animal.change_place(target_location)
            animal.change_state(Animal.SATED)
            return HttpResponseRedirect(reverse('lamenageriemanager:animal_detail', args=(pk,)))
        else:
            context = {'animal': animal, 'error_message': "Aucune mangeoire n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
    else:
        context = {'animal': animal, 'error_message': "L'animal {} n'a pas faim.".format( animal.name)}
        return render(request, 'lamenageriemanager/animal_detail.html', context)


def entertain(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.state == Animal.SATED:
        try:
            target_location = Equipment.objects.filter(type=Equipment.WHEEL).filter(availability=True).first()
        except:
            context = {'animal': animal, 'error_message': "Aucune roue n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
        if target_location:
            animal.change_place(target_location)
            animal.change_state(Animal.TIRED)
            return HttpResponseRedirect(reverse('lamenageriemanager:animal_detail', args=(pk,)))
        else:
            context = {'animal': animal, 'error_message': "Aucune roue n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
    else:
        context = {'animal': animal, 'error_message': "L'animal {} n'est pas en état de faire du sport.".format( animal.name)}
        return render(request, 'lamenageriemanager/animal_detail.html', context)


def sleep(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.state == Animal.TIRED:
        try:
            target_location = Equipment.objects.filter(type=Equipment.NEST).filter(availability=True).first()
        except:
            context = {'animal': animal, 'error_message': "Aucun nid n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
        if target_location:
            animal.change_place(target_location)
            animal.change_state(Animal.SLEEP)
            return HttpResponseRedirect(reverse('lamenageriemanager:animal_detail', args=(pk,)))
        else:
            context = {'animal': animal, 'error_message': "Aucun nid n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
    else:
        context = {'animal': animal, 'error_message': "L'animal {} n'est pas fatigué.".format( animal.name)}
        return render(request, 'lamenageriemanager/animal_detail.html', context)


def wake_up(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.state == Animal.SLEEP:
        try:
            target_location = Equipment.objects.filter(type=Equipment.LITTER).filter(availability=True).first()
        except:
            context = {'animal': animal, 'error_message': "Aucune littière n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
        if target_location:
            animal.change_place(target_location)
            animal.change_state(Animal.HUNGRY)
            return HttpResponseRedirect(reverse('lamenageriemanager:animal_detail', args=(pk,)))
        else:
            context = {'animal': animal, 'error_message': "Aucune littière n'est disponible."}
            return render(request, 'lamenageriemanager/animal_detail.html', context)
    else:
        context = {'animal': animal, 'error_message': "L'animal {} ne dort pas".format( animal.name)}
        return render(request, 'lamenageriemanager/animal_detail.html', context)


def equipments_list(request):
    list = Equipment.objects.all()
    used_by = {e.id: e.used_by() for e in list}
    form = EquipementForm()
    context = {'equipments_list': list,
               'used_by': used_by,
               'form': form}
    return render(request, 'lamenageriemanager/equipments_list.html', context)


def equipment_detail(request, pk):
    equipment= get_object_or_404(Equipment, pk=pk)
    used_by = equipment.used_by()
    context = {'equipment': equipment,
               'used_by': used_by}
    return render(request, 'lamenageriemanager/equipment_detail.html', context)


def equipment_add(request):
    e = EquipementForm(request.POST)
    e.save()
    return HttpResponseRedirect(reverse('lamenageriemanager:equipments_list'))

def equipment_free(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    if equipment.is_available() and equipment.type != Equipment.LITTER:
        list = Equipment.objects.all()
        used_by = {e.id: e.used_by() for e in list}
        form = EquipementForm()
        context = {'equipments_list': list,
                   'used_by': used_by,
                   'form': form,
                   'error_equipement': equipment.id,
                   'error_message': "Equipement is empty"}
        return render(request, 'lamenageriemanager/equipments_list.html', context)

    try:
        target_location = Equipment.objects.filter(type=Equipment.LITTER).filter(availability=True).first()
    except:
        list = Equipment.objects.all()
        used_by = {e.id: e.used_by() for e in list}
        form = EquipementForm()
        context = {'equipments_list': list,
                    'used_by': used_by,
                    'form': form,
                    'error_equipement': equipment.id,
                    'error_message': "Litter does not exist"}
        return render(request, 'lamenageriemanager/equipments_list.html', context)

    if  target_location and target_location != equipment:
        equipment.remove_animal(target_location)
        list = Equipment.objects.all()
        used_by = {e.id: e.used_by() for e in list}
        form = EquipementForm()
        context = {'equipments_list': list,
                   'used_by': used_by,
                   'form': form}
        return render(request, 'lamenageriemanager/equipments_list.html', context)
    list = Equipment.objects.all()
    used_by = {e.id: e.used_by() for e in list}
    form = EquipementForm()
    context = {'equipments_list': list,
                'used_by': used_by,
                'form': form,
                'error_equipement': equipment.id,
                'error_message': "No litter available"}
    return render(request, 'lamenageriemanager/equipments_list.html', context)




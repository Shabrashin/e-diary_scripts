from datacenter.models import Commendation, Schoolkid, Mark, Chastisement, Lesson
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


def fix_marks(schoolkid):
    bad_child_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for bad_mark in bad_child_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisements.delete()


def create_commendation(schoolkid_name, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        schoolkid_lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter)
        last_lesson = schoolkid_lessons.filter(subject__title__contains=subject_title).order_by('-date').first()
        commendation_options = ["Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!", "Ты меня приятно удивил!"]
        Commendation.objects.create(
            text=random.choice(commendation_options),
            created=last_lesson.date,
            schoolkid=schoolkid,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher
        )
    except ObjectDoesNotExist:
        print("Schoolkid or subject doesn't exist")
    except MultipleObjectsReturned:
        print("More than one object was found")

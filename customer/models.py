from django.db import models

# Create your models here.

class Profession(models.Model):
    description= models.CharField(max_length=70)
    @property
    def status(self):
        return True
    def __str__(self):
        return self.description
class DataSheet(models.Model):
    description= models.CharField(max_length=50)
    historical_Data=models.TextField()
    def __str__(self):
        return self.description



class Customer(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    data_sheet= models.OneToOneField(DataSheet, on_delete= models.CASCADE)
    professions=models.ManyToManyField(Profession)
    active=models.BooleanField(default=True)
    # doc_num=models.CharField(max_length=12,unique=True)
    @property
    def status_message(self):
        if self.active:
            return "Customer active"
        else:
            return "Customer not activew"
    def num_professions(self):
        return self.professions.all().count()

    def __str__(self):
        return  self.name


class Documents(models.Model):
    PP='PP'
    ID='ID'
    OT='OT'
    Doc_type=[

        (PP,'Passport'),
        (ID,'Identity card'),
        (OT, 'Others')

    ]
    dtype=models.CharField(choices=Doc_type, max_length=2, default=PP,)
    doc_number= models.CharField(max_length=50)
    customers= models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return self.doc_number
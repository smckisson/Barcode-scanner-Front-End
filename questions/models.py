'''
A MARONE 09/22/2017
All rights reserved.
'''

from __future__ import unicode_literals
from django.db import models

#when changing question models we need to run command python manage.py makemigrations polls
# and then python manage.py migrate

'''
TOP DOWN APPROACH
'''



#ADD JSON REPONSE WITH DJANGO



#Question is here do we want admins assigned to locations,
#like should locations be another class?
#dont think we need.


#MAKE THE BARCODE_NUM UNIQUE
class Location(models.Model):
	loc_barcode_num = models.IntegerField(default=0)
	loc_name = models.CharField(max_length=200, default= " ")#floor1basement
	admin = models.CharField(max_length=200) #should actually be payroll id
	user_assigned = models.CharField(max_length=200)

	@property
	def devices(self):
		maping = LocDev.objects.filter(location=self)
		print (Device.objects.all())
		return [Device.objects.get(pk=i.device.pk) for i in maping ]
	@property
	def num_devices(self):
		return len(LocDev.objects.filter(location=self))
	@property
	def questions(self):
		return Question.objects.filter(location_assoc=self)
	def get_json_object(self):
		def access_lower_object_json(key):
			return key.get_json_object()
		ret={}
		ret["barcode_num"]=self.loc_barcode_num
		ret["loc_barcode_name"]=self.loc_name
		ret["items"]=self.devices()	
		#ret["items"]=map(access_lower_object_json, self.item_set.all())
		ret["loc_questions"]=map(access_lower_object_json, self.question_set.all())
		return ret
	def __str__(self):
		return str(self.loc_barcode_num)

class Device(models.Model):
	device_name = models.CharField(max_length=200) #fireqtinquisher
	manufacturer = models.CharField(max_length=200)
	model_number = models.CharField(max_length=200)
	type_equip = models.CharField(max_length=200)
	def __str__(self):
		return str(self.device_name)

	@property
	def questions(self):
		return Question.objects.filter(item_assoc=self)

class LocDev(models.Model):
	location=models.ForeignKey( Location, null=True, on_delete=models.CASCADE)
	device=models.ForeignKey( Device, null=True, on_delete=models.CASCADE)
	dummy_field=models.IntegerField(default=0)
	def __str__(self):
		return(" and locaction: " )#+ str(self.location_set.all())) 

class Item(models.Model):
	item_type=models.ForeignKey( Device, on_delete=models.CASCADE)
	item_barcode_num = models.IntegerField(default=0)

	def get_json_object(self):
		def access_lower_object_json(key):
			return key.get_json_object()
		ret ={}
		ret["barcode_num"]=self.item_barcode_num
		ret["item_type"]=self.item_type

		ret["questions"]=map(access_lower_object_json, self.question_set.all())
		return ret
	def __str__(self):
		return str(self.item_barcode_num)


class Question(models.Model):
	question_text = models.CharField(max_length=200) #field_example where is the pin?
	#pub_date = models.DateTimeField('date published') #this is obtained from ADMIN
	item_assoc=models.ForeignKey( Device, on_delete=models.CASCADE, null=True)
	location_assoc=models.ForeignKey( Location, on_delete=models.CASCADE, null=True)
	def get_json_object(self):
		ret ={}
		ret["question_text"]=self.question_text
		return ret
	def __str__(self):
		return str((self.question_text, self.pk))


class Choice(models.Model):
	#above is how relationships are defined with the foreign key, each choice is related with questions
	choice_text = models.CharField(max_length=200)
	time_scanned=models.CharField(max_length=200, default= " ")
	person_scanned=models.CharField(max_length=200, default= " ")
	question= models.ForeignKey( Question, on_delete=models.CASCADE, null=True) #posted by users
	location= models.ForeignKey( Location, on_delete=models.CASCADE, null=True) #posted by users
	def __str__(self):
		return self.choice_text

#here variables names are associated with COLUMN OF TABLE. CHOOSE NAMES WISELY



# Create your models here.

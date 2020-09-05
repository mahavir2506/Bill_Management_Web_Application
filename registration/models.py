from django.db import models
# Create your models here.
class patient(models.Model):
	cid=models.CharField(primary_key=True,max_length=50)
	name=models.CharField(max_length=100)
	mobile_no=models.IntegerField()
	address=models.CharField(max_length=200,blank=True)
	gender=models.CharField(max_length=10)


class record(models.Model):
	patient=models.ForeignKey(patient,on_delete=models.CASCADE)
	rid=models.AutoField(primary_key=True)
	date=models.DateField()
	total_ammount=models.IntegerField()
	bill=models.FileField(upload_to="bill/",blank=True)
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from registration.models import patient,record
from registration.utils import render_to_pdf
from django.core.files import File
from io import BytesIO
import os
# Create your views here.
l1=[]
def index(request):
	global l1
	d1={}
	if request.method=="POST":
		try:
			a=patient.objects.get(cid=request.POST["id"])
			l1.clear()
			d1["name"]=a.name
			d1["mobile"]=a.mobile_no
			d1["address"]=a.address
			d1["gender"]=a.gender
			l1.append(d1)
			return render(request,"index.html",{"list":l1[0]})
		except:
			l1.clear()
			d1["name"]=""
			d1["mobile"]=""
			d1["address"]=""
			d1["gender"]=""
			d1["birthyear"]=""
			l1.append(d1)
			return render(request,"index.html",{"list":l1[0],"error":"data is not found"})
	else:
		l1.clear()
		d1["name"]=""
		d1["mobile"]=""
		d1["address"]=""
		d1["gender"]=""
		d1["birthyear"]=""
		l1.append(d1)
		return render(request,"index.html",{"list":l1[0]})


def print(request):
	global l1
	if request.method=="POST":
		try:
			a=patient.objects.get(cid=str(request.POST["mobile"]),name=str(request.POST["name"]).lower())
		except:
			try:
				v=patient.objects.get(cid=str(request.POST["mobile"]))
				return render(request,"index.html",{"error":"Mobile no is must be unique"})
			except:
				a=patient()
				a.cid=str(request.POST["mobile"]).lower()
		try:	
			a.name=str(request.POST["name"]).lower()
			a.mobile_no=int(request.POST["mobile"])
			a.address=str(request.POST["address"]).lower()
			a.gender=request.POST["gender"]
			a.save()
			qty=[]
			item=[]
			rate=[]
			disc=[]
			tax=[]
			unit=[]
			total=[]
			sno=[]
			total1=0
			item=request.POST.getlist('item[]')
			rate=request.POST.getlist('rate[]')
			qty=request.POST.getlist('qty[]')
			disc=request.POST.getlist('disc[]')
			tax=request.POST.getlist('tax[]')
			unit=request.POST.getlist('unit[]')
			bill=[]
			for i in range(len(qty)):
				d={}
				d["item"]=item[i]
				d["rate"]=rate[i]
				d["qty"]=qty[i]
				d["disc"]=disc[i]
				d["tax"]=tax[i]
				d["unit"]=unit[i]
				sno.append(int(i+1))
				d["sno"]=sno[i]
				total.append((int(rate[i])*int(qty[i]))-((int(rate[i])*int(qty[i]))*(int(disc[i])/100))+((int(rate[i])*int(qty[i]))*(int(tax[i])/100)))
				total1=total1+(int(rate[i])*int(qty[i]))-((int(rate[i])*int(qty[i]))*(int(disc[i])/100))+((int(rate[i])*int(qty[i]))*(int(tax[i])/100))
				d["total"]=total[i]
				bill.append(d)
			e=record()
			#return HttpResponse(str(patient.objects.get(cid=request.POST["name"]+"_"+request.POST["year"])))
			e.patient=patient.objects.get(cid=request.POST["mobile"])
			e.date=request.POST["date"]
			e.total_ammount=total1
			e.save()
			#return HttpResponse(str(total1))
			k=record.objects.all()
			for i in k:
				rid=i.rid
			#return HttpResponse(str(request.POST["dv/sph"]))
			data={"no":rid,"mo":request.POST["mobile"],"name":request.POST["name"],"date":request.POST["date"],"address":request.POST["address"],"dr":request.POST["dr"],"sno":sno,"bill":bill,"total1":total1,"dvsph":request.POST["dv/sph"],"dvcyl":request.POST["dv/cyl"],"dvaxix":request.POST["dv/axix"],"dvvn":request.POST["dv/vn"],"dvsph1":request.POST["dv/sph1"],"dvcyl1":request.POST["dv/cyl1"],"dvaxix1":request.POST["dv/axix1"],"dvvn1":request.POST["dv/vn1"],"nvsph":request.POST["nv/sph"],"nvcyl":request.POST["nv/cyl"],"nvaxix":request.POST["nv/axix"],"nvvn":request.POST["nv/vn"],"nvsph1":request.POST["nv/sph1"],"nvcyl1":request.POST["nv/cyl1"],"nvaxix1":request.POST["nv/axix1"],"nvvn1":request.POST["nv/vn1"],"ltype":request.POST["ltype"],"add":request.POST["add"],"add1":request.POST["add1"]}
			pdf = render_to_pdf('bill.html',data)
			z=record.objects.get(rid=rid)
			z.bill.save(str(rid), File(BytesIO(pdf.content)))
			return FileResponse(open("media/bill/"+str(rid),"rb"), content_type='application/pdf')
		except:
			try:
				data={"no":rid,"mo":request.POST["mobile"],"name":request.POST["name"],"date":request.POST["date"],"address":request.POST["address"],"dr":request.POST["dr"],"sno":sno,"bill":bill,"total1":total1,"dvsph":request.POST["dv/sph"],"dvcyl":request.POST["dv/cyl"],"dvaxix":request.POST["dv/axix"],"dvvn":request.POST["dv/vn"],"dvsph1":request.POST["dv/sph1"],"dvcyl1":request.POST["dv/cyl1"],"dvaxix1":request.POST["dv/axix1"],"dvvn1":request.POST["dv/vn1"],"nvsph":request.POST["nv/sph"],"nvcyl":request.POST["nv/cyl"],"nvaxix":request.POST["nv/axix"],"nvvn":request.POST["nv/vn"],"nvsph1":request.POST["nv/sph1"],"nvcyl1":request.POST["nv/cyl1"],"nvaxix1":request.POST["nv/axix1"],"nvvn1":request.POST["nv/vn1"],"ltype":request.POST["ltype"],"add":request.POST["add"],"add1":request.POST["add1"]}
				pdf = render_to_pdf('bill.html',data)
				return FileResponse(pdf, content_type='application/pdf')
			except:
				return render(request,"index.html",{"list":l1[0],"error":"Something wrong"})	
	else:
		return render(request,"index.html",{"list":l1[0]})

l5=[]
total2=0
def report(request):
	global total2,l5
	if request.method=="POST":
		try:
			t=record.objects.filter(date__gte=request.POST["sdate"],date__lte=request.POST["edate"])
			l5.clear()
			total2=0
			if len(t)==0:
				return render(request,"report.html",{"error":"Data is not found between two date "})
			for i in t:
				d={}
				d["name"]=i.patient.name
				d["id"]=i.rid
				d["total"]=i.total_ammount
				d["url"]=int(i.rid)
				total2+=int(i.total_ammount)
				l5.append(d)
			return render(request,"report.html",{"list":l5,"total":total2})
		except:
			return render(request,"report.html",{"error":"Data is not found between two date "})
	else:
		total2=0
		l5=[]
		return render(request,"report.html")


def showbill(request,pk):
	try:
		return FileResponse(open("media/bill/"+str(pk),"rb"),content_type="application/pdf")
	except:
		return render(request,"report.html",{"error":"selected bill delted"})


def deletebill(request,pk):
	global l5,total2
	try:
		x=record.objects.filter(rid=int(pk))
		x.delete()
		for i in l5:
			if i["id"]==pk:
				z=i
		try:
			os.remove("media/bill/"+str(pk))
		except:
			return render(request,"report.html",{"list":l5,"total":total2})
		l5.remove(z)
		return render(request,"report.html",{"list":l5,"total":total2})
	except:
		return render(request,"report.html",{"list":l5,"total":total2})

def reportpdf(request):
	try:
		global l5,total2
		pdf=render_to_pdf("reportpdf.html",{"list":l5,"total":total2})
		return FileResponse(pdf, content_type='application/pdf')
	except:
		return render(request,"report.html",{"error":"Internet error "}) 

def detail(request):
	a=patient.objects.all()
	l8=[]
	for i in a:
		d={}
		d["name"]=i.name
		d["id"]=i.cid
		l8.append(d)
	return render(request,"detail.html",{"list":l8})
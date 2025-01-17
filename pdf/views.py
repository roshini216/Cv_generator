from django.shortcuts import render
from .models import Profile
import pdfkit
import io
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def accept(request):
    if request.method=='POST':
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school= request.POST.get("school","")
        university= request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")

    #creating object

        profile = Profile(name=name,email=email,phone=phone,summary=summary,degree=degree,school=school,university=university,previous_work=previous_work,skills=skills)
        #saving data to backend
        profile.save()
    return render(request,'pdf/accept.html')


def resume(request,id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile':user_profile})
    options={
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'dpi': 300,  # Higher DPI for better quality
        'zoom': 1.3,  # Adjust zoom level for better readability
        'enable-local-file-access': '',  # Enable local file access
    }
    config = pdfkit.configuration(wkhtmltopdf=r'C:\wkhtmltopdf\bin\wkhtmltopdf.exe')
    try:
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="resume_{id}.pdf"'
        return response
    except OSError as e:
        return HttpResponse(f"Error generating PDF: {e}", content_type='text/plain')


def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})
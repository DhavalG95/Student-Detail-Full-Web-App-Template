from django.contrib import admin
from .models import *
from django import forms
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json

admin.site.site_header = "Dhaval's Administration" #update name in header in admin panel
# Register your models here.
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "gender":forms.RadioSelect,
            "status":forms.Select
        }

# class StudentAdmin(admin.ModelAdmin):
#     form = StudentForm
#     list_display = ('id', 'name', 'age', 'email', 'gender','created_by','updated_by')
#     list_display_links = ('id', 'name')
#     list_filter = ('name',)
#     list_editable = ('age',)
#     list_per_page = 5
#     search_fields = ('name', 'email', 'created_by', 'updated_by')

class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('id', 'name', 'age', 'email', 'gender','created_by','updated_by')
    list_display_links = ('id', 'name')
    list_filter = ('name',)
    list_editable = ('age',)
    list_per_page = 5
    search_fields = ('name', 'email', 'created_by', 'updated_by')
    def changelist_view(self, request, extra_context=None):
        # Fetch data from the Student model
        status_counts = Student.objects.values('status').annotate(count=Count('status'))
        age_counts = Student.objects.values('age').annotate(age_count=Count('age'))
        print(status_counts)
        # Serialize the data to JSON format
        chart_data = json.dumps(list(status_counts), cls=DjangoJSONEncoder)
        age_data = json.dumps(list(age_counts),cls=DjangoJSONEncoder)
        print(chart_data)
        # Attach the chart data to the template context
        extra_context = extra_context or {}
        extra_context["chart_data"] = chart_data
        extra_context["age_data"] = age_data

        
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
      

admin.site.register(Student,StudentAdmin)
admin.site.register(LoginUser)
from django.shortcuts import render, get_object_or_404
from .models import Date, Expense, Category
from django.views.generic import CreateView
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ExpenseForm
import json


def date_list(request):
    
    project_list = Date.objects.all().order_by('-id')
    
    return render(request, 'budget/project-list.html', {'project_list':project_list})

def date_detail(request, date_slug):

    date = get_object_or_404(Date, name=date_slug)
    
    if request.method == 'GET':
        return render(request, 'budget/project-detail.html', {'date':date, 'expense_list':date.expenses.all(), 'category_list':Category.objects.filter(date=date)})
    elif request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']
            
            category = get_object_or_404(Category, date=date, name=category_name)
            
            Expense.objects.create(
                date=date,
                title=title,
                amount=amount,
                category=category
            ).save()
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        
        return HttpResponse('')  
        
    return HttpResponseRedirect(date_slug) 
    
    
class ProjectCreateView(CreateView):
    model = Date
    template_name = 'budget/add-date.html'
    fields = {'name','budget'}
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        
        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                date = Date.objects.get(id=self.object.id),
                name = category
            ).save()
            
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return slugify(self.request.POST['name'])
        
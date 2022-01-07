from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Date(models.Model):
    date = models.DateField(default=timezone.now)
    name = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Date, self).save(*args, **kwargs)
        
    def budget_left(self):
        expense_list = Expense.objects.filter(date=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount
            
        return self.budget - total_expense_amount
    
    def total_transactions(self):
        expense_list = Expense.objects.filter(date=self)
        return len(expense_list)
        
    def __str__(self):
        return self.name

class Category(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    name = models.CharField(max_length=50) 

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
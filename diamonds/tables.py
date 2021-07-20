from django_tables2 import tables, TemplateColumn
from .models import Diamond

class DiamondTable(tables.Table):

    class Meta:
         model = Diamond
         attrs = {'class': 'table table-sm mr-5','style':'text-align: right;'}
         fields = ['carat', 'cut', 'color', 'clarity',"depth","table","x","y","z","price"]

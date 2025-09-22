from app.models import Option, Product, Category, Unit
from app.widgets import CustomBooleanWidget, ValidatingForeignKeyWidget
from import_export import resources, fields
from import_export.widgets import DecimalWidget




    # name = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    # description = models.TextField(blank=True)
    # price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # available_quantity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)



class ProductResource(resources.ModelResource):
    name = fields.Field(column_name='name', attribute='name')
    image = fields.Field(column_name='image', attribute='image')
    category= fields.Field(column_name='category',
                           attribute='category',
                           widget= ValidatingForeignKeyWidget(Category, 'name'))

    unit= fields.Field(column_name='unit',
                           attribute='unit',
                           widget= ValidatingForeignKeyWidget(Unit, 'name'))
    description= fields.Field(column_name='description', attribute='description')
    price_per_unit= fields.Field(column_name='price per unit', attribute='price_per_unit',widget=DecimalWidget())
    available_quantity= fields.Field(column_name='available quantity', attribute='available_quantity', widget=DecimalWidget())
    created_at= fields.Field(column_name='Date Created', attribute='created_at', readonly=True)
    updated_at= fields.Field(column_name='Date Updated', attribute='updated_at', readonly=True)
    
    
    def before_import_row(self, row, row_number=None, **kwargs):
        self.category = row['category']  
        self.unit = row['unit']
        # option_name= row['option name']
        # option_price = row['option price']
        # option_names= option_name.split(',') if option_name else None
        # option_prices= option_price.split(',') if option_price else None
        # if option_name and option_price:
             
       
        if (not Category.objects.filter(name=self.category).exists()):
            obj, created = Category.objects.get_or_create(name=self.category)
            
        if (not Unit.objects.filter(name=self.unit).exists()):
            obj, created = Unit.objects.get_or_create(name=self.unit)



    class Meta:
        model= Product
        fields = (
            'id',
            'name',
            'image',
            'unit',
            'category',
            'description',
            'price_per_unit',
            'available_quantity',
            'created_at',
            'updated_at'
        )
        
        # try:   
        #     main_category= row['Main Category']
        #     if (not Category.objects.filter(name=main_category).exists()  and main_category != None ):
        #         obj2, created = Category.objects.get_or_create(name=main_category)
            
        #     category_obj = Category.objects.get(name =main_category )
        #     self.subCategory = row['Category']
        #     if (not SubCategory.objects.filter(name=self.subCategory).exists() and self.subCategory != None):
        #         obj3, created = SubCategory.objects.get_or_create(name=self.subCategory, category=category_obj)
        # except:
        #     raise ValidationError(f"both category and main category are required")



    
    # def before_import_row(self, row, row_number=None, **kwargs):
    #     days = row['days']
    #     days= days.split('|') if days else None
    #     if days:
    #         for d in days:
    #             if( not Day.objects.filter(name=d).exists()):
    #                 if (d == 'Sun' or d== 'Mon' or d== 'Tue' or d== 'Wed' or d== 'Thu' or d== 'Fri' or d=='Sat'):
    #                     obj, created= Day.objects.get_or_create(name= d)
from django.db import models

# Represents Diamond - all features and target
class Diamond(models.Model):
    CUT_CHOICES =[('Ideal','Ideal'), ('Premium','Premium'), ('Very_good','Very Good'), ('Good','Good'), ('fair','Fair')]
    COLOR_CHOCIES = [('D','D'), ('E','E'), ('F','F'), ('G','G'), ('H','H'), ('I','I'), ('J','J')]
    CLARITY_CHOCIES = [('IF','IF'), ('VVS1','VVS1'), ('VVS2','VVS2'), ('VS1','VS1'), ('VS2','VS2'), ('SI1','SI1'), ('SI2','SI2'),('I1','I1')]
    
    #diamond_id = models.AutoField(primary_key=True,auto_created = True,serialize =True)
    carat = models.FloatField()
    cut =  models.CharField(max_length=9,choices=CUT_CHOICES)
    color = models.CharField(max_length=1,choices=COLOR_CHOCIES)
    clarity = models.CharField(max_length=4,choices=CLARITY_CHOCIES)
    depth = models.FloatField()
    table = models.FloatField()
    price = models.BigIntegerField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()


# Represents Diamond that its price was predicted - includes information regarding the predicted price
# and regarding the user's feedback 
class Diamond_predicted(models.Model):
    CUT_CHOICES =[('Ideal','Ideal'), ('Premium','Premium'), ('Very_good','Very Good'), ('Good','Good'), ('fair','Fair')]
    COLOR_CHOCIES = [('D','D'), ('E','E'), ('F','F'), ('G','G'), ('H','H'), ('I','I'), ('J','J')]
    CLARITY_CHOCIES = [('IF','IF'), ('VVS1','VVS1'), ('VVS2','VVS2'), ('VS1','VS1'), ('VS2','VS2'), ('SI1','SI1'), ('SI2','SI2'),('I1','I1')]
        
    carat = models.FloatField()
    cut =  models.CharField(max_length=9,choices=CUT_CHOICES)
    color = models.CharField(max_length=1,choices=COLOR_CHOCIES)
    clarity = models.CharField(max_length=4,choices=CLARITY_CHOCIES)
    depth = models.FloatField()
    table = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    price_predicted = models.BigIntegerField(blank=True,null=True)
    real_price_feedback = models.BigIntegerField(blank=True,null=True)
    price_feedback = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    imported_to_dataset = models.BooleanField(default=False)
    pointer_to_dataset = models.ForeignKey(Diamond,on_delete=models.SET_NULL,blank=True,null=True)

# Represents Log message
class MyLog(models.Model):
    LOGTYPE_CHOICES = [('Info','Info'),('Warning','Warning'),("Error","Error")]
    created = models.DateTimeField(auto_now_add=True)
    logtype = models.CharField(max_length=7,choices=LOGTYPE_CHOICES)
    message = models.TextField()
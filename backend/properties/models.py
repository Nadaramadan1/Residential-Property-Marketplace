# from django.db import models
# from django.db import connection
# cursor.execute("SQL QUERY")

# class Property(models.Model):
#     property_id = models.AutoField(primary_key=True)
#     representative_id = models.IntegerField()
#     style = models.CharField(max_length=100)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     address = models.CharField(max_length=255)
#     market_value = models.DecimalField(max_digits=12, decimal_places=2)
#     property_status = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'PROPERTY'
#         managed = False
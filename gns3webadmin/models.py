from datetime import datetime
from ipaddress import ip_address
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

class Connection(models.Model):
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField(default=3080, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    pub_date = models.DateTimeField(default=datetime.now)

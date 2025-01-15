from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

class RouteResult(models.Model):
    best_route = models.TextField()  # يمكنك استخدام JSONField إذا كان يدعمه إصدار Django الخاص بك
    route_length = models.FloatField()
    route_safety = models.FloatField()

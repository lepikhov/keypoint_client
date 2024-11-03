from django.db import models



class Image(models.Model):
    image=models.ImageField(upload_to='images/')
    date=models.DateTimeField( auto_now_add=True)
    key=models.CharField(max_length=64, default='123') 

    class Meta:
        ordering=['-date']

    def __str__(self):
        return str(self.date)


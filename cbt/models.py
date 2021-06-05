from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


#ゾーン選択モデル
class Zone(models.Model):
    zone=models.IntegerField(verbose_name="ゾーン",default=1,validators=[MinValueValidator(1),MinValueValidator(3)])
    fields=models.CharField(verbose_name="分野")
    num=models.IntegerField(verbose_name="ソート用",
        default=1,
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(1)]
        )
        )
    
    def __str__(self):
        return self.fields
        
    class Meta:
        verbose_name_plural="ゾーンと分野の登録"
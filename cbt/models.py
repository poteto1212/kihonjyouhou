from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


#ゾーン選択モデル
class Zone(models.Model):
    zones=models.CharField(verbose_name="ゾーン",max_length=15)#ゾーン１23
    num=models.IntegerField(verbose_name="ソート用",
        default=1,
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(1)]
        )
        
    def __str__(self):
        return self.zones
        
    class Meta:
        verbose_name_plural="ゾーンと分野の登録"

#科目選択モデル
class Subject(models.Model):
    zone=models.ForeignKey('Zone',verbose_name="分野選択",on_delete=models.CASCADE)
    subjcs=models.CharField(verbose_name="科目",max_length=30)#物理　化学　生物　薬理
    subjctsnum=models.IntegerField(verbose_name="ソート用",
        default=1,
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(1)]
        )
    
    def __str__(self):
        return self.subjcs
    
    class Meta:
        verbose_name_plural="科目登録"
        
        
#領域選択モデル
class Field(models.Model):
    subjct=models.ForeignKey('Subject',verbose_name="科目選択",on_delete=models.CASCADE)
    fields=models.CharField(verbose_name="分野",max_length=30)#熱力学　分析化学　中枢　抹消
    fieldnum=models.IntegerField(verbose_name="ソート用",
        default=1,
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(1)]
        )
    def __str__(self):
        return self.fields
    
    class Meta:
        verbose_name_plural="領域登録"
        #科目名と分野名の組み合わせ制約
        constraints=[
            models.UniqueConstraint(
                fields=['subjct','fields'],
                name="subjct_fields_unique"
                )
            ]

#問題内容詳細モデル
class Detail(models.Model):
    field=models.ForeignKey('Field',verbose_name="科目選択",on_delete=models.CASCADE)
    title=models.CharField(verbose_name="概要",max_length=100)#問題タイトル
    #貼り付け問題用
    questionimg=models.ImageField(upload_to='questionimage',blank=True,null=True,unique=False)
    #手書き問題用紙
    questiontxt=models.TextField(verbose_name='手書き問題',blank=True,null=True)
    
     
    #正しい解答の番号ビューで　answer=[正答１,正答2,正答3]
    #テンプレートから kaitou=[get1,get2,get3]
    #if分で answer=kaitouである事を照合
    answernum1=models.IntegerField(verbose_name="正答1",
        default=1,#選択肢無しは０にする
        unique=False,
        validators=[MinValueValidator(1),MaxValueValidator(10)]
        )
    answernum2=models.IntegerField(verbose_name="正答2",
        default=0,#選択肢無しは０にする
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(0),MaxValueValidator(10)]
        )
    answernum3=models.IntegerField(verbose_name="正答3",
        default=0,#選択肢無しは０にする
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(0),MaxValueValidator(10)]
        )
    
    
    #貼り付け解説
    answerimg=models.ImageField(upload_to='answerimage',blank=True,null=True,unique=False)
    #手書き解説
    answertxt=models.TextField(verbose_name='手書き解説',blank=True,null=True)
    
    #説明画像
    detailimg=models.ImageField(upload_to='detaileimage',blank=True,null=True,unique=False)
    
    #関連問題
    relation=models.ManyToManyField('self',verbose_name="関連分野の問題",blank=True,null=True)
   
    
    #順番
    questionnum=models.IntegerField(verbose_name="ソート用",
        default=1,
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(1)]
        )
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural="出題問題"
    
        
        
        
        
        
        
        
        
        
        
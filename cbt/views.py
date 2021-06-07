from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Zone,Subject,Field,Detail
from django.http import HttpResponse

# Create your views here.
class HomeView(ListView):
    template_name="home.html"
    model=Detail
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        
        #ゾーン選択フォームに渡す
        zone_list=Zone.objects.order_by('num')
        
        #科目選択フォームに渡す
        subject_list=Subject.objects.order_by('zone__num','subjctsnum')
        
        
        #領域選択フォームに渡す
        field_list=Field.objects.order_by(
                                    'subjct__zone__num',
                                    'subjct__subjctsnum',
                                    'fieldnum',
                                    )
        default_field=field_list.first()
        
        #問題一覧表示
        question_list=Detail.objects\
                                .order_by(
                                    'field__subjct__zone__num',
                                    'field__subjct__subjctsnum',
                                    'field__fieldnum',
                                    'questionnum'
                                    )
                                    
        #ゾーンフォーム受け取り時の表示処理
        if self.request.GET.get('getzone'):
            key=self.request.GET.get('getzone')
            subject_list=subject_list.filter(zone__id=key)
            field_list=field_list.filter(subjct__zone__id=key)
            default_field=field_list.first()
            question_list=question_list.filter(field__subjct__zone__id=key)
        
        #科目フォーム受け取り時の表示処理
        elif self.request.GET.get('getsubjects'):
            key=self.request.GET.get('getsubjects')
            subject_list=subject_list.filter(id=key)
            field_list=field_list.filter(subjct__id=key)
            default_field=field_list.first()
            question_list=question_list.filter(field__subjct__id=key)
            
        #分野フォーム受け取り時の処理
        elif self.request.GET.get('getfield'):
            key=self.request.GET.get('getfield')
            question_list=question_list.filter(field__id=key)
            default_field=Field.objects.get(id=key)
            #科目選択時その他フォーム
            try:
                subject_key=question_list.first()
                subject_key=subject_key.field.subjct.id
                field_list=field_list.filter(subjct__id=subject_key)
                subject_list=subject_list.filter(id=subject_key)
            except AttributeError:
                field_list=field_list
                question_list=['該当する問題はありません']
            
                
        context['zone_list']=zone_list
        context['subject_list']=subject_list
        context['field_list']=field_list
        context['default_field']=default_field
        context['question_list']=question_list
        return context
        
        
        
class QuestionView(DetailView):
    template_name='question.html'
    model=Detail   
        
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        correctquery=Detail.objects.get(id=self.kwargs['pk'])
        #正答リストの準備
        correctanswer=[
            str(correctquery.answernum1),
            str(correctquery.answernum2),
            str(correctquery.answernum3)
            ]
        #並べ替え
        correctanswer=sorted(correctanswer)
        #リストからゼロを取り除く
        correctanswer=[x for x in correctanswer if x != "0"]
      
        #getがある時に採点する処理
        if self.request.GET.getlist('getanswer') and self.request.GET.getlist('getanswer')==correctanswer:
            getanswer=self.request.GET.getlist('getanswer')
            context['correctback']="正解!"
            context['youranswer']=getanswer
            context['collectanswer']=correctanswer
        
        elif self.request.GET.getlist('getanswer') and self.request.GET.getlist('getanswer')!=correctanswer:
            getanswer=self.request.GET.getlist('getanswer')
            context['failsback']="不正解!"
            context['youranswer']=getanswer
            context['collectanswer']=correctanswer
        
        
        #問題遷移用パラメータ
        #次の問題
        nowquestion=correctquery.questionnum
        nowfield=correctquery.field.id
        nowsubjcts=correctquery.field.subjct.id
        nextquestion=nowquestion+1
        backquestion=nowquestion-1
        
        
        if Detail.objects.filter(field__subjct__id=nowsubjcts,field__id=nowfield,questionnum=nextquestion).exists():
            #次の問題へ
            context['nextquestion']=Detail.objects.get(field__subjct__id=nowsubjcts,field__id=nowfield,questionnum=nextquestion)
        
        if Detail.objects.filter(field__subjct__subjctsnum=nowsubjcts,field__id=nowfield,questionnum=backquestion).exists():
            #前の問題へ
            context['backquestion']=Detail.objects.get(field__subjct__subjctsnum=nowsubjcts,field__id=nowfield,questionnum=backquestion)
       
        
        return context
        
        
        
        
        
        
        
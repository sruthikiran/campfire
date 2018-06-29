from django.forms import ModelForm
from .models import Question,Answer,Message

class QuesForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title','desc','tags')

class AnsForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('desc',)

class NewMessage(ModelForm):
    class Meta:
        model = Message
        fields = ('subject','content')

class ReplyForm(ModelForm):
    class Meta:
        model = Message
        fields = ('content',)

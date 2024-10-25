from django import forms
from society.models import   ForumComment, ForumReply, Notification
from society.models import Comment, Reply
from society.models import RSVP


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message','is_urgent']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

class RSVPForm(forms.ModelForm):
    attending = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], widget=forms.RadioSelect)

    class Meta:
        model = RSVP
        fields = ['attending']

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']

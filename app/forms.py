import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from app.models import Profile, Question, Tag, Answer, Rating


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Login'))
    password = forms.CharField(label=_('Password'),min_length=5, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label=_('Login'),
                               help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    password = forms.CharField(label=_('Password'), min_length=5,
                               widget=forms.PasswordInput,
                               help_text=_('Required. Minimum 5 characters. Minimum 1 character from @/./+/-/_/&/* '))
    first_name = forms.CharField(label=_('Nick Name'), help_text=_('Required.'))
    email = forms.EmailField(label=_('Email Address'), help_text=_('Required.'))
    repeat_password = forms.CharField(min_length=5, widget=forms.PasswordInput, help_text=_('Required.'))
    avatar = forms.ImageField(label=_('Avatar'), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        char_set = {'@', '.', '+', '-', '_', '&', '*'}
        print(password)
        for i in password:
            if i in char_set:
                return password
        raise forms.ValidationError(_('Password must contain @/./+/-/_/&/*'))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 30 and re.fullmatch(r'(\d|\w|@|\.|\+|-)*', username):
            return username
        raise forms.ValidationError(_('Login does not meet the requirements'))

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repeat_password')

        if password != password2:
            self.add_error('password', '')
            self.add_error('repeat_password', '')
            raise forms.ValidationError(_('Passwords do not match!'))

    def save(self, **kwargs):
        self.cleaned_data.pop('repeat_password')
        user = User.objects.create_user(username=self.cleaned_data.get('username'),
                                        email=self.cleaned_data.get('email'),
                                        first_name=self.cleaned_data.get('first_name'),
                                        password=self.cleaned_data.get('password'))
        profile = Profile.objects.create(user=user)
        Rating.objects.create(profile=profile)
        if self.cleaned_data.get('avatar') is None:
            profile.avatar = None
        else:
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return user


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(label=_('Login'),
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               help_text=_('30 characters or fewer. Letters, digits and @/./+/-/_ only.'))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label=_('Nick Name'), help_text=_('Required.'))
    avatar = forms.ImageField(label=_('Avatar'), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 30 and re.fullmatch(r'(\d|\w|@|\.|\+|-)*', username):
            return username
        raise forms.ValidationError(_('Login does not meet the requirements'))

    def save(self, **kwargs):
        user = super().save(**kwargs)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile = user.profile
            profile.avatar = avatar
            profile.save()
        return user


class NewQuestionForm(forms.ModelForm):
    head = forms.CharField(label=_('Title'), min_length=10,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           help_text=_('Required. Minimum 10 characters.'))
    body = forms.CharField(label=_('Text'), min_length=40,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
                           help_text=_('Required. Minimum 40 characters.'))
    tags = forms.CharField(label=_('Tags'),  required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           help_text=_('Letters and digits only. Enter a comma-separated list of tags.'))

    class Meta:
        model = Question
        fields = ['head', 'body']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if re.fullmatch(r'(\d|\w|,|\s)*', tags):
            return tags
        raise forms.ValidationError(_('List of tags does not meet the requirements'))

    def tags_list(self):
        tags_rec = self.cleaned_data.get('tags')
        tags_rec = re.split(r'\W+', tags_rec)
        tags_list = []
        for tag in tags_rec:
            tag_object = Tag.objects.filter(tag_name=tag).first()
            if tag_object is None:
                tag_object = Tag.objects.create(tag_name=tag)
            tags_list.append(tag_object)
        return tags_list

    def save(self, request=None, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        question = Question.objects.create(author_id=profile.id,
                                           head=self.cleaned_data.get('head'),
                                           body=self.cleaned_data.get('body'))
        tags_list = self.tags_list()
        question.tags.add(*tags_list)
        return question


class NewAnswerForm(forms.ModelForm):
    body = forms.CharField(label=_('Write your answer here!'), min_length=2,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}))

    class Meta:
        model = Answer
        fields = ['body']

    def save(self, request=None, question_id=None, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        print(user.id)
        answer = Answer.objects.create(author_id=profile.id,
                                         question_id=question_id,
                                         body=self.cleaned_data.get('body'),
                                         correctness=False)
        return answer

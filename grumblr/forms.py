from django import forms

from django.contrib.auth.models import User
from models import *

class profileForm(forms.ModelForm):
    cpassword = forms.CharField(max_length=50, label ="Confirm password:",
                                widget = forms.PasswordInput(attrs={'placeholder':"Confirm Password...",
                                                                    'class':'form-control input-username'}))
    email = forms.EmailField(label ="Email:",
                             widget = forms.TextInput(attrs={'placeholder':"Input Email...",
                                                                    'class':'form-control input-username'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':"Input Username...",
                                               'class':'form-control input-username'}),
            'first_name': forms.TextInput(attrs={'placeholder':"Input First name...",
                                                 'class':'form-control input-firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder':"Input Last name...",
                                                'class':'form-control input-lastname'}),
            'password': forms.PasswordInput(attrs={'placeholder':"Input Password...",
                                                   'class':'form-control input-username'})
        }


    def clean(self):
        cleaned_data = super(profileForm, self).clean()

        password = cleaned_data.get('password')
        cpassword = cleaned_data.get('cpassword')
        if password and cpassword and password != cpassword:
            raise forms.ValidationError("Password did not match!")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username


class signForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username:',
                               widget=forms.TextInput(attrs={'placeholder': "Username",
                                                             'class': 'form-control'}))
    password = forms.CharField(max_length=50, label='Password:',
                               widget=forms.PasswordInput(attrs={'placeholder': "Password",
                                                                 'class': 'form-control'}))
    def clean(self):
        cleaned_data = super(signForm, self).clean()
        return cleaned_data


class postForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'class': "form-control post-textarea",
                                          'placeholder': "Input content(Less than 42 characters...)"})
        }
        error_messages = {
            'content': {
                'max_length': "Content should be less than 42 characters."
            }
        }

class editForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':"Input First name...",
                                                 'class':'form-control input-firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder':"Input Last name...",
                                                'class':'form-control input-lastname'}),
            'email': forms.TextInput(attrs={'placeholder':"Input Email...",
                                            'class':'form-control input-username'}),
        }

    def clean(self):
            cleaned_data = super(editForm, self).clean()
            return cleaned_data

class editOtherForm(forms.ModelForm):
    class Meta:
        model = Myuser
        fields = ['age','bio','photo']
        widgets = {
            'age': forms.TextInput(attrs={'placeholder': "Input age...",
                                          'class': 'form-control input-username'}),
            'bio': forms.Textarea(attrs={'placeholder': "Input bio...",
                                         'class': 'form-control input-username'}),
            'photo': forms.FileInput(attrs={'class': 'form-control input-username'})
        }

    def clean(self):
            cleaned_data = super(editOtherForm, self).clean()
            return cleaned_data

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label="Old password",
        error_messages={'required': 'Please input old password!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Input old password...",
                                          'class': 'form-control input-username'}))

    newpassword1 = forms.CharField(
        required=True,
        label="New password",
        error_messages={'required': 'Please input new password!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Input new password...",
                                          'class': 'form-control input-username'}))

    newpassword2 = forms.CharField(
        required=True,
        label="Confirm password",
        error_messages={'required': 'Please input new password again!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm new password...",
                                          'class': 'form-control input-username'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You should complete every textarea!")
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError("New passwords do not match!")
        else:
            cleaned_data = super(ChangePasswordForm, self).clean()
        return cleaned_data

class ForgetPasswordForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="Username",
        error_messages={'required': 'Please input your username!'},
        widget=forms.TextInput(attrs={'placeholder': "Input username...",
                                          'class': 'form-control input-username'}))
    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is not existed.")

        return username

class ResetPasswordForm(forms.Form):

    newpassword1 = forms.CharField(
        required=True,
        label="New password",
        error_messages={'required': 'Please input new password!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Input new password...",
                                          'class': 'form-control input-username'}))

    newpassword2 = forms.CharField(
        required=True,
        label="Confirm password",
        error_messages={'required': 'Please input new password again!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm new password...",
                                          'class': 'form-control input-username'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You should complete every textarea!")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError("New passwords do not match!")
        else:
            cleaned_data = super(ResetPasswordForm, self).clean()
        return cleaned_data

# class postForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': 1, 'class': "form-control comment-text",
#                                           'placeholder': "Input comment..."})
#         }

class postForm(forms.Form):
    blog = forms.CharField(max_length=42, widget=forms.TextInput(attrs={'rows': 1,
                                    'class': "form-control comment-text",'placeholder': "Input comment..."}))
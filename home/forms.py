from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Group, GroupProfile, Messages
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
from crispy_forms.layout import Field


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):

    user_info = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ["user_info", "image"]


class GroupUpdateForm(forms.ModelForm):

    group_info = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Group
        fields = ["group_name", "group_info"]


class GroupCreateForm(forms.ModelForm):

    group_info = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):

        super(GroupCreateForm, self).__init__(*args, **kwargs)

        self.fields["group_name"].label = "Group Name :"
        self.fields["group_info"].label = "Group Info :"
        self.fields["group_name"].widget.attrs["placeholder"] = "Enter Group Name..."
        self.fields["group_info"].widget.attrs["placeholder"] = "Enter Group Info..."

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal form-class"
        self.helper.label_class = "form-group col-lg-2"
        self.helper.field_class = "input-class col-lg-10"
        self.helper.layout = Layout(
            "group_name", "group_info", Submit("submit", "Create", css_class="col-lg-2")
        )

    class Meta:
        model = Group
        fields = ["group_name", "group_info"]


class GroupProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = GroupProfile
        fields = ["image"]


class GroupProfileCreateForm(forms.ModelForm):
    class Meta:
        model = GroupProfile
        fields = ["image"]


class MessageCreateForm(forms.ModelForm):
    message_text = forms.CharField()

    class Meta:
        model = Messages
        fields = ["message_text"]


class SearchUserForm(forms.Form):

    user_name = forms.CharField(max_length=150, label="Username", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].label = "Username :"
        self.fields["user_name"].widget.attrs[
            "placeholder"
        ] = "Search User Name Here..."


class AddMemberForm(forms.Form):
    users = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, label="Select users to add : "
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-class"
        self.helper.field_class = "form-field-class"
        self.helper.layout = Layout(
            "users", Submit("submit", "Add To Group", css_class="col-lg-2")
        )


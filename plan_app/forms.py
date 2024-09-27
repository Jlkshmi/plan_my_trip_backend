from django.contrib.auth.forms import UserCreationForm

from plan_app.models import Login


class Userregister(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Login
        fields = ('username', 'password1', 'password2', 'email', 'name', 'phone', 'address')


class Managerregister(UserCreationForm):
    class Meta(UserCreationForm):
        model = Login
        fields = ('username', 'password1', 'password2', 'email', 'company_name', 'company_address', 'phone')

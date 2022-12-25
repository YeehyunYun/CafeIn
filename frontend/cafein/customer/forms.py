from django import forms
from account.models import User
import bcrypt
import re

class customerPostForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '"-"을 포함하지 않는 전화번호'}),
        }
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control offset-md-1',
                                                                  'placeholder': '비밀번호 확인'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '전화번호 ("-" 없이 작성)'}))
    
    # email이 이미 등록되었는지, 그리고 이메일 형식에 맞는지에 대한 validation
    def check_email(self):
        email = self.cleaned_data.get("email")
        customer = User.objects.filter(email=email).first()
        if customer is None:
            pattern = re.compile('^.+@+.+\.+.+$')  # 이메일 '@'앞에는 아무 문자가 제한 없이 들어올 수 있음
            if not pattern.match(email):
                return False
            else:
                return True  # db에 존재하지 않고, 이메일 형식이 맞다면 데이터를 반환
        else:
            # 필드에 email 값이 db에 존재하는지 확인
            return False
    
    # 고객 전화번호 '-'없이 숫자만 입력하도록 
    def check_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
        if not pattern.match(phone):
            return False
        return True
    

    # 입력한 password가 조건에 맞는지에 대한 validation
    def check_password(self):
        password = self.cleaned_data.get("password")
        # 영어,숫자,특수문자 포함하고 8~25자리수를 허용
        pattern = re.compile('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,25}$')
        if not pattern.match(password):
            return False
        else:
            return True


    # 두개의 password가 일치한지에 대한 validation 
    def check_password1(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            return False
        else:
            return True

    # DB 삭제 탈퇴 회원 정보 
    def delete(self):
        email = self.cleaned_data.get("email")
        customer = User.objects.get(user_id=email)
        customer.delete()

    # DB에 회원가입 값 저장
    def save(self):
        # 고객
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        phone = self.cleaned_data.get("phone")

        user = User(user_id=email)
        user.email = email
        user.phone = phone
        user.set_password(password)
        user.is_owner = 0
        user.save()

        
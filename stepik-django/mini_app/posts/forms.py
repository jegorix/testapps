from django import forms 

class UserForm(forms.Form):
    name = forms.CharField(label="Имя", help_text="Введите имя", 
                           error_messages={"required": "Ошибка, не введено имя"},
                           max_length=10,
                           min_length=2)
    age = forms.IntegerField(label="Ваш возраст")
    captcha_answer = forms.IntegerField(label='2 + 2', label_suffix=' = ')
    description = forms.CharField(label="Описание", widget=forms.Textarea)
    adds = forms.BooleanField(label="Вы согласны получать рекламу?", required=False)
    field_order = ["captcha_answer", "name", "description", "age"]
    
    

class PublisherForm(forms.Form):
    name = forms.CharField(label="Имя", help_text="Введите свое имя", min_length=4, max_length=20)
    adress = forms.CharField(label="Адрес", help_text="Введите свой адрес", max_length=200)
    city = forms.CharField(label="Город", help_text="Введите город", max_length=20)
    post_index = forms.IntegerField(label="Почтовый индекс", help_text="Введите свой почтовый индекс")
    website = forms.URLField(label="Сайт", help_text="Введите адрес своего сайта", required=False)
    
    
class CarForm(forms.Form):
    model = forms.CharField(label="Модель", initial="undefined")
    brand = forms.CharField(label="Марка", initial="undefined")
    factory_year = forms.IntegerField(label="Год выпуска", initial=2023)
    model_year = forms.IntegerField(label="Модельный год", initial=2022)
    price = forms.DecimalField(label="Цена", initial=0)
    
    
class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", help_text="Введите ваше имя",
                           error_messages={"required": "Ошибка, не введено имя."})
    
    email = forms.EmailField(label="E-Mail", help_text="Введите ваш E-Mail",
                             error_messages={"required": "Ошибка, не введён E-Mail."})
    
    message = forms.CharField(label="Сообщение", help_text="Введите сообщение",
                              error_messages={"required": "Ошибка, не введено сообщение."})
    
    promo = forms.BooleanField(label="Подписаться на получение новостных и рекламных рассылок?", required=False)
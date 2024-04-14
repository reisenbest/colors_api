from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


#инициализация супер пользователя если его нет (для докера)
class Command(BaseCommand):
    def handle(self, *args, **options):
        UserModel = get_user_model()
        if UserModel.objects.count() == 0:
            username = 'admin'
            login = 'admin'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, login))
            admin = UserModel.objects.create_superuser(username=username, login=login, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            print('Admin account created successfully.')
        else:
            print('Admin account already exists.')
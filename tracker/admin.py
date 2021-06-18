from django.contrib import admin

from .models import *

admin.site.register(Crypto)
admin.site.register(Fiat)
admin.site.register(UserProfile)
admin.site.register(Rate)
admin.site.register(Exchange)
admin.site.register(ExchangeAccount)
admin.site.register(ExchangeBalance)
admin.site.register(ManualBalance)

from django.contrib import admin
from api import models


class BorrowerAdmin(admin.ModelAdmin):
    model = models.Borrower


admin.site.register(models.Borrower, BorrowerAdmin)


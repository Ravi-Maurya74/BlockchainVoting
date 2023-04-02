from django.contrib import admin
from .models import Election, Choice, Voter

# Register your models here.


class ElectionView(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "choices",
        "created",
    )

    def choices(self, instance):
        return [choice.name for choice in instance.choices.all()]


admin.site.register(Election, ElectionView)
admin.site.register(Choice)
admin.site.register(Voter)

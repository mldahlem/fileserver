from django.contrib import admin
from .models import Categorias, Items


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('category', 'description')
    exclude = ['owner', ]

    # garantir que o usuario logado apenas consiga postar em seu usuário, redefinindo a função save
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('item', 'category', 'topic', 'document')
    exclude = ['owner', ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

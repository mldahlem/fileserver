from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _  # Usado em 'document' da class Items para guardar nome arquivo
import uuid
import os


def get_file_path(_instance, _filename):
    ext = _filename.split('.')[-1]  # 'foto.png' -> ('foto', 'png') -> [-1] pega a extensão
    filename = f'{uuid.uuid4()}.{ext}'  # esta função uuid cria um nome aleatório hexadecial
    return filename


class Base(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create = models.DateField('Criação', auto_now_add=True)
    modify = models.DateField('Atualização', auto_now=True)

    class Meta:
        abstract = True


class Categorias(Base):
    category = models.CharField('Categoria', max_length=30, unique=True)
    description = models.CharField('Descrição', max_length=200)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.category


class Items(Base):
    item = models.CharField('Item', max_length=120)
    category = models.ForeignKey('Categorias', on_delete=models.CASCADE)
    document = models.FileField(_('Documento'), upload_to=get_file_path, blank=True)
    topic = models.TextField('Link / Texto', blank=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return f'{self.item}  {self.category}'


# Decorador e função utilizada para deletar arquivo do disco quando o registro do mesmo é deletado do banco de dados
@receiver(models.signals.post_delete, sender=Items)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import *

@registry.register_document
class BlogDocument(Document):
    class Index:
        name = 'blogs'  

    class Django:
        model = Blog  

        fields = [
            'title',
            'content',
        ]

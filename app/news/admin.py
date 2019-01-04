from django.contrib import admin

# Register your models here.
from .models import ContentType
from .models import Category
from .models import News
from .models import Comment
from .models import Image

admin.site.register(ContentType)
admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Image)

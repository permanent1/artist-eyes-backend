from peewee import CharField, IntegerField
from app.models.base_model import BaseModel

class Artist(BaseModel):
    class Meta:
        table_name = 'artists'

    id = IntegerField(primary_key=True)
    name = CharField(null=True, help_text="艺术家名称")
    year = CharField(null=True, help_text="生卒年")
    genre = CharField(null=True, help_text="艺术家派别")
    introduction = CharField(null=True, help_text="艺术家介绍")
    background = CharField(null=True, help_text="艺术家背景")
    style = CharField(null=True, help_text="艺术家风格")
    characters = CharField(null=True, help_text="作品特点")
    website = CharField(null=True, help_text="艺术家网站")
    image = CharField(null=True, help_text="艺术家代表作图片路径")

    def __str__(self):
        return f'Artist: {self.name} ({self.year}) - {self.genre}'

    def has_website(self):
        return bool(self.website)

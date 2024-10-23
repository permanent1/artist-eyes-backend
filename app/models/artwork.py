from peewee import CharField, ForeignKeyField, IntegerField
from app.models.base_model import BaseModel
from app.models.artist import Artist  # Artist 模型在 artist.py 中

class Artwork(BaseModel):
    class Meta:
        table_name = 'artworks'

    id = IntegerField(primary_key=True)
    artist_id = ForeignKeyField(Artist, backref='artworks', on_delete='CASCADE', on_update='CASCADE', help_text="艺术家外键")
    artwork = CharField(null=True, max_length=255, help_text="作品名称")
    image = CharField(null=True, max_length=255, help_text="图片路径")
    background = CharField(null=True, max_length=255, help_text="作品背景")
    style = CharField(null=True, max_length=255, help_text="作品风格")
    theme = CharField(null=True, max_length=255, help_text="作品主题")

    def __str__(self):
        return f'Artwork: {self.artwork} by {self.artist_id.name}'

    def has_image(self):
        return bool(self.url)

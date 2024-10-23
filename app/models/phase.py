from peewee import CharField, ForeignKeyField, IntegerField
from app.models.base_model import BaseModel
from app.models.artist import Artist  # Artist 模型在 artist.py 中

class Phase(BaseModel):
    class Meta:
        table_name = 'phases'

    id = IntegerField(primary_key=True)
    artist_id = ForeignKeyField(Artist, backref='phases', on_delete='CASCADE', on_update='CASCADE', help_text="艺术家外键")
    phase = CharField(null=True, max_length=255, help_text="阶段时期")
    name = CharField(null=True, max_length=255, help_text="阶段名称")
    introduction = CharField(null=True, max_length=255, help_text="阶段介绍")
    background = CharField(null=True, max_length=255, help_text="阶段代表作背景")
    style = CharField(null=True, max_length=255, help_text="阶段代表作风格")
    theme = CharField(null=True, max_length=255, help_text="阶段代表作主题")
    meaning = CharField(null=True, max_length=255, help_text="阶段意义")
    artwork = CharField(null=True, max_length=255, help_text="阶段代表作名称")
    image = CharField(null=True, help_text="阶段代表作图片路径")

    def __str__(self):
        return f'{self.name} ({self.phase}) by {self.artist_id.name}'

    def get_artwork_info(self):
        return {
            "name": self.artwork,
            "background": self.background,
            "style": self.style,
            "theme": self.theme,
            "meaning": self.meaning
        }

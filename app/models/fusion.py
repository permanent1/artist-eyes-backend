from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField
from app.models.base_model import BaseModel
from app.models.user import User  # User 模型在 user.py 中
from app.models.artist import Artist  # Artist 模型在 artist.py 中

class Fusion(BaseModel):
    class Meta:
        table_name = 'fusions'

    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User, backref='fusions', on_delete='CASCADE', on_update='CASCADE', help_text="用户外键")
    artist_id = ForeignKeyField(Artist, backref='fusions', on_delete='CASCADE', on_update='CASCADE', help_text="艺术家外键")
    title = CharField(null=True, max_length=255, help_text="融合图片名称")
    fusion = CharField(null=True, max_length=255, help_text="融合图片路径")
    description = CharField(null=True, max_length=255, help_text="融合图片描述")
    draft = CharField(null=True, max_length=255, help_text="用户草稿图片路径")
    style = CharField(null=True, max_length=255, help_text="用户选择著作路径")

    def __str__(self):
        return f'Fusion by {self.user_id.username} name {self.title} for artist {self.artist_id}'

    def is_draft_uploaded(self):
        return bool(self.draft)

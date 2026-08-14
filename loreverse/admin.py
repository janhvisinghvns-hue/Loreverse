from django.contrib import admin
from .models import (ReadingProgress, World,WorldImage, Character, CharacterImage,
    Location,LocationImage,Creature,CreatureImage, TimelineEvent)


admin.site.register(ReadingProgress)
admin.site.register(World)
admin.site.register(WorldImage)
admin.site.register(Character)
admin.site.register(CharacterImage)
admin.site.register(Location)
admin.site.register(LocationImage)
admin.site.register(Creature)
admin.site.register(CreatureImage)
admin.site.register(TimelineEvent)
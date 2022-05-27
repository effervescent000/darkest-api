from . import ma


class StatSchema(ma.Schema):
    class Meta:
        fields = ("id", "field", "value", "hero_id")


multi_stat_schema = StatSchema(many=True)


class AbilitySchema(ma.Schema):
    class Meta:
        fields = ("id", "slot", "level", "enabled", "hero_id")


multi_ability_schema = AbilitySchema(many=True)


class HeroSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "hero_class", "resolve", "stats", "abilities")

    stats = ma.Nested(multi_stat_schema)
    abilities = ma.Nested(multi_ability_schema)


multi_hero_schema = HeroSchema(many=True)


class RosterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "user_id", "heroes")

    heroes = ma.Nested(multi_hero_schema)


class UserSchema(ma.Schema):
    # intentionally leaving off the roster right now
    class Meta:
        fields = ("id", "username", "role")

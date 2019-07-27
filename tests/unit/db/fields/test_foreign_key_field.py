from db.fields import ForeignKeyField
from db.query import Model


class FakeModel(Model):
    pass


class TestMagicStr:
    def test_when_field_cannot_be_null_then_renders_with_not_null_flag(self):
        field = ForeignKeyField(to=FakeModel, column_name='coffee_id', type='integer')
        assert str(field) == 'coffee_id INTEGER NOT NULL, FOREIGN KEY (coffee_id) REFERENCES "fakemodel" (id)'

    def test_when_field_can_be_null_then_renders_without_null_flag(self):
        field = ForeignKeyField(to=FakeModel, column_name='coffee_id', type='integer', null=True)
        assert str(field) == 'coffee_id INTEGER, FOREIGN KEY (coffee_id) REFERENCES "fakemodel" (id)'

    def test_when_field_is_primary_key_then_renders_with_primary_key_flag(self):
        field = ForeignKeyField(to=FakeModel, column_name='coffee_id', type='integer', primary_key=True)
        assert str(field) == 'coffee_id INTEGER PRIMARY KEY, FOREIGN KEY (coffee_id) REFERENCES "fakemodel" (id)'

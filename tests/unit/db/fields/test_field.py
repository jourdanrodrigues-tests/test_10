from db.fields import Field


class TestMagicStr:
    def test_when_field_cannot_be_null_then_renders_with_not_null_flag(self):
        field = Field(column_name='coffee', type='integer')
        assert str(field) == 'coffee INTEGER NOT NULL'

    def test_when_field_can_be_null_then_renders_without_not_null_flag(self):
        field = Field(column_name='flower', type='boolean', null=True)
        assert str(field) == 'flower BOOLEAN'

    def test_when_field_is_primary_key_then_renders_with_primary_key_flag(self):
        field = Field(column_name='cookie', type='char', primary_key=True)
        assert str(field) == 'cookie CHAR PRIMARY KEY'

from db.fields import VarCharField


class TestMagicStr:
    def test_when_field_can_be_null_then_renders_without_not_null_flag(self):
        field = VarCharField(column_name='coffee', length=14, null=True)
        assert str(field) == 'coffee VARCHAR(14)'

    def test_when_field_cannot_be_null_then_renders_with_not_null_flag(self):
        field = VarCharField(column_name='flower', length=1)
        assert str(field) == 'flower VARCHAR(1) NOT NULL'

    def test_when_field_is_primary_key_then_renders_with_primary_key_flag(self):
        field = VarCharField(column_name='cookie', length=20, primary_key=True)
        assert str(field) == 'cookie VARCHAR(20) PRIMARY KEY'

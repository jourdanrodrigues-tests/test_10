class Field:
    def __init__(self, **kwargs):
        """
        :type type: str
        :type null: bool
        :type column_name: str
        :type primary_key: bool
        """
        self.type = kwargs['type']
        self.null = kwargs.get('null', False)
        self.column_name = kwargs.get('column_name')
        self.primary_key = kwargs.get('primary_key', False)

    def _get_type(self):
        return self.type.upper()

    def __str__(self):
        schema_string = '{} {}'.format(self.column_name, self._get_type())

        if self.primary_key:
            schema_string += ' PRIMARY KEY'
        elif not self.null:
            schema_string += ' NOT NULL'

        return schema_string


class ForeignKeyField(Field):
    def __init__(self, **kwargs):
        """
        :type to:
        :type type: str
        :type null: bool
        :type column_name: str
        :type primary_key: bool
        """
        self.to = kwargs['to']
        super().__init__(**kwargs)

    def __str__(self):
        string = super().__str__()
        model_to = self.to
        return string + ', FOREIGN KEY ({}) REFERENCES "{}" ({})'.format(
            self.column_name,
            model_to.get_table_name(),
            model_to.pk_field,
        )


class VarCharField(Field):
    def __init__(self, **kwargs):
        """
        :type null: bool
        :type length: int
        :type column_name: str
        :type primary_key: bool
        """
        self.length = kwargs.pop('length')

        super().__init__(type='varchar', **kwargs)

    def _get_type(self):
        return super()._get_type() + '({})'.format(self.length)

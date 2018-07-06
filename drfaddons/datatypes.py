from django.db import models


class UnixTimestampField(models.DateTimeField):
    """
    UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    Source: https://stackoverflow.com/a/11332150
    """
    def __init__(self, null=False, blank=False, **kwargs):
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.isnull, self.blank = null, blank
        self.null = True  # To prevent the framework from shoving in "not null".
        super(UnixTimestampField, self).__init__(**kwargs)

    def db_type(self, connection):
        typ = ['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        else:
            typ += ['default "2017-03-11 05:00:00"']
        return ' '.join(typ)

    def to_python(self, value):
        from datetime import datetime

        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        from time import strftime

        if value is None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S', value.timetuple())

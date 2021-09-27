from pony.orm import set_sql_debug

from models import Option, db_session, select


@db_session
def get_opt_by_id(opt_id):
	return Option[opt_id]

@db_session
def update_opt(data, new_value):
	opt = Option[data["opt_id"]]
	field_id = data["field_id"]
	if field_id == '0':
		opt.text = new_value
	else:
		opt.url = new_value
	return

from platformdirs import user_documents_path, user_data_path

data_dir = user_data_path('spellbook', 'Nathaniel Markham')
data_dir.mkdir(exist_ok=True, parents=True)
documents_dir = user_documents_path()
collection_dir = documents_dir / 'spellbook'
db_file = data_dir / 'mtg_db.fs'

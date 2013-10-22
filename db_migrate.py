#! /usr/bin/python

# this script "migrates" (e.g. updates) a database
# e.g. after changing 'models.py' you'll want to 'migrate' the db
# below is mostly plug-and-play, boilerplate script
# (though make sure config variables and file hierarchy match new projects)
# avoid renaming or re-typing existing fields to smooth migration process
import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version
	(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)+1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, 
	SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration,"wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print'New migration saved as '+ migration
print'Current database version: '+ str(api.db_version(SQLALCHEMY_DATABASE_URI, 
	SQLALCHEMY_MIGRATE_REPO))
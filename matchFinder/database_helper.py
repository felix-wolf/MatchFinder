from . import db
import hashlib
from matchFinder.models import teilnehmer_model
from matchFinder.models import thema_model
from matchFinder.models import thema_list_model
from matchFinder.models import teilnehmer_list_model
from matchFinder.models import verteilung_model
from matchFinder.models import password_model
from matchFinder.models import praeferenz_model

def init_db():
	#db.drop_all()
	#db.create_all()

	from . import password_helper
	#password_helper.create_passwords()

def get_all_teilnehmer():
	return teilnehmer_model.Teilnehmer.query.all()

def get_all_teilnehmer_lists():
	return teilnehmer_list_model.Teilnehmer_List.query.all()

def get_all_themen():
	return thema_model.Thema.query.all()

def get_all_thema_lists():
	return thema_list_model.Thema_List.query.all()

def get_all_verteilungen():
	return verteilung_model.Verteilung.query.all()

def get_all_passwords():
	return password_model.Password.query.all()

def get_teilnehmer_by_id(id):
	return teilnehmer_model.Teilnehmer.query.filter_by(id=id).first()

def get_teilnehmer_list_by_id(id):
	return teilnehmer_list_model.Teilnehmer_List.query.filter_by(id=id).first()

def get_thema_by_id(id):
	return thema_model.Thema.query.filter_by(id=id).first()

def get_thema_list_by_id(id):
	return thema_list_model.Thema_List.query.filter_by(id=id).first()

def get_verteilung_by_id(id):
	return verteilung_model.Verteilung.query.filter_by(id=id).first()

def get_verteilung_by_hashed_id(hashed_id):
	verteilungen = get_all_verteilungen()
	for vert in verteilungen:
		hashed_db_id = hashlib.sha256(str(vert.id).encode()).hexdigest()
		if hashed_db_id == hashed_id:
			return vert
	return None

def delete_teilnehmer_by_id(id):
	db.session.delete(get_teilnehmer_by_id(id))
	db.session.commit()

def delete_teilnehmer_list_by_id(id):
	db.session.delete(get_teilnehmer_list_by_id(id))
	db.session.commit()

def delete_thema_by_id(id):
	db.session.delete(get_thema_by_id(id))
	db.session.commit()

def delete_thema_list_by_id(id):
	db.session.delete(get_thema_list_by_id(id))
	db.session.commit()

def delete_verteilung_by_id(id):
	db.session.delete(get_verteilung_by_id(id))
	db.session.commit()

def insert_password(password):
	db.session.add(password)
	db.session.commit()

def insert_praeferenz(praeferenz):
	db.session.add(praeferenz)
	db.session.commit()

def insert_teilnehmer(teilnehmer):
	db.session.add(teilnehmer)
	db.session.commit()

def get_praeferenz_by_teilnehmer_id(teilnehmer_id):
	return praeferenz_model.Praeferenz.query.filter_by(teilnehmer_id=teilnehmer_id).first()

def save_teilnehmer(teilnehmer_liste, list_name):
	memberlist = []
	for mem in teilnehmer_liste:
		local_member = teilnehmer_model.Teilnehmer(
        	matr_nr = mem['matr_nr'].item(),
        	last_name = mem['last_name'],
        	first_name = mem['first_name']
        )
		db.session.add(local_member)
		memberlist.append(local_member)

	list = teilnehmer_list_model.Teilnehmer_List(
		name = list_name,
		teilnehmer = memberlist
		)
	db.session.add(list)
	db.session.commit()

	return len(teilnehmer_liste)

# saves themen to the database
def save_themen(themen, list_name):
	list_of_themen = []
	for top in themen:
		local_thema = thema_model.Thema(
        	thema_name = top['thema_name'],
        	betreuer = top['betreuer'],
        	zeit = top['zeit']
        )
		db.session.add(local_thema)
		list_of_themen.append(local_thema)

	list = thema_list_model.Thema_List(
		name = list_name,
		themen = list_of_themen
		)
	db.session.add(list)
	db.session.commit()

	return len(themen)

def save_verteilung(teiln_list_id, thema_list_id, protected, editable,
	number_per_thema, min_votes, veto_allowed):

	thema_list = get_thema_list_by_id(thema_list_id)
	if protected:
		teiln_list = get_teilnehmer_list_by_id(teiln_list_id)
	else:
		teiln_list = teilnehmer_list_model.Teilnehmer_List(
			name="Teilnehmer der offenen Verteilung mit Themenname '"
			+ str(thema_list.id) + "'",
			is_for_unprotected=True)
		db.session.add(teiln_list)
		db.session.commit()

	local_verteilung = verteilung_model.Verteilung(
		thema_list_id = thema_list.id,
		teilnehmer_list_id = teiln_list.id,
		protected = protected,
		editable = editable,
		max_teilnehmer_per_thema = number_per_thema,
		min_votes = min_votes,
		veto_allowed = veto_allowed
	)
	db.session.add(local_verteilung)
	db.session.commit()
	return local_verteilung.id

def check_membership(hashed_verteilung_id, matr_nr):
	verteilung_to_id = get_verteilung_by_hashed_id(hashed_verteilung_id)
	if verteilung_to_id != None:
		teilnehmer_to_verteilung = get_teilnehmer_list_by_id(verteilung_to_id.teilnehmer_list_id)
		if teilnehmer_to_verteilung != None:
			for teil in teilnehmer_to_verteilung.teilnehmer:
				if int(teil.matr_nr) == int(matr_nr):
					return verteilung_to_id, teil
	return None, None







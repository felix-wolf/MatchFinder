from . import db
from matchFinder.models import teilnehmer
from matchFinder.models import thema
from matchFinder.models import thema_list
from matchFinder.models import teilnehmer_list
from matchFinder.models import verteilung

def save_teilnehmer(teilnehmer_liste, list_name):
	memberlist = []
	for mem in teilnehmer_liste:
		local_member = teilnehmer.Teilnehmer(
        	matr_nr = mem['matr_nr'].item(),
        	last_name = mem['last_name'],
        	first_name = mem['first_name']
        )
		db.session.add(local_member)
		memberlist.append(local_member)

	list = teilnehmer_list.Teilnehmer_List(name = list_name, teilnehmer = memberlist)
	db.session.add(list)
	db.session.commit()

	return len(teilnehmer_liste)

def save_themen(themen, list_name, max_participants):
	list_of_themen = []
	for top in themen:
		local_topic = thema.Thema(
			stine_id = top['stine_id'].item(),
        	topic_name = top['topic_name'],
        	max_participants = max_participants,
        	tutor_last_name = top['tutor_last_name'],
        	tutor_first_name = top['tutor_first_name']
        )
		db.session.add(local_topic)
		list_of_themen.append(local_topic)

	list = thema_list.Thema_List(
		name = list_name, themen = list_of_themen
		)
	db.session.add(list)
	db.session.commit()

	return len(themen)

def save_verteilung(teilnehmer_list_name, thema_list_name):
	from matchFinder.models import teilnehmer_list
	from matchFinder.models import thema_list
	teilnehmer_list_entries = teilnehmer_list.Teilnehmer_List.query.all()
	thema_list_entries = thema_list.Thema_List.query.all()
	for teilnehmer_list in teilnehmer_list_entries:
		if teilnehmer_list.name == teilnehmer_list_name:
			matching_teilnehmer_list = teilnehmer_list
	for thema_list in thema_list_entries:
		if thema_list.name == thema_list_name:
			matching_thema_list = thema_list

	local_verteilung = verteilung.Verteilung(
		thema_list_id = matching_thema_list.id,
		teilnehmer_list_id = matching_teilnehmer_list.id
	)
	db.session.add(local_verteilung)
	db.session.commit()
	return local_verteilung.id
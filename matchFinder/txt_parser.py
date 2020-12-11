import pandas as pd
import os

def array_from_teilnehmer(file):
	df = pd.read_csv(file, sep='\t', names=['id', 'matr_nr', 'last_name', 'first_name', 'NaN1', 'uebung', 'NaN2'])
	print(df)
	df.columns = df.columns.str.strip()
	df = df.drop('id', axis=1)
	df = df.drop('NaN1', axis=1)
	df = df.drop('NaN2', axis=1)
	df = df.drop('uebung', axis=1)
	print(df)
	participants = []
	for ind in df.index:
		participant = {}
		participant['matr_nr'] = df['matr_nr'][ind]
		participant['last_name'] = df['last_name'][ind].strip()
		participant['first_name'] = df['first_name'][ind].strip()
		participants.append(participant)
	return participants

def array_from_themen(file):
	'''
	df = pd.read_csv(file, sep='\t', names=[
		'stine_id', 'tutor_last_name', 'tutor_first_name', 'NaN1', 'topic_name', 'NaN2']
		)
	df.columns = df.columns.str.strip()
	df = df.drop('NaN1', axis=1)
	df = df.drop('NaN2', axis=1)
	topics = []
	for ind in df.index:
		topic = {}
		topic['stine_id'] = df['stine_id'][ind]
		topic['tutor_last_name'] = df['tutor_last_name'][ind]
		topic['tutor_first_name'] = df['tutor_first_name'][ind]
		topic['topic_name'] = df['topic_name'][ind]
		topics.append(topic)
		'''
	return topics

def load_ips():
	with open('list_of_blocked_ips.txt', 'r') as f:
		return f.read().split('\n')

def load_passwords():
	with open('passwords.txt', 'r') as f:
		return f.read().split('\n')
import pandas as pd
import numpy as np
import os

def array_from_teilnehmer(file):
	df = pd.read_csv(file, sep='\t', names=['id', 'matr_nr', 'last_name', 'first_name', 'NaN1', 'uebung', 'NaN2'])
	df.columns = df.columns.str.strip()
	df = df.drop('id', axis=1)
	df = df.drop('NaN1', axis=1)
	df = df.drop('NaN2', axis=1)
	df = df.drop('uebung', axis=1)
	participants = []
	for ind in df.index:
		participant = {}
		participant['matr_nr'] = df['matr_nr'][ind]
		participant['last_name'] = df['last_name'][ind].strip()
		participant['first_name'] = df['first_name'][ind].strip()
		participants.append(participant)
	return participants

def array_from_themen(file):
	df = pd.read_csv(file, sep=',', names=['thema_name', 'zeit', 'betreuer'])
	df = df.replace(np.nan, '', regex=True)
	df.columns = df.columns.str.strip()
	themen = []
	for ind in df.index:
		thema = {}
		thema['thema_name'] = df['thema_name'][ind]
		thema['zeit'] = df['zeit'][ind]
		thema['betreuer'] = df['betreuer'][ind]
		themen.append(thema)
	return themen

def load_values_from_file(file):
	with open(file, 'r') as f:
		return f.read().split('\n')
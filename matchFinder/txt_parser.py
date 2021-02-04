import pandas as pd
import numpy as np
import os

def array_from_teilnehmer(file):
	"""
	parses a file containing teilnehmer in STiNE format to an array of teilnehmer
	It does so by assigning and then dropping unessecary columns and
	making sure that the data has the correct format.

	Parameters
	----------
	file : file
    	text file in STiNE format containsing teilnehmer
    Returns
    ----------
    array
    	returns the teilnehmer as an array
	"""

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
	"""
	parses a file containing themen in csv format to an array of themen

	Parameters
	----------
	file : file
    	csv file of themen
    Returns
    ----------
    array
    	returns the themen as an array
	"""

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
	"""
	this function returns an array where each item is a line in the text file
	Parameters
	----------
	file : file
    	text file of several lines
    Returns
    ----------
    array
    	returns an array of lines
	"""
	with open(file, 'r') as f:
		return f.read().split('\n')
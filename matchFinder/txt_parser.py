import pandas as pd

def array_from_participants(file):
	df = pd.read_csv(file, sep='\t', names=['matr_nr', 'last_name', 'first_name', 'NaN'])
	df.columns = df.columns.str.strip()
	df = df.drop('NaN', axis=1)
	participants = []
	for ind in df.index:
		participant = {}
		participant['matr_nr'] = df['matr_nr'][ind]
		participant['last_name'] = df['last_name'][ind]
		participant['first_name'] = df['first_name'][ind]
		participants.append(participant)
	return participants
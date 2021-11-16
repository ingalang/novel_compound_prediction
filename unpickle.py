import pickle


with open('pickles/compound_testset.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)



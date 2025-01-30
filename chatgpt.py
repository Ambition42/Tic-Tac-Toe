import pickle


ai_file = open("ai_data.dat", "rb")


ai = pickle.load(ai_file)

print(ai)

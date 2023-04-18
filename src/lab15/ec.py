from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

import nltk as nl
import scipy
import itertools
import numpy as np

nl.download('punkt')

#Responses from chat GPT
response1 = "The sky appears blue to us because of the way our atmosphere scatters sunlight. When the sun's light enters our atmosphere, it collides with molecules of air and other particles in the atmosphere, causing the light to scatter in all directions. Blue light has a shorter wavelength and higher frequency than other colors in the visible spectrum, which causes it to scatter more easily than other colors. As a result, more blue light is scattered in all directions, making the sky appear blue to us. At sunrise or sunset, when the sun is lower in the sky, the light has to travel through more of the Earth's atmosphere to reach us. This causes even more scattering of the light, and as a result, the sky appears more orange or red."
response2 = "The blue color of the sky is due to a phenomenon called Rayleigh scattering, which occurs when sunlight passes through the Earth's atmosphere. The atmosphere is made up of a mixture of gases, including nitrogen, oxygen, and trace amounts of other gases. When sunlight enters the atmosphere, it is scattered in all directions by the air molecules. However, the shorter blue wavelengths of light are scattered more than the longer red wavelengths, which causes the blue light to be scattered in all directions and appear to come from all parts of the sky. This is why the sky appears blue during the day. At sunrise or sunset, when the sun is low on the horizon, the light has to pass through more of the atmosphere to reach our eyes, which causes more of the blue light to be scattered out and away from our line of sight. This allows the longer red wavelengths of light to dominate, giving the sky a red or orange appearance. Overall, the blue color of the sky is a result of the scattering of sunlight by the Earth's atmosphere."

#Split both text into sentences.
response1Sentences = nl.sent_tokenize(response1)
response2Sentences = nl.sent_tokenize(response2)

#Check sentences
#print("Response1Sentences",response1Sentences)
#print("Response2Sentences",response2Sentences)

#for i, (sentence1, sentence2) in enumerate(itertools.zip_longest(response1Sentences, response2Sentences)):
    #print(i, sentence1, sentence2)

embeddings1 = model.encode(response1Sentences)
embeddings2 = model.encode(response2Sentences)

for sentence1, sentence2 in zip(response1Sentences, response2Sentences):
    sentence1_embedding = model.encode(sentence1)
    sentence2_embedding = model.encode(sentence2)
    similarity_score = 1 - scipy.spatial.distance.cosine(sentence1_embedding, sentence2_embedding)
    print(f"Similarity between '{sentence1}' and '{sentence2}': {similarity_score:.4f}")








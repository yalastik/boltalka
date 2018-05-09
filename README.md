# boltalka
telegram bot maintaining native language conversation
what's under the hood:
**1.** parsed messages from two main social sources - vkontakte & telegram in form of (question (other user's reply); answer (my own reply))
**2.** prebuilt word2vec model for my vocab corpus
**3.** structure of (sentence vector (sum of its words vectors); its reply) - used to efficiently find the most appropriate reply
**4.** searching for *K* closest (most similar sentences) for the input using cosine similarity
**5.** cleaning output from names (in order to keep the publicity away)
**6.** corner cases with voice/doc/location/photo messages to bot

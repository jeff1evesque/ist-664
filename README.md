# IST-664

This is final project for a short 10 week course in Natural Language Processing (NLP). In this project, different models will be generated, then ensembled in an attempt to create a generative + rules based chatbot.

## Dependency

Since this project is a proof of concept, the necessary build has been automated using a `Vagrantfile`. This means both ([vagrant](https://www.vagrantup.com/) + [virtualbox](https://www.virtualbox.org/)) will need to be installed. However, another proof of concept can be further extended using a `docker-compose.yml`. For production systems, kubernetes would likely replace the `docker-compose` variant.

## Data

Three different datasets are used to generate respective models

- QuestionAnswerCMU
- StackOverflow
- Reddit

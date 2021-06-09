
# create-luis.py
# Based on https://docs.microsoft.com/en-us/learn/modules/add-basic-conversational-intelligence/2-create-language-understanding-intelligent-service-resource?pivots=python
# After sudo pip install azure-cognitiveservices-language-luis
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time

# Obtain from environment variables:
authoring_key =      os.environ['MY_LUIS_AUTHORING_KEY']
authoring_endpoint = os.environ['MY_LUIS_ENDPOINT']

# instantiate a client object and authenticate to the service.
client = LUISAuthoringClient(authoring_endpoint, CognitiveServicesCredentials(authoring_key))

def create_app():
    # Create a new LUIS app
    app_name    = "PictureBotLUIS"
    app_desc    = "Picture Bot app built with LUIS Python SDK."
    app_version = "0.1"
    app_locale  = "en-us"

    app_id = client.apps.add(dict(name=app_name,
                                initial_version_id=app_version,
                                description=app_desc,
                                culture=app_locale))

    print("Created LUIS app {}\n    with ID {}".format(app_name, app_id))
    return app_id, app_version

# https://docs.microsoft.com/en-us/learn/modules/add-basic-conversational-intelligence/3-exercise-add-intents?pivots=python
def add_intents(app_id, app_version):
    intents = ["Greeting", "SearchPics", "OrderPic", "SharePic"]
    for intent in intents:
        intentId = client.model.add_intent(app_id, app_version, intent)
        print("Intent {} {} added.".format(intent, intentId))
Modify the create_app() function and add this line of code before the existing return statement.

# For reals: create_app()
# add_intents(app_id, app_version)

# https://docs.microsoft.com/en-us/learn/modules/manage-language-understanding-intelligent-service-apps/4-manage-data-language-understanding-intelligent-service-app?pivots=python
# Helper function for creating the utterance data structure.
# <createUtterance>
def create_utterance(intent, utterance, *labels):
    """Add an example LUIS utterance from utterance text and a list of
       labels.  Each label is a 2-tuple containing a label name and the
       text within the utterance that represents that label.
       Utterances apply to a specific intent, which must be specified."""

    text = utterance.lower()

    def label(name, value):
        value = value.lower()
        start = text.index(value)
        return dict(entity_name=name, start_char_index=start,
                    end_char_index=start + len(value))

    return dict(text=text, intent_name=intent,
                entity_labels=[label(n, v) for (n, v) in labels])
# </createUtterance>

# Add example utterances for the intent.  Each utterance includes labels
# that identify the entities within each utterance by index.  LUIS learns
# how to find entities within user utterances from the provided examples.
#
# Example utterance: "find flights in economy to Madrid"
# Labels: Flight -> "economy to Madrid" (composite of Destination and Class)
#         Destination -> "Madrid"
#         Class -> "economy"
# <addUtterances>
def add_utterances(app_id, app_version):
    # Now define the utterances
    utterances = [create_utterance("FindFlights", "find flights in economy to Madrid",
                            ("Flight", "economy to Madrid"),
							("Destination", "Madrid"),
							("Class", "economy")),

				  create_utterance("FindFlights", "find flights to London in first class",
							("Flight", "London in first class"),
							("Destination", "London"),
							("Class", "first")),

				  create_utterance("FindFlights", "find flights from seattle to London in first class",
							("Flight", "flights from seattle to London in first class"),
							("Destination", "London"),
							("Class", "first"))]

	# Add the utterances in batch. You may add any number of example utterances
	# for any number of intents in one call.
	client.examples.batch(app_id, app_version, utterances)
	print("{} example utterance(s) added.".format(len(utterances)))
# </addUtterances>


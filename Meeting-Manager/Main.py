import requests
import json
import time
import pandas as pd

def my_logic(trancript,meetingMinutes, participantsList, followUp):
    url = "https://meeting-manager-bot-text-analytics.cognitiveservices.azure.com/text/analytics/v3.2-preview.1/analyze"

    payload = json.dumps({
        "analysisInput": {
            "documents": [
                {
                    "language": "en",
                    "id": "1",
                    "text": trancript
                }
            ]
        },
        "tasks": {
            "extractiveSummarizationTasks": [
                {
                    "parameters": {
                        "model-version": "latest",
                        "sentenceCount": 20,
                        "sortBy": "Rank"
                    }
                }
            ]
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '3df4c133276e4c2bacfcc220e713a4a7'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    operationLocation = response.headers.get("operation-location")
    operationLocationSplit = operationLocation.split("jobs/")
    jobId = operationLocationSplit[1]

    url = "https://meeting-manager-bot-text-analytics.cognitiveservices.azure.com/text/analytics/v3.2-preview.1/analyze/jobs/{}".format(jobId)

    payload={}
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '3df4c133276e4c2bacfcc220e713a4a7'
    }
    time.sleep(10)
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)

    sentences = []
    sentenceRankScore = []

    # print(data)

    sentenceObjects = data['tasks']['extractiveSummarizationTasks'][0]['results']['documents'][0]['sentences']
    for j in range(0,len(sentenceObjects)):
        sentences.append([sentenceObjects[j]['text'], sentenceObjects[j]['rankScore']])
        # sentenceRankScore.append(sentenceObjects[j]['rankScore'])
        # print(sentenceObjects[j]['text'])

    # print(sentences)
    df = pd.DataFrame(sentences, columns=['Sentence', 'Rank Score'])
    print(df)


import requests
import json
import time
import pandas as pd

def my_logic(trancript,meetingMinutes, participantsList, followUp):
    newTextFile = trancript.splitlines()
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    statementslist = []
    nameslist = []
    speakerstatements = []

    for x in newTextFile[2::4]:
        statementslist.append(x)

    for x in newTextFile[1::4]:
        nameslist.append(x)

    for a in range(0, len(nameslist)):
        speakerstatements.append([nameslist[a], statementslist[a]])

    df2 = pd.DataFrame(speakerstatements, columns=['Name', 'Sentence'])
    print(df2)

    # print(statementslist)
    # print(nameslist)

    statements = ' '.join(statementslist)

    url = "https://meeting-manager-bot-text-analytics.cognitiveservices.azure.com/text/analytics/v3.2-preview.1/analyze"

    payload = json.dumps({
        "analysisInput": {
            "documents": [
                {
                    "language": "en",
                    "id": "1",
                    "text": statements
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

    # df.Speaker = df.Sentence.map(df2.set_index('Sentence').Name)
    # df.merge(df2.rename(columns={'Name': 'Person'}), on='Sentence')
    # df3 = pd.merge(df, df2)
    # df.merge(df2[['Sentence', 'Name']], 'left')
    result = pd.concat([df, df2], axis=1, join="inner")

    result = df[df2["Sentence"] == df["Sentence"]]


    print(result)


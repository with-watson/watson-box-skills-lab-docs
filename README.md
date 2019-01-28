# Document Enrichment using Watson Natural Language Understanding with Box Custom Skills

## Introduction

In this lab we will create a simple and powerful custom skill powered by the [IBM Watson Natural Language Understanding service](https://www.ibm.com/watson/services/natural-language-understanding/). This capability will allow you to gain AI insights from a .docx file that is uploaded to a Box to make it more searchable and consumable to enhance and automate your business process. Your file will be enriched by Watson with metadata, such as concepts and keywords, that are relevant to the content of your document. This metadata is then attached to the original file in Box and displayed visually as a Skills "card". 

## Important Note

This code is being provided AS-IS for evaluation purposes and is not a production solution. Many additional aspects need to be considered before implementing a custom skill in production. This example is supported on Mac and Linux. To deploy using Windows, you would need to generate a Microsoft-compatible script like the `deployCapability.sh` provided.

## Prerequisites

* An [IBM Cloud account](https://console.bluemix.net/)
* The [IBM Cloud Functions CLI](https://console.bluemix.net/docs/openwhisk/bluemix_cli.html#cloudfunctions_cli)
* An instance of IBM Watson's Natural Language Understanding Service (available [here](https://console.bluemix.net/catalog/services/natural-language-understanding))
* A Docker account and [Docker Desktop](https://www.docker.com/products/docker-desktop)
* A [Box developer account](https://developer.box.com/)

## Configuration for Watson NLU service

This skill is expecting a `config.json` file to be present in the root folder of the skill. An example `config.json.example` has been provided that you can leverage and rename accordingly. 

### API Key & Endpoint

Your Natural Language Understanding service credentials can be found in the service at Service Credentials > New Credentials > Add. Then, click View Credentials to copy your API key & URL.

![Api Key Example](/docs/api_key_example.png)

Paste your API key to the top of the config.json file as such and update your URL accordingly:

```json
"nlu_iam_key": "<YOUR API KEY>"
"url": "<YOUR URL>"
```

### Text Analytics Feature Configuration

Also included in your `config.json` file are several keys that control the output of AI enrichments as metadata to the Box Skill card.
* A `keywords` key that causes the card to display keywords when set to `true`.
* A `concepts` key that causes the card to display concepts when set to `true`.
* A `keyword_limit` key that controls the maximum amount of keywords to show in the card. (Note: It is possible to show less than this limit if fewer keywords are detected in the source document)
* A `concept_limit` key that controls the maximum amount of concepts to show in the card. (Note: It is possible to show less than this limit if fewer concepts are detected in the source document)

Please note that there are additional enrichments provided by Watson's NLU service such as entities, sentiment, emotion and categories. To view more information on all of these enrichments, visit the documentation:  https://cloud.ibm.com/apidocs/natural-language-understanding#text-analytics-features

As an example, the information included in the `config.json.example` file  will show the top 5 detected concepts and keywords in the Box Skill Card

```
  "keywords": true,
  "concepts": true,
  "keyword_limit":5,
  "concept_limit": 5
  ```
Finally, there is one other key in your `config.json` that is called `storage`. This defines the location of the file that you want to analyze, which in this case is Box, and is referenced from the `storage.py` accordingly. Do not modify this value.

### Deploying the Skill

1. Login to the IBM Cloud CLI by running the command `ibmcloud login` and input your credentials when prompted. Then, specify your org and space by running the command `ibmcloud target -o <YOUR_ORG> -s <YOUR_SPACE>`.
2. From the main root of the repository run the command `deployCapability.sh <NAME OF SKILL>` where <NAME OF SKILL> can be whatever name you want to call your skill.
3. Navigate to https://console.bluemix.net/openwhisk/actions to look at your newly created function. Click on its name and then navigate to the 'Endpoints' tab in the sidebar. Copy the URL under Web Action (should end in .json). This URL will later be registered with Box to activate the skill.
4. Using the URL gathered in the last step as the invocation url, [Follow the steps here to register your skill with Box](https://developer.box.com/docs/configure-a-box-skill). (This skill will only work on .docx files, so it is recommended to limit the invocations of this skill to the appropriate filetype during this process)

And you have done it! Now any .docx files uploaded to the registered Box folder will invoke the custom skill. So drop a .docx file in, and within a few seconds, view the AI insights provided by Watson!

![Example picture](/docs/DocEnrichmentSkill_example.png)

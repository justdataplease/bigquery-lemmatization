# Microservices as Functions in BigQuery - Words Lemmatization using SQL (Part 3)

## How to reproduce

***Perform the following actions

Enable Google Cloud Functions. Read more [here](https://cloud.google.com/functions/docs/create-deploy-gcloud). \
Install and configure gcloud CLI. Read more [here](https://cloud.google.com/functions/docs/create-deploy-gcloud). 

***Replace the following with your own

1) \<your-project-id>
2) \<gcf-endpoint> (step 2)
3) \<gcf-conn> (step 3)

### 1. Clone the repository

    git clone https://github.com/justdataplease/bigquery-lemmatization.git

### 2. CLI : Deploy Cloud Function (gcf)

    gcloud functions deploy bigquery-lemmatization --gen2 --runtime python39 --trigger-http --project=<your-project-id> --entry-point=lemmatize --source . --region=europe-west3 --memory=256Mi --max-instances=3 --allow-unauthenticated

Visit Google [Cloud Console Functions](https://console.cloud.google.com/functions/list?project=) to retrieve <
gcf-endpoint> (i.e https://bigquery-lemmatization-xxxxxx.a.run.app)

### 3. CLI : Create a connection between BigQuery and Cloud Functions (gcf-conn).

    gcloud components update
    bq mk --connection --display_name='my_gcf_conn' --connection_type=CLOUD_RESOURCE --project_id=<your-project-id> --location=EU gcf-conn
    bq show --project_id=<your-project-id> --location=EU --connection gcf-conn

From the output of the last command, note the name <gcf-conn-name> (i.e. xxxxxx.eu.gcf-conn)

### 4. CLI : Create a toy dataset

    bq mk --dataset_id=<your-project-id>:lemmatization --location=EU

### 5. BIGQUERY : Create a Remote Function

    CREATE OR REPLACE FUNCTION `lemmatization.lemmatize`(text STRING)
    RETURNS STRING
    REMOTE WITH CONNECTION `<gcf-conn-name>`
        OPTIONS (
            -- change this to reflect the Trigger URL of your cloud function (look for the TRIGGER tab)
            endpoint = '<gcf-endpoint>'
        );

### 6. BIGQUERY : Test the Remote Function

    -- Define corpus
    DECLARE enString STRING;
    SET enString = "The|cats|are|sitting|on|the|couch";

    SELECT `justfunctions.lemmatization.lemmatize`(enString) word_lemmas

    -- Output
    The|cat|be|sit|on|the|couch

### 7. CLI : Remove everything

    # Remove Cloud Function (gcf)
    gcloud functions delete bigquery-lemmatize --region=europe-west3 --project=<your-project-id> --gen2

    # Remove DATASET
    bq rm -r -f -d <your-project-id>:lemmatization

    # Remove connection between BigQuery and Cloud Functions (gcf-conn)
    bq rm --connection --location=EU <gcf-conn-name>
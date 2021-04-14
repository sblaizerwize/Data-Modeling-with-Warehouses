# **README**

## **Introduction**

Sparkify is a digital music application that enables users to listen to music online. Currently, the application aims to offer new content to users based on their song preferences. However, the information collected from users, including songs and user logs (metadata), is stored in JSON files in a S3 bucket, which avoids querying data and therefore running analytics on it. As follows, you can find excerpts of the JSON files. 

JSON file containing song's information. 
```
{
    "num_songs": 1,
    "artist_id": "ARD7TVE1187B99BFB1",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "California - LA",
    "artist_name": "Casual",
    "song_id": "SOMZWCG12A8C13C480",
    "title": "I Didn't Mean To",
    "duration": 218.93179,
    "year": 0
}
```


JSON file containing user logs information. 
```
{
    "artist": null,
    "auth": "Logged In",
    "firstName": "Walter",
    "gender": "M",
    "itemInSession": 0,
    "lastName": "Frye",
    "length": null,
    "level": "free",
    "location": "San Francisco-Oakland-Hayward, CA",
    "method": "GET",
    "page": "Home",
    "registration": 1540919166796.0,
    "sessionId": 38,
    "song": null,
    "status": 200,
    "ts": 1541105830796,
    "userAgent": "\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
    "userId": "39"
}
```
---

## **Proposed solution**

The proposed solution in this repository consists of a two-step migration process, see Figure 1. The first stage named **staging** extracts source data from the S3 bucket and loads it into an AWS Redshift cluster. Data is loaded into two staging tables. The second stage consists of a SQL-to-SQL ETL that extracts, transforms, and loads staging data into tables complying with a star schema design. The star schema  consists of a FACT table surrounded by DIMENSION tables that contain data attributes. A star schema is simple to implement because data located in fact tables is not normalized. Also, this schema fosters data fetching by performing direct join operations among the dimension tables and the fact table. 

![sparkify schema](/images/migration.png)
**Figure 1** Design of the AWS Datawarehouse.
<br />

---
## **Explanation of the files in this repository**

The following table describes the content of this repository. 

<table>
  <tr>
   <td><strong>File</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>create_tables_staging.py
   </td>
   <td>Python script that drops existing staging tables, and creates the required staging tables including staging_events and staging_songs.
   </td>
  </tr>
  <tr>
   <td>create_tables_star.py
   </td>
   <td>Python script that drops existing star schema tables, and creates the required star tables including songplay, songs, artists, users, and time.
   </td>
  </tr>
  <tr>
   <td>sql_queries_staging.py
   </td>
   <td>Python script that describes the queries for dropping and creating tables, and copying data from the S3 bucket to the staging tables.
   </td>
  </tr>
  <tr>
  <tr>
   <td>sql_queries_star.py
   </td>
   <td>Python script that describes the queries for dropping and creating tables, and inserting data from the staging tables into the star schema tables.
   </td>
  </tr>
  <tr>
   <td>etl_staging.py
   </td>
   <td>Python script that implements queries to copy data from the S3 bucket to the staging tables.
   </td>
  </tr>
  <tr>
   <td>etl_star.py
   </td>
   <td>Python script that implements queries to insert data from the staging tables into the star schema tables.
   </td>
  </tr>
  <tr>
   <td>dwh_test.ipynb
   </td>
   <td>Jupyter notebook that runs sample queries to test the final migration of data into the star schema tables. 
   </td>
  </tr>
  <tr>
   <td>dwh.cfg
   </td>
   <td>File that contains information about the AWS Redshift cluster, IAM role, and S3 bucket. 
   </td>
  </tr>
  <tr>
   <td>README.md
   </td>
   <td>File that contains the main information and instructions of how to use this repository.
   </td>
  </tr>
</table>

---
## **Prerequisites**

Before using this repository, you must comply with the following:

*   Create an AWS IAM role   
*   Attach a policy to the IAM role to read data from a S3 bucket
*   Create an AWS Redshift Cluster
*   Open an incoming TCP port to access the cluster endpoint
*   Clone this repository

---
## **How to run the Python scripts**

After you clone this repository:

1. Go to the root folder of this repository. 
2. Run on your terminal the following command to create the staging tables:

    ```python create_tables_staging.py```

3. Run on your terminal the following command to perform the extraction, and loading of records from the source files of the S3 bucket into the staging tables of the Redshift cluster:

    ```python etl_staging.py```

    **Note: This step takes approximately 2 h**

4. Run on your terminal the following command to create the tables with the star schema design: 

    ```python create_tables_star.py```

5. Run on your terminal the following command to perform the extraction, transformation and inserting of the records from the staging tables into the the tables with the star schema design:

    ```python etl_star.py```

6. Run step-by-step the `dwh_test.ipynb` to test the two-step migration  process. 

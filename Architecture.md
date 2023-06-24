# Architecture

## Lambda

It's a parallel computing of streams and batches.<br>
You stream continously, but whith some periodicity you overwrite stream data with batch processed data

 
 ```
            Batch layer 
        /                 \
 Source                     Serving layer
        \                 /
          Streaming layer
```

Pro:
- speed from stream
- reliability from batch
- simple reprocessing (just restart batch process for needed period) 

Contra:
- You need to handle same business logic for two of that processes


## Kappa

In that architecture you consider batches as a special case of streaming

```Source - Log - Streaming layer - Serving layer```

And streaming layer contains log (like databases do, in ther replication process)

So when you need to reprocess something, you just delete old stream and restart it from some checkpoint in log.


Pro:
- fast streaming

Contra:
- reprocessing can be hard. You need to choose right instruments, to not end up like regular streaming 


## Delta

it's "unofficial" architecture pattern, based on delta lake capabilities<br>

It's like Kappa, but based on delta lake, so it's much more simpler to reprocess

### Delta Table
	It's framework, based on Parquet files, but it's implement ACID'ness for handling concurrent access to one parquet file.
	Delta lake handle all files in Parquet, but also has transaction log (json), which contains all transactions info.
	Every 10 transactions that json converts to new parquet checkpoint, so it will be simpler to read it.

	Delta lake has optimistic concurrency control, so when two transactions start manipulate with data, based on same log id file, when transaction finished, it need to check, if there their base log id still latest. If not - transaction reprocess it, based on new transaction log

## Inmon

It's approach, where you at first create normalized tables, and only after you create needed dashboards

pro:
- you can create new dashboards easily from already prepared data

contra:
- some dashboards can overlap information (no single source of truth)

## Kimpball

In this approach you need at first to understand, which dashboards do you need, and after that make ETL processes exactly for them

pro:
- single source of truth

contra:
- you need to implement full etl process for each dashboard

## Data Vault

Killer-feature of that approach - it's to separate data and relations (so you will not use PK-FK relations between fact tables)

You have this objects:
- Hub: contains only business object. Key can be business key, or surrogate key (hash from business)
- Sattelite: contains information about object (you can create as many satellites, as you want). can be linked only to hub
- Link: contains relations between Hubs

Also, in Data Vault paradigm Link-tables can have their own satellite (to store facts)


## Anchor Model

Pretty similar to Data Vault, but it's on hard-mode

You have this objects:
- Anchor: contains only business object. And contains only surrogate key. Business key it's just an attribute
- Attribute: contains information about object, and you should create table for each attribute
- Tie: contains relations between Anchors
- Knot: it's object for Anchor+Attribute, but i don't sure, that you want to use it.

And in AM you can't link Attributes tables to Tie


## Clouds

IaaS - Infrastructure as a service (Virtual Machine)
PaaS - Platform as a servise ()
SaaS - Software as a service

### Comparison between clouds and on-prem solutions

| Function | AWS | Azure | GCP |
| ---------| --- |----- | --- |
| Virtual machine/ Server | EC2 ||
| Docker | ECS ||
| Kubernetes | EKS ||
| VM Cluster (Serverless container) | Fargate ||
| Serverless Function | Lambda ||
| Storage for VM | EBS ||
| File storage | S3 ||
| Relational Data Base (Amazon Aurora, MySQL, MariaDB, PostgreSQL, Oracle, MSSQL) | RDS ||
| Key Value DB | Dynamo DB ||
| inMemory DB | ElasticCashe ||
| Document DB | DocumentDB (MongoDB compatible) ||
| Graph DB | Neptune ||
| Monitoring | CloudWatch ||
| Load Balancer | ELB ||
| Message Broker (kafka) | SNS ||
| Queue | SQS ||


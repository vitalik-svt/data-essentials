# Architecture

## Lambda

It's a parallel computing of streams and batches.<br>
So you need to handle same business logic for two of that processes

## Kappa

In that architecture you consider batches as a special case of streaming

## Delta

it's "unofficial" architecture pattern, based on delta lake capabilities<br>

### Delta Table
	It's framework, based on Parquet files, but it's implement ACID'ness for handling concurrent access to one parquet file
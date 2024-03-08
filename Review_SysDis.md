# Review and System Design


## Review algorithm

Me, personnaly divide review to three parts:

1. **Is code working as it is?**
	*In standalone environment. There i need to check all logic inside functions and so on. It's similar to unit-testing, and in test covered production maybe not so nessecary, because we assume, that code tested before pull request*

2. **Will code be working in production environment?**
	*How that code will interact with other things in production?*

	- Is the pipeline idempotent? 
	- Are they incorrectly using "current time" in the pipeline?
	- Are they using date > "start date" without a corresponding date < "end date" 
	- Are they doing JOINs with SCD (slowly changing dimension) tables that don't have the needed timeframe filters?
    - Is there "dtm", "source", another technical fields?

	- Is the data model efficient? 
	- Is there any excessive data duplication?
    - Is SQL efficient?
    - Is there nulls, how it handled?
	- Could they leverage complex data types for a better model?  
	- Are the column names reasonable and understandable? 

	- Do they have data quality checks at all?
	- Are they checking for NULLs, duplicates, and malformed values?
	- Are they doing row count anomaly detection?  
	- Will any of these quality checks be excessively noisy?

	- Can pipeline be less costy (in cloud solutions)?

3. **Refactoring**
	*Can code be cleaner, with the same functionality?*



## System Design questions

- You drive the process!
- You should clarify all requirements in the start!

    dev part:
    - How many users/data in the system?
    - is that system for company, or regional, global?
    - is data availiability crucial?
    - what about data latency?
    - OLTP/OLAP share
    - what features should be implemented?
    
    data part:
    - what is source of data?
    - Is it need to be batch or streaming? with which frequency, if batch?
    - size of data?
    - is it migration, or new system? 
    - who will use that system? BA, DS, OPS? 
    - What is target? BI?

- You should continiously ask, if your client understand your way of thinkning!

### links
- https://www.youtube.com/watch?v=Be7INI_U6GY
- https://github.com/donnemartin/system-design-primer
- Youtube channel "system design interview"


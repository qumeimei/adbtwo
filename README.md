(a)
Yu Zheng yz2583
Jingyi Guo jg3421

(b)
README.txt
result.txt:	the result of testing queries "snow leopard", "gates", "columbia"
adbone:
	Makefile
	run.sh

	
(c)
Compile
1. move to the adbone directory:
	$ cd adbone
2. compile .java and make a .jar file:
	$ make
3. if necessary, you clean compiled files and transcripts:
	$ make clean

Run


After each test, this program will record the transcript to a file named "transcript.txt".

(d)
In the part 2, 
we use MQLRead API to send MQL queries to Freebase. In the question of "Who created [x]",
we defined the queries separately as followings:
1. [{
	"/book/author/works_written": [{
		"a:name": null,
		"name~=": "[x]"
	}],
	"id": null,
	"name": null,
	"type": "/book/author"
}]
2. [{
	"/organization/organization_founder/organizations_founded": [{
		"a:name": null,
		"name~=": "[x]"
	}],
	"id": null,
	"name": null,
	"/organization/organization_founder"
}]

For the names we got by 1, we labelled as (as Author) and for those from 2, we labelled as (as Businessperson).
We mapped names and their book or established institution using a hashMap with one key multiple values, and print 
them alphabetically.
The following is the table we used to map from Freebase properties to the entities of interest that we return.

Freebase property	                                           Entity property
/book/author/works_written	                                      as Author
/book/author	
/organization/organization_founder/organizations_founded	  as Businessperson
/organization/organization_founder


(f)
Account_Key = "AIzaSyCKMFQ2Ia1mRjEZzQS2Newi2AZQnrCkPLU"
100,000 requests/day,which is 1 request per second per user 


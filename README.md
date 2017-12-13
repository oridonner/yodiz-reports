This Yodiz version(v0.1.6), imports on daily basis, data from Yodiz through Yodiz API, into Postgres YodizDB.
Daily sprints summary reports and Capacity reports are sent to sprint's conductor, QA & Autumation Manager and R&D Manager.

Examples:
truncate issues table and import issues resource to yodizdb database
./yodiz.py pull -r "issues" -tr

build views ddl for yodizdb database
./yodiz.py build --views -d

execute ddl views for yodizdb database
./yodiz.py build --views -x

email sprint report to mailing list
./yodiz mail --sprints -ls
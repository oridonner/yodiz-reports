# get issues
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/issues?fields=all&limit=50&offset=1650' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'
# get issues : specific fields
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/issues?fields=id,severity&limit=50&offset=1650' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'

# get projects
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'

# get users
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/users' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'


# get realeses no limit property in query
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/releases?fields=status' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/releases?fields=id,title,owner,createdon,updatedon,startdate,enddate,status' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'

# Get sprints
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/sprints?fields=all' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'

# Get tasks
curl -X GET 'https://app.yodiz.com/api/rest/v1/userstories/1466/tasks?fields=all' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'
curl -X GET 'https://app.yodiz.com/api/rest/v1/userstories/1464/tasks?fields=all' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'

# get userstories
curl -X GET 'https://app.yodiz.com/api/rest/v1/projects/4/userstories?limit=1&fields=all&offset=0' -H 'api-token: v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4' -H 'api-key: 083c5c49-c1cc-490b-bffa-58b6d457ab57'
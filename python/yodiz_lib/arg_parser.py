import argparse as ag


# function description: parses the arguments received from the user
# function arguments: none
# return value: dictionary with each argument and its value
def params():
    parser = ag.ArgumentParser("Import resources from Yodiz")

    ##sqream subparser##
    subparsers = parser.add_subparsers(description="Yodiz API CLI",help='sub-command help')
    
    parser_build = subparsers.add_parser('build', help="builds postgres Yodizdb")
    parser_build.add_argument("-t", "--table", help="recreate specific table and its relevat views from script")
    parser_build.add_argument("-db", "--database", help="recreates all database objects from script")
    parser_build.add_argument("-s", "--show", help="show objects created from script")
    
    parser_pull = subparsers.add_parser('pull', help="import resources from Yodiz")
    parser_pull.add_argument("-r", "--resource", help="name of resource to import")
    parser_pull.add_argument("-tk", "--token", help="yodiz api token", default="v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4")
    parser_pull.add_argument("-k", "--key", help="yodiz api key", default="083c5c49-c1cc-490b-bffa-58b6d457ab57")
    parser_pull.add_argument("-a", "--add",action='store_true',default=True, help="recreate postgres tabe before import")
    parser_pull.add_argument("-tr", "--truncate",action='store_true',default=False, help="truncate postgres tabe before import")
    
    
    parser_mail = subparsers.add_parser('mail', help="send different alerts to users")
    parser_mail.add_argument("-i", "--issues", nargs = 1,help ="name of resource ")
    parser_mail.add_argument("-u", "--userstories", nargs = 1,help ="name of resource ")
   # parser_mail.add_argument("-r", "--report", nargs = 1,choices =['user bugs','bugs severity','bugs mtd'],help ="name of report to send")


    flags = parser.parse_args()
    return vars(flags)

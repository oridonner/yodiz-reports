import argparse as ag

import sys

# function description: parses the arguments received from the user
# function arguments: none
# return value: dictionary with each argument and its value
reports=[]
reports.append('sprints summary')
reports.append('sprint userstories')

def params():
    parser = ag.ArgumentParser("Import resources from Yodiz",fromfile_prefix_chars='@')
    subparsers = parser.add_subparsers(description="Yodiz API CLI",help='sub-command help',dest='cmd_object')
    
    # build positional argument
    parser_build = subparsers.add_parser('build', help="builds postgres Yodizdb")
    build_group = parser_build.add_mutually_exclusive_group(required = True)
    #build_group.add_argument("-t", "--table", help="recreate specific table and its relevat views from script")
    build_group.add_argument("--ddl", help="creates ddl script file",action='store_true')
    build_group.add_argument("--database", help="executes ddl script file",action='store_true')
    build_group.add_argument("--views", help="executes views ddl script file",action='store_true')
    #build_group.add_argument("-s", "--show", help="show objects created from script")
    
    # pull positional argument
    parser_pull = subparsers.add_parser('pull', help="import resources from Yodiz")
    parser_pull.add_argument("-r", "--resource", help="name of resource to import",required = True)
    parser_pull.add_argument("-tk", "--token", help="yodiz api token", nargs='?',default="v29APgj5S3I6PvjbHu8l2az-IpQtZhe1n2hGDXOAKv4")
    parser_pull.add_argument("-k", "--key", help="yodiz api key", nargs = '?', default="083c5c49-c1cc-490b-bffa-58b6d457ab57")
    pull_group = parser_pull.add_mutually_exclusive_group(required = True)
    pull_group.add_argument("-a", "--add",action='store_true',default=True, help="recreate postgres tabe before import")
    pull_group.add_argument("-tr", "--truncate",action='store_true',default=False, help="truncate postgres tabe before import")
    
    # query positional argument
    query_parser = subparsers.add_parser('query', help="query data from YodizDB on postgres")
    query_group = query_parser.add_mutually_exclusive_group(required = True)
    query_group.add_argument('--sprints',help="get sprints names from postgers YodizDB", action='store_const', const='vw_sprints_headers')

    # mail positional argument
    mail_parser = subparsers.add_parser('mail', help="send different alerts to users")
# mail_parser.add_argument("-t", "--test", nargs = '+', help = "sends ori and yuval test mail",dest = 'cc')
#    mail_parser.add_argument("-t1", "--test", nargs = '+', help = "sends ori test mail",dest = 'cc')
    mail_parser.add_argument("-ls", "--mailing-list",action='store_true',default=False, help = "sends mail to default mailing list")
    mail_parser.add_argument("-o", "--output-file",action='store_true',default=False, help = "output report as html file")
    mail_group = mail_parser.add_mutually_exclusive_group(required = True)
    mail_group.add_argument("--sprints", help="mail sprints summary report",action='store_true')
    mail_group.add_argument("--capacity", help="mail capacity summary report",action='store_true')
    mail_group.add_argument("--release", help="mail release summary report",action='store_true')
    mail_group.add_argument("--inv", help="mail inventory summary report",action='store_true')
    return parser.parse_args()

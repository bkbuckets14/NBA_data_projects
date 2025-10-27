#function to get database information from a password file
def get_database_url(args):

    #if there is no password file passed
    if args.pwd == None:
        ROOT_PASSWORD = "admin"
        DATABASE_NAME = "basketball_db"
        CONTAINER_NAME = "mysql_container"
    #if there is a password file passed
    else:
        with args.pwd as ff:
            url_info = ff.readlines()
            ROOT_PASSWORD = url_info[0].split(":")[1].strip()
            DATABASE_NAME = url_info[1].split(":")[1].strip()
            CONTAINER_NAME = url_info[2].split(":")[1].strip()

    #form DATABASE_URL
    DATABASE_URL = "mysql+mysqlconnector://root:"+ROOT_PASSWORD+"@"+CONTAINER_NAME+":3306/"+DATABASE_NAME

    #return DATABASE_URL
    return DATABASE_URL
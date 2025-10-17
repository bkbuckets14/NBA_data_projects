def get_database_url(args):

    if args.pwd == None:
        ROOT_PASSWORD = "admin"
        DATABASE_NAME = "database"
        CONTAINER_NAME = "mysql_container"
    else:
        with args.pwd as ff:
            url_info = ff.readlines()
            ROOT_PASSWORD = url_info[0].split(":")[1].strip()
            DATABASE_NAME = url_info[1].split(":")[1].strip()
            CONTAINER_NAME = url_info[2].split(":")[1].strip()

    DATABASE_URL = "mysql+mysqlconnector://root:"+ROOT_PASSWORD+"@"+CONTAINER_NAME+":3306/"+DATABASE_NAME

    return DATABASE_URL
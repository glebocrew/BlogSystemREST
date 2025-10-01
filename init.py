from db import *
from logger import Logger


conf = load(open("confs/conf.json", encoding="utf-8"))
sql = load(open(conf["db"]["queries"], encoding="utf-8"))

init_logger = Logger(conf["logger"]["init"])


mariamanager = MariaConnection(
    host=conf["db"]["conn"]["host"],
    port=conf["db"]["conn"]["port"],
    user=conf["db"]["conn"]["user"],
    password=conf["db"]["conn"]["password"],
    database=conf["db"]["conn"]["database"]
)


try:
    init_logger.log(
        status="l", 
        message="Initializing users"
    )

    mariamanager._execute(
        query=sql["init_users"],
        data=[]
    )

    init_logger.log(
        status="l",
        message="Users are successfully initialized"
    )

except Exception as e:
    init_logger.log(
        status="f", 
        message=f"Initialization failed! Full exception {e}"
    )

try:
    init_logger.log(
        status="l", 
        message="Initializing posts"
    )

    mariamanager._execute(
        query=sql["init_posts"],
        data=[]
    )

    init_logger.log(
        status="l",
        message="Posts are successfully initialized"
    )

except Exception as e:
    init_logger.log(
        status="f", 
        message=f"Initialization failed! Full exception {e}"
    )

    
    


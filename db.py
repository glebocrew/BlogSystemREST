from mariadb import Connection, Cursor

from uuid import UUID
from typing import Dict, List

from datetime import datetime
from sys import exit
from json import load
from uuid import uuid4
from hashlib import sha512

from models import InvalidMariaArguments, User, Post

from logger import Logger

confs = load(open("confs/conf.json", encoding="utf-8"))
queries = load(open(confs["db"]["queries"], encoding="utf-8"))

db_logger = Logger(confs["logger"]["db"])


class MariaConnection:
    """
        Class that established connection with MariaDB and provides plenty of operations with it
        
        :param host: hostname of a DB server (ex. "localhost"/"127.0.0.1")
        :type host: str

        :param port: port of a DB server that is installed on host
        :type port: int

        :param user: username of a user that executes queries, make sure that it has enough permissions.
        :type user: str

        :param password: user's password
        :type password: str

        :param database: name of a database that contains tables
        :type database: str
    """

    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            database: str
        ) -> None:

        if type(port) != int:
            try:
                port = int(port)
            except Exception as e:
                exit(-1)
            
        self.args = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }

        try:
            db_logger.log(
                status="l", 
                message="Testing mariadb connection"
            )
            
            self.mariaconn = Connection(**self.args)

            db_logger.log(
                status="l", 
                message="Connection is successful"
            )

        except Exception as e:
            db_logger.log(
                status="f",
                message=f"Connection failed! Full error {e}"
            )

            raise InvalidMariaArguments("Maria arguments are incorrect!")
        
        self.mariaconn.close()

    def _open_session(
            self
        ) -> None:
        """
        Opens new mariadb session

        :returns: none
        :rtype: None
        """

        try:
            db_logger.log(
                status="l",
                message="Creating new mariadb session"
            )
            
            self.mariaconn = Connection(**self.args)
            self.mariaconn.autocommit = True
            self.mariaconn.auto_reconnect = True

            self.cursor = Cursor(self.mariaconn)

            db_logger.log(
                status="l",
                message="Mariadb session created successfully"
            )

        except Exception as e:
            db_logger.log(
                status="f",
                message=f"Something went wrong with mariadb. Probably it's a problem with it's args. Full exception {e}"
            )

            raise InvalidMariaArguments("Maria arguments are incorrect!")

    
    def _execute(
            self,
            query: str,
            data: tuple
        ) -> tuple:
        """
        Executes any query.

        :param query: sql query
        :type query: str

        :param data: data that you need to insert into query
        :type data: tuple

        :returns: empty tuple of fetched tuple
        :rtype: tuple
        """
        self._open_session()

        try:
            db_logger.log(
                status="l", 
                message="Executing query"
            )
            
            self.cursor.execute(
                statement=query,
                data=data
            )

            db_logger.log(
                status="l",
                message="Query executed successfully"
            )
        except Exception as e:
            db_logger.log(
                status="e",
                message=f"An exception was raised while executing the query. Full exception: {e}"
            )

            return ["400"]
        
        try:
            info = self.cursor.fetchall()
        except:
            return []

        if info:
            return info
        else:
            self.mariaconn.close()
            return []


   
    def get_users(self) -> list:
        """
        Gets all users from table
        
        :returns: list with all users
        :rtype: list
        """
        try:
            db_logger.log(
                status="l",
                message="Getting all users"
            )

            data = self._execute(
                query=queries["get_users"],
                data=[]
            )

            if (len(data) > 0 and data[0] != "400") or (len(data) == 0):
                db_logger.log(
                    status="l",
                    message="Users were got successfully"
                )
            else:
                db_logger.log(
                    status="l",
                    message="Something went wrong! Read logs higher"
                )

            outlist = []
            for user in data:
                outlist.append({
                    "id": user[0],
                    "email": user[1],
                    "login": user[2],
                    "password": user[3],
                    "createdAt": user[4],
                    "updatedAt": user[5]
                })

            return outlist    
        except Exception as e:
            db_logger.log(
                status="e",
                message=f"Users were not got correctly! Full exception: {e}"
            )
            return ["404"]
    
    def create_user(
            self,
            email: str,
            login: str,
            password_unhashed: str,
        ) -> None:
        """
        Creating new user in database

        :param email: user's email
        :type email: str

        :param login: user's login
        :type login: str

        :param password_unhashed: unhashed password
        :type password_unhashed: str

        :returns: none
        :rtype: None
        """

        try:
            check = self._execute(
                query=queries["check_user"],
                data=(email, login,)
            )
        
            if check:
                return 0

            self.password_unhashed = password_unhashed
            self.password_hashed = sha512()

            self.password_hashed.update(
                self.password_unhashed.encode(
                    encoding="utf-8"
                )
            )


            self.new_user = User(
                id=uuid4(), 
                email=email, 
                login=login, 
                password=self.password_hashed.hexdigest(),
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )

            db_logger.log(
                status="l",
                message="Creating new user"
            )

            status = self._execute(
                query=queries["create_user"],
                data=(
                    self.new_user.id,
                    self.new_user.email,
                    self.new_user.login,
                    self.new_user.password,
                    self.new_user.createdAt,
                    self.new_user.updatedAt,
                )
            )

            if (len(status) > 0 and status[0] != "400") or (len(status) == 0):
                db_logger.log(
                    status="l",
                    message="User created successfully"
                )

                return ["200"]
            else:
                db_logger.log(
                    status="l",
                    message="Something went wrong! Read logs higher"
                )
                return ["400"]
        except Exception as e:
            db_logger.log(
                status="e",
                message=f"Something went wrong! Full exception: {e}"
            )
            
            return ["400"]
    
    
    def get_user(
            self,
            id: str = "",
        ) -> list:
        """
        Gets all user's info

        :param id: user's id
        :type id: str
        
        :returns: list with all user's information
        :rtype: list
        """

        try:

            db_logger.log(
                status="l",
                message="Getting user's info"
            )

            data = self._execute(
                query=queries["get_user"],
                data=(id,)
            )

            if (len(data) > 0 and data[0] != "400") or (len(data) == 0):
                db_logger.log(
                    status="l",
                    message="Users were got successfully"
                )
            else:
                db_logger.log(
                    status="l",
                    message="Something went wrong! Read logs higher"
                )

            outlist = []
            for user in data:
                outlist.append({
                    "id": user[0],
                    "email": user[1],
                    "login": user[2],
                    "password": user[3],
                    "createdAt": user[4],
                    "updatedAt": user[5]
                })

            if outlist == []:
                return ["404"]

            return outlist
        
        except Exception as e:
            return ["404"]


    def update_user(
            self,
            id: str,
            login: str,
            email: str,
            password_unhashed: str,
        ) -> List[str]:
        """
        Equivalent to PUT method

        :param id: current id
        :type id: str

        :param login: new login
        :type login: str

        :param email: new email
        :type email: str

        :param password_unhashed: new password
        :type password_unhashed: str

        :returns: none
        :rtype: None
        """

        try:
            db_logger.log(
                status="l",
                message="Updating user"
            )

            status = self._execute(
                query=queries["put_user"],
                data=(email, login, sha512(str(password_unhashed).encode("utf-8")).hexdigest(), datetime.now(), id)
            )
            
            try:
                if status[0] == "400":
                    return ["400"]
            except:
                db_logger.log(
                    status="l",
                    message="User was successfully updated"
                )

        except Exception as e:
            db_logger.log(
                status="e",
                message=f"Updating user failed! Full exception {e}"
            )
            return ["400"]

    def delete_user(
            self,
            id: str
        ) -> List[str]:

        try:
            db_logger.log(
                status="l",
                message="Deleting user"
            )

            status = self._execute(
                query=queries["delete_user"],
                data=(id,)
            )

            self.delete_posts(
                authorId=id
            )

            try:
                if status[0] == "400":
                    return ["400"]
                
            except:
                db_logger.log(
                    status="l",
                    message="User and it's posts was successfully deleted"
                )
        
        except Exception as e:
            db_logger.log(
                status="e",
                message=f"Deleting user failed! Full exception {e}"
            )
            return ["400"]

    def get_posts(self) -> list:
        """
        Gets all posts from table
        
        :returns: list with all users
        :rtype: list
        """
        db_logger.log(
            status="l",
            message="Getting all posts"
        )

        data = self._execute(
            query=queries["get_posts"],
            data=[]
       )

        if (len(data) > 0 and data[0] != "400") or (len(data) == 0):
            db_logger.log(
                status="l",
                message="Posts were got successfully"
            )
        else:
            db_logger.log(
                status="l",
                message="Something went wrong! Read logs higher"
            )

        outlist = []
        for post in data:
            outlist.append({
                "id": post[0],
                "authorId": post[1],
                "title": post[2],
                "content": post[3],
                "createdAt": post[4],
                "updatedAt": post[5]
            })

        return outlist

    def get_post(
            self,
            id: str = "",
        ) -> list:
        """
        Gets all post info

        :param id: post id
        :type id: str
        
        :returns: list with all information about post
        :rtype: list
        """

        try:

            db_logger.log(
                status="l",
                message="Getting post info"
            )

            data = self._execute(
                query=queries["get_post"],
                data=(id,)
            )

            if (len(data) > 0 and data[0] != "400") or (len(data) == 0):
                db_logger.log(
                    status="l",
                    message="Post was got successfully"
                )
            else:
                db_logger.log(
                    status="l",
                    message="Something went wrong! Read logs higher"
                )

            outlist = []
            for user in data:
                outlist.append({
                    "id": user[0],
                    "authorId": user[1],
                    "title": user[2],
                    "content": user[3],
                    "createdAt": user[4],
                    "updatedAt": user[5]
                })

            if outlist == []:
                return ["404"]

            return outlist
        
        except Exception as e:
            return ["404"]

    def create_post(
            self,
            author_id: str,
            title: str,
            content: str,
        ) -> list:
        """
        Creates a new post

        :param authorId: author's id
        :type authorId: UUID

        :param title: post's title
        :type title: str

        :param content: post's content
        :type content: str
        """
        try:

            if self.get_user(author_id) == []:
                db_logger.log(
                    status="e",
                    message="User does not exits"
                )
                return 0
        
            db_logger.log(
                status="l",
                message="Creating post"
            )

            status = self._execute(
                query=queries["create_post"],
                data=(uuid4(), author_id, title, content, datetime.now(), datetime.now())
            )

            try:
                if status[0] == "400":
                    db_logger.log(
                        status="d",
                        message="400"
                    )
                    return ["400"]
            except:
                db_logger.log(
                    status="l",
                    message="Post was successfully created"
                )

        except:
            return ["400"]

    def delete_post(
            self,
            id: UUID
        ) -> List[str]:
        """
        Deletes post by it's id

        :param id: post's id
        :type id: UUID
        """
        try:
            db_logger.log(
                status="l",
                message="Deleting post"
            )

            status = self._execute(
                query=queries["delete_post"],
                data=(id,)
            )

            try:
                if status[0] == "400":
                    return ["400"]
                
            except:
                db_logger.log(
                    status="l",
                    message="Post was successfully deleted"
                )
        except:
            return ["400"]
    
    def delete_posts(
            self,
            authorId: str
        ) -> None:
        
        """
        Deletes posts by author's id

        :param authorId: authors id
        :type authorId: UUID
        """

        db_logger.log(
            status="l",
            message="Deleting author's posts"
        )

        self._execute(
            query=queries["delete_all_user_posts"],
            data=(authorId,)
        )

        db_logger.log(
            status="l",
            message="Post was successfully deleted"
        )

    def update_post(
            self,
            id: str,
            title: str,
            content: str,
        ) -> List[str]:
        """
        Equivalent to PUT method

        :param id: post id
        :type id: str

        :param title: new title
        :type title: str

        :param content: new content
        :type content: str

        :returns: dictionary with code
        :rtype: Dict[str]
        """

        try:
            db_logger.log(
                status="l",
                message="Updating post"
            )

            status = self._execute(
                query=queries["update_post"],
                data=(title, content, datetime.now(), id)
            )
            
            try:
                if status[0] == "400":
                    return ["400"]
            except:
                db_logger.log(
                    status="l",
                    message="Post was successfully updated"
                )

        except Exception as e:
            db_logger.log(
                status="e",
                message=f"Updating [post] failed! Full exception {e}"
            )
            return ["400"]
        

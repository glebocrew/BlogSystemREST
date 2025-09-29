from os import path, getpid
from datetime import datetime

logs_init_msg = "=" * 5 + f"FILE CREATED {datetime.now()}" + "=" * 5 + "\n"

class Logger:
    filepath: str

    def __init__(self,
                 filepath: str
                 ) -> None:
        """
        A class that enables logging in the project
        
        :param filepath: the path of logs file
        :type filepath: str
        """
        self.filepath = filepath

        if not path.exists(path=self.filepath):
            self.file = open(file=self.filepath, mode="a+", encoding="utf-8")
            self.file.write(logs_init_msg)
        else: 
            self.file = open(file=self.filepath, mode="a+", encoding="utf-8")
        
    def log(self,
            status: str,
            message: str) -> None:
        
        status: str
        message: str

        """
        Logs some message

        :param status: d - debug, l - log, e - error, f - fatal
        :type status: str
        
        :param message: any text
        :type message: str
        """
        status_val = {
            "d": "DEBUG",
            "l": "LOG",
            "e": "ERROR",
            "f": "FATAL"
        }

        if status in status_val.keys():
            self.file.write(f"({datetime.now()}) [{str(getpid()):^5}] |{status_val[status]}| -> {message}\n")
        else:
            self.file.write(f"({datetime.now()}) [{str(getpid()):^5}] |{status.upper()}| -> {message}\n")

        self.file.flush()

from colorama import init, Fore, Style

init()


class Logger:
    def __init__(self, level=3):
        """
        Initialize the Logger object.

        :param int level: The logging level.
        """
        self.level = level
        self.log_levels = {
            "info": Fore.BLUE,
            "debug": Fore.CYAN,
            "warning": Fore.YELLOW,
            "error": Fore.RED,
            "critical": Fore.MAGENTA,
        }
        
        self.name_to_level = {
            "info": 0,
            "critical": 1,
            "error": 2,
            "warning": 3,
            "debug": 4,
        }
        
        self.level_to_name = {v: k for k, v in self.name_to_level.items()}
        
        
    def set_level(self, level):
        """
        Set the logging level.

        :param str|int level: The logging level to set.
        :return bool: True if the level was set successfully, False otherwise.
        """
        if isinstance(level, str):
            if level.isdigit():
                level = int(level)
            elif level in self.name_to_level:
                level = self.name_to_level[level]
            else:
                return False
        elif isinstance(level, int):
            if level not in self.level_to_name:
                return False
        else:
            return False
        
        self.INFO("Log level set to {}".format(self.level_to_name[level]))
        self.level = level
    

    def get_level(self):
        """
        Get the current logging level.

        :return int: The current logging level.
        """
        return self.level

    def log(self, level, text):
        """
        Log a message at the specified level.

        :param str level: The logging level of the message.
        :param str text: The message to log.
        """
        if self.level >= self.name_to_level[level]:
            timestamp = Style.BRIGHT + "[{}]".format(self.get_timestamp()) + Style.RESET_ALL
            log_level = self.log_levels[level] + level.upper() + Style.RESET_ALL
            print("{} {} {}".format(timestamp, log_level, text))
        # else:
        #     print("Log level too low to display message")

    def INFO(self, text):
        """
        Log an info message.

        :param str text: The info message to log.
        """
        self.log("info", text)

    def DEBUG(self, text):
        """
        Log a debug message.

        :param str text: The debug message to log.
        """
        self.log("debug", text)

    def WARNING(self, text):
        """
        Log a warning message.

        :param str text: The warning message to log.
        """
        self.log("warning", text)

    def ERROR(self, text):
        """
        Log an error message.

        :param str text: The error message to log.
        """
        self.log("error", text)

    def CRITICAL(self, text):
        """
        Log a critical message.

        :param str text: The critical message to log.
        """
        self.log("critical", text)

    def get_timestamp(self):
        """
        Get the current timestamp.

        :return str: The current timestamp in the format YYYY-MM-DD HH:MM:SS.mmm.
        """
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def main():
    logger = Logger()

    logger.INFO("This is an info message")
    logger.DEBUG("This is a debug message")
    logger.WARNING("This is a warning message")
    logger.ERROR("This is an error message")
    logger.CRITICAL("This is a critical message")


if __name__ == "__main__":
    main()
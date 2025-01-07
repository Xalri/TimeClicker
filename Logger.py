from colorama import init, Fore, Style

init()

class Logger:
    def __init__(self):
        self.log_levels = {
            'info': Fore.BLUE,
            'debug': Fore.CYAN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'critical': Fore.MAGENTA
        }

    def log(self, level, text):
        timestamp = Style.BRIGHT + '[{}]'.format(self.get_timestamp()) + Style.RESET_ALL
        log_level = self.log_levels[level] + level.upper() + Style.RESET_ALL
        print('{} {} {}'.format(timestamp, log_level, text))

    def INFO(self, text):
        self.log('info', text)

    def DEBUG(self, text):
        self.log('debug', text)

    def WARNING(self, text):
        self.log('warning', text)

    def ERROR(self, text):
        self.log('error', text)

    def CRITICAL(self, text):
        self.log('critical', text)

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def main():
    logger = Logger()

    logger.INFO('This is an info message')
    logger.DEBUG('This is a debug message')
    logger.WARNING('This is a warning message')
    logger.ERROR('This is an error message')
    logger.CRITICAL('This is a critical message')

if __name__ == "__main__":
    main()
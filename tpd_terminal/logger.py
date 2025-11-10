import logging
import sys
from colorama import init, Fore, Back, Style

init(autoreset=True)

class TPDLogger:
    def __init__(self, config):
        self.config = config
        self.setup_file_logger()

    def setup_file_logger(self):
        log_format = '%(asctime)s,%(levelname)s,%(message)s'
        logging.basicConfig(
            filename=self.config['output']['log_file'],
            level=self.config['output']['log_level'],
            format=log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.file_logger = logging.getLogger('TPD')

        # Also log to stdout with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.file_logger.addHandler(console_handler)

    def log(self, level, message):
        color_map = {
            'INFO': Fore.CYAN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'SIGNAL': Fore.GREEN + Style.BRIGHT
        }

        if self.config['output']['colors'] and level in color_map:
            colored_msg = f"{color_map[level]}{message}"
            print(colored_msg)
        else:
            print(message)

        self.file_logger.log(getattr(logging, level.upper()), message)

    def signal(self, signal_data):
        header = f"⚡ SIGNAL: {signal_data['type']} {signal_data['instrument']} @ {signal_data['entry']:.2f}"
        details = f"""
   Confidence: {signal_data['confidence']:.2%} | Impact: {signal_data['sweep_impact']:.2f}
   Entry: {signal_data['entry']:.2f} | Stop: {signal_data['stop']:.2f} ({signal_data['risk_percent']:.2f}%)
   Target: {signal_data['target']:.2f} (1.5R)
   Time: Execute within 30 seconds of sweep detection
"""
        self.log('SIGNAL', header + details)

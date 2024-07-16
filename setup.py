from colorama import Fore

IF_COLOR = 0

LENGTH = 10
HEIGHT = 20
SLEEP = 0.4

#字符显示
BLANK = '  '

if IF_COLOR:
    RED_BLOCK = Fore.RED+'█'+Fore.RESET
    GREEN_BLOCK = Fore.GREEN+'█'+Fore.RESET
    YELLOW_BLOCK = Fore.YELLOW+'█'+Fore.RESET
    BLUE_BLOCK = Fore.BLUE+'█'+Fore.RESET
    MAGENTA_BLOCK = Fore.MAGENTA+'█'+Fore.RESET
    CYAN_BLOCK = Fore.CYAN+'█'+Fore.RESET
    WHITE_BLOCK = '█'

else: 
    RED_BLOCK = '█'
    GREEN_BLOCK = '█'
    YELLOW_BLOCK = '█'
    BLUE_BLOCK = '█'
    MAGENTA_BLOCK = '█'
    CYAN_BLOCK = '█'
    WHITE_BLOCK = '█'

ICONS = [BLANK, RED_BLOCK, GREEN_BLOCK, YELLOW_BLOCK, BLUE_BLOCK, MAGENTA_BLOCK, CYAN_BLOCK, WHITE_BLOCK]

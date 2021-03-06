import cfg
import pd_interface
import obs_interface
import rpi_interface
import voice_interface
import animals
import talk_to_michael
import aggregate_commands
import extra_commands_handler

from datetime import datetime
import importlib

# interface functions to be called once a command match is found
interface_func_calls = {
	"obs":obs_interface.main,
	"pd":pd_interface.main,
	"rpi":rpi_interface.main,
	"text2speech":voice_interface.text2speech,
    "animal_sounds":animals.play_animal_sound,
    "aggregate_commands":aggregate_commands.call_interfaces,
    "extra_commands":extra_commands_handler.main
}


def call_interface(cmd_info, message, sender_username) -> None:
    """
    Does a few checks and then calls the appropriate interface to handle the command
    """
    importlib.reload(extra_commands_handler)
    
    # variable will be set to False if it fails a check
    command_unlocked = True
    
    # check whether the command has been unlocked
    if cmd_info[6]:
        if cmd_info[6] >= datetime.now():
            print(f"utilities: command {cmd_info[0]} is time locked")
            command_unlocked = False
        else:
            print(f"utilities: command {cmd_info[0]} is time unlocked")
    
    if command_unlocked:
        interface_func_calls.get(cmd_info[1])(cmd_info, message, sender_username)
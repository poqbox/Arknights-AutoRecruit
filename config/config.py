import configparser
import os


config_file = os.path.join(os.path.dirname(__file__), "config.ini")
v_config = configparser.ConfigParser()
v_config.read(config_file)

v_config["VERSION"] = {"AutoRecruit_ver": "1.0.0",
                       "recruitment_database_ver": "unknown"
                       }
v_config["PROFILES"] = {"last_used_profile": "DEFAULT"
                        }
with open(config_file, "w") as file:
    v_config.write(file)


def set_database_version(value):
    v_config["AutoRecruit"]["recruitment_database_ver"] = str(value)


def get_autorecruit_version():
    return v_config["VERSION"]["autorecruit_ver"]


def get_database_version():
    return v_config["VERSION"]["recruitment_database_ver"]


def get_last_used_profile():
    return v_config["PROFILES"]["last_used_profile"]


class Profile():
    def __init__(self, profile):
        folder_dir = os.path.dirname(__file__)
        self.profile_dir = os.path.join(folder_dir, "AutoRecruit_profiles", profile + ".ini")
        self.profile = profile
        self.config = configparser.ConfigParser()
        self.config.read(self.profile_dir)
        if not os.path.exists(self.profile_dir):
            # if profile does not exist, use default settings
            self.config["settings"] = {"emulator_path": r"C:\Program Files\Google\Play Games\Bootstrapper.exe",
                                       "emulator_title": "Google Play Games beta",
                                       "permits_num": "1",
                                       "recruitment_time": "01:00",
                                       "use_expedited_plans": "False",
                                       "prepare_end_recruits": "False",
                                       "priority_list": "6-star|5-star|4-star"
                                       }
        self.settings = dict(self.config.items("settings"))

    def get_profile(self):
        return self.settings

    def get_profile_option(self, option: str):
        return self.config["settings"][option]

    def save_profile(self):
        for key in self.settings:
            self.config["settings"][key] = self.settings.get(key)
        with open(self.profile_dir, "w") as file:
            self.config.write(file)

    def save_as_new_profile(self, profile_name):
        folder_dir = os.path.dirname(__file__)
        file_dir = os.path.join(folder_dir, "AutoRecruit_profiles", profile_name + ".ini")
        for key in self.settings:
            self.config["settings"][key] = self.settings.get(key)
        with open(file_dir, "w") as file:
            self.config.write(file)


def create_recruitment_profile(emulator_path: str, emulator_title: str, recruit_num: int=0, recruit_time: str="00:00",
                               use_expedited_plans=False, prepare_recruitment=False, priority_tags=[]):
    folder_dir = os.path.dirname(__file__)
    config = configparser.ConfigParser()
    config["settings"] = {}
    config["settings"]["emulator_path"] = emulator_path
    config["settings"]["emulator_title"] = emulator_title
    config["settings"]["permits_num"] = str(recruit_num)
    config["settings"]["recruitment_time"] = recruit_time
    config["settings"]["use_expedited_plans"] = str(use_expedited_plans)
    config["settings"]["prepare_end_recruits"] = str(prepare_recruitment)
    config["settings"]["priority_list"] = "|".join(priority_tags)

    with open(os.path.join(folder_dir, "AutoRecruit_profiles", "DEFAULT.ini"), "w") as profile:
        config.write(profile)


def delete_profile(profile: str):
    os.rmdir(os.path.join("AutoRecruit_profiles", profile + ".ini"))

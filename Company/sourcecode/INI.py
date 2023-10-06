import configparser

def write_ini(filename, settings:dict):
    """
    寫入INI文件。

    :param filename: INI文件的名字或路徑。
    :param settings: 一個字典，其中包含將寫入INI文件的設置。
    """
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve case for option names

    for section, options in settings.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, str(option), str(value))

    with open(filename, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def read_ini(filename):
    """
    讀取 INI 文件並返回一個字典，其中包含文件中的所有設置。

    :param filename: INI 文件的名字或路徑。
    :return: 一個字典，其中包含 INI 文件中的所有設置。
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(filename, encoding='utf-8')

    settings = {}
    for section in config.sections():
        settings[section] = {}
        for option in config.options(section):
            settings[section][option] = config.get(section, option)

    return settings

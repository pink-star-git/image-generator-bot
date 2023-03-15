# config lib v1.0 | 2022
# by zebra

class COSfig:
    var_name:str = ""
    var_value = 0
    cfg_name:str = ""
    file_name:str = ""
    file_path:str = ""
    def __init__(self, cfg_name:str, file_name:str, file_path:str) -> None:
        self.cfg_name = cfg_name
        self.file_name = file_name
        self.file_path = file_path
    def set_element(self, var_name:str, var_value) -> None:
        self.var_name = var_name
        self.var_value = var_value
    def get_element(self, var_name:str):
        return self.var_value if var_name == self.var_name else  ValueError(f"get name'{var_name}' != cfg name'{self.var_name}'")

class Config:
    cfg_d:dict = {}
    cfg_name:str = ""
    file_name:str = ""
    file_path:str = ""
    def __init__(self, cfg_name:str, file_name:str, file_path:str) -> None:
        self.cfg_name = cfg_name
        self.file_name = file_name
        self.file_path = file_path
    def set_element(self, var_name:str, var_value) -> None:
        self.cfg_d[var_name] = var_value
    def get_element(self, var_name:str):
        return self.cfg_d[var_name]


class Configs:
    def __init__(self, cfg_name:str = None, file_name:str = None, file_path:str = None, cos:bool = False) -> None:
        self._configs = {}
        if cfg_name:
            if cos:
                print(cfg_name)
                self.add_cosfig(cfg_name=cfg_name, file_name=file_name, file_path=file_path)
            else:
                self.add_config(cfg_name=cfg_name, file_name=file_name, file_path=file_path)

    def add_config(self, cfg_name:str, file_name:str, file_path:str = None):
        file_path = f"{file_path}{'/' if file_path else ''}{file_name}.cfg" if file_path != None else f"config/{file_name}.cfg"
        with open(file_path,'r') as file:
            config = Config(cfg_name, file_name, file_path)
            for linenum, string in enumerate(file.readlines()):
                string = string.strip()
                if (string == '') or (string[0] == '#'):
                    continue
                if '#' in string:
                    string = string.split('#')[0]
                # if string.count('=') != 1:
                #     raise ValueError(f"'=' number of != 1 in {linenum+1} config line") from None
                value_name, *value = string.split('=')
                value = '='.join(value)
                value_name = value_name.strip()
                value = value.strip()
                if len(value) == 0:
                    config.set_element(value_name, None)
                elif value in ("true","false"):
                    config.set_element(value_name, bool(value))
                elif value.isdecimal():
                    config.set_element(value_name, int(value))
                elif value[0] == value[-1] and value[0] in "'\"":
                    config.set_element(value_name, value[1:-1])
                else:
                    try:
                        config.set_element(value_name, float(value))
                    except ValueError:
                        raise ValueError(f"'{value_name}' value<{value}> is not in [bool, int, str, float]") from None
        self._configs[cfg_name] = config
    
    def add_cosfig(self, cfg_name:str, file_name:str, file_path:str = None):
        file_path = f"{file_path}{'/' if file_path else ''}{file_name}.cfg" if file_path != None else f"config/{file_name}.cfg"
        with open(file_path,'r') as file:
            cosfig = COSfig(cfg_name, file_name, file_path)
            string = file.readline()
            string = string.strip()
            # if string.count('=') != 1:
            #     raise ValueError(f"'=' number of != 1 in config") from None
            value_name, *value = string.split('=')
            value = '='.join(value)
            value_name = value_name.strip()
            value = value.strip()
            if len(value) == 0:
                cosfig.set_element(value_name, None)
            elif value in ("true","false"):
                cosfig.set_element(value_name, bool(value))
            elif value.isdecimal():
                cosfig.set_element(value_name, int(value))
            elif value[0] == value[-1] and value[0] in "'\"":
                cosfig.set_element(value_name, value[1:-1])
            else:
                try:
                    cosfig.set_element(value_name, float(value))
                except ValueError:
                    raise ValueError(f"'{value_name}' value<{value}> is not in [bool, int, str, float]") from None
        self._configs[cfg_name] = cosfig

    def get_config(self, name:str):
        return self._configs[name]


if __name__ == "__main__":
    print("\n !!! TEST CONFRLIB !!! ")
    confs = Configs()
    print("\n       TEST CONF       \n")
    confs.add_config("test", "testconflib", "test")
    conf:Config = confs.get_config("test")
    print(conf.cfg_d)
    print(' =')
    print({"aboba": 5, "name": "alex","id": 'b2c3d7f=', "fl": 5.8})
    print("\n= = = = = = = =\n")
    print(conf.get_element("name"))
    print(' =')
    print("alex")
    print("\n       TEST COS       \n")
    confs.add_cosfig("costest", "testcoslib", "test")
    cos:COSfig = confs.get_config("costest")
    print(cos.var_name)
    print(' =')
    print("restart")
    print("\n= = = = = = = =\n")
    print(cos.var_value)
    print(' =')
    print(True)
    print("\n !!! END TEST CONFLIB !!! \n")
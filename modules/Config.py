import json
from typing import Any

#!!! TEST THIS BEFORE USING


class Config:
    BACKUP = "/settings/default.json"
    PATH   = "/settings/settings.json"
    
    def __init__(self):
        self.initialState = self.readSettings(Config.BACKUP)
        

    def readSettings(self, _path: str = PATH) -> dict[str, Any]:
        try:
            with open(_path) as file:
                return json.load(file)
        except FileNotFoundError:
            raise ValueError(f"Settings file not found at {_path}.")
        except json.JSONDecodeError:
            raise ValueError(f"The settings file at {_path} is not in valid JSON format.")

    def updateSetting(self, _args: str, newVal: str | int | list[str | None]):
        keys     = _args.split('.')
        settings = self.readSettings()
        
        temp = settings
        for key in keys[:-1]:
            temp = temp.setdefault(key, {})

        currVal = temp.get(keys[-1], None)

        # If current_value is a list and new_value is a string, append. Otherwise, replace.
        if isinstance(currVal, list) and isinstance(newVal, str):
            temp[keys[-1]] += [newVal]
        else:
            temp[keys[-1]] = newVal
        
        self.writeSettings(settings)

    def writeSettings(self, settings: dict[str | Any]) -> None:
        with open(Config.PATH, 'w') as file:
            json.dump(settings, file, indent=4)


    def clear(self):
        def resetDefault(obj: dict | Any, refObj: dict | Any) -> dict | Any:
            for key, value in refObj.items():
                match value:
                    case dict(): tmp = resetDefault(obj.get(key, {}), value)
                    case list(): tmp = []
                    case str():  tmp = ""
                    case int():  tmp = value
                    case _:
                        raise ValueError(f"In Config::resetDefault\n\tUnknown type: {type(value)}")
                obj[key] = tmp
            return obj

        settings       = self.readSettings()
        reset_settings = resetDefault(settings, self.initialState)
        self.writeSettings(reset_settings)
        
        
    def __getitem__(self, _args: str) -> Any:
        keys = _args.split('.')
        settings = self.readSettings()
        
        temp = settings
        for key in keys:
            try:
                temp = temp[key]
            except KeyError:
                raise KeyError(f"Setting '{_args}' not found.")
        return temp
    
    
    def __setitem__(self, _args: str, newVal: str | int | list[str]) -> None:
        self.updateSetting(_args, newVal)
    
    
_CFG = Config()
    
if __name__ == "__main__":
    # Updating a setting with dot notation path and a new value
    _CFG.updateSetting("Linker.Redemption.submissions", "../Desktop/subs/")
    _CFG.updateSetting("Search.csvFiles", "../new/csv/path.csv")
    _CFG.updateSetting("Search.csvFiles", "../new/csv/path.csv")
    
    # Getting a setting value using dict-style syntax
    print(_CFG["Linker.Base.submissions"])
    
    # Setting a setting value using dict-style syntax
    _CFG["Linker.Base.submissions"] = "/usr/Desktop/rand/"
    
    # Clearing all settings to their initial states
    _CFG.clear()
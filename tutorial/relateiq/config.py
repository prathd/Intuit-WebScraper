import client as riq

class Config(object) :
    def __init__(self, data=None) :
        """
        :param data: for testing only.
        :return:
        """
        if data is not None:
            config = data
        else:
            config = riq.get('configs')
        self.__dict__.update(config)
        if "isPaused" not in config or config["isPaused"] is None or config["isPaused"] == "":
            self.isPaused = False

    def save(self) :
        return riq.post('configs',{'meta':self.meta,'creds':self.creds,'mappings':self.mappings})

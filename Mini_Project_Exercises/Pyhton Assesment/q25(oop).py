from abc import ABC, abstractmethod

class DataSource(ABC):
    def describe(self):
        print("Data Pipeline Component")

    @abstractmethod
    def extract(self):
        pass

class CSVSource(DataSource):
    def __init__(self, filepath):
        self.filepath = filepath

    def extract(self):
        return {self.filepath}

class APISource(DataSource):
    def __init__(self, url, endpoint):
        self.__url = None
        self.url = url
        self.endpoint = endpoint

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if value.startswith("https://"):
            self.__url = value
        else:
            print("Invalid URL! Must use https://")

    def extract(self):
        return f"Fetching API from {self.url}{self.endpoint}"
    
sources = [
    CSVSource("users.csv"), 
    APISource("https://api.com", "/users")]

for src in sources:
    src.describe()
    print(src.extract())
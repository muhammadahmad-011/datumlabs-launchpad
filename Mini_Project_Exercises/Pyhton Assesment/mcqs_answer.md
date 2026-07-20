1. b
2. b
3. b
4. ('Hello','World')
   {'lang':'python','ver'=3}
5. result = list(map(lambda n:n**2 , numbers))
   1,4,9,16,25
6. high_value = []
   for s in sales:
      if s > 100 and s % 2 == 0
      high_value.append(s)
7. b
8. c
9. {'python','sql','dbt','dagster'}
    4
10. csv file
    generic source
11. c
12. b
13. in approach 1 if error may occur in mid read f.close() didn't execute so file is remain open 
    and in approach 2 file close automatically after the execution.
14. pipeline: stack exchange loaded 14823
    pipeline: stack excahnge loaded 14823
    pipeline: stack exchange loaded 14,823
15. false
    false
    false
    true
    pipeline
16. from abc import ABC, abstractmethod
    class DataSource(ABC):
    @abstractmethod
    def extract(self):
        pass
    class CSVSource(DataSource):
    def __init__(self, filepath):
        self.filepath = filepath    
    def extract(self):
        return f"Loading CSV from {self.filepath}"
    class APISource(DataSource):
    def __init__(self, url):
        self.url = url
    def extract(self):
        return f"Extracting data from API endpoint: {self.url}"
    sources = [CSVSource("data.csv"), APISource("https://api.example.com")]
    for source in sources:
        print(source.extract())
16. b:
      polymorphism is oop principle that allows different class to implement same method.
    Real world analogy:
                    like .read() method to read data from postgresql and api
17. part a:
        def prime_gen(n):
            for num in range(2, n + 1):
                for i in range(2, int(num ** 0.5) + 1):  # Optimized to check up to square root
                    if num % i == 0:
                    break
                else:
                    yield num
        output = 2,3,5,7,11,13

    part b:
        def make_multiplier(factor):
            def multiplier(number):
                return number * factor
        return multiplier

        double = make_multiplier(2)
        triple = make_multiplier(3)

        print(double(5))
        print(triple(5))

    part c:
        functions are called first-class citizens in Python bcz function can be assign to variable and return from a function.

18. part a:
        import pandas as pd
        df = pd.read_csv("sales.csv")
        high_value = df[df["revenue"] > 1000]
        avg_revenue = df["revenue"].mean()
        print(f"Average revenue: {avg_revenue}")
        df = df.fillna(0)
        print(high_value.head())

    part b:
        print(df.shape)
        print(df['revenue'].isnull().sum())

19. part a:
        Snippet 1 output: 1
        Snippet 2 output: [0, 1, 2, 3, 4]
        Snippet 3 output: [('dlt', 3), ('dbt', 2)]

    part b:
        fibonacci(5) returns: 5

20. part a:
        import numpy as np
        import pandas as pd
        arr = np.array([120, 95, 140, 110, 88, 200, 75])
        print(arr.mean()) 
        df = pd.DataFrame({"revenue": [900, 1200, 450, 180, 600]})
        filtered = df[df["revenue"] > 800]
        print(filtered)

    part b: 
        import matplotlib.pyplot as plt
        pipelines = ["users", "questions", "answers", "comments"]
        load_times = [2.1, 4.5, 3.8, 1.2]
        plt.bar(pipelines, load_times)
        plt.xlabel('Pipeline')
        plt.ylabel('Load Time')
        plt.show()


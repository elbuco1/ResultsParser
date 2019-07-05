import sys 
from classes.results_parser import ResultsParser

def main():
    args = sys.argv 
    parameters_path = args[1]
    results_parser = ResultsParser(parameters_path)
    results_parser.temp()
     

if __name__ == "__main__":
    main()
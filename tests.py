from functions.functions import *

def test():
    # result = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "pkg")
    # print("Result for 'pkg' directory:")
    # print(result)

    # result = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(result)

    # result = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(result)
    
    # result = get_file_content("calculator", "lorem.txt")
    # print(f"Result for first {len(result)} characters of 'calculator/lorem.txt' file:")
    # print(result)

    # result = get_file_content("calculator", "main.py")
    # print("TEST: Result for 'calculator/main.py' file:")
    # print(result)
    
    # result = get_file_content("calculator", "pkg/calculator.py")
    # print("TEST: Result for 'calculator/pkg/calculator.py' file:")
    # print(result)
    
    # result = get_file_content("calculator", "/bin/cat")
    # print("TEST: Result for '/bin/cat' file:")
    # print(result)
    
    # result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print("WRITE TEST: Result for 'calculator, lorem.txt, wait, this isn't lorem ipsum':")
    # print(result)

    # result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print("WRITE TEST: Result for 'calculator, morelorem.txt, lorem ipsum dolor sit amet':")
    # print(result)

    # result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print("WRITE TEST: Result for 'calculator, /tmp/temp.txt, this should not be allowed':")
    # print(result)
    
    cwd = "calculator"
    file = "main.py"
    result = run_python_file(cwd, file)
    print(f"Ran: '{cwd}, {file}':")
    print(result)

    cwd = "calculator"
    file = "tests.py"
    result = run_python_file(cwd, file)
    print(f"Ran: '{cwd}, {file}':")
    print(result)

    cwd = "calculator"
    file = "../main.py"
    result = run_python_file(cwd, file)
    print(f"Ran: '{cwd}, {file}':")
    print(result)

    cwd = "calculator"
    file = "nonexistent.py"
    result = run_python_file(cwd, file)
    print(f"Ran: '{cwd}, {file}':")
    print(result)
    
    
if __name__ == "__main__":
    test()

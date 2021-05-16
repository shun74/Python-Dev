import os
import subprocess
if __name__ == "__main__":
    com = r'$env:G="C:\Users\syunn\Documents\Dev\Scanner\my_cred.json"'
    # print(com)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\syunn\Documents\Dev\Scanner\my_cred.json"
    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
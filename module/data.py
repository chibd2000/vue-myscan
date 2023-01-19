
try:
    from module.logger import Logger
    gLogger = Logger()
except:
    print('[-] logger init fail.')
    # exit(0)

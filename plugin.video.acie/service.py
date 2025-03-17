import server
import func

#Service launch
if __name__ == '__main__':
    #Check user folders
    func.check_user_folders()

    #Run ace stream server
    server.run_server()
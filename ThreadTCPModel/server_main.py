import server as tcpServer

if __name__ == '__main__':
    print("Starting TCP Server ...")
    while True:
        print('<Menu>')
        print('   1. Start Server')
        print('   2. Stop Server')
        print('   99. Finish')

        menu = input('Input the menu: ')

        # print('   --> Your input is {}'.format(menu))

        if menu == '1':
            tcpServer.start_server()
        elif menu == '2':
            tcpServer.stop_server()
        elif menu == '99':
            print("Exit !!!")
            tcpServer.stop_server()
            break

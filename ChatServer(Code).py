import asynchat
import asyncore


# 定义端口
PORT = 6666

# 定义结束异常类
class EndSession(Exception):
    pass


class ChatServer(asyncore.dispatcher):
    """
    聊天服务器
    """

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        # 创建socket
        self.create_socket()
        # 设置 socket 为可重用
        self.set_reuse_addr()
        # 监听端口
        self.bind(('', port))
        self.listen(5)
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)

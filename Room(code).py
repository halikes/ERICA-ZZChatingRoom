class Room(CommandHandler):
    """
    기본 명령 처리 및 방송을위한 다중 사용자 환경
    """

    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        # 사용자가 방에 들어간다
        self.sessions.append(session)

    def remove(self, session):
        # 사용자가 방을 떠난다
        self.sessions.remove(session)

    def broadcast(self, line):
        # 지정된 메시지를 모든 사용자에게 보낸다
        # asynchat.asyn_chat.push 메소드를 사용하여 데이터 전송
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        # 방을 나간다
        raise EndSession


class LoginRoom(Room):
    """
    로그인 한 사용자 처리
    """

    def add(self, session):
        # 사용자 연결 성공의 응답
        Room.add(self, session)
        # asynchat.asyn_chat.push 메소드를 사용하여 데이터 전송
        session.push(b'Connect Success')

    def do_login(self, session, line):
        # 사용자 로그인 로직
        name = line.strip()
        # 사용자 이름 얻기
        if not name:
            session.push(b'UserName Empty')
        # 같은 이름의 사용자가 있는지 확인
        elif name in self.server.users:
            session.push(b'UserName Exist')
        # 사용자 이름 확인에 성공하면 기본 대화방에 입장한다[
        else:
            session.name = name
            session.enter(self.server.main_room)


class LogoutRoom(Room):
    """
   로그 아웃 한 사용자 처리
    """

    def add(self, session):
        # 서버에서 제거
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatRoom(Room):
    """
     대화방
    """

    def add(self, session):
        # 새로운 사용자 항목 브로드 캐스트
        session.push(b'Login Success')
        self.broadcast((session.name + ' has entered the room.\n').encode("utf-8"))
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        # 브로드 캐스트 사용자가 남음
        Room.remove(self, session)
        self.broadcast((session.name + ' has left the room.\n').encode("utf-8"))

    def do_say(self, session, line):
        # 고객이 메시지를 보낸다
        self.broadcast((session.name + ': ' + line + '\n').encode("utf-8"))

    def do_look(self, session, line):
        # 온라인 사용자보기
        session.push(b'Online Users:\n')
        for other in self.sessions:
            session.push((other.name + '\n').encode("utf-8"))

if __name__ == '__main__':

    s = ChatServer(PORT)
    try:
        print("chat server run at '0.0.0.0:{0}'".format(PORT))
        asyncore.loop()
    except KeyboardInterrupt:
        print("chat server exit")

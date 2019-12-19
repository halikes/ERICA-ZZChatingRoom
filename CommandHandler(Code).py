class CommandHandler:
    """
      명령 처리 클래스
    """

    def unknown(self, session, cmd):
        # 알 수없는 명령에 대한 응답
        # asynchat.async_chat.push 메소드를 통해 메시지 보내기
        session.push(('Unknown command {} \n'.format(cmd)).encode("utf-8"))

    def handle(self, session, line):
        line = line.decode()
        # 명령 처리
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        # 프로토콜 코드를 통해 해당 방법을 실행
        method = getattr(self, 'do_' + cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)

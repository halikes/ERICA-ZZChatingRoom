
class ChatFrame(wx.Frame):
    """
   채팅 창
    """

    def __init__(self, parent, id, title, size):
        # 초기화, 컨트롤 추가 및 이벤트 바인듬
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos=(5, 5), size=(490, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos=(5, 320), size=(300, 25))
        self.sendButton = wx.Button(self, label="Send", pos=(310, 320), size=(58, 25))
        self.usersButton = wx.Button(self, label="Users", pos=(373, 320), size=(58, 25))
        self.closeButton = wx.Button(self, label="Close", pos=(436, 320), size=(58, 25))
        # 보내기 버튼 바인듬 메시지 보내기 방법
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # 사용자 버튼으로  온라인 사용자 수를 얻는 바인듬 방법
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # 닫기 버튼 바인듬 닫기 방법
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()

    def send(self, event):
        # 메시지 보내기
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write(('say ' + message + '\n').encode("utf-8"))
            self.message.Clear()

    def lookUsers(self, event):
        # 현재 온라인 사용자보기
        con.write(b'look\n')

    def close(self, event):
        #창 닫기
        con.write(b'logout\n')
        con.close()
        self.Close()

    def receive(self):
        #서버 메시지 수락
        while True:
            sleep(0.6)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)

if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title="Login", size=(320, 250))
    app.MainLoop()
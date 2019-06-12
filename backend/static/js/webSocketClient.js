var firstGet = function (data) {
    for (var i = 0; i < data.friend.length; i++) {
        thisUser.addFriend(data.friend[i].name, data.friend[i].id)
    }
    for (var y = 0; y < data.group.length; y++) {
        thisUser.addGroup(data.group[y].id, data.group[y].name)
    }
}

var dealMessage = function (data) {
    thisUser.addMessage(data.type, data)
}

var addFriend = function(data) {
    thisUser.addFriend(data.name, data.m_id)
    alert('添加好友: ' + data.name + ' 成功！')
}

var addLoginFriend = function (data) {
    for (var i = 0; i < data.m_id.length; i++) {
        thisUser.addLoginFriend(data.m_id[i])
    }
}

var removeLoginFriend = function (data) {
    thisUser.removeLoginFriend(data.m_id)
}

var addGroup = function(data) {
    thisUser.addGroup(data.m_id, data.name)
    alert('添加群: ' + data.name + ' 成功！')
}

var createGroup = function(data) {
    thisUser.addGroup(data.m_id, data.name)
    alert('创建群: ' + data.name + ' 成功！')
}

var bindSendMessage = function (websocket) {
    // 发送信息方法
    for (var i = 0; i < sendFunction.length; i++) {
        sendFunction[i](websocket)
    }
}


var clientWebSocket = function (wsUrl) {
    var websocket = new WebSocket(wsUrl)
    websocket.onmessage = function(evt) {
        var getMessageObject = JSON.parse(evt.data);
        var func = getMessageObject.method
        log('收到json信息: ')
        log(getMessageObject)
        getFunction[func](getMessageObject)
    }
    bindSendMessage(websocket)
}

var web_socket_main = function() {
    var wsUrl = e('#id-p-chat-url').innerText
    clientWebSocket(wsUrl)
}

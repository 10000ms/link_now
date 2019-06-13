// 首次获取信息处理
const firstGet = function (data) {
    // 处理好友
    for (let i = 0; i < data.friend.length; i++) {
        thisUser.addFriend(data.friend[i].name, data.friend[i].id);
    }
    // 处理组
    for (let y = 0; y < data.group.length; y++) {
        thisUser.addGroup(data.group[y].id, data.group[y].name);
    }
};


// 信息处理
const dealMessage = function (data) {
    thisUser.addMessage(data.type, data)
};


// 添加好友信息处理
const addFriend = function(data) {
    thisUser.addFriend(data.name, data.m_id);
    alert('添加好友: ' + data.name + ' 成功！');
};


// 好友上线信息处理
const addLoginFriend = function (data) {
    for (let i = 0; i < data.m_id.length; i++) {
        thisUser.addLoginFriend(data.m_id[i]);
    }
};


// 好友下线信息处理
const removeLoginFriend = function (data) {
    thisUser.removeLoginFriend(data.m_id);
};


// 加群信息处理
const addGroup = function(data) {
    thisUser.addGroup(data.m_id, data.name);
    alert('添加群: ' + data.name + ' 成功！');
};


// 创建群信息处理
const createGroup = function(data) {
    thisUser.addGroup(data.m_id, data.name);
    alert('创建群: ' + data.name + ' 成功！');
};


// 把建立的连接与发送方法连接
const bindSendMessage = function (websocket) {
    // 发送信息方法
    for (let i = 0; i < sendFunction.length; i++) {
        sendFunction[i](websocket);
    }
};


// websocket客户端启动方法
const clientWebSocket = function (wsUrl) {
    let websocket = new WebSocket(wsUrl);
    // 绑定接收到信息的方法
    websocket.onmessage = function(evt) {
        let getMessageObject = JSON.parse(evt.data);
        let func = getMessageObject.method;
        log('收到json信息: ');
        log(getMessageObject);
        // 根据不同的消息类型调用不同的方法处理
        getFunction[func](getMessageObject);
    };
    bindSendMessage(websocket);
};


// websocket的入口
const web_socket_main = function() {
    // 从渲染的页面获取websocket的地址
    // TODO: 改为通过ajax获取
    const wsUrl = e('#id-p-chat-url').innerText;
    // 使用这个url启动websocket客户端
    clientWebSocket(wsUrl);
};

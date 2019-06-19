// 发送信息方法
const sendMessageEvent = function (websocket) {
    let b = e('#id-btn-send-user-message');
    let textarea = e('#id-user-message');
    // 绑定方法
    b.addEventListener('click', function() {
        let thisOneMessage = e('#id-user-message').value;
        // 发送对象的id
        let titleId = e('#id-title-id').innerText;
        // 消息类型
        let titleType = e('#id-title-type').innerText;
        let messageJson = {
            method: 'message',
            type: parseInt(titleType),
            id: titleId,
            message: thisOneMessage,
        };
        let jsonData = JSON.stringify(messageJson);
        // 发送请求
        websocket.send(jsonData);

        if (titleType === config.friend) {
            let message = {
                account: titleId,
                name: thisUser.username,
                message: thisOneMessage,

            };
            thisUser.addMessage(titleType, message);
        }

        textarea.value = '';
    });
};


// 添加好友信息
const bindAddFriendEvent = function (websocket) {
    let b = e('#id-footer-add-friend');
    b.addEventListener('click', function(){
        // 弹出input框
        let account = prompt('请输入要添加的好友帐号');
        if (account != null) {
            let messageJson = {
                method: 'add_friend',
                id: account,
            };
            let jsonData = JSON.stringify(messageJson);
            // 发送请求
            websocket.send(jsonData);
        }
    });
};


// 加群
const bindAddGroupEvent = function (websocket) {
    let b = e('#id-footer-add-group');
    b.addEventListener('click', function(){
        let groupId=prompt('请输入要添加的群ID'); // 弹出input框
        if (groupId != null) {
            let messageJson = {
                method: 'add_group',
                id: groupId,
            };
            let jsonData = JSON.stringify(messageJson);
            // 发送请求
            websocket.send(jsonData);
        }
    });
};


// 建群
const bindCreateGroupEvent = function (websocket) {
    let b = e('#id-footer-create-group');
    b.addEventListener('click', function(){
        // 弹出input框
        let groupName=prompt('请输入要创建的群名');
        if (groupName != null) {
            let messageJson = {
                method: 'create_group',
                name: groupName,
            };
            let jsonData = JSON.stringify(messageJson);
            // 发送请求
            websocket.send(jsonData);
        }
    });
};


// 设置
const bindConfigEvent = function () {
    let b = e('#id-footer-config');
    b.addEventListener('click', function(){
        alert('开发中');
    });
};

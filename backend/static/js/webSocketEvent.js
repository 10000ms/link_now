var sendMessageEvent = function (websocket) {
    var b = e('#id-btn-send-user-message')
    var textarea = e('#id-user-message')
    b.addEventListener('click', function(event) {
        var thisOneMessage = e('#id-user-message').value
        var titleId = e('#id-title-id').innerText
        var titleType = e('#id-title-type').innerText
        var messageJson = {
            method: 'message',
            type: titleType,
            id: titleId,
            message: thisOneMessage,
        }
        var jsonData = JSON.stringify(messageJson)
        // 发送请求
        websocket.send(jsonData)

        if (titleType == config.friend) {
            var message = {
                account: titleId,
                name: thisUser.username,
                message: thisOneMessage,

            }
            thisUser.addMessage(titleType, message)
        }

        textarea.value = ''
    })
}

var bindAddFriendEvent = function (websocket) {
    var b = e('#id-footer-add-friend')
    b.addEventListener('click', function(event){
        var account=prompt('请输入要添加的好友帐号'); // 弹出input框
        if (account != null) {
            var messageJson = {
                method: 'add_friend',
                id: account,
            }
            var jsonData = JSON.stringify(messageJson)
            // 发送请求
            websocket.send(jsonData)
        }
    })
}


var bindAddGroupEvent = function (websocket) {
    var b = e('#id-footer-add-group')
    b.addEventListener('click', function(event){
        var groupId=prompt('请输入要添加的群ID'); // 弹出input框
        if (groupId != null) {
            var messageJson = {
                method: 'add_group',
                id: groupId,
            }
            var jsonData = JSON.stringify(messageJson)
            // 发送请求
            websocket.send(jsonData)
        }
    })
}


var bindCreateGroupEvent = function (websocket) {
    var b = e('#id-footer-create-group')
    b.addEventListener('click', function(event){
        var groupName=prompt('请输入要创建的群名') // 弹出input框
        if (groupName != null) {
            log(groupName)
            var messageJson = {
                method: 'create_group',
                name: groupName,
            }
            var jsonData = JSON.stringify(messageJson)
            // 发送请求
            websocket.send(jsonData)
        }
    })
}

var bindconfigEvent = function (websocket) {
    var b = e('#id-footer-config')
    b.addEventListener('click', function(event){
        alert('开发中')
    })
}

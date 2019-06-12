var singleMemberItem = function (id, name, icon) {
    var t = `
        <li class="single-member" data-id="${id}" data-name="${name}">
            <img class="profile" src="${icon}">
            <span class="name">${name}</span>
        </li>
        `
    return t
}


var memberItemTemplate = function (type, memberList) {
    var memberItems = ''
    if (type == config.friend) {
        var memberType = 'member-friend'
        for (var i = 0; i < memberList.length; i++) {
            var flag = false
            for (var y = 0; y < thisUser.loginFriend.length; y++) {
                log(thisUser.loginFriend)
                log(memberList)
                if (thisUser.loginFriend[y].id == memberList[i].id) {
                    flag = true
                }
            }
            if (flag) {
                var icon = config.loginIconUrl
            } else {
                var icon = config.userIconUrl
            }
            memberItems += singleMemberItem(memberList[i].id, memberList[i].name, icon)
        }
    } else if (type == config.group) {
        var memberType = 'member-group'
        for (var i = 0; i < memberList.length; i++) {
            memberItems += singleMemberItem(memberList[i].id, memberList[i].name, config.groupIconUrl)
        }
    }
    var t = `
            <ul class="member-div ${memberType}">
                ${memberItems}
            </ul>
            `
    return t
}

var singleMessageItem = function (username, message) {
    var t = `
        <div class="one-message">
            <div class="message-username">${username}</div>
            <div class="message-message"><div class="message-message-div">${message}</div></div>
        </div>
    `
    return t
}

var MessageItemTemplate = function (type, messageList) {
    var messageDiv = ''
    for (var i = 0; i < messageList.length; i++) {
        messageDiv += singleMessageItem(messageList[i].username, messageList[i].message)
    }
    return messageDiv
}
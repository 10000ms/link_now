var userInfo = function () {

    var info = {
        account: e('#id-user-account').innerText,
        username: e('#id-user-username').innerText,
        friend: [],
        loginFriend: [],
        group: [],
        all: [],
    }

    var checkAndRenewItem = function(type) {
        var memberTab = e('.memberTab')
        var nowTab = e('.active', memberTab)
        var nowTabId = nowTab.getAttribute('id')
        if (type == config.friend && nowTabId == 'id-memberTab-friend') {
            renewFriendItem()
        } else if (type == config.group && nowTabId == 'id-memberTab-group') {
            renewGroupItem()
        }
    }

    info.addFriend = function (username, account) {
        var singleFriend = singleItem(account, username)
        info.friend.push(singleFriend)
        checkAndRenewItem(config.friend)
    }

    info.addLoginFriend = function (account) {
        var singleLoginFriend = {
            id: account,
        }
        info.loginFriend.push(singleLoginFriend)
        checkAndRenewItem(config.friend)
    }

    info.addGroup = function (groupId, groupName) {
        var singleGroup = singleItem(groupId, groupName)
        info.group.push(singleGroup)
        checkAndRenewItem(config.group)
    }

    info.removeLoginFriend = function (account) {
        var index = -1
        for (var i = 0; i < info.loginFriend.length; i++) {
            if (info.loginFriend[i].id == account) {
                index = i
                break
            }
        }
        if (index > -1) {
            info.loginFriend.splice(index, 1)
        }
        checkAndRenewItem(config.friend)
    }

    var checkAndRenewMessage = function(type, id) {
        var titleId = e('#id-title-id').innerText
        var titleType = e('#id-title-type').innerText
        if (type == config.all && titleType == type) {
            renewMessageDiv()
        } else if (titleType == type && titleId == id) {
            renewMessageDiv()
        }
    }

    info.addMessage = function (type, data) {
        if (type == config.friend) {
            var id = data.account
            var username = data.name
            var message = data.message
            for (var i = 0; i < info.friend.length; i++) {
                if (info.friend[i].id == id) {
                    var needAddMessage = singleMessage(username, message)
                    info.friend[i].message.push(needAddMessage)
                    checkAndRenewMessage(config.friend, id)
                    return
                }
            }
        } else if (type == config.group) {
            var id = data.id
            var username = data.name
            var message = data.message
            for (var i = 0; i < info.group.length; i++) {
                if (info.group[i].id == id) {
                    var needAddMessage = singleMessage(username, message)
                    info.group[i].message.push(needAddMessage)
                    checkAndRenewMessage(config.group, id)
                    return
                }
            }
        } else if (type == config.all) {
            var username = data.name
            var message = data.message
            var needAddMessage = singleMessage(username, message)
            info.all.push(needAddMessage)
            checkAndRenewMessage(config.all, config.all)
            return
        }
    }

    return info
}


var singleItem = function (id ,name) {
    var Item = {
        id: id,
        name: name,
        message: [],
    }
    return Item
}


var singleMessage = function (username, message) {
    var one = {
        username: username,
        message: message,
    }
    return one
}
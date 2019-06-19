const userInfo = function () {

    let info = {
        account: e('#id-user-account').innerText,
        username: e('#id-user-username').innerText,
        friend: [],
        loginFriend: [],
        group: [],
        all: [],
    };

    let checkAndRenewItem = function(type) {
        let memberTab = e('.memberTab');
        let nowTab = e('.active', memberTab);
        let nowTabId = nowTab.getAttribute('id');
        if (type === config.friend && nowTabId === 'id-memberTab-friend') {
            renewFriendItem();
        } else if (type === config.group && nowTabId === 'id-memberTab-group') {
            renewGroupItem();
        }
    };

    info.addFriend = function (username, account) {
        let singleFriend = singleItem(account, username);
        info.friend.push(singleFriend);
        checkAndRenewItem(config.friend);
    };

    info.addLoginFriend = function (account) {
        let singleLoginFriend = {
            id: account,
        };
        info.loginFriend.push(singleLoginFriend);
        checkAndRenewItem(config.friend);
    };

    info.addGroup = function (groupId, groupName) {
        let singleGroup = singleItem(groupId, groupName);
        info.group.push(singleGroup);
        checkAndRenewItem(config.group);
    };

    info.removeLoginFriend = function (account) {
        let index = -1;
        for (let i = 0; i < info.loginFriend.length; i++) {
            if (info.loginFriend[i].id === account) {
                index = i;
                break;
            }
        }
        if (index > -1) {
            info.loginFriend.splice(index, 1);
        }
        checkAndRenewItem(config.friend);
    };

    let checkAndRenewMessage = function(type, id) {
        let titleId = e('#id-title-id').innerText;
        let titleType = e('#id-title-type').innerText;
        titleType = parseInt(titleType);
        if (type === config.all && titleType === type) {
            renewMessageDiv();
        } else if (titleType === type && titleId === id) {
            renewMessageDiv();
        }
    };

    info.addMessage = function (type, data) {
        if (type === config.friend) {
            let id = data.account;
            let username = data.name;
            let message = data.message;
            for (let i = 0; i < info.friend.length; i++) {
                if (info.friend[i].id === id) {
                    let needAddMessage = singleMessage(username, message);
                    info.friend[i].message.push(needAddMessage);
                    checkAndRenewMessage(config.friend, id);
                    return;
                }
            }
        } else if (type === config.group) {
            let id = data.id;
            let username = data.name;
            let message = data.message;
            for (let i = 0; i < info.group.length; i++) {
                if (info.group[i].id === id) {
                    let needAddMessage = singleMessage(username, message);
                    info.group[i].message.push(needAddMessage);
                    checkAndRenewMessage(config.group, id);
                }
            }
        } else if (type === config.all) {
            let username = data.name;
            let message = data.message;
            let needAddMessage = singleMessage(username, message);
            info.all.push(needAddMessage);
            checkAndRenewMessage(config.all, config.all);
        }
    };

    return info;
};


const singleItem = function (id ,name) {
    return {
        id: id,
        name: name,
        message: [],
    };
};


const singleMessage = function (username, message) {
    return {
        username: username,
        message: message,
    };
};

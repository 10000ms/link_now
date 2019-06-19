const singleMemberItem = function (id, name, icon) {
    return `
        <li class="single-member" data-id="${id}" data-name="${name}">
            <img class="profile" src="${icon}" alt="头像">
            <span class="name">${name}</span>
        </li>
        `;
};


const memberItemTemplate = function (type, memberList) {
    let memberItems = '';
    let memberType;
    if (type === config.friend) {
        memberType = 'member-friend';
        for (let i = 0; i < memberList.length; i++) {
            let flag = false;
            for (let y = 0; y < thisUser.loginFriend.length; y++) {
                if (thisUser.loginFriend[y].id === memberList[i].id) {
                    flag = true;
                }
            }
            let icon;
            if (flag) {
                icon = config.loginIconUrl;
            } else {
                icon = config.userIconUrl;
            }
            memberItems += singleMemberItem(memberList[i].id, memberList[i].name, icon);
        }
    } else if (type === config.group) {
        memberType = 'member-group';
        for (let i = 0; i < memberList.length; i++) {
            memberItems += singleMemberItem(memberList[i].id, memberList[i].name, config.groupIconUrl);
        }
    }
    return `
            <ul class="member-div ${memberType}">
                ${memberItems}
            </ul>
            `;
};

const singleMessageItem = function (username, message) {
    return `
        <div class="one-message">
            <div class="message-username">${username}</div>
            <div class="message-message"><div class="message-message-div">${message}</div></div>
        </div>
    `;
};

const MessageItemTemplate = function (type, messageList) {
    let messageDiv = '';
    for (let i = 0; i < messageList.length; i++) {
        messageDiv += singleMessageItem(messageList[i].username, messageList[i].message);
    }
    return messageDiv;
};

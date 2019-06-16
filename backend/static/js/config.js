// 界面配置
const config = {
    userIconUrl: '/static/img/user.png',
    loginIconUrl: '/static/img/login_user.png',
    groupIconUrl: '/static/img/group.png',
    friend: 1,
    group: 2,
    all: 3,
};


// 发送方法
const sendFunction = [
    sendMessageEvent,
    bindAddFriendEvent,
    bindAddGroupEvent,
    bindCreateGroupEvent,
    bindConfigEvent,
];


// 接收到信息处理方法
const getFunction = {
    user_info: firstGet,
    user_message: dealMessage,
    add_friend: addFriend,
    add_login_friend: addLoginFriend,
    remove_login_friend: removeLoginFriend,
    add_group: addGroup,
    create_group: createGroup,
};


// 当前用户信息
const thisUser = userInfo();

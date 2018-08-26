var config = {
    userIconUrl: 'http://p8th9ds1l.bkt.clouddn.com/user.png',
    loginIconUrl: 'http://p8th9ds1l.bkt.clouddn.com/login_user.png',
    groupIconUrl: 'http://p8th9ds1l.bkt.clouddn.com/group.png',
    friend: 1,
    group: 2,
    all: 3,
}

var sendFunction = [
    sendMessageEvent,
    bindAddFriendEvent,
    bindAddGroupEvent,
    bindCreateGroupEvent,
    bindconfigEvent,
]

var getFunction = {
    user_info: firstGet,
    user_message: dealMessage,
    add_friend: addFriend,
    add_login_friend: addLoginFriend,
    remove_login_friend: removeLoginFriend,
    add_group: addGroup,
    create_group: createGroup,
}

var thisUser = userInfo()

var __main = function () {
    web_socket_main()
    surfaceMain()
}


__main()
var renewFriendItem = function () {
    var memberDiv = e('.member-item')
    var temp = memberItemTemplate(config.friend, thisUser.friend)
    insertTemplate(memberDiv, temp)
}

var renewGroupItem = function () {
    var memberDiv = e('.member-item')
    var temp = memberItemTemplate(config.group, thisUser.group)
    insertTemplate(memberDiv, temp)
}

var renewMessageDiv = function () {
    var titleId = e('#id-title-id').innerText
    var titleType = e('#id-title-type').innerText
    var message = e('.total-message')
    if (titleType == config.friend) {
        var getMessage = findMessage(config.friend, titleId)
        var messageTemplate = MessageItemTemplate(config.friend, getMessage)
        insertTemplate(message, messageTemplate)
        MessageScrollTop()
    } else if (titleType == config.group) {
        var getMessage = findMessage(config.group, titleId)
        var messageTemplate = MessageItemTemplate(config.group, getMessage)
        insertTemplate(message, messageTemplate)
        MessageScrollTop()
    } else if (titleType == config.all) {
        var messageTemplate = MessageItemTemplate(config.all, thisUser.all)
        insertTemplate(message, messageTemplate)
        MessageScrollTop()
    }
}
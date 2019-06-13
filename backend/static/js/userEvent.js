const renewFriendItem = function () {
    let memberDiv = e('.member-item');
    let temp = memberItemTemplate(config.friend, thisUser.friend);
    insertTemplate(memberDiv, temp);
};


const renewGroupItem = function () {
    let memberDiv = e('.member-item');
    let temp = memberItemTemplate(config.group, thisUser.group);
    insertTemplate(memberDiv, temp);
};


const renewMessageDiv = function () {
    let titleId = e('#id-title-id').innerText;
    let titleType = e('#id-title-type').innerText;
    let message = e('.total-message');
    if (titleType === config.friend) {
        let getMessage = findMessage(config.friend, titleId);
        let messageTemplate = MessageItemTemplate(config.friend, getMessage);
        insertTemplate(message, messageTemplate);
        MessageScrollTop();
    } else if (titleType === config.group) {
        let getMessage = findMessage(config.group, titleId);
        let messageTemplate = MessageItemTemplate(config.group, getMessage);
        insertTemplate(message, messageTemplate);
        MessageScrollTop();
    } else if (titleType === config.all) {
        let messageTemplate = MessageItemTemplate(config.all, thisUser.all);
        insertTemplate(message, messageTemplate);
        MessageScrollTop();
    }
};

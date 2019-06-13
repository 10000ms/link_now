const bindChangeMemberTabEvent = function() {
    let b = e('.memberTab');
    let memberDiv = e('.member-item');
    let friendTitle = e('#id-memberTab-friend');
    let groupTitle = e('#id-memberTab-group');
    let allTitle = e('#id-memberTab-all');
    let message = e('.total-message');
    b.addEventListener('click', function(event){
        let self = event.target;
        if (self.id === 'id-memberTab-friend') {
            friendTitle.classList.add('active');
            groupTitle.classList.remove('active');
            allTitle.classList.remove('active');

            let temp = memberItemTemplate(config.friend, thisUser.friend);
            insertTemplate(memberDiv, temp);

        } else if (self.id === 'id-memberTab-group') {
            friendTitle.classList.remove('active');
            groupTitle.classList.add('active');
            allTitle.classList.remove('active');

            let temp = memberItemTemplate(config.group, thisUser.group);
            insertTemplate(memberDiv, temp);

        } else if (self.id === 'id-memberTab-all') {
            let title = e('#id-title-name');
            let titleId = e('#id-title-id');
            let titleType = e('#id-title-type');
            title.innerText = '大厅';
            titleId.innerText = '1';
            titleType.innerText = config.all;

            insertTemplate(memberDiv, '');

            friendTitle.classList.remove('active');
            groupTitle.classList.remove('active');
            allTitle.classList.add('active');

            let messageTemplate = MessageItemTemplate(config.all, thisUser.all);
            insertTemplate(message, messageTemplate);

            MessageScrollTop();
        }
    });
};


const findMessage = function (type, id) {
    if (type === config.friend) {
        for (let i = 0; i < thisUser.friend.length; i++) {
            if (thisUser.friend[i].id === id) {
                return thisUser.friend[i].message;
            }
        }
    } else if (type === config.group) {
        for (let i = 0; i < thisUser.group.length; i++) {
            if (thisUser.group[i].id === id) {
                return thisUser.group[i].message;
            }
        }
    }
};


const bindChangeFriendEvent = function () {
    let b = e('.member-item');
    let message = e('.total-message');
    let title = e('#id-title-name');
    let titleId = e('#id-title-id');
    let titleType = e('#id-title-type');
    b.addEventListener('click', function(event){
        let self = event.target;
        let checkTargetItself = self.classList.contains('single-member');
        let checkTargetParent = self.parentElement.classList.contains('single-member');
        let checkTab = self.parentElement.classList.contains('member-friend');
        let checkParentTab = self.parentElement.parentElement.classList.contains('member-friend');
        if ((checkTargetItself && checkTab) || (checkTargetParent && checkParentTab)) {
            let thisMemberItem = self.closest('.single-member');
            let account = thisMemberItem.dataset['id'];
            title.innerText = thisMemberItem.dataset['name'];
            titleId.innerText = account;
            titleType.innerText = config.friend;

            let getMessage = findMessage(config.friend, account);
            let messageTemplate = MessageItemTemplate(config.friend, getMessage);
            insertTemplate(message, messageTemplate);

            MessageScrollTop();
        }
    });
};


const bindChangeGroupEvent = function () {
    let b = e('.member-item');
    let message = e('.total-message');
    let title = e('#id-title-name');
    let titleId = e('#id-title-id');
    let titleType = e('#id-title-type');
    b.addEventListener('click', function(event){
        let self = event.target;
        let checkTargetItself = self.classList.contains('single-member');
        let checkTargetParent = self.parentElement.classList.contains('single-member');
        let checkTab = self.parentElement.classList.contains('member-group');
        let checkParentTab = self.parentElement.parentElement.classList.contains('member-group');
        if ((checkTargetItself && checkTab) || (checkTargetParent && checkParentTab)) {
            let thisMemberItem = self.closest('.single-member');
            let groupId = thisMemberItem.dataset['id'];
            let groupName = thisMemberItem.dataset['name'];
            title.innerText = groupName + '(id:' + groupId + ')';
            titleId.innerText = groupId;
            titleType.innerText = config.group;

            let getMessage = findMessage(config.group, groupId);
            let messageTemplate = MessageItemTemplate(config.group, getMessage);
            insertTemplate(message, messageTemplate);

            MessageScrollTop();
        }
    });
};


const bindEvents = function() {
    bindChangeMemberTabEvent();
    bindChangeFriendEvent();
    bindChangeGroupEvent();
};


const surfaceMain = function () {
    bindEvents();
};

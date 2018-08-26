var bindChangeMemberTabEvent = function() {
    var b = e('.memberTab')
    var memberDiv = e('.member-item')
    var friendTitle = e('#id-memberTab-friend')
    var groupTitle = e('#id-memberTab-group')
    var allTitle = e('#id-memberTab-all')
    var message = e('.total-message')
    b.addEventListener('click', function(event){
        var self = event.target
        if (self.id == 'id-memberTab-friend') {
            friendTitle.classList.add("active")
            groupTitle.classList.remove("active")
            allTitle.classList.remove("active")

            var temp = memberItemTemplate(config.friend, thisUser.friend)
            insertTemplate(memberDiv, temp)

        } else if (self.id == 'id-memberTab-group') {
            friendTitle.classList.remove("active")
            groupTitle.classList.add("active")
            allTitle.classList.remove("active")

            var temp = memberItemTemplate(config.group, thisUser.group)
            insertTemplate(memberDiv, temp)

        } else if (self.id == 'id-memberTab-all') {
            var title = e('#id-title-name')
            var titleId = e('#id-title-id')
            var titleType = e('#id-title-type')
            title.innerText = '大厅'
            titleId.innerText = '1'
            titleType.innerText = config.all

            insertTemplate(memberDiv, '')

            friendTitle.classList.remove("active")
            groupTitle.classList.remove("active")
            allTitle.classList.add("active")

            var messageTemplate = MessageItemTemplate(config.all, thisUser.all)
            insertTemplate(message, messageTemplate)

            MessageScrollTop()
        }
    })
}


var findMessage = function (type, id) {
    if (type == config.friend) {
        for (var i = 0; i < thisUser.friend.length; i++) {
            if (thisUser.friend[i].id == id) {
                return thisUser.friend[i].message
            }
        }
    } else if (type == config.group) {
        for (var i = 0; i < thisUser.group.length; i++) {
            if (thisUser.group[i].id == id) {
                return thisUser.group[i].message
            }
        }
    }
}


var bindChangeFriendEvent = function () {
    var b = e('.member-item')
    var message = e('.total-message')
    var title = e('#id-title-name')
    var titleId = e('#id-title-id')
    var titleType = e('#id-title-type')
    b.addEventListener('click', function(event){
        var self = event.target
        var checkTargetItself = self.classList.contains('single-member')
        var checkTargetParent = self.parentElement.classList.contains('single-member')
        var checkTab = self.parentElement.classList.contains('member-friend')
        var checkParentTab = self.parentElement.parentElement.classList.contains('member-friend')
        if ((checkTargetItself && checkTab) || (checkTargetParent && checkParentTab)) {
            var thisMemberItem = self.closest('.single-member')
            var account = thisMemberItem.dataset['id']
            var username = thisMemberItem.dataset['name']
            title.innerText = username
            titleId.innerText = account
            titleType.innerText = config.friend

            var getMessage = findMessage(config.friend, account)
            var messageTemplate = MessageItemTemplate(config.friend, getMessage)
            insertTemplate(message, messageTemplate)

            MessageScrollTop()
        }
    })
}


var bindChangeGroupEvent = function () {
    var b = e('.member-item')
    var message = e('.total-message')
    var title = e('#id-title-name')
    var titleId = e('#id-title-id')
    var titleType = e('#id-title-type')
    b.addEventListener('click', function(event){
        var self = event.target
        var checkTargetItself = self.classList.contains('single-member')
        var checkTargetParent = self.parentElement.classList.contains('single-member')
        var checkTab = self.parentElement.classList.contains('member-group')
        var checkParentTab = self.parentElement.parentElement.classList.contains('member-group')
        if ((checkTargetItself && checkTab) || (checkTargetParent && checkParentTab)) {
            var thisMemberItem = self.closest('.single-member')
            var groupId = thisMemberItem.dataset['id']
            var groupName = thisMemberItem.dataset['name']
            title.innerText = groupName + '(id:' + groupId + ')'
            titleId.innerText = groupId
            titleType.innerText = config.group

            var getMessage = findMessage(config.group, groupId)
            var messageTemplate = MessageItemTemplate(config.group, getMessage)
            insertTemplate(message, messageTemplate)

            MessageScrollTop()
        }
    })
}

var bindEvents = function() {
    bindChangeMemberTabEvent()
    bindChangeFriendEvent()
    bindChangeGroupEvent()
}


var surfaceMain = function () {
    bindEvents()
}

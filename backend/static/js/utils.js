var log = console.log.bind(console)

var e = function(selector, parent=document) {
    return parent.querySelector(selector)
}

var MessageScrollTop = function () {
    var doc = e('.message-div')
    doc.scrollTop = doc.scrollHeight;
}

var insertTemplate = function (doc, template) {
    doc.innerHTML = template
}


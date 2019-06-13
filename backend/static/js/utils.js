// log方法
const log = console.log.bind(console, new Date().toLocaleString());


// 获取dom元素方法
const e = function(selector, parent=document) {
    return parent.querySelector(selector);
};


// 消息滚动
const MessageScrollTop = function () {
    const doc = e('.message-div');
    doc.scrollTop = doc.scrollHeight;
};


// 插入模板方法
const insertTemplate = function (doc, template) {
    doc.innerHTML = template;
};

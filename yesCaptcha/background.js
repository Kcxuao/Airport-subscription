(()=>{var e={3239:(e,t,n)=>{e.exports={default:n(2742),__esModule:!0}},2742:(e,t,n)=>{var o=n(4579),r=o.JSON||(o.JSON={stringify:JSON.stringify});e.exports=function(e){return r.stringify.apply(r,arguments)}},4579:e=>{var t=e.exports={version:"2.6.12"};"number"==typeof __e&&(__e=t)},129:(e,t,n)=>{"use strict";n.r(t),n.d(t,{createContextMenu:()=>r});var o=function(e){return chrome.i18n.getMessage(e)},r=function(){chrome.contextMenus.removeAll((function(){chrome.contextMenus.create({id:"1",title:o("context_menu_1"),visible:!0,contexts:["image"]}),chrome.contextMenus.create({id:"2",title:o("context_menu_2"),visible:!0,contexts:["editable"]}),chrome.contextMenus.onClicked.addListener((function(e,t){(null==t?void 0:t.id)&&chrome.tabs.sendMessage(t.id,{type:"getClickedEl",info:e},{frameId:e.frameId})}))}))}}},t={};function n(o){var r=t[o];if(void 0!==r)return r.exports;var c=t[o]={exports:{}};return e[o](c,c.exports,n),c.exports}n.d=(e,t)=>{for(var o in t)n.o(t,o)&&!n.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})},n.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),n.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{"use strict";var e,t=n(3239),o=(e=t)&&e.__esModule?e:{default:e},r=n(129);chrome.runtime.onMessage.addListener((function(e,t,n){return"screenshot"===e.action&&chrome.tabs.captureVisibleTab().then(n),"gettabs"===e.action&&chrome.tabs.query({currentWindow:!0},(function(e){n(e)})),"removetab"===e.action&&chrome.tabs.remove(t.tab.id),"getconfig"===e.action?(chrome.storage.local.get(["config"],(function(e){n(e.config)})),!0):"setconfig"===e.action?(chrome.storage.local.set({config:e.config},(function(){n(!0)})),!0):"testnetwork"===e.action?(fetch(e.url).then((function(e){return e.json()})).then((function(e){n(!0)})).catch((function(e){n(!1)})),!0):"post"===e.action?(e.url&&e.url.includes("createTask")&&(e.data.softID="11088"),fetch(e.url,{method:"POST",body:(0,o.default)(e.data)}).then((function(e){return e.json()})).then((function(e){n(e)})),!0):"get"===e.action?(fetch(e.url).then((function(e){return e.json()})).then((function(e){n(e)})),!0):(e.getLocalVersion,!0)})),(0,r.createContextMenu)();try{importScripts("config.js")}catch(e){console.error(e)}})()})();
/*!
 * © 2016 Avira Operations GmbH & Co. KG. All rights reserved.
 * No part of this extension may be reproduced, stored or transmitted in any
 * form, for any reason or by any means, without the prior permission in writing
 * from the copyright owner. The text, layout, and designs presented are
 * protected by the copyright laws of the United States and international
 * treaties.
 */
!function e(r,t,n){function u(i,f){if(!t[i]){if(!r[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(o)return o(i,!0);var s=new Error("Cannot find module '"+i+"'");throw s.code="MODULE_NOT_FOUND",s}var d=t[i]={exports:{}};r[i][0].call(d.exports,(function(e){return u(r[i][1][e]||e)}),d,d.exports,e,r,t,n)}return t[i].exports}for(var o="function"==typeof require&&require,i=0;i<n.length;i++)u(n[i]);return u}({1:[function(e,r,t){"use strict";!function(e){let r=-1;const t=e.addListener.bind(e);e.addListener=(e,...n)=>{t((t=>{const n=e(t);return t.requestId===r?null:(n&&null!=n.redirectUrl&&(r=t.requestId),n)}),...n)}}(chrome.webRequest.onBeforeRequest)},{}]},{},[1]);
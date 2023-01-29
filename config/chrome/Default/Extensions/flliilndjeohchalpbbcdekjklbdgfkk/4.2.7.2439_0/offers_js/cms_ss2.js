/*!
 * © 2016 Avira Operations GmbH & Co. KG. All rights reserved.
 * No part of this extension may be reproduced, stored or transmitted in any
 * form, for any reason or by any means, without the prior permission in writing
 * from the copyright owner. The text, layout, and designs presented are
 * protected by the copyright laws of the United States and international
 * treaties.
 */
!function e(r,n,t){function i(u,f){if(!n[u]){if(!r[u]){var a="function"==typeof require&&require;if(!f&&a)return a(u,!0);if(o)return o(u,!0);var s=new Error("Cannot find module '"+u+"'");throw s.code="MODULE_NOT_FOUND",s}var c=n[u]={exports:{}};r[u][0].call(c.exports,(function(e){return i(r[u][1][e]||e)}),c,c.exports,e,r,n,t)}return n[u].exports}for(var o="function"==typeof require&&require,u=0;u<t.length;u++)i(t[u]);return i}({1:[function(e,r,n){"use strict";!function(e){if(!window._fixBrokenFirefoxLinksApplied){window._fixBrokenFirefoxLinksApplied=!0;var r=navigator.userAgent.match(/Firefox\/(\d+)/);!r||parseInt(r[1],10)<53||chrome&&chrome.runtime&&chrome.runtime.sendMessage&&$(e).on("click","a[target=_blank][href]",(function(e){e.preventDefault(),chrome.runtime.sendMessage({publish:"navigate",message:{url:e.currentTarget.href,as_separate:!0}})}))}}(document.body)},{}]},{},[1]);
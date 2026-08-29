/* ============================================================================
   SACRVM — shared web components. Vanilla custom elements, light DOM on
   purpose: every page links one stylesheet, and a shadow root would wall the
   shared styles off. The markup a component replaces is its no-JS fallback,
   so the imprint link stays reachable even with scripting disabled.
   ========================================================================== */
(function(){
  'use strict';

  /* <site-nav page="home|blog|cv|imprint"> — the top navigation. Brand on
     the left, the site's pages on the right, the one you are on marked.
     Root-absolute hrefs: blog pages live a directory deep. */
  class SiteNav extends HTMLElement{
    connectedCallback(){
      var page = this.getAttribute('page') || '';
      var links = [
        { id:'home',    href:'/',             label:'HOME' },
        { id:'map',     href:'/map.html',     label:'MAP' },
        { id:'blog',    href:'/blog/',        label:'BLOG' },
        { id:'cv',      href:'/cv.html',      label:'CV' },
        { id:'imprint', href:'/imprint.html', label:'IMPRINT' }
      ];
      this.innerHTML =
        '<nav class="bar">' +
          '<a class="brand" href="/">SACRVM.DEV</a>' +
          '<div class="links">' +
            links.map(function(l){
              var here = l.id === page;
              return '<a href="' + l.href + '"' +
                     (here ? ' class="here" aria-current="page"' : '') +
                     '>' + l.label + '</a>';
            }).join('') +
          '</div>' +
        '</nav>';
    }
  }

  /* <site-footer page="home|blog|cv|imprint"> — copyright plus the site
     links, minus the page you are already on. */
  class SiteFooter extends HTMLElement{
    connectedCallback(){
      var page = this.getAttribute('page') || '';
      var links = [
        { id:'home',    href:'/',             label:'HOME' },
        { id:'map',     href:'/map.html',     label:'MAP' },
        { id:'blog',    href:'/blog/',        label:'BLOG' },
        { id:'cv',      href:'/cv.html',      label:'CV' },
        { id:'imprint', href:'/imprint.html', label:'IMPRINT &amp; DISCLAIMER' }
      ].filter(function(l){ return l.id !== page; });

      this.innerHTML =
        '<footer class="foot">' +
          '<span>&copy; MMXXVI MARCUS WILHELM</span>' +
          '<nav class="foot-nav">' +
            links.map(function(l){
              return '<a href="' + l.href + '">' + l.label + '</a>';
            }).join('') +
          '</nav>' +
        '</footer>';
    }
  }

  customElements.define('site-nav', SiteNav);
  customElements.define('site-footer', SiteFooter);
})();

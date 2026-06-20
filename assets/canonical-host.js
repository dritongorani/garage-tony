(function () {
  var CANONICAL_HOST = 'mecanolyon.fr';
  var CANONICAL_ORIGIN = 'https://' + CANONICAL_HOST;

  var loc = window.location;
  var host = loc.hostname;
  var path = loc.pathname;
  var search = loc.search;
  var hash = loc.hash;

  var needsRedirect = false;

  // www → apex
  if (host === 'www.' + CANONICAL_HOST) {
    needsRedirect = true;
  }

  // http → https (GitHub Pages + custom domain)
  if (loc.protocol === 'http:') {
    needsRedirect = true;
  }

  // /index.html → /
  if (path === '/index.html' || path.endsWith('/index.html')) {
    path = path.replace(/\/index\.html$/, '/') || '/';
    needsRedirect = true;
  }

  // trailing slash normalization (except root)
  if (path.length > 1 && path.endsWith('/')) {
    path = path.replace(/\/+$/, '');
    needsRedirect = true;
  }

  if (needsRedirect) {
    window.location.replace(CANONICAL_ORIGIN + path + search + hash);
  }
})();

(function () {
  var canonicalHost = 'mecanolyon.fr';
  var host = window.location.hostname;
  if (host === 'www.' + canonicalHost) {
    window.location.replace(
      'https://' + canonicalHost + window.location.pathname + window.location.search + window.location.hash
    );
  }
})();

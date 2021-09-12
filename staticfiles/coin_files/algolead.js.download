(function ($) {

    'use strict';
    const client = new ClientJS();

    $.extend({
        algolead: {
            init: function () {
                this.startImpression();
            },
            startImpression: function () {
                $.ajax({
                    method: 'POST',
                    url: '/algolead/impression-logs',
                    data: {
                        url: document.location.href,
                        referrer: document.referrer,
                        fingerprint: client.getFingerprint(),
                    }
                });
            }
        }
    });

    $.algolead.init();

})(jQuery);
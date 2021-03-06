var casper = casper || {};
var phantom = phantom || {};
var document_list_url = casper.cli.options['url'];

casper.options.clientScripts.push("../../../static/js/vendor/sinon.js");

function inject_cookies() {
    var m = casper.cli.options['url-base'].match(/https?:\/\/([^:]+)(:\d+)?\//);
    var domain = m ? m[1] : 'localhost';

    for (var key in casper.cli.options) {
        if (key.indexOf('cookie-') === 0) {
            var cn = key.substring('cookie-'.length);
            var c = phantom.addCookie({
                name: cn,
                value: casper.cli.options[key],
                domain: domain
            });
        }
    }
}
inject_cookies();

casper.on('remote.message', function(message) {
    this.echo(message);
});

casper.test.begin('Documents are fetched on page load', 0, function suite(test) {
    casper.start(document_list_url, function() {
        test.assertTitle('Phase');

        // Reduced viewport so the "see more docs" buttons
        // is not visible until we scroll to bottom
        casper.viewport(1024, 250);
        casper.wait(100);
    });

    casper.then(function() {
        test.assertElementCount('table#documents tbody tr', 5);
        test.assertSelectorHasText('#display-results', '5 documents on 20');

        // It's visible, but not inview
        test.assertVisible('#documents-pagination');
        casper.click('#documents-pagination');
        casper.wait(300);
    });

    casper.then(function() {
        test.assertElementCount('table#documents tbody tr', 10);
        test.assertSelectorHasText('#display-results', '10 documents on 20');
    });

    casper.then(function() {
        casper.click('#documents-pagination');
        casper.wait(500);
    });

    casper.then(function() {
        casper.click('#documents-pagination');
        casper.wait(500);
    });

    casper.then(function() {
        test.assertElementCount('table#documents tbody tr', 20);
        test.assertSelectorHasText('#display-results', '20 documents on 20');
        test.assertNotVisible('#documents-pagination');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Clicking on a checkbox add a class to the tr', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(100);
        test.assertDoesntExist('tr.selected');
    });

    casper.then(function() {
        casper.click('td.columnselect input[type=checkbox]');
        test.assertExists('tr.selected');
    });

    casper.then(function() {
        casper.click('td.columnselect input[type=checkbox]');
        test.assertDoesntExist('tr.selected');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Buttons are enabled on checkbox click', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(100);
        test.assertExists('#batch-action-buttons>button.disabled');
    });

    casper.then(function() {
        casper.click('td.columnselect input[type=checkbox]');
        test.assertDoesntExist('#batch-action-buttons>button.disabled');
        test.assertExists('#batch-action-buttons>button');
    });

    casper.then(function() {
        casper.click('td.columnselect input[type=checkbox]');
        test.assertElementCount('#documents input:checked', 0);
        test.assertExists('#batch-action-buttons>button.disabled');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Select all checkbox', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(100);
        test.assertElementCount('#documents input:checked', 0);
    });

    casper.then(function() {
        casper.click('#select-all');
    });

    casper.then(function() {
        test.assertElementCount('#documents input:checked', 6);
    });

    casper.then(function() {
        casper.click('#select-all');
    });

    casper.then(function() {
        test.assertElementCount('#documents input:checked', 0);

    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Selecting a row creates an input field in download form', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(500);
        test.assertDoesntExist('input[name=document_ids]');
    });

    casper.then(function() {
        casper.click('td.columnselect input[type=checkbox]');
        test.assertExists('input[name=document_ids]');
    });

    casper.then(function() {
        casper.click('td.columnselect input[type=checkbox]');
        test.assertDoesntExist('input[name=document_ids]');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Clicking a row redirects to the document page', 0, function suite(test) {
    casper.start(document_list_url, function() {
        test.assertUrlMatch(/\/organisation_\d+\/category_\d+\/$/);
        casper.wait(500);
    });

    casper.then(function() {
        casper.click('td.columndocument_number');
    });

    casper.then(function() {
        test.assertUrlMatch(/\/organisation_\d+\/category_\d+\/hazop-report-0\/$/);
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Clicking the "Search" button shows the search sidebar', 0, function suite(test) {
    casper.start(document_list_url, function() {
        test.assertNotVisible('div.sidebar-offcanvas');
        casper.click('button#toggle-filters-button');
    });

    casper.then(function() {
        test.assertVisible('div.sidebar-offcanvas');
        casper.click('button#sidebar-close-btn');
    });

    casper.then(function() {
        test.assertNotVisible('div.sidebar-offcanvas');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('The filter form cannot be submitted', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.fill('#search-sidebar form', {
            'search_terms': 'toto'
        }, true);
    });

    casper.then(function() {
        test.assertEqual(casper.getCurrentUrl(), document_list_url);
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Clicking a column sorts stuff', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(500);
    });

    casper.then(function() {
        test.assertExists('#columndocument_number span.glyphicon.glyphicon-chevron-down');
        test.assertSelectorHasText('tbody tr:first-of-type td:nth-of-type(3)', 'hazop-report-0');
    });

    casper.then(function() {
        casper.click('#columndocument_number');
        casper.wait(500);
    });

    casper.then(function() {
        test.assertExists('#columndocument_number span.glyphicon.glyphicon-chevron-up');
        test.assertSelectorHasText('tbody tr:first-of-type td:nth-of-type(3)', 'hazop-report-9');
    });

    casper.then(function() {
        casper.click('#columndocument_number');
        casper.wait(500);
    });

    casper.then(function() {
        test.assertExists('#columndocument_number span.glyphicon.glyphicon-chevron-down');
        test.assertSelectorHasText('tbody tr:first-of-type td:nth-of-type(3)', 'hazop-report-0');
    });

    casper.then(function() {
        casper.click('#columntitle');
        casper.wait(500);
    });

    casper.then(function() {
        test.assertDoesntExist('#columndocument_number span.glyphicon');
        test.assertExists('#columntitle span.glyphicon.glyphicon-chevron-down');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('The search form searches', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(500);
    });

    casper.then(function() {
        test.assertElementCount('table#documents tbody tr', 5);
        casper.click('button#toggle-filters-button');
    });

    casper.then(function() {
        casper.sendKeys('#id_search_terms', 'gloubiboulga', {keepFocus: true});
        casper.wait(400);
    });

    casper.then(function() {
        test.assertElementCount('table#documents tbody tr', 0);
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Favorite tests', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.wait(500);
    });

    casper.then(function() {
        test.assertElementCount('td.columnfavorite span.glyphicon-star', 0);
        casper.click('tbody tr:nth-of-type(1) td.columnfavorite span');
    });

    casper.then(function() {
        casper.click('tbody tr:nth-of-type(3) td.columnfavorite span');
    });

    casper.then(function() {
        casper.click('tbody tr:nth-of-type(5) td.columnfavorite span');
        casper.reload();
    });

    casper.then(function() {
        casper.wait(500);
    });

    casper.then(function() {
        casper.capture('/tmp/phase.png');
        test.assertElementCount('td.columnfavorite span.glyphicon-star', 3);
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Searching updates the url', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.click('button#toggle-filters-button');
    });

    casper.then(function() {
        casper.fill('#search-sidebar form', {
            'status': 'FIN',
            'search_terms': 'toto'
        });
        casper.sendKeys('#id_search_terms', casper.page.event.key.Enter, {keepFocus: true});
        casper.wait(300);
    });

    casper.then(function() {
        test.assertUrlMatches(/search_terms=toto/);
        test.assertUrlMatches(/status=FIN/);
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Search queries can be bookmarked', 0, function suite(test) {
    casper.start(document_list_url + '?search_terms=gloubi&status=ASB', function() {
        casper.viewport(1024, 768);
    });

    casper.waitUntilVisible('div.sidebar-offcanvas', function() {
        test.assertField({type: 'css', path: '#id_search_terms'}, 'gloubi');
        test.assertField({type: 'css', path: '#id_status'}, 'ASB');
    });

    casper.run(function() {
        test.done();
    });
});

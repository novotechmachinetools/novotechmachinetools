<?php
/**
 * Black Friday 2026 — settings of bf-quote.php (the instant quote on /black-friday-machine-sale).
 *
 * The real file is bf-config.php, kept OUTSIDE the website on the server, in ~/novotech-private/black-friday/ next to the
 * price list PDF (the deploy copies the site into public_html and deletes what is not in the build; a file outside it is
 * never touched, never served and never in Git, so the prices and the lists below stay private). This sample shows the
 * keys only. bf-quote.php also writes its log there (requests.csv and requests/<id>.json).
 */
return [
    // signs the "Review and send" links in the e-mails about requests on hold: any long random text (bin2hex(random_bytes(32)))
    'secret' => '',

    // false = every request waits for the owner's approval (nothing is sent by itself)
    'auto_send' => true,

    // the price list e-mailed to the buyer: a PDF in this folder, and the name the buyer sees
    'pdf'      => 'NovoTech-Black-Friday-2026-Price-List.pdf',
    'pdf_name' => 'NovoTech-Black-Friday-2026-Price-List.pdf',

    // the in-stock machines with their Black Friday prices, shown as a table in the e-mail (optional: without them the PDF
    // alone carries the prices). id = the machine's id on the page (its checkbox in the form)
    'machines' => [
        // ['id' => 'xl-30135', 'name' => 'Dener XL 30135', 'type' => 'Hydraulic CNC press brake', 'price' => '$00,000', 'regular' => '$00,000', 'qty' => 1],
    ],

    // who gets the copy of every request
    'notify_to' => 'info@NovoTechMachineTools.com',

    // NovoTech's suppliers: an e-mail or website domain containing one of these words, or a company name containing one,
    // puts the request on hold
    'suppliers' => [],

    // competitors: words of their domains and names, their exact e-mail addresses and their phone numbers (any format)
    'competitors' => [],
    'competitor_emails' => [],
    'competitor_phones' => [],

    // words in a company name or domain that suggest a machinery seller ("machinery", "machine tools", "equipment sales" …)
    'dealer_words' => [],

    // true = requests from free e-mail addresses (gmail.com, outlook.com …) wait for approval too
    'hold_free_email' => false,
];

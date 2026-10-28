/* kornall demo website. No server, no tracking: every "purchase" stays in this browser (localStorage). */
(function () {
  'use strict';

  // ---- Prices: change them here. Business prices are EXAMPLES per seat and year, excluding VAT. ----
  var CONFIG = {
    personal: { year: 27, month: 2.8 },
    business: { 100: 24, 200: 22, 300: 20 },
    businessIsExample: true,
    vatRate: 0.2,
    trialDays: 7,
  };
  var EU = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'];
  var STORE = 'kornall-demo-order';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var eur = function (n) { return new Intl.NumberFormat('en-IE', { style: 'currency', currency: 'EUR' }).format(n); };
  var fmtDate = function (d) { return new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }); };
  var params = new URLSearchParams(location.search);

  function load() { try { return JSON.parse(localStorage.getItem(STORE) || 'null'); } catch (e) { return null; } }
  function save(o) { try { localStorage.setItem(STORE, JSON.stringify(o)); } catch (e) { /* private mode: the demo still works on this page */ } }
  function clear() { try { localStorage.removeItem(STORE); } catch (e) { /* ignore */ } }

  function randomBlock(n) {
    var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    var out = '';
    var buf = new Uint32Array(n);
    crypto.getRandomValues(buf);
    for (var i = 0; i < n; i++) out += chars[buf[i] % chars.length];
    return out;
  }
  function licenceKey(prefix) { return prefix + '-' + randomBlock(4) + '-' + randomBlock(4) + '-' + randomBlock(4) + '-' + randomBlock(4); }
  function addMonths(d, m) { var x = new Date(d); x.setMonth(x.getMonth() + m); return x.getTime(); }

  /** Line items for a plan. Personal prices include VAT; business prices exclude it. */
  function quote(sel, country, vatId) {
    var rate = CONFIG.vatRate;
    if (sel.plan === 'business') {
      var per = CONFIG.business[sel.seats] || CONFIG.business[100];
      var net = per * sel.seats;
      var reverse = !!vatId && EU.indexOf(country) !== -1 && country !== 'FR';
      var outside = country && EU.indexOf(country) === -1;
      var vat = reverse || outside ? 0 : Math.round(net * rate * 100) / 100;
      return {
        label: 'kornall Business, ' + sel.seats + ' licences',
        detail: sel.seats + ' × ' + eur(per) + ' per seat, 1 year' + (CONFIG.businessIsExample ? ' (example price)' : ''),
        net: net, vat: vat, total: net + vat,
        vatNote: reverse ? 'VAT reverse charge (EU business)' : outside ? 'No EU VAT (outside the EU)' : 'VAT 20%',
        period: 'year', recurring: 'Renews yearly',
      };
    }
    var month = sel.billing === 'month';
    var total = month ? CONFIG.personal.month : CONFIG.personal.year;
    var netP = Math.round((total / (1 + rate)) * 100) / 100;
    return {
      label: 'kornall Personal, ' + (month ? 'monthly' : 'yearly'),
      detail: '1 person, up to 2 PCs',
      net: netP, vat: Math.round((total - netP) * 100) / 100, total: total,
      vatNote: 'Including VAT 20%',
      period: month ? 'month' : 'year', recurring: month ? 'Renews monthly, cancel anytime' : 'Renews yearly, cancel anytime',
    };
  }

  function selection() {
    var plan = params.get('plan') === 'business' ? 'business' : 'personal';
    var seats = parseInt(params.get('seats') || '100', 10);
    if (!CONFIG.business[seats]) seats = 100;
    return { plan: plan, billing: params.get('billing') === 'month' ? 'month' : 'year', seats: seats };
  }

  // ---------- shared: mobile menu, year ----------
  function initShell() {
    var btn = $('.menu-btn');
    var nav = $('.nav');
    if (btn && nav) {
      btn.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        btn.setAttribute('aria-expanded', String(open));
      });
    }
    $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
  }

  // ---------- pricing ----------
  function initPricing() {
    var billing = 'year';
    var seats = 100;
    function render() {
      $$('[data-billing]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.billing === billing)); });
      $$('[data-seats]').forEach(function (b) { b.setAttribute('aria-pressed', String(Number(b.dataset.seats) === seats)); });
      var p = $('#personal-price');
      if (p) {
        p.innerHTML = billing === 'year' ? '€27<small> / year</small>' : '€2.80<small> / month</small>';
        $('#personal-note').textContent = billing === 'year' ? 'That is €2.25 a month, billed once a year' : 'Billed monthly, cancel anytime';
        $('#personal-buy').href = 'checkout.html?plan=personal&billing=' + billing;
      }
      var b = $('#business-price');
      if (b) {
        var per = CONFIG.business[seats];
        b.innerHTML = eur(per) + '<small> / seat / year</small>';
        $('#business-note').textContent = seats + ' licences: ' + eur(per * seats) + ' a year, excluding VAT';
        $('#business-buy').href = 'checkout.html?plan=business&seats=' + seats;
        $('#business-buy').textContent = 'Buy ' + seats + ' licences';
      }
    }
    $$('[data-billing]').forEach(function (b) { b.addEventListener('click', function () { billing = b.dataset.billing; render(); }); });
    $$('[data-seats]').forEach(function (b) { b.addEventListener('click', function () { seats = Number(b.dataset.seats); render(); }); });
    render();
  }

  // ---------- validation helpers ----------
  function setError(input, msg) {
    var field = input.closest('.field') || input.closest('.check') || input.parentElement;
    var err = field && field.querySelector('.err');
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (err) err.textContent = msg || '';
    return !msg;
  }
  function luhn(num) {
    var sum = 0;
    var alt = false;
    for (var i = num.length - 1; i >= 0; i--) {
      var n = parseInt(num.charAt(i), 10);
      if (alt) { n *= 2; if (n > 9) n -= 9; }
      sum += n;
      alt = !alt;
    }
    return sum % 10 === 0;
  }
  var emailOk = function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); };

  // ---------- checkout ----------
  function initCheckout() {
    var sel = selection();
    var form = $('#checkout-form');
    var isBiz = sel.plan === 'business';
    $$('[data-biz]').forEach(function (el) { el.hidden = !isBiz; });
    $$('[data-personal]').forEach(function (el) { el.hidden = isBiz; });
    $('#plan-title').textContent = isBiz ? 'kornall Business' : 'kornall Personal';

    // plan switches inside the summary
    var bill = $('#sum-billing');
    if (bill) {
      bill.value = sel.billing;
      bill.addEventListener('change', function () { sel.billing = bill.value; history.replaceState(null, '', '?plan=personal&billing=' + sel.billing); renderSummary(); });
    }
    var seatSel = $('#sum-seats');
    if (seatSel) {
      seatSel.value = String(sel.seats);
      seatSel.addEventListener('change', function () { sel.seats = Number(seatSel.value); history.replaceState(null, '', '?plan=business&seats=' + sel.seats); renderSummary(); });
    }

    function renderSummary() {
      var q = quote(sel, $('#country').value, isBiz ? $('#vat-id').value.trim() : '');
      $('#sum-label').textContent = q.label;
      $('#sum-detail').textContent = q.detail;
      $('#sum-net').textContent = eur(q.net);
      $('#sum-vat-label').textContent = q.vatNote;
      $('#sum-vat').textContent = eur(q.vat);
      $('#sum-total').textContent = eur(q.total);
      $('#sum-recurring').textContent = q.recurring;
      $('#pay-amount').textContent = eur(q.total);
      return q;
    }
    $('#country').addEventListener('change', renderSummary);
    if (isBiz) $('#vat-id').addEventListener('input', renderSummary);

    // payment method panels
    function showMethod() {
      var m = form.querySelector('input[name=method]:checked').value;
      $$('[data-method]').forEach(function (el) { el.hidden = el.dataset.method !== m; });
    }
    $$('input[name=method]').forEach(function (r) { r.addEventListener('change', showMethod); });
    showMethod();

    // card input formatting
    var cardNum = $('#card-number');
    cardNum.addEventListener('input', function () {
      var d = cardNum.value.replace(/\D/g, '').slice(0, 19);
      cardNum.value = d.replace(/(.{4})/g, '$1 ').trim();
    });
    var exp = $('#card-exp');
    exp.addEventListener('input', function () {
      var d = exp.value.replace(/\D/g, '').slice(0, 4);
      exp.value = d.length > 2 ? d.slice(0, 2) + ' / ' + d.slice(2) : d;
    });
    $$('#checkout-form input, #checkout-form select').forEach(function (el) {
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') setError(el, ''); });
    });

    function validate() {
      var ok = true;
      var first = null;
      function check(el, msg) {
        var good = setError(el, msg);
        if (!good && !first) first = el;
        ok = ok && good;
      }
      var email = $('#email');
      check(email, emailOk(email.value.trim()) ? '' : 'Enter a valid email address, for example name@company.com.');
      var name = $('#full-name');
      check(name, name.value.trim().length >= 2 ? '' : 'Enter your full name.');
      var country = $('#country');
      check(country, country.value ? '' : 'Choose your country.');
      if (isBiz) {
        var company = $('#company');
        check(company, company.value.trim() ? '' : 'Enter your company name.');
        var vat = $('#vat-id');
        var v = vat.value.trim().toUpperCase().replace(/\s/g, '');
        check(vat, !v || /^[A-Z]{2}[A-Z0-9]{2,13}$/.test(v) ? '' : 'Use the format of your country, for example FR12345678901.');
      }
      var method = form.querySelector('input[name=method]:checked').value;
      if (method === 'card') {
        var num = cardNum.value.replace(/\s/g, '');
        check(cardNum, /^\d{13,19}$/.test(num) && luhn(num) ? '' : 'This card number is not valid. In this demo, use 4242 4242 4242 4242.');
        var m = exp.value.match(/^(\d{2}) \/ (\d{2})$/);
        var expMsg = 'Enter the expiry date as MM / YY.';
        if (m) {
          var mm = Number(m[1]);
          var yy = 2000 + Number(m[2]);
          var now = new Date();
          if (mm < 1 || mm > 12) expMsg = 'The month must be between 01 and 12.';
          else if (yy < now.getFullYear() || (yy === now.getFullYear() && mm < now.getMonth() + 1)) expMsg = 'This card has expired.';
          else expMsg = '';
        }
        check(exp, expMsg);
        var cvc = $('#card-cvc');
        check(cvc, /^\d{3,4}$/.test(cvc.value.trim()) ? '' : 'Enter the 3 or 4 digits on the back of the card.');
      }
      var terms = $('#accept-terms');
      check(terms, terms.checked ? '' : 'Accept the terms of sale to continue.');
      if (!isBiz) {
        var waiver = $('#accept-waiver');
        check(waiver, waiver.checked ? '' : 'Tick this box to receive your licence immediately.');
      }
      if (first) first.focus();
      return ok;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var formErr = $('#form-error');
      formErr.hidden = true;
      if (!validate()) return;
      var q = renderSummary();
      var method = form.querySelector('input[name=method]:checked').value;
      var num = cardNum.value.replace(/\s/g, '');
      var overlay = $('#processing');
      overlay.hidden = false;
      // Never keep card details, even in this demo.
      var last4 = num.slice(-4);
      cardNum.value = '';
      $('#card-cvc').value = '';
      setTimeout(function () {
        overlay.hidden = true;
        if (method === 'card' && num === '4000000000000002') {
          formErr.hidden = false;
          formErr.textContent = 'Your bank declined the payment (demo test card). Nothing was charged. Try another card.';
          cardNum.focus();
          return;
        }
        var now = Date.now();
        var order = {
          id: 'KN-' + new Date().getFullYear() + '-' + randomBlock(6),
          createdAt: now,
          plan: sel.plan,
          billing: isBiz ? 'year' : sel.billing,
          seats: isBiz ? sel.seats : 1,
          email: $('#email').value.trim(),
          name: $('#full-name').value.trim(),
          company: isBiz ? $('#company').value.trim() : '',
          vatId: isBiz ? $('#vat-id').value.trim().toUpperCase() : '',
          country: $('#country').value,
          method: method,
          last4: method === 'card' ? last4 : '',
          quote: q,
          key: licenceKey(isBiz ? 'KNB' : 'KNP'),
          status: method === 'transfer' ? 'awaiting-payment' : 'active',
          renewsAt: addMonths(now, !isBiz && sel.billing === 'month' ? 1 : 12),
          cancelAt: null,
          devices: isBiz ? [] : [],
          seatsUsed: 0,
        };
        save(order);
        location.href = 'success.html';
      }, 1600);
    });

    renderSummary();
  }

  // ---------- success ----------
  function initSuccess() {
    var o = load();
    if (!o) { $('#no-order').hidden = false; $('#order').hidden = true; return; }
    $('#ok-email').textContent = o.email;
    $('#ok-id').textContent = o.id;
    $('#ok-plan').textContent = o.quote.label;
    $('#ok-total').textContent = eur(o.quote.total) + (o.quote.period === 'month' ? ' / month' : ' / year');
    $('#ok-renew').textContent = o.status === 'awaiting-payment' ? 'Starts when your bank transfer arrives' : fmtDate(o.renewsAt);
    $('#ok-method').textContent = o.method === 'card' ? 'Card ending ' + o.last4 : o.method === 'paypal' ? 'PayPal' : 'Bank transfer';
    $('#ok-key').textContent = o.key;
    if (o.status === 'awaiting-payment') $('#transfer-note').hidden = false;
    $('#ok-seats-note').hidden = o.plan !== 'business';
    $('#copy-key').addEventListener('click', function () {
      navigator.clipboard.writeText(o.key).then(function () { $('#copy-key').textContent = 'Copied'; });
    });
  }

  // ---------- invoice ----------
  function initInvoice() {
    var o = load();
    if (!o) { $('#no-order').hidden = false; $('#invoice').hidden = true; return; }
    $('#inv-id').textContent = 'INV-' + o.id.slice(3);
    $('#inv-date').textContent = fmtDate(o.createdAt);
    $('#inv-order').textContent = o.id;
    $('#inv-to').textContent = [o.company, o.name, o.email, o.vatId ? 'VAT ' + o.vatId : '', o.country].filter(Boolean).join('\n');
    $('#inv-label').textContent = o.quote.label;
    $('#inv-detail').textContent = o.quote.detail;
    $('#inv-net').textContent = eur(o.quote.net);
    $('#inv-vat-label').textContent = o.quote.vatNote;
    $('#inv-vat').textContent = eur(o.quote.vat);
    $('#inv-total').textContent = eur(o.quote.total);
    $('#inv-status').textContent = o.status === 'awaiting-payment' ? 'Awaiting bank transfer' : 'Paid';
    $('#print').addEventListener('click', function () { window.print(); });
  }

  // ---------- account ----------
  function initAccount() {
    var dlg = $('#cancel-dialog');
    function render() {
      var o = load();
      $('#no-account').hidden = !!o;
      $('#account').hidden = !o;
      if (!o) return;
      var biz = o.plan === 'business';
      $('#acc-email').textContent = o.email;
      $('#acc-plan').textContent = o.quote.label;
      $('#acc-price').textContent = eur(o.quote.total) + (o.quote.period === 'month' ? ' / month' : ' / year');
      var st = $('#acc-status');
      var renew = $('#acc-renew-label');
      if (o.status === 'awaiting-payment') {
        st.textContent = 'Awaiting payment';
        st.className = 'status status-warn';
        renew.textContent = 'Starts';
        $('#acc-renew').textContent = 'when your transfer arrives';
      } else if (o.cancelAt) {
        st.textContent = 'Cancelled, active until ' + fmtDate(o.cancelAt);
        st.className = 'status status-warn';
        renew.textContent = 'Ends on';
        $('#acc-renew').textContent = fmtDate(o.cancelAt);
      } else {
        st.textContent = 'Active';
        st.className = 'status status-ok';
        renew.textContent = 'Renews on';
        $('#acc-renew').textContent = fmtDate(o.renewsAt);
      }
      $('#acc-method').textContent = o.method === 'card' ? 'Card ending ' + o.last4 : o.method === 'paypal' ? 'PayPal' : 'Bank transfer';
      $('#acc-key').textContent = o.key;
      $('#cancel-btn').hidden = !!o.cancelAt || o.status === 'awaiting-payment';
      $('#resume-btn').hidden = !o.cancelAt;
      $('#switch-yearly').hidden = biz || o.billing !== 'month' || !!o.cancelAt;

      $('#devices-personal').hidden = biz;
      $('#devices-business').hidden = !biz;
      if (biz) {
        $('#seat-count').textContent = o.seatsUsed + ' of ' + o.seats + ' licences assigned';
        $('#seat-bar').style.width = Math.round((o.seatsUsed / o.seats) * 100) + '%';
      } else {
        var list = $('#device-list');
        list.innerHTML = '';
        o.devices.forEach(function (d, i) {
          var li = document.createElement('li');
          var name = document.createElement('div');
          name.style.flex = '1';
          var strong = document.createElement('strong');
          strong.style.fontWeight = '500';
          strong.textContent = d.name;
          var sub = document.createElement('div');
          sub.className = 'small muted';
          sub.textContent = 'Activated ' + fmtDate(d.at);
          name.appendChild(strong);
          name.appendChild(sub);
          var rm = document.createElement('button');
          rm.type = 'button';
          rm.className = 'btn btn-ghost';
          rm.textContent = 'Remove';
          rm.setAttribute('aria-label', 'Remove ' + d.name);
          rm.addEventListener('click', function () {
            o.devices.splice(i, 1);
            save(o);
            render();
          });
          li.appendChild(name);
          li.appendChild(rm);
          list.appendChild(li);
        });
        $('#device-count').textContent = o.devices.length + ' of 2 PCs activated';
        $('#add-device').hidden = o.devices.length >= 2;
        $('#device-empty').hidden = o.devices.length > 0;
      }
      $('#invoice-row-date').textContent = fmtDate(o.createdAt);
      $('#invoice-row-amount').textContent = eur(o.quote.total);
      $('#invoice-row-id').textContent = 'INV-' + o.id.slice(3);
    }

    $('#cancel-btn').addEventListener('click', function () {
      var o = load();
      $('#cancel-until').textContent = fmtDate(o.renewsAt);
      dlg.hidden = false;
      $('#confirm-cancel').focus();
    });
    $('#keep-btn').addEventListener('click', function () { dlg.hidden = true; $('#cancel-btn').focus(); });
    dlg.addEventListener('keydown', function (e) { if (e.key === 'Escape') { dlg.hidden = true; $('#cancel-btn').focus(); } });
    $('#confirm-cancel').addEventListener('click', function () {
      var o = load();
      o.cancelAt = o.renewsAt;
      save(o);
      dlg.hidden = true;
      render();
      $('#account-msg').hidden = false;
      $('#account-msg').textContent = 'Subscription cancelled. kornall keeps working until ' + fmtDate(o.cancelAt) + '. No further payment will be taken.';
    });
    $('#resume-btn').addEventListener('click', function () {
      var o = load();
      o.cancelAt = null;
      save(o);
      render();
      $('#account-msg').hidden = false;
      $('#account-msg').textContent = 'Subscription resumed. It renews on ' + fmtDate(o.renewsAt) + '.';
    });
    $('#switch-yearly').addEventListener('click', function () {
      var o = load();
      o.billing = 'year';
      o.quote = quote({ plan: 'personal', billing: 'year' }, o.country, '');
      o.renewsAt = addMonths(o.renewsAt, 0);
      save(o);
      render();
      $('#account-msg').hidden = false;
      $('#account-msg').textContent = 'Switched to yearly billing: €27 a year from ' + fmtDate(o.renewsAt) + '.';
    });
    $('#add-device').addEventListener('click', function () {
      var o = load();
      var names = ['Office PC', 'Laptop'];
      o.devices.push({ name: names[o.devices.length] || 'PC ' + (o.devices.length + 1), at: Date.now() });
      save(o);
      render();
    });
    $('#assign-seat').addEventListener('click', function () {
      var o = load();
      o.seatsUsed = Math.min(o.seats, o.seatsUsed + 10);
      save(o);
      render();
    });
    $('#copy-acc-key').addEventListener('click', function () {
      navigator.clipboard.writeText(load().key).then(function () { $('#copy-acc-key').textContent = 'Copied'; });
    });
    $('#reset-demo').addEventListener('click', function () { clear(); render(); });
    $('#sample-order').addEventListener('click', function () {
      var now = Date.now();
      save({
        id: 'KN-' + new Date().getFullYear() + '-' + randomBlock(6), createdAt: now, plan: 'personal', billing: 'month', seats: 1,
        email: 'you@example.com', name: 'Sample customer', company: '', vatId: '', country: 'FR', method: 'card', last4: '4242',
        quote: quote({ plan: 'personal', billing: 'month' }, 'FR', ''), key: licenceKey('KNP'), status: 'active',
        renewsAt: addMonths(now, 1), cancelAt: null, devices: [{ name: 'Office PC', at: now }], seatsUsed: 0,
      });
      render();
    });
    render();
  }

  // ---------- trial ----------
  function initTrial() {
    var form = $('#trial-form');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = $('#trial-email');
      if (!setError(email, emailOk(email.value.trim()) ? '' : 'Enter a valid email address, for example name@company.com.')) { email.focus(); return; }
      var consent = $('#trial-consent');
      if (!setError(consent, consent.checked ? '' : 'Accept the licence agreement to start the trial.')) { consent.focus(); return; }
      form.hidden = true;
      $('#trial-done').hidden = false;
      $('#trial-to').textContent = email.value.trim();
      $('#trial-key').textContent = licenceKey('KNT');
      var end = new Date(Date.now() + CONFIG.trialDays * 86400000);
      $('#trial-end').textContent = fmtDate(end);
      $('#trial-done h2').focus();
    });
  }

  // ---------- download ----------
  function initDownload() {
    $('#download-btn').addEventListener('click', function () {
      $('#download-msg').hidden = false;
      $('#download-msg').focus();
    });
  }

  // ---------- contact ----------
  function initContact() {
    var form = $('#contact-form');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      var first = null;
      [['#c-name', function (v) { return v.length >= 2; }, 'Enter your name.'],
       ['#c-email', emailOk, 'Enter a valid email address.'],
       ['#c-company', function (v) { return v.length >= 1; }, 'Enter your organization.'],
       ['#c-message', function (v) { return v.length >= 10; }, 'Tell us a little more (at least 10 characters).']].forEach(function (r) {
        var el = $(r[0]);
        var good = setError(el, r[1](el.value.trim()) ? '' : r[2]);
        if (!good && !first) first = el;
        ok = ok && good;
      });
      if (!ok) { first.focus(); return; }
      form.hidden = true;
      $('#contact-done').hidden = false;
      $('#contact-done h2').focus();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initShell();
    var page = document.body.dataset.page;
    var init = { pricing: initPricing, home: initPricing, checkout: initCheckout, success: initSuccess, invoice: initInvoice, account: initAccount, trial: initTrial, download: initDownload, contact: initContact }[page];
    if (init) init();
  });
})();

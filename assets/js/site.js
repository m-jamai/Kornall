/* kornall demo website. No server, no tracking: every "purchase" stays in this browser (localStorage). */
(function () {
  'use strict';

  // ---- Prices: change them here. ----
  // Personal prices include VAT. Professional and Team prices exclude VAT.
  var CONFIG = {
    personal: { year: 27, month: 2.8 },
    professional: { year: 190, month: 19 },
    team: { perUserMonth: 15, min: 5, max: 50 },
    vatRate: 0.2,
    trialDays: 7,
  };
  var EU = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'];
  var STORE = 'kornall-demo-order';
  var PLAN_NAME = { personal: 'Personal', professional: 'Professional', team: 'Team' };

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var eur = function (n) { return new Intl.NumberFormat('en-IE', { style: 'currency', currency: 'EUR' }).format(n); };
  var eur0 = function (n) { return new Intl.NumberFormat('en-IE', { style: 'currency', currency: 'EUR', maximumFractionDigits: n % 1 ? 2 : 0 }).format(n); };
  var fmtDate = function (d) { return new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }); };
  var params = new URLSearchParams(location.search);
  var round2 = function (n) { return Math.round(n * 100) / 100; };

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
  function clampSeats(n) { return Math.min(CONFIG.team.max, Math.max(CONFIG.team.min, Math.round(Number(n) || CONFIG.team.min))); }

  /** VAT for business-priced plans: reverse charge for EU companies outside France with a VAT number, none outside the EU. */
  function businessVat(net, country, vatId) {
    var reverse = !!vatId && EU.indexOf(country) !== -1 && country !== 'FR';
    var outside = !!country && EU.indexOf(country) === -1;
    if (reverse) return { vat: 0, note: 'VAT reverse charge (EU business)' };
    if (outside) return { vat: 0, note: 'No EU VAT (outside the EU)' };
    return { vat: round2(net * CONFIG.vatRate), note: 'VAT 20%' };
  }

  /** Line items for a selection: { plan, billing, seats }. */
  function quote(sel, country, vatId) {
    if (sel.plan === 'team') {
      var seats = clampSeats(sel.seats);
      var per = CONFIG.team.perUserMonth * 12;
      var net = per * seats;
      var v = businessVat(net, country, vatId);
      return {
        label: 'kornall Team, ' + seats + ' users',
        detail: seats + ' × ' + eur0(CONFIG.team.perUserMonth) + ' per user per month, billed yearly',
        net: net, vat: v.vat, total: round2(net + v.vat), vatNote: v.note,
        period: 'year', recurring: 'Renews yearly. Add users anytime.',
      };
    }
    var month = sel.billing === 'month';
    if (sel.plan === 'professional') {
      var netP = month ? CONFIG.professional.month : CONFIG.professional.year;
      var vp = businessVat(netP, country, vatId);
      return {
        label: 'kornall Professional, ' + (month ? 'monthly' : 'yearly'),
        detail: '1 professional, up to 2 PCs, Data Book module included',
        net: netP, vat: vp.vat, total: round2(netP + vp.vat), vatNote: vp.note,
        period: month ? 'month' : 'year', recurring: month ? 'Renews monthly, cancel anytime' : 'Renews yearly, cancel anytime',
      };
    }
    var total = month ? CONFIG.personal.month : CONFIG.personal.year;
    var netPe = round2(total / (1 + CONFIG.vatRate));
    return {
      label: 'kornall Personal, ' + (month ? 'monthly' : 'yearly'),
      detail: '1 person, up to 2 PCs',
      net: netPe, vat: round2(total - netPe), total: total, vatNote: 'Including VAT 20%',
      period: month ? 'month' : 'year', recurring: month ? 'Renews monthly, cancel anytime' : 'Renews yearly, cancel anytime',
    };
  }

  function selection() {
    var p = params.get('plan');
    var plan = p === 'team' || p === 'professional' ? p : 'personal';
    return { plan: plan, billing: params.get('billing') === 'month' ? 'month' : 'year', seats: clampSeats(params.get('seats') || 10) };
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
    if (!$('#plans')) return;
    var billing = 'year';
    var seatsInput = $('#team-seats');
    function render() {
      $$('[data-billing]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.billing === billing)); });
      var y = billing === 'year';
      $('#personal-price').innerHTML = y ? '€27<small> / year</small>' : '€2.80<small> / month</small>';
      $('#personal-note').textContent = y ? 'That is €2.25 a month. VAT included.' : 'VAT included. Cancel anytime.';
      $('#personal-buy').href = 'checkout.html?plan=personal&billing=' + billing;
      $('#pro-price').innerHTML = y ? '€190<small> / year</small>' : '€19<small> / month</small>';
      $('#pro-note').textContent = y ? 'That is €15.83 a month, 2 months free. Excl. VAT.' : 'Excl. VAT. Cancel anytime.';
      $('#pro-buy').href = 'checkout.html?plan=professional&billing=' + billing;
      var n = clampSeats(seatsInput.value);
      $('#team-total').textContent = n + ' users: ' + eur(n * CONFIG.team.perUserMonth * 12) + ' a year, excl. VAT';
      $('#team-buy').href = 'checkout.html?plan=team&seats=' + n;
      $('#team-buy').textContent = 'Buy for ' + n + ' users';
    }
    $$('[data-billing]').forEach(function (b) { b.addEventListener('click', function () { billing = b.dataset.billing; render(); }); });
    seatsInput.addEventListener('input', render);
    seatsInput.addEventListener('change', function () { seatsInput.value = String(clampSeats(seatsInput.value)); render(); });
    $('#seat-minus').addEventListener('click', function () { seatsInput.value = String(clampSeats(Number(seatsInput.value) - 1)); render(); });
    $('#seat-plus').addEventListener('click', function () { seatsInput.value = String(clampSeats(Number(seatsInput.value) + 1)); render(); });
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
    var isTeam = sel.plan === 'team';
    var isPro = sel.plan === 'professional';
    $$('[data-company]').forEach(function (el) { el.hidden = sel.plan === 'personal'; });
    $$('[data-team]').forEach(function (el) { el.hidden = !isTeam; });
    $$('[data-period]').forEach(function (el) { el.hidden = isTeam; });
    $('#plan-title').textContent = 'kornall ' + PLAN_NAME[sel.plan];
    $('#company-label-opt').hidden = isTeam;

    var bill = $('#sum-billing');
    bill.innerHTML = isPro
      ? '<option value="year">Yearly, €190 (2 months free)</option><option value="month">Monthly, €19</option>'
      : '<option value="year">Yearly, €27 (save 20%)</option><option value="month">Monthly, €2.80</option>';
    bill.value = sel.billing;
    bill.addEventListener('change', function () { sel.billing = bill.value; history.replaceState(null, '', '?plan=' + sel.plan + '&billing=' + sel.billing); renderSummary(); });
    var seatIn = $('#sum-seats');
    seatIn.value = String(sel.seats);
    seatIn.addEventListener('change', function () { sel.seats = clampSeats(seatIn.value); seatIn.value = String(sel.seats); history.replaceState(null, '', '?plan=team&seats=' + sel.seats); renderSummary(); });

    var vatInput = $('#vat-id');
    function waiverNeeded() { return sel.plan !== 'team' && !vatInput.value.trim(); }
    function renderSummary() {
      var q = quote(sel, $('#country').value, sel.plan === 'personal' ? '' : vatInput.value.trim());
      $('#sum-label').textContent = q.label;
      $('#sum-detail').textContent = q.detail;
      $('#sum-net').textContent = eur(q.net);
      $('#sum-vat-label').textContent = q.vatNote;
      $('#sum-vat').textContent = eur(q.vat);
      $('#sum-total').textContent = eur(q.total);
      $('#sum-recurring').textContent = q.recurring;
      $('#pay-amount').textContent = eur(q.total);
      $('#waiver-row').hidden = !waiverNeeded();
      return q;
    }
    $('#country').addEventListener('change', renderSummary);
    vatInput.addEventListener('input', renderSummary);

    function showMethod() {
      var m = form.querySelector('input[name=method]:checked').value;
      $$('[data-method]').forEach(function (el) { el.hidden = el.dataset.method !== m; });
    }
    $$('input[name=method]').forEach(function (r) { r.addEventListener('change', showMethod); });
    showMethod();

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
      if (isTeam) {
        var company = $('#company');
        check(company, company.value.trim() ? '' : 'Enter your company name.');
      }
      if (sel.plan !== 'personal') {
        var v = vatInput.value.trim().toUpperCase().replace(/\s/g, '');
        check(vatInput, !v || /^[A-Z]{2}[A-Z0-9]{2,13}$/.test(v) ? '' : 'Use the format of your country, for example FR12345678901.');
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
      if (waiverNeeded()) {
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
      var last4 = num.slice(-4);
      // Never keep card details, even in this demo.
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
        save({
          id: 'KN-' + new Date().getFullYear() + '-' + randomBlock(6),
          createdAt: now,
          plan: sel.plan,
          billing: isTeam ? 'year' : sel.billing,
          seats: isTeam ? clampSeats(sel.seats) : 1,
          email: $('#email').value.trim(),
          name: $('#full-name').value.trim(),
          company: sel.plan === 'personal' ? '' : $('#company').value.trim(),
          vatId: sel.plan === 'personal' ? '' : vatInput.value.trim().toUpperCase(),
          country: $('#country').value,
          method: method,
          last4: method === 'card' ? last4 : '',
          quote: q,
          key: licenceKey(isTeam ? 'KNT' : isPro ? 'KNR' : 'KNP'),
          status: method === 'transfer' ? 'awaiting-payment' : 'active',
          renewsAt: addMonths(now, !isTeam && sel.billing === 'month' ? 1 : 12),
          cancelAt: null,
          devices: [],
          seatsUsed: 0,
        });
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
    $('#ok-seats-note').hidden = o.plan !== 'team';
    $('#ok-databook-note').hidden = o.plan === 'personal';
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
    function msg(text) { $('#account-msg').hidden = false; $('#account-msg').textContent = text; }
    function render() {
      var o = load();
      $('#no-account').hidden = !!o;
      $('#account').hidden = !o;
      if (!o) return;
      var team = o.plan === 'team';
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
      $('#switch-yearly').hidden = team || o.billing !== 'month' || !!o.cancelAt;
      $('#upgrade-pro').hidden = o.plan !== 'personal' || !!o.cancelAt;

      $('#devices-personal').hidden = team;
      $('#devices-team').hidden = !team;
      if (team) {
        $('#seat-count').textContent = o.seatsUsed + ' of ' + o.seats + ' users assigned';
        $('#seat-bar').style.width = Math.round((o.seatsUsed / o.seats) * 100) + '%';
        $('#assign-seat').hidden = o.seatsUsed >= o.seats;
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
          rm.addEventListener('click', function () { o.devices.splice(i, 1); save(o); render(); });
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
      $('#cancel-until').textContent = fmtDate(load().renewsAt);
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
      msg('Subscription cancelled. kornall keeps working until ' + fmtDate(o.cancelAt) + '. No further payment will be taken.');
    });
    $('#resume-btn').addEventListener('click', function () {
      var o = load();
      o.cancelAt = null;
      save(o);
      render();
      msg('Subscription resumed. It renews on ' + fmtDate(o.renewsAt) + '.');
    });
    $('#switch-yearly').addEventListener('click', function () {
      var o = load();
      o.billing = 'year';
      o.quote = quote({ plan: o.plan, billing: 'year' }, o.country, o.vatId);
      save(o);
      render();
      msg('Switched to yearly billing: ' + eur(o.quote.total) + ' a year from ' + fmtDate(o.renewsAt) + '.');
    });
    $('#upgrade-pro').addEventListener('click', function () {
      var o = load();
      o.plan = 'professional';
      o.quote = quote({ plan: 'professional', billing: o.billing }, o.country, o.vatId);
      save(o);
      render();
      msg('Upgraded to Professional. The Data Book module is now included. The price difference is charged pro rata (simulated).');
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
      o.seatsUsed = Math.min(o.seats, o.seatsUsed + 1);
      save(o);
      render();
    });
    $('#copy-acc-key').addEventListener('click', function () {
      navigator.clipboard.writeText(load().key).then(function () { $('#copy-acc-key').textContent = 'Copied'; });
    });
    $('#reset-demo').addEventListener('click', function () { clear(); $('#account-msg').hidden = true; render(); });
    $('#sample-order').addEventListener('click', function () {
      var now = Date.now();
      save({
        id: 'KN-' + new Date().getFullYear() + '-' + randomBlock(6), createdAt: now, plan: 'professional', billing: 'month', seats: 1,
        email: 'qa@example.com', name: 'Sample customer', company: 'Example Valves Ltd', vatId: '', country: 'FR', method: 'card', last4: '4242',
        quote: quote({ plan: 'professional', billing: 'month' }, 'FR', ''), key: licenceKey('KNR'), status: 'active',
        renewsAt: addMonths(now, 1), cancelAt: null, devices: [{ name: 'Office PC', at: now }], seatsUsed: 0,
      });
      render();
    });
    render();
  }

  // ---------- simple forms (trial, contact, early access) ----------
  function simpleForm(formSel, doneSel, rules, onDone) {
    var form = $(formSel);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      var first = null;
      rules.forEach(function (r) {
        var el = $(r[0]);
        var v = el.type === 'checkbox' ? el.checked : el.value.trim();
        var good = setError(el, r[1](v) ? '' : r[2]);
        if (!good && !first) first = el;
        ok = ok && good;
      });
      if (!ok) { first.focus(); return; }
      form.hidden = true;
      $(doneSel).hidden = false;
      if (onDone) onDone();
      var h = $(doneSel + ' h2');
      if (h) h.focus();
    });
  }
  var filled = function (n) { return function (v) { return typeof v === 'string' && v.length >= n; }; };
  var ticked = function (v) { return v === true; };

  function initTrial() {
    simpleForm('#trial-form', '#trial-done', [
      ['#trial-email', emailOk, 'Enter a valid email address, for example name@company.com.'],
      ['#trial-consent', ticked, 'Accept the licence agreement to start the trial.'],
    ], function () {
      $('#trial-to').textContent = $('#trial-email').value.trim();
      $('#trial-key').textContent = licenceKey('KNTR');
      $('#trial-end').textContent = fmtDate(Date.now() + CONFIG.trialDays * 86400000);
    });
  }
  function initContact() {
    var topic = params.get('topic');
    if (topic && $('#c-topic option[value="' + topic + '"]')) $('#c-topic').value = topic;
    simpleForm('#contact-form', '#contact-done', [
      ['#c-name', filled(2), 'Enter your name.'],
      ['#c-email', emailOk, 'Enter a valid email address.'],
      ['#c-company', filled(1), 'Enter your organization.'],
      ['#c-message', filled(10), 'Tell us a little more (at least 10 characters).'],
    ]);
  }
  function initEarly() {
    simpleForm('#early-form', '#early-done', [
      ['#e-email', emailOk, 'Enter a valid work email address.'],
      ['#e-role', filled(1), 'Choose your role.'],
      ['#e-consent', ticked, 'Tick this box so we can contact you.'],
    ]);
  }
  function initDownload() {
    $('#download-btn').addEventListener('click', function () {
      $('#download-msg').hidden = false;
      $('#download-msg').focus();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initShell();
    var init = {
      home: initPricing, pricing: initPricing, checkout: initCheckout, success: initSuccess, invoice: initInvoice, account: initAccount,
      trial: initTrial, download: initDownload, contact: initContact, early: initEarly,
    }[document.body.dataset.page];
    if (init) init();
  });
})();

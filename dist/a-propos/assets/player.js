// Lecteur vidéo maison des pages Stratèges.
// La vidéo reste hébergée sur YouTube (non répertoriée), mais la famille ne voit
// ni le titre, ni la chaîne, ni le logo, ni les suggestions : uniquement nos contrôles.
// Usage : <div class="video" data-yt="IDENTIFIANT" data-tag="Libellé"></div>
(function () {
  var css =
    '.video .ply-frame{position:absolute;left:0;right:0;top:-70px;height:calc(100% + 140px);pointer-events:none}' +
    '.video .ply-frame iframe{width:100%;height:100%;border:0}' +
    '.video .ply-shield{position:absolute;inset:0;cursor:pointer;z-index:2}' +
    '.video .ply-shield.pass{pointer-events:none}' +
    '.video .ply-cover{position:absolute;inset:0;z-index:3;display:flex;align-items:center;justify-content:center;background:rgba(17,17,17,.55);cursor:pointer;transition:opacity .2s}' +
    '.video .ply-cover.hide{opacity:0;pointer-events:none}' +
    '.video .ply-cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0}.video .ply-cover.end{background:#111}.video .ply-cover.end img{opacity:.55}' +
    '.video .ply-big{position:relative;width:76px;height:76px;border-radius:50%;background:#C9A24D;display:flex;align-items:center;justify-content:center;padding-left:4px}' +
    '.video .ply-big.replay{padding-left:0}' +
    '.video .ply-bar{position:absolute;left:0;right:0;bottom:0;z-index:4;display:flex;align-items:center;gap:12px;padding:22px 14px 10px;background:linear-gradient(transparent,rgba(0,0,0,.7));color:#F7F4EC;font:500 13px Inter,Arial,sans-serif;opacity:1;transition:opacity .3s}' +
    '.video.idle .ply-bar{opacity:0}' +
    '.video .ply-bar button{all:unset;cursor:pointer;width:30px;height:30px;display:flex;align-items:center;justify-content:center;border-radius:6px;flex:none}' +
    '.video .ply-bar button:focus-visible{outline:2px solid #C9A24D}' +
    '.video .ply-track{flex:1;height:18px;display:flex;align-items:center;cursor:pointer;touch-action:none}' +
    '.video .ply-rail{position:relative;width:100%;height:4px;border-radius:2px;background:rgba(247,244,236,.28)}' +
    '.video .ply-fill{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:2px;background:#C9A24D}' +
    '.video .ply-bar .ply-speed{width:auto;min-width:38px;padding:0 6px;font:600 13px Inter,Arial,sans-serif;border:1px solid rgba(247,244,236,.35)}' +
    '.video .ply-time{font-variant-numeric:tabular-nums;white-space:nowrap;flex:none}' +
    '.video:fullscreen{border-radius:0;max-width:none}' +
    '.video:-webkit-full-screen{border-radius:0;max-width:none}' +
    '@media (max-width:760px){.video .ply-big{width:60px;height:60px}.video .ply-bar{gap:8px;padding:18px 8px 6px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var ICON = {
    play: '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z" fill="#F7F4EC"/></svg>',
    pause: '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="#F7F4EC"/></svg>',
    son: '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M4 9h4l5-4v14l-5-4H4z" fill="#F7F4EC"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="#F7F4EC" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>',
    muet: '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M4 9h4l5-4v14l-5-4H4z" fill="#F7F4EC"/><path d="M16.5 9.5l5 5M21.5 9.5l-5 5" stroke="#F7F4EC" stroke-width="1.8" stroke-linecap="round"/></svg>',
    plein: '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" stroke="#F7F4EC" stroke-width="2" fill="none"/></svg>',
    bigplay: '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z" fill="#111111"/></svg>',
    replay: '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M12 5a7 7 0 1 1-6.6 4.7" stroke="#111" stroke-width="2.2" fill="none" stroke-linecap="round"/><path d="M4 4v5h5" stroke="#111" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  };

  var apiQueue = [], apiLoading = false;
  function withApi(cb) {
    if (window.YT && window.YT.Player) return cb();
    apiQueue.push(cb);
    if (apiLoading) return;
    apiLoading = true;
    var prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = function () {
      if (prev) prev();
      apiQueue.splice(0).forEach(function (f) { f(); });
    };
    var s = document.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; document.head.appendChild(s);
  }

  function fmt(t) {
    t = Math.max(0, Math.floor(t || 0));
    var h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60;
    return (h ? h + ':' + (m < 10 ? '0' : '') : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }
  var touch = window.matchMedia && matchMedia('(hover: none)').matches;
  var fsOK = document.fullscreenEnabled || document.webkitFullscreenEnabled;
  var current = null; // une seule vidéo à la fois sur la page

  function start(box, id, tag) {
    box.innerHTML =
      '<div class="ply-frame"><div></div></div>' +
      '<div class="ply-shield' + (touch ? ' pass' : '') + '"></div>' +
      '<div class="ply-cover hide"><img alt="" src="https://i.ytimg.com/vi/' + id + '/hqdefault.jpg"><span class="ply-big"></span></div>' +
      '<div class="ply-bar">' +
        '<button type="button" class="ply-pp" aria-label="Pause">' + ICON.pause + '</button>' +
        '<div class="ply-track" role="slider" aria-label="Avancer ou reculer dans la vidéo" tabindex="0"><div class="ply-rail"><div class="ply-fill"></div></div></div>' +
        '<span class="ply-time">0:00</span>' +
        '<button type="button" class="ply-speed" aria-label="Vitesse de lecture">1x</button>' +
        '<button type="button" class="ply-mute" aria-label="Couper le son">' + ICON.son + '</button>' +
        (fsOK ? '<button type="button" class="ply-fs" aria-label="Plein écran">' + ICON.plein + '</button>' : '') +
      '</div>';
    var $ = function (q) { return box.querySelector(q); };
    var shield = $('.ply-shield'), cover = $('.ply-cover'), big = $('.ply-big'), pp = $('.ply-pp'),
        track = $('.ply-track'), fill = $('.ply-fill'), time = $('.ply-time'), mute = $('.ply-mute'), fs = $('.ply-fs'), speed = $('.ply-speed');
    var RATES = [1, 1.25, 1.5, 1.75, 2], rate = 0;
    var player, ended = false, idleT;

    function wake() {
      box.classList.remove('idle'); clearTimeout(idleT);
      idleT = setTimeout(function () { if (player && player.getPlayerState && player.getPlayerState() === 1) box.classList.add('idle'); }, 2500);
    }
    function toggle() {
      if (!player || !player.getPlayerState) return;
      if (ended) { ended = false; player.seekTo(0, true); player.playVideo(); return; }
      player.getPlayerState() === 1 ? player.pauseVideo() : player.playVideo();
    }
    function seek(e) {
      if (!player || !player.getDuration) return;
      var r = track.getBoundingClientRect(), x = (e.touches ? e.touches[0].clientX : e.clientX);
      var p = Math.min(1, Math.max(0, (x - r.left) / r.width));
      fill.style.width = p * 100 + '%';
      player.seekTo(p * player.getDuration(), true);
    }

    withApi(function () {
      player = new YT.Player($('.ply-frame div'), {
        videoId: id,
        host: 'https://www.youtube-nocookie.com',
        playerVars: { autoplay: 1, controls: 0, rel: 0, playsinline: 1, iv_load_policy: 3, cc_load_policy: 0, disablekb: 1, fs: 0, modestbranding: 1 },
        events: {
          onReady: function () {
            var f = box.querySelector('iframe'); if (f) f.title = tag;
            try { player.unloadModule('captions'); } catch (e) {}
            player.playVideo();
            setInterval(function () {
              if (!player.getDuration) return;
              var d = player.getDuration() || 0, c = player.getCurrentTime() || 0;
              if (d) fill.style.width = (c / d * 100) + '%';
              time.textContent = fmt(c) + ' / ' + fmt(d);
            }, 250);
          },
          onStateChange: function (e) {
            var s = e.data;
            if (s === 1) { // lecture
              if (current && current !== player) { try { current.pauseVideo(); } catch (x) {} }
              current = player; ended = false;
              shield.classList.remove('pass'); cover.classList.add('hide');
              pp.innerHTML = ICON.pause; pp.setAttribute('aria-label', 'Pause');
              try { player.unloadModule('captions'); } catch (x) {}
              wake();
            } else if (s === 2 || s === 0) { // pause ou fin : notre écran couvre celui de YouTube
              ended = s === 0;
              big.className = 'ply-big' + (ended ? ' replay' : '');
              big.innerHTML = ended ? ICON.replay : ICON.bigplay;
              cover.classList.toggle('end', ended); cover.classList.remove('hide'); box.classList.remove('idle');
              pp.innerHTML = ICON.play; pp.setAttribute('aria-label', 'Lecture');
            }
          }
        }
      });
    });

    shield.addEventListener('click', function () { toggle(); wake(); });
    cover.addEventListener('click', toggle);
    pp.addEventListener('click', toggle);
    box.addEventListener('mousemove', wake);
    box.addEventListener('touchstart', wake, { passive: true });
    track.addEventListener('click', seek);
    track.addEventListener('touchmove', seek, { passive: true });
    track.addEventListener('keydown', function (e) {
      if (!player || !player.getCurrentTime) return;
      if (e.key === 'ArrowRight') player.seekTo(player.getCurrentTime() + 10, true);
      if (e.key === 'ArrowLeft') player.seekTo(player.getCurrentTime() - 10, true);
    });
    speed.addEventListener('click', function () {
      if (!player || !player.setPlaybackRate) return;
      rate = (rate + 1) % RATES.length;
      player.setPlaybackRate(RATES[rate]);
      speed.textContent = String(RATES[rate]).replace('.', ',') + 'x';
      speed.setAttribute('aria-label', 'Vitesse de lecture : ' + speed.textContent);
      wake();
    });
    mute.addEventListener('click', function () {
      if (!player || !player.isMuted) return;
      if (player.isMuted()) { player.unMute(); mute.innerHTML = ICON.son; mute.setAttribute('aria-label', 'Couper le son'); }
      else { player.mute(); mute.innerHTML = ICON.muet; mute.setAttribute('aria-label', 'Remettre le son'); }
    });
    if (fs) fs.addEventListener('click', function () {
      var inFs = document.fullscreenElement || document.webkitFullscreenElement;
      if (inFs) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
      else (box.requestFullscreen || box.webkitRequestFullscreen).call(box);
    });
  }

  document.querySelectorAll('.video[data-yt]').forEach(function (box) {
    var id = box.getAttribute('data-yt'), tag = box.getAttribute('data-tag') || '';
    var showTag = !box.hasAttribute('data-no-tag');
    box.innerHTML =
      '<button type="button" class="ply-start" aria-label="Lire la vidéo : ' + tag + '">' +
      '<img class="thumb" src="https://i.ytimg.com/vi/' + id + '/hqdefault.jpg" alt="" loading="lazy">' +
      '<span class="play">' + ICON.bigplay + '</span></button>' +
      (showTag && tag ? '<div class="tag">' + tag + '</div>' : '');
    box.querySelector('.ply-start').addEventListener('click', function () { start(box, id, tag); });
  });
})();
